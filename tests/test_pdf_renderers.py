"""Exercise PPTX-to-PDF renderer discovery and fallback without launching an office suite."""

import importlib.util
from pathlib import Path
import sys
import tempfile
import textwrap
import unittest
from unittest import mock


BRIDGE = Path(__file__).resolve().parents[1] / "scripts" / "powerpoint-mac-bridge.py"
spec = importlib.util.spec_from_file_location("sivia_ooxml_bridge", BRIDGE)
bridge = importlib.util.module_from_spec(spec)
spec.loader.exec_module(bridge)

HOME = Path("/home/u")
FLATPAK_FONTS = HOME / ".var/app/org.onlyoffice.desktopeditors/data/onlyoffice/desktopeditors/data/fonts"


def discover(*, platform="linux", env=None, binaries=(), files=(), flatpaks=()):
    return bridge._pdf_renderers(
        platform=platform,
        env=env or {},
        home=HOME,
        which=lambda name: f"/usr/bin/{name}" if name in binaries else None,
        exists=lambda path: str(path) in {str(item) for item in files},
        flatpak_installed=lambda app_id: app_id in flatpaks,
    )


def fake_executable(directory: Path, name: str, body: str) -> str:
    script = directory / name
    script.write_text(f"#!{sys.executable}\nimport pathlib, sys\n{textwrap.dedent(body)}", "utf-8")
    script.chmod(0o755)
    return str(script)


class RendererDiscoveryTests(unittest.TestCase):
    def test_linux_prefers_native_libreoffice_then_flatpaks(self):
        renderers = discover(
            binaries={"soffice"},
            files={FLATPAK_FONTS / "AllFonts.js"},
            flatpaks={"org.libreoffice.LibreOffice", "org.onlyoffice.desktopeditors"},
        )
        self.assertEqual([item["name"] for item in renderers], ["LibreOffice", "LibreOffice (Flatpak)", "ONLYOFFICE (Flatpak)"])
        self.assertTrue(all("unavailable" not in item for item in renderers))

    def test_libreoffice_command_name_is_accepted(self):
        renderers = discover(binaries={"libreoffice"})
        self.assertEqual(renderers, [{"name": "LibreOffice", "family": "libreoffice", "executable": "/usr/bin/libreoffice"}])

    def test_onlyoffice_without_font_index_is_reported_unavailable(self):
        renderers = discover(flatpaks={"org.onlyoffice.desktopeditors"})
        self.assertEqual(len(renderers), 1)
        self.assertIn("launch ONLYOFFICE Desktop Editors once", renderers[0]["unavailable"])

    def test_native_onlyoffice_reads_fonts_from_xdg_data_home(self):
        fonts = Path("/data/onlyoffice/desktopeditors/data/fonts")
        renderers = discover(env={"XDG_DATA_HOME": "/data"}, files={"/opt/onlyoffice/desktopeditors/converter/x2t", fonts / "AllFonts.js"})
        self.assertEqual(renderers[0]["executable"], "/opt/onlyoffice/desktopeditors/converter/x2t")
        self.assertEqual(renderers[0]["fonts_dir"], fonts)
        self.assertNotIn("unavailable", renderers[0])

    def test_selection_filters_by_family_and_rejects_unknown_names(self):
        everything = dict(binaries={"soffice"}, files={FLATPAK_FONTS / "AllFonts.js"}, flatpaks={"org.onlyoffice.desktopeditors"})
        selected = discover(env={"YOU_ONLY_FIGURE_ONCE_RENDERER": "ONLYOFFICE"}, **everything)
        self.assertEqual([item["family"] for item in selected], ["onlyoffice"])
        with self.assertRaisesRegex(ValueError, "libreoffice or onlyoffice"):
            discover(env={"YOU_ONLY_FIGURE_ONCE_RENDERER": "keynote"}, **everything)

    def test_macos_and_windows_find_default_libreoffice_installs(self):
        mac = discover(platform="darwin", files={"/Applications/LibreOffice.app/Contents/MacOS/soffice"}, flatpaks={"org.libreoffice.LibreOffice"})
        self.assertEqual([item["executable"] for item in mac], ["/Applications/LibreOffice.app/Contents/MacOS/soffice"])
        windows_soffice = "C:\\Program Files\\LibreOffice\\program\\soffice.exe"
        windows = discover(platform="win32", env={"ProgramFiles": "C:\\Program Files"}, files={windows_soffice})
        self.assertEqual([item["executable"] for item in windows], [windows_soffice])

    def test_flatpak_command_grants_only_the_work_directory(self):
        renderer = {"flatpak": "org.onlyoffice.desktopeditors", "flatpak_command": "/app/x2t"}
        self.assertEqual(
            bridge._renderer_argv(renderer, Path("/tmp/work")),
            ["flatpak", "run", "--filesystem=/tmp/work", "--command=/app/x2t", "org.onlyoffice.desktopeditors"],
        )


@unittest.skipIf(sys.platform == "win32", "fake converters use POSIX shebang scripts")
class RendererExecutionTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.source = self.root / "deck.pptx"
        self.source.write_bytes(b"pptx")
        self.silent = fake_executable(self.root, "silent", "sys.exit(0)\n")

    def tearDown(self):
        self.temp.cleanup()

    def test_falls_back_when_a_converter_exits_without_a_pdf(self):
        working = fake_executable(self.root, "working", """\
            args = sys.argv[1:]
            assert args[0].startswith("-env:UserInstallation=file://"), args
            outdir = pathlib.Path(args[args.index("--outdir") + 1])
            outdir.mkdir(parents=True, exist_ok=True)
            (outdir / (pathlib.Path(args[-1]).stem + ".pdf")).write_bytes(b"%PDF-1.7")
        """)
        renderers = [
            {"name": "Silent", "family": "libreoffice", "executable": self.silent},
            {"name": "Working", "family": "libreoffice", "executable": working},
        ]
        destination = self.root / "out" / "deck.pdf"
        with mock.patch.object(bridge, "_pdf_renderers", return_value=renderers):
            used = bridge._render_pdf(self.source, destination)
        self.assertEqual(used["name"], "Working")
        self.assertEqual(destination.read_bytes(), b"%PDF-1.7")

    def test_reports_every_attempt_when_no_renderer_succeeds(self):
        renderers = [
            {"name": "Silent", "family": "libreoffice", "executable": self.silent},
            {"name": "ONLYOFFICE (Flatpak)", "family": "onlyoffice", "unavailable": "font index is missing"},
        ]
        with mock.patch.object(bridge, "_pdf_renderers", return_value=renderers):
            with self.assertRaises(RuntimeError) as raised:
                bridge._render_pdf(self.source, self.root / "deck.pdf")
        message = str(raised.exception)
        self.assertIn("Silent: exited with code 0 without producing a PDF", message)
        self.assertIn("ONLYOFFICE (Flatpak): font index is missing", message)

    def test_x2t_task_escapes_paths_and_names_the_font_index(self):
        x2t = fake_executable(self.root, "x2t", """\
            import xml.etree.ElementTree as ET
            task = ET.parse(sys.argv[1]).getroot()
            assert task.findtext("m_nFormatTo") == "513"
            assert task.findtext("m_sAllFontsPath").endswith("fonts & more/AllFonts.js")
            pathlib.Path(task.findtext("m_sFileTo")).write_bytes(b"%PDF-1.7")
        """)
        renderer = {"name": "ONLYOFFICE", "family": "onlyoffice", "executable": x2t, "fonts_dir": self.root / "fonts & more"}
        work = self.root / "work & co"
        work.mkdir()
        generated = bridge._convert_to_pdf(renderer, work / "deck.pptx", work)
        self.assertEqual(generated.read_bytes(), b"%PDF-1.7")


if __name__ == "__main__":
    unittest.main()

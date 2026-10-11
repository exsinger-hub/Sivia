import assert from "node:assert/strict";
import test from "node:test";
import { ooxmlPythonCandidates, ooxmlPythonSetupHint, siviaVenvDirectory } from "../scripts/python-runtime.mjs";

const executables = (options) => ooxmlPythonCandidates(options).map((candidate) => candidate.executable);

test("Linux checks the plugin venv, then a stable Sivia venv, without macOS-only paths", () => {
  const found = executables({ platform: "linux", env: {}, homeDir: "/home/u", scriptDir: "/plugin/scripts" });
  assert.deepEqual(found, [
    "/plugin/scripts/.venv/bin/python3",
    "/home/u/.local/share/sivia/venv/bin/python3",
    "/home/u/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3",
    "python3",
    "/usr/local/bin/python3",
  ]);
});

test("an explicit interpreter is tried first and XDG_DATA_HOME relocates the stable venv", () => {
  const env = { YOU_ONLY_FIGURE_ONCE_PYTHON: "/opt/py/bin/python3", XDG_DATA_HOME: "/data" };
  const found = executables({ platform: "linux", env, homeDir: "/home/u", scriptDir: "/plugin/scripts" });
  assert.equal(found[0], "/opt/py/bin/python3");
  assert.equal(found[2], "/data/sivia/venv/bin/python3");
});

test("macOS keeps the Homebrew interpreter", () => {
  const found = executables({ platform: "darwin", env: {}, homeDir: "/Users/u", scriptDir: "/plugin/scripts" });
  assert.ok(found.includes("/opt/homebrew/bin/python3"));
  assert.ok(found.indexOf("/opt/homebrew/bin/python3") < found.indexOf("/usr/local/bin/python3"));
});

test("Windows uses Scripts\\python.exe venvs and the py launcher", () => {
  const env = { LOCALAPPDATA: "C:\\Users\\u\\AppData\\Local" };
  const candidates = ooxmlPythonCandidates({ platform: "win32", env, homeDir: "C:\\Users\\u", scriptDir: "C:\\plugin\\scripts" });
  const found = candidates.map((candidate) => candidate.executable);
  assert.equal(found[0], "C:\\plugin\\scripts\\.venv\\Scripts\\python.exe");
  assert.equal(found[1], "C:\\Users\\u\\AppData\\Local\\sivia\\venv\\Scripts\\python.exe");
  assert.deepEqual(candidates.at(-1), { executable: "py.exe", args: ["-3"] });
  assert.ok(!found.includes("python3"));
});

test("the setup hint points at a venv and the repository requirements file", () => {
  const linux = ooxmlPythonSetupHint({ platform: "linux", env: {}, homeDir: "/home/u", scriptDir: "/plugin/scripts" });
  assert.match(linux, /python3 -m venv "\/home\/u\/.local\/share\/sivia\/venv"/);
  assert.match(linux, /-m pip install -r "\/plugin\/requirements.txt"/);
  assert.match(linux, /python3-venv/);
  assert.match(linux, /YOU_ONLY_FIGURE_ONCE_PYTHON/);

  const windows = ooxmlPythonSetupHint({ platform: "win32", env: {}, homeDir: "C:\\Users\\u", scriptDir: "C:\\plugin\\scripts" });
  assert.match(windows, /py -3 -m venv "C:\\Users\\u\\AppData\\Local\\sivia\\venv"/);
  assert.doesNotMatch(windows, /python3-venv/);
  assert.equal(siviaVenvDirectory({ platform: "win32", env: {}, homeDir: "C:\\Users\\u" }), "C:\\Users\\u\\AppData\\Local\\sivia\\venv");
});

import os from "node:os";
import path from "node:path";

function pathApi(platform) {
  return platform === "win32" ? path.win32 : path.posix;
}

function venvPython(venvDirectory, platform) {
  const platformPath = pathApi(platform);
  return platform === "win32"
    ? platformPath.join(venvDirectory, "Scripts", "python.exe")
    : platformPath.join(venvDirectory, "bin", "python3");
}

// A virtual environment outside the versioned plugin cache survives plugin updates.
export function siviaVenvDirectory({ platform = process.platform, env = process.env, homeDir = os.homedir() } = {}) {
  const platformPath = pathApi(platform);
  if (platform === "win32") {
    return platformPath.join(env.LOCALAPPDATA || platformPath.join(homeDir, "AppData", "Local"), "sivia", "venv");
  }
  return platformPath.join(env.XDG_DATA_HOME?.trim() || platformPath.join(homeDir, ".local", "share"), "sivia", "venv");
}

export function ooxmlPythonCandidates({ platform = process.platform, env = process.env, homeDir = os.homedir(), scriptDir } = {}) {
  const platformPath = pathApi(platform);
  const codexPython = platformPath.join(homeDir, ".cache", "codex-runtimes", "codex-primary-runtime", "dependencies", "python");
  const candidates = [
    { executable: env.SIVIA_PYTHON, args: [] },
    { executable: env.YOU_ONLY_FIGURE_ONCE_PYTHON, args: [] },
    { executable: venvPython(platformPath.join(scriptDir, ".venv"), platform), args: [] },
    { executable: venvPython(siviaVenvDirectory({ platform, env, homeDir }), platform), args: [] },
  ];
  if (platform === "win32") {
    candidates.push(
      { executable: platformPath.join(codexPython, "python.exe"), args: [] },
      { executable: platformPath.join(codexPython, "bin", "python.exe"), args: [] },
      { executable: "python.exe", args: [] },
      { executable: "py.exe", args: ["-3"] },
    );
  } else {
    candidates.push(
      { executable: platformPath.join(codexPython, "bin", "python3"), args: [] },
      { executable: "python3", args: [] },
    );
    if (platform === "darwin") candidates.push({ executable: "/opt/homebrew/bin/python3", args: [] });
    candidates.push({ executable: "/usr/local/bin/python3", args: [] });
  }
  return candidates.filter((candidate) => candidate.executable);
}

export function ooxmlPythonSetupHint({ platform = process.platform, env = process.env, homeDir = os.homedir(), scriptDir } = {}) {
  const platformPath = pathApi(platform);
  const venvDirectory = siviaVenvDirectory({ platform, env, homeDir });
  const requirements = platformPath.join(platformPath.dirname(scriptDir), "requirements.txt");
  const create = platform === "win32" ? `py -3 -m venv "${venvDirectory}"` : `python3 -m venv "${venvDirectory}"`;
  const hints = [
    `Create a dedicated environment with \`${create}\`, then run \`"${venvPython(venvDirectory, platform)}" -m pip install -r "${requirements}"\`.`,
  ];
  if (platform === "linux") {
    hints.push("On Debian/Ubuntu, install the python3-venv package first if venv creation fails.");
  }
  hints.push("Or set SIVIA_PYTHON (legacy: YOU_ONLY_FIGURE_ONCE_PYTHON) to a Python interpreter that already has python-pptx.");
  return hints.join(" ");
}

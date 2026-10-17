// Locations for Sivia's private state (OOXML sessions, Office.js certificate).
//
// The default is unchanged from earlier releases (~/.codex/you-only-figure-once), so existing Codex and
// Claude Code installations keep their sessions and trusted localhost certificate. Hosts that should not
// create a ~/.codex directory (for example OpenCode / OpenWork, via scripts/install-opencode.mjs) set
// SIVIA_HOME instead.
import os from "node:os";
import path from "node:path";

function pathApi(platform) {
  return platform === "win32" ? path.win32 : path.posix;
}

export function siviaHomeDirectory({ platform = process.platform, env = process.env, homeDir = os.homedir() } = {}) {
  const platformPath = pathApi(platform);
  const configured = env.SIVIA_HOME?.trim();
  if (configured) return platformPath.resolve(configured);
  return platformPath.join(homeDir, ".codex", "you-only-figure-once");
}

export function siviaStateSubdirectory(name, options) {
  const platformPath = pathApi(options?.platform ?? process.platform);
  return platformPath.join(siviaHomeDirectory(options), name);
}

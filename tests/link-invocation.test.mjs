import assert from "node:assert/strict";
import { execFile } from "node:child_process";
import { mkdtemp, rm, symlink } from "node:fs/promises";
import os from "node:os";
import path from "node:path";
import test from "node:test";
import { fileURLToPath } from "node:url";
import { promisify } from "node:util";

const execFileAsync = promisify(execFile);
const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");

// OpenCode installs skills as links (a junction on Windows). Node resolves the real path for the entry module but
// not for process.argv[1], so a naive "am I the entry point" check silently ran nothing.
async function linked(target, t) {
  const dir = await mkdtemp(path.join(os.tmpdir(), "sivia-link-"));
  t.after(() => rm(dir, { recursive: true, force: true, maxRetries: 5, retryDelay: 100 }));
  const link = path.join(dir, "linked");
  await symlink(target, link, process.platform === "win32" ? "junction" : "dir");
  return link;
}

test("install-opencode.mjs runs when invoked through a link", async (t) => {
  const link = await linked(path.join(root, "scripts"), t);
  const { stdout } = await execFileAsync(process.execPath, [path.join(link, "install-opencode.mjs"), "--help"]);
  assert.match(stdout, /Install Sivia into OpenCode/);
});

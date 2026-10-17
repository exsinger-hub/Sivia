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

// Hosts that install skills as links (a junction on Windows) run the script through the link. Node resolves the real
// path for the entry module but not for process.argv[1], so a naive "am I the entry point" check ran nothing.
test("imagegen.mjs runs when invoked through a link", async (t) => {
  const dir = await mkdtemp(path.join(os.tmpdir(), "sivia-link-"));
  t.after(() => rm(dir, { recursive: true, force: true, maxRetries: 5, retryDelay: 100 }));
  const link = path.join(dir, "linked");
  await symlink(path.join(root, "skills", "generate-figure-elements", "scripts"), link, process.platform === "win32" ? "junction" : "dir");
  const env = { PATH: process.env.PATH, SystemRoot: process.env.SystemRoot };
  let stdout = "";
  try {
    ({ stdout } = await execFileAsync(process.execPath, [path.join(link, "imagegen.mjs"), "status"], { env }));
  } catch (error) {
    stdout = error.stdout; // status exits 1 when no provider is configured, but must still answer
  }
  const report = JSON.parse(stdout);
  assert.equal(report.configured, false);
  assert.match(report.error, /No image provider is configured/);
});

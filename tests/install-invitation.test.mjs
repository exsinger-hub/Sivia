import assert from "node:assert/strict";
import { execFileSync } from "node:child_process";
import { existsSync } from "node:fs";
import { mkdtemp, readFile, readdir, rm, writeFile } from "node:fs/promises";
import os from "node:os";
import path from "node:path";
import test from "node:test";
import { fileURLToPath } from "node:url";
import { claimInvitation } from "../skills/support-sivia/scripts/install-invitation.mjs";

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const script = path.join(root, "skills/support-sivia/scripts/install-invitation.mjs");

async function temporary(t) {
  const dir = await mkdtemp(path.join(os.tmpdir(), "sivia install invitation "));
  t.after(async () => {
    assert.equal(path.dirname(path.resolve(dir)), path.resolve(os.tmpdir()));
    assert.ok(path.basename(dir).startsWith("sivia install invitation "));
    await rm(dir, { recursive: true, force: true });
  });
  return dir;
}

test("neither client registers a runtime Star hook", async () => {
  for (const name of [".codex-plugin/plugin.json", ".claude-plugin/plugin.json"]) {
    const manifest = JSON.parse(await readFile(path.join(root, name), "utf8"));
    assert.equal(manifest.hooks, undefined);
  }
  assert.equal(existsSync(path.join(root, "hooks/hooks.json")), false);
  assert.equal(existsSync(path.join(root, "hooks/welcome.mjs")), false);
});

test("without verified first-install completion no question or marker is created", async t => {
  const stateDirectory = await temporary(t);
  assert.deepEqual(claimInvitation({ stateDirectory }), { ask: false });
  assert.deepEqual(claimInvitation({ stateDirectory, firstInstallCompleted: false }), { ask: false });
  assert.deepEqual(await readdir(stateDirectory), []);
});

test("first installation reserves one invitation; later calls cannot repeat it", async t => {
  const stateDirectory = await temporary(t);
  const first = claimInvitation({ stateDirectory, firstInstallCompleted: true });
  assert.equal(first.ask, true);
  assert.equal(first.repository, "https://github.com/exsinger-hub/Sivia");
  assert.deepEqual(await readdir(stateDirectory), ["install-star-invitation-v1.json"]);
  assert.deepEqual(claimInvitation({ stateDirectory, firstInstallCompleted: true }), { ask: false });
});

test("declining or ignoring an invitation cannot leave a deferred question", async t => {
  const stateDirectory = await temporary(t);
  claimInvitation({ stateDirectory, firstInstallCompleted: true });
  for (const firstInstallCompleted of [false, true]) {
    assert.deepEqual(claimInvitation({ stateDirectory, firstInstallCompleted }), { ask: false });
  }
});

test("disabled invitations create no state", async t => {
  const stateDirectory = await temporary(t);
  assert.deepEqual(claimInvitation({ stateDirectory, firstInstallCompleted: true, disabled: true }), { ask: false });
  assert.deepEqual(await readdir(stateDirectory), []);
});

test("missing, relative or unusable state does not ask or block installation", async t => {
  const directory = await temporary(t);
  const file = path.join(directory, "file");
  await writeFile(file, "preserve");
  for (const stateDirectory of [undefined, "relative", file]) {
    assert.deepEqual(claimInvitation({ stateDirectory, firstInstallCompleted: true }), { ask: false });
  }
  assert.equal(await readFile(file, "utf8"), "preserve");
});

test("ordinary CLI execution and lifecycle-like arguments never invite", () => {
  for (const args of [[], ["startup"], ["resume"], ["--first-install-completed", "startup"]]) {
    const output = execFileSync(process.execPath, [script, ...args], { encoding: "utf8", windowsHide: true });
    assert.deepEqual(JSON.parse(output), { ask: false });
  }
});

test("CI and opt-out suppress even an explicit installation invocation", () => {
  for (const extra of [{ CI: "true" }, { SIVIA_STAR_INVITE: "0" }]) {
    const output = execFileSync(process.execPath, [script, "--first-install-completed"], {
      env: { ...process.env, ...extra }, encoding: "utf8", windowsHide: true,
    });
    assert.deepEqual(JSON.parse(output), { ask: false });
  }
});

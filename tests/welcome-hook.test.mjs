import assert from "node:assert/strict";
import { spawn } from "node:child_process";
import { mkdtemp, readFile, readdir, rm, writeFile } from "node:fs/promises";
import os from "node:os";
import path from "node:path";
import test from "node:test";
import { fileURLToPath } from "node:url";

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const script = path.join(root, "hooks/welcome.mjs");
const startup = { hook_event_name: "SessionStart", source: "startup" };

function invoke(data, { client = "codex", event = startup, env = {}, command } = {}) {
  const cleanEnv = { ...process.env };
  for (const key of ["PLUGIN_ROOT", "PLUGIN_DATA", "CLAUDE_PLUGIN_ROOT", "CLAUDE_PLUGIN_DATA", "SIVIA_STAR_INVITE", "CI"]) delete cleanEnv[key];
  const prefix = client === "codex" ? "PLUGIN" : "CLAUDE_PLUGIN";
  Object.assign(cleanEnv, { [`${prefix}_ROOT`]: root, [`${prefix}_DATA`]: data, ...env });
  return new Promise((resolve, reject) => {
    const child = spawn(process.execPath, command ? ["-e", command] : [script], {
      cwd: os.tmpdir(), env: cleanEnv, windowsHide: true, stdio: ["pipe", "pipe", "pipe"],
    });
    let out = "", err = "";
    child.stdout.on("data", chunk => { out += chunk; });
    child.stderr.on("data", chunk => { err += chunk; });
    child.on("error", reject);
    child.on("close", code => resolve({ code, out, err }));
    child.stdin.end(typeof event === "string" ? event : JSON.stringify(event));
  });
}

async function temporary(t) {
  const dir = await mkdtemp(path.join(os.tmpdir(), "sivia welcome test "));
  t.after(async () => {
    assert.equal(path.dirname(path.resolve(dir)), path.resolve(os.tmpdir()));
    assert.ok(path.basename(dir).startsWith("sivia welcome test "));
    await rm(dir, { recursive: true, force: true });
  });
  return dir;
}

for (const client of ["codex", "claude"]) {
  test(`${client}: first startup emits one notice; later starts stay quiet`, async t => {
    const data = await temporary(t);
    const first = await invoke(data, { client });
    assert.equal(first.code, 0);
    assert.equal(first.err, "");
    const result = JSON.parse(first.out);
    assert.equal(result.continue, true);
    assert.ok(result.systemMessage.includes("https://github.com/exsinger-hub/Sivia"));
    assert.equal(result.hookSpecificOutput, undefined, "the notice must not issue model instructions");
    assert.deepEqual(await readdir(data), ["star-invitation-shown-v1.json"]);
    assert.deepEqual(await invoke(data, { client }), { code: 0, out: "", err: "" });
  });
}

test("concurrent sessions emit a single invitation", async t => {
  const data = await temporary(t);
  const results = await Promise.all(Array.from({ length: 6 }, () => invoke(data)));
  assert.equal(results.filter(r => r.out).length, 1);
  assert.ok(results.every(r => r.code === 0 && r.err === ""));
});

for (const [name, options] of [
  ["opt-out", { env: { SIVIA_STAR_INVITE: "0" } }],
  ["CI", { env: { CI: "true" } }],
  ["resume", { event: { ...startup, source: "resume" } }],
  ["compact", { event: { ...startup, source: "compact" } }],
  ["wrong event", { event: { ...startup, hook_event_name: "SubagentStart" } }],
  ["malformed input", { event: "not json" }],
  ["missing data directory", { env: { PLUGIN_DATA: "" } }],
  ["relative data directory", { env: { PLUGIN_DATA: "relative-state" } }],
]) {
  test(`${name} produces no notice or state`, async t => {
    const data = await temporary(t);
    assert.deepEqual(await invoke(data, options), { code: 0, out: "", err: "" });
    assert.deepEqual(await readdir(data), []);
  });
}

test("unusable state path cannot block startup", async t => {
  const data = await temporary(t);
  const file = path.join(data, "file");
  await writeFile(file, "preserve");
  assert.deepEqual(await invoke(file), { code: 0, out: "", err: "" });
  assert.equal(await readFile(file, "utf8"), "preserve");
});

test("packaged command loads from both client root variables", async t => {
  const config = JSON.parse(await readFile(path.join(root, "hooks/hooks.json"), "utf8"));
  const group = config.hooks.SessionStart[0];
  assert.equal(group.matcher, "startup");
  const match = /^node -e "(.+)"$/.exec(group.hooks[0].command);
  assert.ok(match, "expected a portable Node command");
  for (const client of ["codex", "claude"]) {
    const result = await invoke(await temporary(t), { client, command: match[1] });
    assert.equal(result.code, 0);
    assert.equal(result.err, "");
    assert.ok(JSON.parse(result.out).systemMessage);
  }
});

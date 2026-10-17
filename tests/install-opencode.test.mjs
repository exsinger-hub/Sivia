import assert from "node:assert/strict";
import { existsSync } from "node:fs";
import { lstat, mkdtemp, mkdir, readFile, realpath, rm, writeFile } from "node:fs/promises";
import os from "node:os";
import path from "node:path";
import test from "node:test";
import { fileURLToPath } from "node:url";
import {
  SERVERS, SIVIA_ROOT, listSkills, main, mcpEntry, parseArgs, parseConfigText, resolveTargets, runInstall, runStatus, runUninstall, stripJsonc,
} from "../scripts/install-opencode.mjs";

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");

async function workspace(t) {
  const dir = await mkdtemp(path.join(os.tmpdir(), "sivia-opencode-"));
  t.after(() => rm(dir, { recursive: true, force: true }));
  return dir;
}

test("the installer's root is this checkout and every skill is discoverable", async () => {
  assert.equal(SIVIA_ROOT, root);
  const skills = await listSkills();
  for (const expected of ["design-scientific-figure", "recreate-scientific-figure-in-drawio", "edit-powerpoint-live", "audit-scientific-figure", "correct-scientific-figure"]) {
    assert.ok(skills.includes(expected), expected);
  }
});

test("MCP entries use OpenCode's local server shape and the same scripts as the other manifests", async () => {
  const codex = JSON.parse(await readFile(path.join(root, ".codex-plugin/plugin.json"), "utf8"));
  assert.deepEqual(Object.keys(SERVERS).sort(), Object.keys(codex.mcpServers).sort());
  for (const [name, server] of Object.entries(codex.mcpServers)) {
    const entry = mcpEntry(name);
    assert.equal(entry.type, "local");
    assert.ok(Array.isArray(entry.command) && entry.command.length === 2);
    assert.equal(entry.command[1], path.join(root, server.args[0]));
    assert.ok(entry.environment.SIVIA_HOME, "a host-neutral state directory is provided");
    assert.equal(entry.enabled, true);
  }
});

test("JSONC parsing keeps // inside strings and tolerates comments and trailing commas", () => {
  const { value, hadComments } = parseConfigText('{\n  // keep\n  "url": "https://x.test/a//b", /* c */\n  "list": [1, 2,],\n}\n');
  assert.equal(hadComments, true);
  assert.equal(value.url, "https://x.test/a//b");
  assert.deepEqual(value.list, [1, 2]);
  assert.equal(parseConfigText('{"a":1}').hadComments, false);
  assert.equal(stripJsonc('{"a": "/* not a comment */"}').hadComments, false);
});

test("argument parsing validates scope, mode, profile and server names", () => {
  assert.equal(parseArgs(["uninstall"]).command, "uninstall");
  assert.deepEqual(parseArgs(["--profile", "powerpoint"]).servers, ["powerpoint-live"]);
  assert.deepEqual(parseArgs(["--profile", "drawio"]).servers, ["drawio-live", "drawio-file-utils"]);
  assert.throws(() => parseArgs(["--scope", "team"]), /scope/);
  assert.throws(() => parseArgs(["--mode", "move"]), /mode/);
  assert.throws(() => parseArgs(["--servers", "nope"]), /Unknown server/);
  assert.throws(() => parseArgs(["--bogus"]), /Unknown option/);
});

test("user scope honours OPENCODE_CONFIG_DIR, then XDG_CONFIG_HOME, then ~/.config/opencode", () => {
  assert.equal(resolveTargets({ env: { OPENCODE_CONFIG_DIR: "/x/oc" }, homeDir: "/h" }).configDir, "/x/oc");
  assert.equal(resolveTargets({ env: { XDG_CONFIG_HOME: "/x/cfg" }, homeDir: "/h" }).configDir, path.join("/x/cfg", "opencode"));
  assert.equal(resolveTargets({ env: {}, homeDir: "/h" }).skillsDir, path.join("/h", ".config", "opencode", "skills"));
  const project = resolveTargets({ scope: "project", project: "/w" });
  assert.equal(project.skillsDir, path.join(path.resolve("/w"), ".opencode", "skills"));
});

test("project install links every skill and merges MCP servers without disturbing existing config", async (t) => {
  const dir = await workspace(t);
  await writeFile(path.join(dir, "opencode.json"), JSON.stringify({ $schema: "https://opencode.ai/config.json", theme: "dark", mcp: { other: { type: "remote", url: "https://example.test/mcp" } } }));
  const report = await runInstall({ scope: "project", project: dir, servers: Object.keys(SERVERS) });
  assert.ok(report.skills.every((skill) => ["linked", "copied"].includes(skill.outcome)), JSON.stringify(report.skills));
  for (const name of await listSkills()) {
    assert.ok(existsSync(path.join(dir, ".opencode", "skills", name, "SKILL.md")), `${name} resolves through the link`);
  }
  const config = JSON.parse(await readFile(path.join(dir, "opencode.json"), "utf8"));
  assert.equal(config.theme, "dark");
  assert.equal(config.mcp.other.url, "https://example.test/mcp");
  for (const name of Object.keys(SERVERS)) assert.equal(config.mcp[`sivia-${name}`].type, "local");
  assert.ok(existsSync(path.join(dir, "opencode.json.sivia-backup")), "the original config is backed up once");

  const again = await runInstall({ scope: "project", project: dir, servers: Object.keys(SERVERS) });
  assert.equal(again.mcp.changed, false, "a second run is idempotent");
  assert.ok(again.skills.every((skill) => skill.outcome === "linked"), "refreshing our own links is allowed");
});

test("a skill with the same name that Sivia did not install is skipped unless --force is given", async (t) => {
  const dir = await workspace(t);
  const foreign = path.join(dir, ".opencode", "skills", "design-scientific-figure");
  await mkdir(foreign, { recursive: true });
  await writeFile(path.join(foreign, "SKILL.md"), "---\nname: design-scientific-figure\ndescription: someone else's\n---\n");
  const skipped = await runInstall({ scope: "project", project: dir, servers: [] });
  assert.equal(skipped.skills.find((skill) => skill.name === "design-scientific-figure").outcome, "skipped");
  assert.match(await readFile(path.join(foreign, "SKILL.md"), "utf8"), /someone else/);
  const forced = await runInstall({ scope: "project", project: dir, servers: [], force: true });
  assert.equal(forced.skills.find((skill) => skill.name === "design-scientific-figure").outcome, "linked");
});

test("a config with comments is never rewritten silently", async (t) => {
  const dir = await workspace(t);
  const original = '{\n  // my notes\n  "theme": "dark"\n}\n';
  await writeFile(path.join(dir, "opencode.jsonc"), original);
  const report = await runInstall({ scope: "project", project: dir, servers: ["drawio-live"], skills: false });
  assert.equal(report.mcp.blockedByComments, true);
  assert.equal(await readFile(path.join(dir, "opencode.jsonc"), "utf8"), original);
  assert.ok(report.mcp.snippet["sivia-drawio-live"]);
  const code = await main(["--scope", "project", "--project", dir, "--servers", "drawio-live", "--mcp-only", "--json"].filter(Boolean));
  assert.equal(code, 3);
  const rewritten = await runInstall({ scope: "project", project: dir, servers: ["drawio-live"], skills: false, rewriteJsonc: true });
  assert.equal(rewritten.mcp.written, true);
  assert.ok(existsSync(path.join(dir, "opencode.jsonc.sivia-backup")));
});

test("dry run changes nothing", async (t) => {
  const dir = await workspace(t);
  await runInstall({ scope: "project", project: dir, dryRun: true, servers: Object.keys(SERVERS) });
  assert.equal(existsSync(path.join(dir, ".opencode")), false);
  assert.equal(existsSync(path.join(dir, "opencode.json")), false);
});

test("uninstall removes only what Sivia added", async (t) => {
  const dir = await workspace(t);
  await writeFile(path.join(dir, "opencode.json"), JSON.stringify({ mcp: { other: { type: "remote", url: "https://example.test/mcp" } } }));
  const mine = path.join(dir, ".opencode", "skills", "my-own-skill");
  await mkdir(mine, { recursive: true });
  await writeFile(path.join(mine, "SKILL.md"), "---\nname: my-own-skill\ndescription: x\n---\n");
  await runInstall({ scope: "project", project: dir, servers: Object.keys(SERVERS) });
  const report = await runUninstall({ scope: "project", project: dir });
  assert.ok(report.skills.filter((skill) => skill.outcome === "removed").length >= 7);
  assert.equal(existsSync(path.join(dir, ".opencode", "skills", "design-scientific-figure")), false);
  assert.ok(existsSync(path.join(mine, "SKILL.md")), "unrelated skills survive");
  const config = JSON.parse(await readFile(path.join(dir, "opencode.json"), "utf8"));
  assert.deepEqual(Object.keys(config.mcp), ["other"]);
  // The link was removed without deleting the checkout it pointed to.
  assert.ok(existsSync(path.join(root, "skills", "design-scientific-figure", "SKILL.md")));
});

test("copy mode writes an ownership marker and status reports installed skills and servers", async (t) => {
  const dir = await workspace(t);
  await runInstall({ scope: "project", project: dir, mode: "copy", servers: ["drawio-live"] });
  const copied = path.join(dir, ".opencode", "skills", "audit-scientific-figure");
  assert.equal((await lstat(copied)).isSymbolicLink(), false);
  assert.ok(existsSync(path.join(copied, ".sivia-installed.json")));
  const status = await runStatus({ scope: "project", project: dir });
  assert.ok(status.skills.every((skill) => skill.installed));
  assert.equal(status.servers["sivia-drawio-live"].configured, true);
  assert.equal(status.servers["sivia-drawio-live"].script_exists, true);
  assert.equal(status.servers["sivia-powerpoint-live"].configured, false);
});

test("a linked skill resolves to the Sivia root, a copied skill records where it came from", async (t) => {
  const dir = await workspace(t);
  await runInstall({ scope: "project", project: dir, mode: "link", servers: [] });
  const linkedSkill = path.join(dir, ".opencode", "skills", "design-scientific-figure");
  // Lexically, ../.. from the link location is the workspace, not Sivia; the skills tell agents to resolve the link first.
  assert.equal(existsSync(path.join(linkedSkill, "..", "..", "scripts")), false);
  const real = await realpath(linkedSkill);
  assert.equal(path.resolve(real, "..", ".."), root);
  assert.ok(existsSync(path.join(path.resolve(real, "..", ".."), "scripts", "prepare-overview-review.py")));

  const copyDir = await workspace(t);
  await runInstall({ scope: "project", project: copyDir, mode: "copy", servers: [] });
  const marker = JSON.parse(await readFile(path.join(copyDir, ".opencode", "skills", "design-scientific-figure", ".sivia-installed.json"), "utf8"));
  assert.equal(path.resolve(marker.source, "..", ".."), root);
});

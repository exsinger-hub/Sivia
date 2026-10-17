import assert from "node:assert/strict";
import { readFile } from "node:fs/promises";
import path from "node:path";
import test from "node:test";
import { fileURLToPath } from "node:url";

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const json = async (relative) => JSON.parse(await readFile(path.join(root, relative), "utf8"));
const codex = await json(".codex-plugin/plugin.json");
const portable = await json("plugin.json");
const mcp = await json("mcp.json");

// https://agent-plugins.org/specification (1.0.0): the manifest schema is closed.
const MANIFEST_FIELDS = new Set(["$schema", "name", "version", "description", "author", "homepage", "repository", "license", "keywords", "extensions"]);

test("the Agent Plugins manifest uses only permitted fields and mirrors the source manifest", () => {
  assert.equal(portable.$schema, "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json");
  for (const key of Object.keys(portable)) assert.ok(MANIFEST_FIELDS.has(key), `unexpected manifest field ${key}`);
  assert.match(portable.name, /^[a-z0-9]+(?:[-.][a-z0-9]+)*$/);
  assert.ok(portable.name.length <= 64);
  for (const key of ["name", "version", "description", "homepage", "repository", "license"]) assert.equal(portable[key], codex[key], key);
  assert.deepEqual(portable.author, codex.author);
  assert.deepEqual(portable.keywords, codex.keywords);
  assert.deepEqual(Object.keys(portable.author).sort(), ["name", "url"]);
});

test("mcp.json is a closed stdio configuration matching the other manifests", () => {
  assert.equal(mcp.$schema, "https://agent-plugins.org/schemas/1.0.0/mcp.schema.json");
  assert.deepEqual(Object.keys(mcp).sort(), ["$schema", "mcpServers"]);
  assert.deepEqual(Object.keys(mcp.mcpServers), Object.keys(codex.mcpServers));
  for (const [name, server] of Object.entries(mcp.mcpServers)) {
    assert.deepEqual(Object.keys(server).sort(), ["args", "command", "cwd", "type"]);
    assert.equal(server.type, "stdio");
    assert.equal(server.command, "node", "a single executable token, never a shell string");
    assert.equal(server.cwd, "${PLUGIN_ROOT}");
    assert.equal(server.args.length, 1);
    assert.equal(server.args[0], `\${PLUGIN_ROOT}/${codex.mcpServers[name].args[0].slice(2)}`);
  }
});

test("both manifests live at the plugin root next to skills/", async () => {
  await readFile(path.join(root, "skills", "design-scientific-figure", "SKILL.md"));
  assert.equal(portable.$schema.split("/").at(-2), mcp.$schema.split("/").at(-2), "plugin.json and mcp.json target the same version");
});

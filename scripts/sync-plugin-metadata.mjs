#!/usr/bin/env node
// Keep the public Codex/Claude catalogs, the Claude manifest and the portable Agent Plugins package
// (plugin.json + mcp.json, https://agent-plugins.org) aligned with Sivia's source manifest.
// This never edits installed marketplaces or user configuration.
import assert from "node:assert/strict";
import { mkdir, readFile, writeFile } from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const manifest = JSON.parse(await readFile(path.join(root, ".codex-plugin/plugin.json"), "utf8"));
assert.match(manifest.name, /^[a-z0-9]+(?:-[a-z0-9]+)*$/);
assert.equal(manifest.repository, "https://github.com/exsinger-hub/Sivia");
const codexCatalogPath = ".agents/plugins/marketplace.json";
const catalog = JSON.parse(await readFile(path.join(root, codexCatalogPath), "utf8"));
assert.equal(catalog.plugins.length, 1, "Review additional entries before changing this single-plugin catalog.");
assert.ok(["you-only-figure-once", manifest.name].includes(catalog.plugins[0].name));

catalog.name = manifest.name;
catalog.interface.displayName = manifest.interface.displayName;
catalog.plugins[0].name = manifest.name;
catalog.plugins[0].source = { source: "url", url: `${manifest.repository}.git`, ref: "main" };

const claude = {};
for (const key of ["name", "version", "description", "author", "homepage", "repository", "license", "keywords", "skills"]) {
  claude[key] = manifest[key];
}
claude.mcpServers = Object.fromEntries(Object.entries(manifest.mcpServers).map(([name, server]) => {
  assert.equal(server.command, "node");
  assert.equal(server.cwd, ".");
  assert.equal(server.args.length, 1);
  assert.match(server.args[0], /^\.\/scripts\/[a-z0-9-]+\.mjs$/);
  return [name, {
    command: "node",
    args: [`\${CLAUDE_PLUGIN_ROOT}/${server.args[0].slice(2)}`],
  }];
}));

// Agent Plugins 1.0.0 is the vendor-neutral package format that OpenWork's importer and other clients read.
// Its manifest is a closed schema, so only the permitted fields are copied; skills live in the fixed skills/ directory.
const AGENT_PLUGINS_SCHEMA = "https://agent-plugins.org/schemas/1.0.0";
const portable = { $schema: `${AGENT_PLUGINS_SCHEMA}/plugin.schema.json` };
for (const key of ["name", "version", "description", "author", "homepage", "repository", "license", "keywords"]) {
  portable[key] = manifest[key];
}
const portableMcp = {
  $schema: `${AGENT_PLUGINS_SCHEMA}/mcp.schema.json`,
  mcpServers: Object.fromEntries(Object.entries(manifest.mcpServers).map(([name, server]) => [name, {
    type: "stdio",
    command: "node",
    args: [`\${PLUGIN_ROOT}/${server.args[0].slice(2)}`],
    cwd: "${PLUGIN_ROOT}",
  }])),
};

const outputs = {
  "plugin.json": portable,
  "mcp.json": portableMcp,
  [codexCatalogPath]: catalog,
  ".claude-plugin/plugin.json": claude,
  ".claude-plugin/marketplace.json": {
    name: manifest.name,
    owner: manifest.author,
    metadata: { description: manifest.description },
    plugins: [{ name: manifest.name, source: "./", description: manifest.description }],
  },
};
for (const [relativePath, payload] of Object.entries(outputs)) {
  const target = path.join(root, relativePath);
  const expected = `${JSON.stringify(payload, null, 2)}\n`;
  if (process.argv.includes("--check")) {
    assert.equal((await readFile(target, "utf8")).replaceAll("\r\n", "\n"), expected, `Run node scripts/sync-plugin-metadata.mjs: ${relativePath}`);
  } else {
    await mkdir(path.dirname(target), { recursive: true });
    await writeFile(target, expected, "utf8");
  }
}
console.log(`${process.argv.includes("--check") ? "Verified" : "Updated"} Sivia metadata for Codex, Claude Code and Agent Plugins clients.`);

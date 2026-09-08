import assert from "node:assert/strict";
import { spawn } from "node:child_process";
import { mkdtemp, readFile, rmdir } from "node:fs/promises";
import os from "node:os";
import path from "node:path";
import { createInterface } from "node:readline";
import test from "node:test";
import { fileURLToPath } from "node:url";

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const json = async (relative) => JSON.parse(await readFile(path.join(root, relative), "utf8"));
const codex = await json(".codex-plugin/plugin.json");
const claude = await json(".claude-plugin/plugin.json");

test("documented install selectors resolve to the shared plugin and version", async () => {
  const codexCatalog = await json(".agents/plugins/marketplace.json");
  const claudeCatalog = await json(".claude-plugin/marketplace.json");
  assert.equal(codex.name, "sivia");
  assert.equal(claude.name, codex.name);
  assert.equal(claude.version, codex.version);
  for (const catalog of [codexCatalog, claudeCatalog]) {
    assert.equal(catalog.name, "sivia");
    assert.equal(catalog.plugins.length, 1);
    assert.equal(catalog.plugins[0].name, codex.name);
  }
  assert.equal(codexCatalog.plugins[0].source.url, "https://github.com/exsinger-hub/Sivia.git");
  assert.equal(claudeCatalog.plugins[0].source, "./");
  assert.equal(claude.skills, codex.skills);
  assert.deepEqual(Object.keys(claude.mcpServers), Object.keys(codex.mcpServers));
  await readFile(path.join(root, claude.skills, "design-scientific-figure/SKILL.md"));
});

function discover(server, cwd) {
  return new Promise((resolve, reject) => {
    const args = server.args.map((arg) => arg.replaceAll("${CLAUDE_PLUGIN_ROOT}", root));
    const child = spawn(process.execPath, args, { cwd, windowsHide: true, stdio: ["pipe", "pipe", "pipe"] });
    const lines = createInterface({ input: child.stdout });
    let stderr = "";
    let result;
    let failure;
    const timer = setTimeout(() => {
      failure = new Error(`MCP handshake timed out: ${args[0]} ${stderr}`);
      child.kill();
    }, 10000);
    child.stderr.on("data", (data) => { stderr += data; });
    child.once("error", (error) => {
      clearTimeout(timer);
      reject(error);
    });
    child.once("close", () => {
      clearTimeout(timer);
      lines.close();
      if (failure) reject(failure);
      else if (result) resolve(result);
      else reject(new Error(`MCP exited before tools/list: ${stderr}`));
    });
    const send = (message) => child.stdin.write(`${JSON.stringify(message)}\n`);
    lines.on("line", (line) => {
      try {
        const response = JSON.parse(line);
        if (response.error) throw new Error(JSON.stringify(response.error));
        if (response.id === 1) {
          assert.equal(response.result.protocolVersion, "2024-11-05");
          send({ jsonrpc: "2.0", method: "notifications/initialized" });
          send({ jsonrpc: "2.0", id: 2, method: "tools/list", params: {} });
        } else if (response.id === 2) {
          result = response.result.tools;
          child.kill();
        }
      } catch (error) {
        failure = error;
        child.kill();
      }
    });
    send({ jsonrpc: "2.0", id: 1, method: "initialize", params: {
      protocolVersion: "2024-11-05", capabilities: {}, clientInfo: { name: "sivia-packaging-test", version: "1.0.0" },
    } });
  });
}

for (const [serverName, server] of Object.entries(claude.mcpServers)) {
  test(`Claude ${serverName} initializes from an unrelated working directory`, async () => {
    const temp = await mkdtemp(path.join(os.tmpdir(), "sivia-mcp-test-"));
    try {
      assert.ok(server.args[0].startsWith("${CLAUDE_PLUGIN_ROOT}/scripts/"));
      const tools = await discover(server, temp);
      const expected = { "drawio-live": "drawio_live_get_capabilities", "drawio-file-utils": "drawio_status", "powerpoint-live": "powerpoint_status" };
      assert.ok(tools.some((tool) => tool.name === expected[serverName]));
    } finally {
      await rmdir(temp);
    }
  });
}

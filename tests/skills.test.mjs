import assert from "node:assert/strict";
import { existsSync } from "node:fs";
import { readFile, readdir } from "node:fs/promises";
import path from "node:path";
import test from "node:test";
import { fileURLToPath } from "node:url";

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const skillsRoot = path.join(root, "skills");
const names = (await readdir(skillsRoot, { withFileTypes: true })).filter((entry) => entry.isDirectory()).map((entry) => entry.name).sort();

function frontmatter(source) {
  const match = /^---\r?\n([\s\S]*?)\r?\n---/.exec(source);
  assert.ok(match, "SKILL.md starts with YAML frontmatter");
  const fields = {};
  // Descriptions here are single-line scalars; the Agent Skills fields we validate need nothing richer.
  for (const line of match[1].split(/\r?\n/)) {
    const pair = /^([A-Za-z][\w-]*):\s*(.*)$/.exec(line);
    if (pair) fields[pair[1]] = pair[2].trim();
  }
  return fields;
}

for (const name of names) {
  test(`${name}: frontmatter follows the Agent Skills / OpenCode rules`, async () => {
    const source = await readFile(path.join(skillsRoot, name, "SKILL.md"), "utf8");
    const fields = frontmatter(source);
    assert.equal(fields.name, name, "name matches its directory");
    assert.match(fields.name, /^[a-z0-9]+(-[a-z0-9]+)*$/);
    assert.ok(fields.name.length <= 64);
    assert.ok(fields.description && fields.description.length >= 1 && fields.description.length <= 1024, `description length ${fields.description?.length}`);
  });
}

test("skill names are unique and cross-references to other skills resolve", async () => {
  assert.equal(new Set(names).size, names.length);
  for (const name of names) {
    const source = await readFile(path.join(skillsRoot, name, "SKILL.md"), "utf8");
    for (const [, referenced] of source.matchAll(/`\$([a-z0-9]+(?:-[a-z0-9]+)+)`/g)) {
      assert.ok(names.includes(referenced), `${name} mentions $${referenced}, which is not a skill in this repository`);
    }
  }
});

const hostBullets = [
  "Other Sivia skills are loaded by name: Codex mentions `$name`, Claude Code uses `/sivia:<name>`, OpenCode and OpenWork call the `skill` tool with `{ name }`.",
  "MCP tools are written by bare name (`drawio_live_add_shape`). Some hosts prefix the server name, for example `sivia-drawio-live_drawio_live_add_shape` in OpenCode; use the tool whose name ends with the bare name.",
];

for (const name of names.filter((item) => item !== "support-sivia")) {
  test(`${name}: carries the shared Host notes`, async () => {
    const source = (await readFile(path.join(skillsRoot, name, "SKILL.md"), "utf8")).replaceAll("\r\n", "\n");
    assert.ok(source.includes("\n## Host notes\n"), "has a Host notes section");
    for (const bullet of hostBullets) assert.ok(source.includes(bullet), `missing shared bullet: ${bullet.slice(0, 50)}`);
    assert.match(source, /Sivia root/);
    assert.match(source, /\.sivia-installed\.json/, "tells the agent how to find the root for a copied skill");
  });
}

test("every skill ships a Codex interface file", () => {
  for (const name of names) assert.ok(existsSync(path.join(skillsRoot, name, "agents", "openai.yaml")) || name === "support-sivia", `${name}/agents/openai.yaml`);
});

test("sibling-relative skill references only point at skills that exist", async () => {
  for (const name of names) {
    const source = await readFile(path.join(skillsRoot, name, "SKILL.md"), "utf8");
    for (const [, sibling] of source.matchAll(/(?<![./])\.\.\/([a-z0-9-]+)\//g)) {
      assert.ok(names.includes(sibling), `${name} points at ../${sibling}/`);
    }
  }
});

import assert from "node:assert/strict";
import { existsSync } from "node:fs";
import { readFile, readdir } from "node:fs/promises";
import path from "node:path";
import test from "node:test";
import { fileURLToPath } from "node:url";

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const skillDir = path.join(root, "skills", "generate-figure-elements");

test("generate-figure-elements is a valid, self-contained skill", async () => {
  const source = await readFile(path.join(skillDir, "SKILL.md"), "utf8");
  const header = /^---\r?\n([\s\S]*?)\r?\n---/.exec(source)?.[1] ?? "";
  const name = /^name:\s*(.+)$/m.exec(header)?.[1].trim();
  const description = /^description:\s*(.+)$/m.exec(header)?.[1].trim() ?? "";
  assert.equal(name, "generate-figure-elements", "name matches the directory");
  assert.ok(description.length > 0 && description.length <= 1024, `description length ${description.length}`);
  for (const file of ["agents/openai.yaml", "scripts/imagegen.mjs", "scripts/sivia_assets.py", "references/templates/element-sheet.txt", "references/element-plan.md", "references/sheet-prompting.md", "references/placement.md"]) {
    assert.ok(existsSync(path.join(skillDir, file)), file);
  }
});

test("every $skill mentioned by the skills this change touches exists", async () => {
  const skills = (await readdir(path.join(root, "skills"), { withFileTypes: true })).filter((entry) => entry.isDirectory()).map((entry) => entry.name);
  for (const name of ["design-scientific-figure", "recreate-scientific-figure", "recreate-scientific-figure-in-drawio", "edit-powerpoint-live", "generate-figure-elements"]) {
    const source = await readFile(path.join(root, "skills", name, "SKILL.md"), "utf8");
    for (const [, referenced] of source.matchAll(/`\$([a-z0-9]+(?:-[a-z0-9]+)+)`/g)) {
      assert.ok(skills.includes(referenced), `${name} mentions $${referenced}`);
    }
  }
});

test("the script fills every placeholder of the element prompt template", async () => {
  const template = await readFile(path.join(skillDir, "references", "templates", "element-sheet.txt"), "utf8");
  const script = await readFile(path.join(skillDir, "scripts", "sivia_assets.py"), "utf8");
  const used = new Set([...template.matchAll(/{{(\w+)}}/g)].map((match) => match[1]));
  assert.ok(used.size >= 8, "the template has placeholders");
  for (const placeholder of used) assert.ok(script.includes(`"${placeholder}":`), `{{${placeholder}}} is never filled`);
});

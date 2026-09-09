import assert from "node:assert/strict";
import { access, readFile } from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";
import test from "node:test";

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const docs = ["README.md", "README_ZH.md", "docs/workflow.md", "docs/workflow_ZH.md", "CHANGELOG.md", "skills/edit-powerpoint-live/references/reconstruction-recovery.md", "skills/edit-powerpoint-live/SKILL.md", "skills/recreate-scientific-figure/SKILL.md", "skills/audit-scientific-figure/SKILL.md", "skills/audit-scientific-figure/references/review-copies.md", "skills/design-scientific-figure/references/imagegen-first-workflow.md"];

for (const file of docs) {
  test(`${file}: local links resolve`, async () => {
    const source = (await readFile(path.join(root, file), "utf8")).replace(/```[\s\S]*?```/g, "");
    const links = [...source.matchAll(/\]\(([^\s)]+)\)|(?:href|src)="([^"]+)"/g)].map(m => m[1] ?? m[2]);
    for (const target of links) {
      if (/^(?:https?:|mailto:|#)/.test(target)) continue;
      const destination = path.resolve(root, path.dirname(file), decodeURIComponent(target.split("#")[0]));
      assert.ok(destination.startsWith(root + path.sep), `${file}: non-repository link ${target}`);
      await assert.doesNotReject(access(destination), `${file}: broken link ${target}`);
    }
  });
}

test("both language editions expose current version and resolvable install selectors", async () => {
  const manifest = JSON.parse(await readFile(path.join(root, ".codex-plugin/plugin.json"), "utf8"));
  const catalog = JSON.parse(await readFile(path.join(root, ".agents/plugins/marketplace.json"), "utf8"));
  for (const file of ["README.md", "README_ZH.md"]) {
    const source = await readFile(path.join(root, file), "utf8");
    assert.ok(source.includes(`version-${manifest.version}-blue`), `${file}: stale version badge`);
    assert.ok(source.includes(`codex plugin add ${manifest.name}@${catalog.name}`), `${file}: invalid Codex selector`);
    assert.ok(source.includes(`/plugin install ${manifest.name}@${catalog.name}`), `${file}: invalid Claude selector`);
    assert.ok(source.includes(file === "README.md" ? "README_ZH.md" : "README.md"), `${file}: missing language link`);
  }
});

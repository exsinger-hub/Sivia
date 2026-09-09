import assert from "node:assert/strict";
import { spawnSync } from "node:child_process";
import { readFileSync } from "node:fs";
import test from "node:test";

test("COM arrow names produce the Office MsoArrowheadStyle values", () => {
  const source = readFileSync(new URL("../scripts/powerpoint-bridge.ps1", import.meta.url), "utf8");
  // Execute the real pure mapper without loading the bridge or starting Office.
  const match = /^function Get-ArrowStyle \{[\s\S]*?^\}/m.exec(source);
  assert.ok(match, "Get-ArrowStyle must remain available");
  const program = `${match[0]}\n@('none','triangle','open','stealth','diamond','oval') | ForEach-Object { Get-ArrowStyle $_ } | ConvertTo-Json -Compress`;
  const result = spawnSync("pwsh", ["-NoProfile", "-NonInteractive", "-EncodedCommand", Buffer.from(program, "utf16le").toString("base64")], { encoding: "utf8", windowsHide: true });
  assert.equal(result.status, 0, result.stderr || result.stdout);
  // https://learn.microsoft.com/en-us/office/vba/api/office.msoarrowheadstyle
  assert.deepEqual(JSON.parse(result.stdout), [1, 2, 3, 4, 5, 6]);
});

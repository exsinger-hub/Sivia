import assert from "node:assert/strict";
import test from "node:test";
import { siviaHomeDirectory, siviaStateSubdirectory } from "../scripts/sivia-paths.mjs";

test("without overrides the state directory is the long-standing Codex location", () => {
  assert.equal(siviaHomeDirectory({ platform: "linux", env: {}, homeDir: "/home/u" }), "/home/u/.codex/you-only-figure-once");
  assert.equal(siviaHomeDirectory({ platform: "win32", env: {}, homeDir: "C:\\Users\\u" }), "C:\\Users\\u\\.codex\\you-only-figure-once");
  assert.equal(siviaStateSubdirectory("presentations", { platform: "linux", env: {}, homeDir: "/home/u" }), "/home/u/.codex/you-only-figure-once/presentations");
  assert.equal(siviaStateSubdirectory("officejs", { platform: "linux", env: {}, homeDir: "/home/u" }), "/home/u/.codex/you-only-figure-once/officejs");
});

test("SIVIA_HOME relocates every state subdirectory; blank values are ignored", () => {
  assert.equal(siviaHomeDirectory({ platform: "linux", env: { SIVIA_HOME: "/data/sivia" }, homeDir: "/home/u" }), "/data/sivia");
  assert.equal(siviaStateSubdirectory("officejs", { platform: "linux", env: { SIVIA_HOME: "/data/sivia" }, homeDir: "/home/u" }), "/data/sivia/officejs");
  assert.equal(siviaHomeDirectory({ platform: "linux", env: { SIVIA_HOME: "   " }, homeDir: "/home/u" }), "/home/u/.codex/you-only-figure-once");
});

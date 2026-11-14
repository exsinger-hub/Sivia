import assert from "node:assert/strict";
import { spawn } from "node:child_process";
import { mkdtemp, readFile, rm, writeFile } from "node:fs/promises";
import os from "node:os";
import path from "node:path";
import { createInterface } from "node:readline";
import test from "node:test";
import { fileURLToPath } from "node:url";

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
// A 1x1 PNG.
const PNG = Buffer.from("iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8z8BQDwAEhQGAhKmMIQAAAABJRU5ErkJggg==", "base64");

function callTool(name, args, cwd) {
  return new Promise((resolve, reject) => {
    const child = spawn(process.execPath, [path.join(root, "scripts", "server.mjs")], { cwd, windowsHide: true, stdio: ["pipe", "pipe", "pipe"] });
    const lines = createInterface({ input: child.stdout });
    const timer = setTimeout(() => { child.kill(); reject(new Error("tool call timed out")); }, 20000);
    const send = (message) => child.stdin.write(`${JSON.stringify(message)}\n`);
    lines.on("line", (line) => {
      const response = JSON.parse(line);
      if (response.id === 1) {
        send({ jsonrpc: "2.0", method: "notifications/initialized" });
        send({ jsonrpc: "2.0", id: 2, method: "tools/call", params: { name, arguments: args } });
      } else if (response.id === 2) {
        clearTimeout(timer);
        // Resolve only once the process is gone: on Windows it keeps its working directory locked until then.
        child.once("close", () => resolve(response));
        child.kill();
      }
    });
    send({ jsonrpc: "2.0", id: 1, method: "initialize", params: { protocolVersion: "2024-11-05", capabilities: {}, clientInfo: { name: "sivia-image-style-test", version: "1" } } });
  });
}

test("embedded images keep their payload: draw.io style data URIs must not contain ';base64'", async (t) => {
  const dir = await mkdtemp(path.join(os.tmpdir(), "sivia-image-style-"));
  t.after(() => rm(dir, { recursive: true, force: true, maxRetries: 5, retryDelay: 100 }));
  const image = path.join(dir, "asset.png");
  const output = path.join(dir, "figure.drawio");
  await writeFile(image, PNG);
  const response = await callTool("drawio_create_diagram", {
    output_path: output,
    workflow_context: "explicit-file-only-request",
    vertices: [{
      id: "asset", shape: "image", x: 10, y: 10, width: 100, height: 100, image_path: image,
      raster_reason: "Independent illustrative artwork with no native equivalent", source_is_tightly_cropped: true,
      atomic_raster_unit: true, contains_reconstructable_content: false, decomposition_note: "Labels are rebuilt natively outside the picture",
    }],
  }, dir);
  assert.ok(!response.error && !response.result?.isError, JSON.stringify(response).slice(0, 400));
  const xml = await readFile(output, "utf8");
  const style = xml.match(/style="([^"]*shape=image[^"]*)"/)?.[1];
  assert.ok(style, "an image cell was written");
  assert.ok(style.includes(`image=data:image/png,${PNG.toString("base64")}`), "the base64 payload follows 'data:image/png,' directly");
  assert.ok(!style.includes(";base64,"), "';' would end the style value and leave a broken image");
  // Everything after the image value must still parse as ordinary style entries.
  const entries = style.split(";").filter(Boolean);
  assert.ok(entries.every((entry) => entry.includes("=") || entry === "html" || /^[a-zA-Z]+$/.test(entry)), entries.filter((entry) => !entry.includes("=")).join("|"));
});

test("the live draw.io server applies the same rule when it inserts an image", async () => {
  // The live server needs a draw.io desktop window, so assert the wiring in source and keep the
  // behaviour covered by the file-utils test above.
  const source = await readFile(path.join(root, "scripts", "live-server.mjs"), "utf8");
  assert.match(source, /function styleSafeDataUri\(/);
  assert.match(source, /image=\$\{styleSafeDataUri\(imageDataUrl\)\}/);
});

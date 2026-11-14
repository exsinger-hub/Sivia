import assert from "node:assert/strict";
import { execFile, spawn } from "node:child_process";
import { mkdir, mkdtemp, readFile, rm, writeFile } from "node:fs/promises";
import os from "node:os";
import path from "node:path";
import { createInterface } from "node:readline";
import test from "node:test";
import { fileURLToPath } from "node:url";
import { promisify } from "node:util";

const execFileAsync = promisify(execFile);
const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const script = path.join(root, "skills", "generate-figure-elements", "scripts", "sivia_assets.py");

async function findPython() {
  const candidates = [
    process.env.SIVIA_PYTHON && [process.env.SIVIA_PYTHON, []],
    process.env.YOU_ONLY_FIGURE_ONCE_PYTHON && [process.env.YOU_ONLY_FIGURE_ONCE_PYTHON, []],
    ["python3", []], ["python", []], ["py", ["-3"]],
  ].filter(Boolean);
  for (const [command, prefix] of candidates) {
    try {
      await execFileAsync(command, [...prefix, "-c", "import PIL, numpy"], { timeout: 20000 });
      return { command, prefix };
    } catch { /* try the next interpreter */ }
  }
  return null;
}

const python = await findPython();

async function assets(workdir, ...args) {
  try {
    const { stdout } = await execFileAsync(python.command, [...python.prefix, script, args[0], "--workdir", workdir, ...args.slice(1)], { maxBuffer: 32 * 1024 * 1024 });
    return JSON.parse(stdout);
  } catch (error) {
    throw new Error(`${args[0]} failed: ${error.stderr || error.message}`);
  }
}

function listTools(serverScript, cwd) {
  return new Promise((resolve, reject) => {
    const child = spawn(process.execPath, [path.join(root, "scripts", serverScript)], { cwd, windowsHide: true, stdio: ["pipe", "pipe", "pipe"] });
    const lines = createInterface({ input: child.stdout });
    const timer = setTimeout(() => { child.kill(); reject(new Error(`${serverScript} did not answer tools/list`)); }, 15000);
    const send = (message) => child.stdin.write(`${JSON.stringify(message)}\n`);
    lines.on("line", (line) => {
      const response = JSON.parse(line);
      if (response.id === 1) {
        send({ jsonrpc: "2.0", method: "notifications/initialized" });
        send({ jsonrpc: "2.0", id: 2, method: "tools/list", params: {} });
      } else if (response.id === 2) {
        clearTimeout(timer);
        // Resolve only once the process is gone: on Windows it keeps its working directory locked until then.
        const tools = Object.fromEntries(response.result.tools.map((tool) => [tool.name, tool.inputSchema]));
        child.once("close", () => resolve(tools));
        child.kill();
      }
    });
    send({ jsonrpc: "2.0", id: 1, method: "initialize", params: { protocolVersion: "2024-11-05", capabilities: {}, clientInfo: { name: "sivia-elements-test", version: "1" } } });
  });
}

// The subset of JSON Schema the Sivia tools use.
function validate(schema, value, where, problems = []) {
  const type = schema.type;
  if (schema.const !== undefined && value !== schema.const) problems.push(`${where}: must equal ${JSON.stringify(schema.const)}`);
  if (type === "string" && typeof value !== "string") problems.push(`${where}: expected string`);
  if (type === "boolean" && typeof value !== "boolean") problems.push(`${where}: expected boolean`);
  if (type === "number" && typeof value !== "number") problems.push(`${where}: expected number`);
  if (type === "integer" && !Number.isInteger(value)) problems.push(`${where}: expected integer`);
  if (typeof value === "string" && schema.minLength && value.length < schema.minLength) problems.push(`${where}: shorter than ${schema.minLength}`);
  if (typeof value === "number") {
    if (schema.minimum !== undefined && value < schema.minimum) problems.push(`${where}: below ${schema.minimum}`);
    if (schema.maximum !== undefined && value > schema.maximum) problems.push(`${where}: above ${schema.maximum}`);
    if (schema.exclusiveMinimum !== undefined && value <= schema.exclusiveMinimum) problems.push(`${where}: not above ${schema.exclusiveMinimum}`);
  }
  if (type === "object") {
    for (const key of schema.required ?? []) if (!(key in value)) problems.push(`${where}: missing required ${key}`);
    for (const [key, item] of Object.entries(value)) {
      const child = schema.properties?.[key];
      if (!child) { if (schema.additionalProperties === false) problems.push(`${where}: unexpected property ${key}`); continue; }
      validate(child, item, `${where}.${key}`, problems);
    }
  }
  return problems;
}

const skip = python ? false : "no Python with Pillow and numpy available";

test("placement arguments satisfy the live draw.io and PowerPoint tool schemas", { skip }, async (t) => {
  const dir = await mkdtemp(path.join(os.tmpdir(), "sivia-elements-"));
  t.after(() => rm(dir, { recursive: true, force: true, maxRetries: 5, retryDelay: 100 }));
  const plan = {
    figure: { id: "t", ref_size_px: [1600, 900], width_mm: 160, target_dpi: 300 },
    style: { summary: "flat", palette: ["#1F2937", "#F58518"] },
    elements: [
      { id: "robot", description: "round robot", slot: { bbox_px: [100, 200, 500, 600] }, alt_text: "Robot" },
      { id: "book", description: "closed book", slot: { bbox_px: [700, 200, 1100, 600] } },
    ],
  };
  await writeFile(path.join(dir, "elements.json"), JSON.stringify(plan));
  await assets(dir, "prompt", "--canvas", "1536x1024", "--key", "#00FF00", "--per-sheet", "2");
  const sheetId = JSON.parse(await readFile(path.join(dir, "prompts", "sheet-01.layout.json"), "utf8")).sheet_id;
  const draw = `
import sys
from PIL import Image, ImageDraw
img = Image.new("RGB", (1536, 1024), (0, 255, 0))
d = ImageDraw.Draw(img)
d.ellipse([190, 260, 570, 740], fill=(245, 133, 24), outline=(31, 41, 55), width=8)
d.rectangle([960, 290, 1340, 730], fill=(31, 41, 80))
img.save(sys.argv[1])
`;
  await mkdir(path.join(dir, "sheets"), { recursive: true });
  await execFileAsync(python.command, [...python.prefix, "-c", draw, path.join(dir, "sheets", `${sheetId}.png`)]);
  await assets(dir, "cutout", "--sheet-id", sheetId);
  await assets(dir, "split", "--sheet-id", sheetId);
  const qa = await assets(dir, "qa");
  assert.equal(qa.summary.fail, 0, JSON.stringify(qa.elements));

  const drawio = await assets(dir, "place", "--backend", "drawio");
  const ppt = await assets(dir, "place", "--backend", "pptx", "--canvas", "960x540");
  const liveTools = await listTools("live-server.mjs", dir);
  const pptTools = await listTools("powerpoint-server.mjs", dir);

  assert.equal(drawio.calls.length, 2);
  for (const call of drawio.calls) {
    const schema = liveTools[call.tool];
    assert.ok(schema, `${call.tool} exists on the draw.io server`);
    assert.deepEqual(validate(schema, call.arguments, call.tool), []);
  }
  assert.equal(ppt.calls.length, 2);
  for (const call of ppt.calls) {
    const schema = pptTools[call.tool];
    assert.ok(schema, `${call.tool} exists on the PowerPoint server`);
    assert.deepEqual(validate(schema, call.arguments, call.tool), []);
  }
  assert.equal(ppt.warnings.length, 0, "16:9 reference on a 16:9 canvas needs no aspect warning");
});

test("a canvas whose aspect differs from the approved reference is called out", { skip }, async (t) => {
  const dir = await mkdtemp(path.join(os.tmpdir(), "sivia-elements-"));
  t.after(() => rm(dir, { recursive: true, force: true, maxRetries: 5, retryDelay: 100 }));
  await writeFile(path.join(dir, "elements.json"), JSON.stringify({
    figure: { ref_size_px: [1800, 800], width_mm: 160 },
    elements: [{ id: "a", description: "x", slot: { bbox_px: [0, 0, 100, 100] } }],
  }));
  await assets(dir, "prompt", "--key", "#00FF00");
  await mkdir(path.join(dir, "sheets"), { recursive: true });
  const make = `
import sys
from PIL import Image, ImageDraw
img = Image.new("RGBA", (1024, 1024), (0, 0, 0, 0))
ImageDraw.Draw(img).ellipse([300, 300, 700, 700], fill=(245, 133, 24, 255))
img.save(sys.argv[1])
`;
  await execFileAsync(python.command, [...python.prefix, "-c", make, path.join(dir, "sheets", "sheet-01.rgba.png")]);
  await assets(dir, "split", "--sheet-id", "sheet-01");
  const placed = await assets(dir, "place", "--backend", "pptx");
  assert.match(placed.warnings[0], /aspect/);
  assert.match(placed.warnings[0], /--canvas 960x426/);
});

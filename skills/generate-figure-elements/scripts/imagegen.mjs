#!/usr/bin/env node
// Host-neutral image generation for Sivia: Azure OpenAI / Microsoft Foundry, OpenAI, or any OpenAI-compatible endpoint.
//
// Codex ships its own image tool; OpenCode, OpenWork and Claude Code do not. This CLI gives those hosts the same
// "prompt in, PNG + exact prompt record out" step, with no dependencies beyond Node 18+.
//
//   node imagegen.mjs status
//   node imagegen.mjs generate --prompt-file sheet.txt --size 1536x1024 --quality high --out sheets/sheet-01.png
//   node imagegen.mjs edit --prompt-file sheet.txt --image style-ref.png --out sheets/sheet-01.png
//
// Credentials are read from the environment only and are never printed or written to the sidecar record:
//   Azure : AZURE_OPENAI_API_KEY, AZURE_OPENAI_ENDPOINT (or AZURE_OPENAI_BASE_URL), AZURE_OPENAI_DEPLOYMENT,
//           AZURE_OPENAI_API_VERSION (legacy endpoints only)
//   OpenAI: OPENAI_API_KEY, optional OPENAI_BASE_URL, OPENAI_IMAGE_MODEL (default gpt-image-1)
//   Other : SIVIA_IMAGE_BASE_URL, SIVIA_IMAGE_MODEL, optional SIVIA_IMAGE_API_KEY
import { createHash } from "node:crypto";
import { realpathSync } from "node:fs";
import { mkdir, readFile, writeFile } from "node:fs/promises";
import path from "node:path";
import { parseArgs } from "node:util";
import { fileURLToPath } from "node:url";

// Node resolves links (junctions, symlinks) for the entry module but leaves process.argv[1] untouched, so a plain
// URL comparison would never run main() when the skill is installed as a link. Compare real paths instead.
export function isEntryPoint(metaUrl, argv1 = process.argv[1]) {
  if (!argv1) return false;
  try {
    return realpathSync.native(argv1) === realpathSync.native(fileURLToPath(metaUrl));
  } catch {
    return false;
  }
}

export class ImageGenError extends Error {
  constructor(message, { code = 1, status, hint } = {}) {
    super(message);
    this.exitCode = code;
    this.status = status;
    this.hint = hint;
  }
}

const QUALITIES = new Set(["low", "medium", "high", "auto"]);
const FORMATS = new Set(["png", "jpeg", "webp"]);
const BACKGROUNDS = new Set(["transparent", "opaque", "auto"]);
const FIXED_SIZES = new Set(["1024x1024", "1024x1536", "1536x1024"]);
const RETRYABLE = new Set([408, 429, 500, 502, 503, 504]);

// ---------------------------------------------------------------------------------------------
// Provider resolution
// ---------------------------------------------------------------------------------------------
function trimUrl(value) {
  return String(value ?? "").trim().replace(/[?#].*$/, "").replace(/\/+$/, "");
}

export function resolveProvider(env = process.env, flags = {}) {
  const requested = (flags.provider || "auto").toLowerCase();
  if (!["auto", "azure", "openai", "compatible"].includes(requested)) {
    throw new ImageGenError(`--provider must be auto, azure, openai or compatible (got ${requested})`, { code: 2 });
  }
  const azureKey = env.AZURE_OPENAI_API_KEY?.trim();
  const azureEndpoint = flags.endpoint || env.AZURE_OPENAI_ENDPOINT || env.AZURE_OPENAI_BASE_URL;
  const azureDeployment = flags.model || env.AZURE_OPENAI_DEPLOYMENT;
  const openaiKey = env.OPENAI_API_KEY?.trim();
  const otherBase = flags.endpoint || env.SIVIA_IMAGE_BASE_URL;

  const missing = [];
  let kind = requested;
  if (kind === "auto") {
    if (azureKey && azureEndpoint && azureDeployment) kind = "azure";
    else if (openaiKey) kind = "openai";
    else if (otherBase && env.SIVIA_IMAGE_MODEL) kind = "compatible";
    else {
      throw new ImageGenError(
        "No image provider is configured. Set AZURE_OPENAI_API_KEY + AZURE_OPENAI_ENDPOINT (or AZURE_OPENAI_BASE_URL) + AZURE_OPENAI_DEPLOYMENT, or OPENAI_API_KEY, or SIVIA_IMAGE_BASE_URL + SIVIA_IMAGE_MODEL.",
        { code: 2 },
      );
    }
  }

  if (kind === "azure") {
    if (!azureKey) missing.push("AZURE_OPENAI_API_KEY");
    if (!azureEndpoint) missing.push("AZURE_OPENAI_ENDPOINT (or AZURE_OPENAI_BASE_URL)");
    if (!azureDeployment) missing.push("AZURE_OPENAI_DEPLOYMENT (or --model)");
    if (missing.length) throw new ImageGenError(`Azure provider is missing: ${missing.join(", ")}`, { code: 2 });
    let base = trimUrl(azureEndpoint);
    let deployment = azureDeployment;
    const legacy = base.match(/^(.*?)\/openai\/deployments\/([^/]+)(?:\/.*)?$/);
    let apiVersion = null;
    let mode = "v1";
    if (legacy) {
      base = legacy[1];
      deployment = flags.model || legacy[2];
      mode = "legacy";
    } else if (!/\/openai\/v1$/.test(base)) {
      mode = "legacy";
    }
    if (mode === "legacy") {
      apiVersion = flags["api-version"] || env.AZURE_OPENAI_API_VERSION || String(azureEndpoint).match(/api-version=([^&]+)/)?.[1];
      if (!apiVersion) {
        throw new ImageGenError("A legacy Azure endpoint also needs AZURE_OPENAI_API_VERSION (for example 2025-04-01-preview), or use the .../openai/v1 base URL.", { code: 2 });
      }
    }
    const root = mode === "v1" ? base : `${base}/openai/deployments/${deployment}`;
    return {
      kind, mode, model: deployment, key: azureKey, authHeaders: { "api-key": azureKey },
      url: (operation) => `${root}/images/${operation}${apiVersion ? `?api-version=${encodeURIComponent(apiVersion)}` : ""}`,
      host: new URL(base).host,
    };
  }

  if (kind === "openai") {
    if (!openaiKey) throw new ImageGenError("OpenAI provider needs OPENAI_API_KEY", { code: 2 });
    const base = trimUrl(flags.endpoint || env.OPENAI_BASE_URL || "https://api.openai.com/v1");
    return {
      kind, mode: "v1", model: flags.model || env.OPENAI_IMAGE_MODEL || "gpt-image-1", key: openaiKey,
      authHeaders: { Authorization: `Bearer ${openaiKey}` }, url: (operation) => `${base}/images/${operation}`, host: new URL(base).host,
    };
  }

  const base = trimUrl(otherBase);
  const model = flags.model || env.SIVIA_IMAGE_MODEL;
  if (!base) missing.push("SIVIA_IMAGE_BASE_URL");
  if (!model) missing.push("SIVIA_IMAGE_MODEL (or --model)");
  if (missing.length) throw new ImageGenError(`Compatible provider is missing: ${missing.join(", ")}`, { code: 2 });
  const key = env.SIVIA_IMAGE_API_KEY?.trim();
  return { kind: "compatible", mode: "v1", model, key, authHeaders: key ? { Authorization: `Bearer ${key}` } : {}, url: (operation) => `${base}/images/${operation}`, host: new URL(base).host };
}

// ---------------------------------------------------------------------------------------------
// Validation
// ---------------------------------------------------------------------------------------------
export function validateSize(size, model = "") {
  if (size === "auto") return;
  const match = /^(\d+)x(\d+)$/.exec(size);
  if (!match) throw new ImageGenError(`--size must be WxH (for example 1536x1024) or auto, got ${size}`, { code: 2 });
  const width = Number(match[1]);
  const height = Number(match[2]);
  if (/image-2/i.test(model)) {
    const problems = [];
    if (width % 16 || height % 16) problems.push("both edges must be multiples of 16");
    if (Math.max(width, height) > 3840) problems.push("the long edge must be at most 3840");
    if (Math.max(width, height) / Math.min(width, height) > 3) problems.push("the aspect ratio must be at most 3:1");
    const pixels = width * height;
    if (pixels < 655360 || pixels > 8294400) problems.push("the total pixel count must be between 655,360 and 8,294,400");
    if (problems.length) throw new ImageGenError(`Size ${size} is not valid for ${model}: ${problems.join("; ")}.`, { code: 2 });
  } else if (/gpt-image-1/i.test(model) && !FIXED_SIZES.has(size)) {
    throw new ImageGenError(`${model} only accepts ${[...FIXED_SIZES].join(", ")} or auto (got ${size}).`, { code: 2 });
  }
}

function mimeFor(file) {
  const ext = path.extname(file).toLowerCase();
  return ext === ".jpg" || ext === ".jpeg" ? "image/jpeg" : ext === ".webp" ? "image/webp" : "image/png";
}

function pngSize(buffer) {
  if (buffer.length > 24 && buffer.readUInt32BE(0) === 0x89504e47) return { width: buffer.readUInt32BE(16), height: buffer.readUInt32BE(20) };
  return null;
}

const sha256 = (buffer) => createHash("sha256").update(buffer).digest("hex");

// ---------------------------------------------------------------------------------------------
// Request construction
// ---------------------------------------------------------------------------------------------
export async function buildRequest(operation, provider, options) {
  const common = { model: provider.model, prompt: options.prompt, n: options.n, size: options.size, quality: options.quality, output_format: options.format };
  if (options.background) common.background = options.background;
  if (operation === "generate") {
    return { url: provider.url("generations"), headers: { "Content-Type": "application/json", ...provider.authHeaders }, json: common };
  }
  const form = new FormData();
  for (const [name, value] of Object.entries(common)) form.append(name, String(value));
  if (options.inputFidelity) form.append("input_fidelity", options.inputFidelity);
  const inputs = [];
  for (const file of options.images) {
    const bytes = await readFile(file).catch(() => { throw new ImageGenError(`Cannot read input image: ${file}`, { code: 2 }); });
    form.append("image[]", new Blob([bytes], { type: mimeFor(file) }), path.basename(file));
    inputs.push({ path: path.resolve(file), sha256: sha256(bytes) });
  }
  let mask = null;
  if (options.mask) {
    const bytes = await readFile(options.mask).catch(() => { throw new ImageGenError(`Cannot read mask: ${options.mask}`, { code: 2 }); });
    form.append("mask", new Blob([bytes], { type: "image/png" }), path.basename(options.mask));
    mask = { path: path.resolve(options.mask), sha256: sha256(bytes) };
  }
  return { url: provider.url("edits"), headers: { ...provider.authHeaders }, form, inputs, mask };
}

function redact(headers) {
  return Object.fromEntries(Object.entries(headers).map(([key, value]) => [key, /key|authorization/i.test(key) ? "<redacted>" : value]));
}

async function send(request, { fetchImpl, timeoutMs, retries }) {
  let lastError;
  for (let attempt = 0; attempt <= retries; attempt += 1) {
    try {
      const response = await fetchImpl(request.url, {
        method: "POST",
        headers: request.headers,
        body: request.json ? JSON.stringify(request.json) : request.form,
        signal: AbortSignal.timeout(timeoutMs),
      });
      const text = await response.text();
      let payload;
      try { payload = text ? JSON.parse(text) : {}; } catch { payload = { raw: text.slice(0, 500) }; }
      if (response.ok) return payload;
      const message = payload?.error?.message || payload?.message || payload?.raw || `HTTP ${response.status}`;
      const error = new ImageGenError(`Image API returned ${response.status}: ${message}`, {
        status: response.status,
        hint: /transparent/i.test(message) ? "This deployment cannot return a transparent background. Generate on a flat key color and run sivia_assets.py cutout instead." : undefined,
      });
      if (!RETRYABLE.has(response.status) || attempt === retries) throw error;
      lastError = error;
      const wait = Number(response.headers.get("retry-after")) * 1000 || Math.min(30000, 2000 * 1.8 ** attempt);
      await new Promise((resolve) => setTimeout(resolve, wait));
    } catch (error) {
      if (error instanceof ImageGenError) throw error;
      const timedOut = error?.name === "TimeoutError" || error?.name === "AbortError";
      lastError = new ImageGenError(timedOut ? `Image API did not answer within ${Math.round(timeoutMs / 1000)} s (high quality can take 60-120 s; raise --timeout-s)` : `Network error: ${error.message}`);
      if (attempt === retries) throw lastError;
      await new Promise((resolve) => setTimeout(resolve, 1500 * (attempt + 1)));
    }
  }
  throw lastError;
}

async function download(url, fetchImpl) {
  const response = await fetchImpl(url);
  if (!response.ok) throw new ImageGenError(`Could not download generated image (HTTP ${response.status})`);
  return Buffer.from(await response.arrayBuffer());
}

// ---------------------------------------------------------------------------------------------
// Commands
// ---------------------------------------------------------------------------------------------
function outputPaths(options, count) {
  const extension = options.format === "jpeg" ? "jpg" : options.format;
  if (options.out) {
    if (count === 1) return [path.resolve(options.out)];
    const parsed = path.parse(path.resolve(options.out));
    return Array.from({ length: count }, (_, index) => path.join(parsed.dir, `${parsed.name}-${index + 1}${parsed.ext || `.${extension}`}`));
  }
  const dir = path.resolve(options.outDir || ".");
  const stem = options.name || `image-${new Date().toISOString().replace(/[-:T.Z]/g, "").slice(0, 14)}`;
  return Array.from({ length: count }, (_, index) => path.join(dir, count === 1 ? `${stem}.${extension}` : `${stem}-${index + 1}.${extension}`));
}

export async function runOperation(operation, options, { env = process.env, fetchImpl = globalThis.fetch } = {}) {
  const provider = resolveProvider(env, options);
  if (!options.prompt?.trim()) throw new ImageGenError("A prompt is required: --prompt or --prompt-file", { code: 2 });
  if (!QUALITIES.has(options.quality)) throw new ImageGenError(`--quality must be one of ${[...QUALITIES].join(", ")}`, { code: 2 });
  if (!FORMATS.has(options.format)) throw new ImageGenError(`--format must be one of ${[...FORMATS].join(", ")}`, { code: 2 });
  if (options.background && !BACKGROUNDS.has(options.background)) throw new ImageGenError(`--background must be one of ${[...BACKGROUNDS].join(", ")}`, { code: 2 });
  if (options.background === "transparent" && options.format === "jpeg") throw new ImageGenError("transparent backgrounds need --format png or webp", { code: 2 });
  if (!Number.isInteger(options.n) || options.n < 1 || options.n > 10) throw new ImageGenError("--n must be an integer from 1 to 10", { code: 2 });
  validateSize(options.size, provider.model);
  if (operation === "edit" && !options.images.length) throw new ImageGenError("edit needs at least one --image", { code: 2 });

  const request = await buildRequest(operation, provider, options);
  const summary = {
    operation, provider: provider.kind, mode: provider.mode, model: provider.model, endpoint_host: provider.host,
    url: request.url, headers: redact(request.headers), size: options.size, quality: options.quality, n: options.n, format: options.format,
    background: options.background ?? null, prompt_chars_nonspace: options.prompt.replace(/\s+/g, "").length,
  };
  if (options.dryRun) return { dry_run: true, ...summary, prompt: options.prompt, input_images: request.inputs ?? [], mask: request.mask ?? null };
  if (typeof fetchImpl !== "function") throw new ImageGenError("This Node version has no fetch; use Node 18 or newer", { code: 2 });

  const started = Date.now();
  const payload = await send(request, { fetchImpl, timeoutMs: options.timeoutS * 1000, retries: options.retries });
  const items = Array.isArray(payload.data) ? payload.data : [];
  if (!items.length) throw new ImageGenError(`The API answered without images: ${JSON.stringify(payload).slice(0, 300)}`);
  const targets = outputPaths(options, items.length);
  const outputs = [];
  for (let index = 0; index < items.length; index += 1) {
    const item = items[index];
    const bytes = item.b64_json ? Buffer.from(item.b64_json, "base64") : item.url ? await download(item.url, fetchImpl) : null;
    if (!bytes?.length) throw new ImageGenError(`Result ${index + 1} contained neither b64_json nor url`);
    await mkdir(path.dirname(targets[index]), { recursive: true });
    await writeFile(targets[index], bytes);
    const dimensions = pngSize(bytes);
    const record = {
      tool: "sivia-imagegen", record_version: 1, created_at: new Date().toISOString(), operation, provider: provider.kind, model: provider.model,
      endpoint_host: provider.host, request: { size: options.size, quality: options.quality, n: options.n, format: options.format, background: options.background ?? null,
        input_images: request.inputs ?? [], mask: request.mask ?? null, input_fidelity: options.inputFidelity ?? null },
      prompt: options.prompt, prompt_chars_nonspace: summary.prompt_chars_nonspace, revised_prompt: item.revised_prompt ?? null,
      output: { file: targets[index], bytes: bytes.length, sha256: sha256(bytes), ...(dimensions ?? {}) }, usage: payload.usage ?? null,
    };
    await writeFile(`${targets[index]}.json`, `${JSON.stringify(record, null, 2)}\n`, "utf8");
    outputs.push({ file: targets[index], record: `${targets[index]}.json`, bytes: bytes.length, ...(dimensions ?? {}) });
  }
  return { ...summary, seconds: Math.round((Date.now() - started) / 100) / 10, outputs, hint: "Inspect the image itself: requested and returned sizes can differ, and transparency must be verified from real alpha." };
}

export function statusReport(env = process.env, flags = {}) {
  try {
    const provider = resolveProvider(env, flags);
    return { configured: true, provider: provider.kind, mode: provider.mode, model: provider.model, endpoint_host: provider.host, has_key: Boolean(provider.key) };
  } catch (error) {
    return { configured: false, error: error.message };
  }
}

const OPTIONS = {
  provider: { type: "string" }, model: { type: "string" }, endpoint: { type: "string" }, "api-version": { type: "string" },
  prompt: { type: "string" }, "prompt-file": { type: "string" },
  size: { type: "string", default: "1024x1024" }, quality: { type: "string", default: "medium" }, n: { type: "string", default: "1" },
  format: { type: "string", default: "png" }, background: { type: "string" },
  out: { type: "string" }, "out-dir": { type: "string" }, name: { type: "string" },
  image: { type: "string", multiple: true }, mask: { type: "string" }, "input-fidelity": { type: "string" },
  "timeout-s": { type: "string", default: "300" }, retries: { type: "string", default: "2" },
  "dry-run": { type: "boolean", default: false }, help: { type: "boolean", short: "h", default: false },
};

const HELP = `Sivia image generation

  node imagegen.mjs status
  node imagegen.mjs generate --prompt-file prompt.txt --size 1536x1024 --quality high --out sheet.png
  node imagegen.mjs edit --prompt-file prompt.txt --image reference.png [--mask mask.png] --out result.png

Options: --provider auto|azure|openai|compatible  --model  --endpoint  --api-version
         --size WxH|auto  --quality low|medium|high|auto  --n 1-10  --format png|jpeg|webp  --background transparent|opaque|auto
         --out FILE | --out-dir DIR --name STEM   --image FILE (repeat)  --mask FILE  --input-fidelity low|high
         --timeout-s 300  --retries 2  --dry-run (print the request without calling the API)

Every output gets a <file>.json record with the exact prompt, parameters and SHA-256. Keys are never written.
`;

export async function main(argv = process.argv.slice(2), context = {}) {
  const write = context.stdout ?? ((text) => process.stdout.write(text));
  let parsed;
  try {
    parsed = parseArgs({ args: argv, options: OPTIONS, allowPositionals: true, strict: true });
  } catch (error) {
    process.stderr.write(`imagegen: ${error.message}\n`);
    return 2;
  }
  const { values, positionals } = parsed;
  const command = positionals[0];
  if (values.help || !command) { write(HELP); return command || values.help ? 0 : 2; }
  const env = context.env ?? process.env;
  try {
    if (command === "status") {
      const report = statusReport(env, { provider: values.provider, model: values.model, endpoint: values.endpoint, "api-version": values["api-version"] });
      write(`${JSON.stringify(report, null, 2)}\n`);
      return report.configured ? 0 : 1;
    }
    if (command !== "generate" && command !== "edit") throw new ImageGenError(`Unknown command: ${command}`, { code: 2 });
    let prompt = values.prompt;
    if (values["prompt-file"]) prompt = await readFile(values["prompt-file"], "utf8").catch(() => { throw new ImageGenError(`Cannot read prompt file: ${values["prompt-file"]}`, { code: 2 }); });
    const result = await runOperation(command, {
      provider: values.provider, model: values.model, endpoint: values.endpoint, "api-version": values["api-version"],
      prompt, size: values.size, quality: values.quality, n: Number(values.n), format: values.format, background: values.background,
      out: values.out, outDir: values["out-dir"], name: values.name, images: values.image ?? [], mask: values.mask,
      inputFidelity: values["input-fidelity"], timeoutS: Number(values["timeout-s"]), retries: Number(values.retries), dryRun: values["dry-run"],
    }, { env, fetchImpl: context.fetchImpl ?? globalThis.fetch });
    write(`${JSON.stringify(result, null, 2)}\n`);
    return 0;
  } catch (error) {
    if (!(error instanceof ImageGenError)) throw error;
    process.stderr.write(`imagegen: ${error.message}\n${error.hint ? `hint: ${error.hint}\n` : ""}`);
    return error.exitCode;
  }
}

if (isEntryPoint(import.meta.url)) {
  main().then((code) => { process.exitCode = code; }, (error) => {
    process.stderr.write(`imagegen: unexpected error: ${error.stack || error}\n`);
    process.exitCode = 1;
  });
}

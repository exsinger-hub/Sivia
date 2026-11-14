import assert from "node:assert/strict";
import { createServer } from "node:http";
import { mkdtemp, readFile, rm, writeFile } from "node:fs/promises";
import os from "node:os";
import path from "node:path";
import test from "node:test";
import { ImageGenError, main, resolveProvider, runOperation, statusReport, validateSize } from "../skills/generate-figure-elements/scripts/imagegen.mjs";

const PNG_1X1 = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8z8BQDwAEhQGAhKmMIQAAAABJRU5ErkJggg==";
const SECRET = "sk-test-secret-value-123";
const AZURE = {
  AZURE_OPENAI_API_KEY: SECRET,
  AZURE_OPENAI_ENDPOINT: "https://res.services.ai.azure.com/openai/v1/",
  AZURE_OPENAI_DEPLOYMENT: "gpt-image-2.5-test",
};

async function temp(t) {
  const dir = await mkdtemp(path.join(os.tmpdir(), "sivia-imagegen-"));
  t.after(() => rm(dir, { recursive: true, force: true }));
  return dir;
}

function options(dir, extra = {}) {
  return { prompt: "flat sheet", size: "1024x1024", quality: "medium", n: 1, format: "png", images: [], timeoutS: 5, retries: 0, out: path.join(dir, "out.png"), ...extra };
}

function jsonResponse(status, body, headers = {}) {
  return new Response(JSON.stringify(body), { status, headers: { "content-type": "application/json", ...headers } });
}

test("Azure v1 endpoints keep their /openai/v1 path and authenticate with api-key", () => {
  const provider = resolveProvider(AZURE);
  assert.equal(provider.kind, "azure");
  assert.equal(provider.model, "gpt-image-2.5-test");
  assert.equal(provider.url("generations"), "https://res.services.ai.azure.com/openai/v1/images/generations");
  assert.deepEqual(provider.authHeaders, { "api-key": SECRET });
});

test("AZURE_OPENAI_BASE_URL is accepted as an alias for the endpoint", () => {
  const { AZURE_OPENAI_ENDPOINT, ...rest } = AZURE;
  const provider = resolveProvider({ ...rest, AZURE_OPENAI_BASE_URL: "https://res.services.ai.azure.com/openai/v1" });
  assert.equal(provider.url("edits"), "https://res.services.ai.azure.com/openai/v1/images/edits");
});

test("legacy Azure endpoints need an API version and build the deployment URL", () => {
  const legacy = { ...AZURE, AZURE_OPENAI_ENDPOINT: "https://res.cognitiveservices.azure.com" };
  assert.throws(() => resolveProvider(legacy), /API_VERSION/);
  const provider = resolveProvider({ ...legacy, AZURE_OPENAI_API_VERSION: "2025-04-01-preview" });
  assert.equal(provider.url("generations"), "https://res.cognitiveservices.azure.com/openai/deployments/gpt-image-2.5-test/images/generations?api-version=2025-04-01-preview");
  const full = resolveProvider({ AZURE_OPENAI_API_KEY: SECRET, AZURE_OPENAI_DEPLOYMENT: "x", AZURE_OPENAI_ENDPOINT: "https://res.cognitiveservices.azure.com/openai/deployments/gpt-image-2/images/generations?api-version=2025-04-01-preview" });
  assert.equal(full.model, "gpt-image-2", "the deployment is read from a pasted full URL");
  assert.match(full.url("generations"), /deployments\/gpt-image-2\/images\/generations\?api-version=2025-04-01-preview$/);
});

test("OpenAI and compatible providers resolve, and auto prefers Azure then OpenAI", () => {
  const openai = resolveProvider({ OPENAI_API_KEY: "k" });
  assert.equal(openai.url("generations"), "https://api.openai.com/v1/images/generations");
  assert.equal(openai.model, "gpt-image-1");
  assert.equal(resolveProvider({ ...AZURE, OPENAI_API_KEY: "k" }).kind, "azure");
  const other = resolveProvider({ SIVIA_IMAGE_BASE_URL: "http://localhost:9000/v1", SIVIA_IMAGE_MODEL: "local-img" });
  assert.equal(other.kind, "compatible");
  assert.deepEqual(other.authHeaders, {});
  assert.throws(() => resolveProvider({}), (error) => error instanceof ImageGenError && error.exitCode === 2);
  assert.throws(() => resolveProvider({ OPENAI_API_KEY: "k" }, { provider: "azure" }), /Azure provider is missing/);
});

test("status never reveals the key", () => {
  const report = statusReport(AZURE);
  assert.equal(report.configured, true);
  assert.equal(report.has_key, true);
  assert.ok(!JSON.stringify(report).includes(SECRET));
  assert.equal(statusReport({}).configured, false);
});

test("size rules follow the model family", () => {
  validateSize("1536x1024", "gpt-image-1");
  validateSize("auto", "gpt-image-1");
  assert.throws(() => validateSize("1024x768", "gpt-image-1"), /only accepts/);
  validateSize("2048x1360", "gpt-image-2.5-sunburst");
  assert.throws(() => validateSize("1500x1000", "gpt-image-2"), /multiples of 16/);
  assert.throws(() => validateSize("3840x1024", "gpt-image-2"), /3:1/);
  assert.throws(() => validateSize("512x512", "gpt-image-2"), /pixel count/);
  validateSize("123x456", "some-custom-deployment");
  assert.throws(() => validateSize("big", "x"), /WxH/);
});

test("generate writes the image, a sidecar with the exact prompt, and never the key", async (t) => {
  const dir = await temp(t);
  const calls = [];
  const fetchImpl = async (url, init) => {
    calls.push({ url, init });
    return jsonResponse(200, { data: [{ b64_json: PNG_1X1 }], usage: { total_tokens: 5 } });
  };
  const result = await runOperation("generate", options(dir, { prompt: "exact prompt text", size: "1536x1024", quality: "high", background: "opaque" }), { env: AZURE, fetchImpl });
  assert.equal(calls.length, 1);
  assert.equal(calls[0].url, "https://res.services.ai.azure.com/openai/v1/images/generations");
  assert.equal(calls[0].init.headers["api-key"], SECRET);
  const body = JSON.parse(calls[0].init.body);
  assert.deepEqual(body, { model: "gpt-image-2.5-test", prompt: "exact prompt text", n: 1, size: "1536x1024", quality: "high", output_format: "png", background: "opaque" });
  assert.equal(result.outputs[0].width, 1);
  const record = JSON.parse(await readFile(`${path.join(dir, "out.png")}.json`, "utf8"));
  assert.equal(record.prompt, "exact prompt text");
  assert.equal(record.output.sha256.length, 64);
  assert.ok(!JSON.stringify(record).includes(SECRET));
  assert.ok(!JSON.stringify(result).includes(SECRET));
  assert.deepEqual(new Uint8Array(await readFile(path.join(dir, "out.png"))).slice(0, 4), new Uint8Array([0x89, 0x50, 0x4e, 0x47]));
});

test("n greater than one numbers the files", async (t) => {
  const dir = await temp(t);
  const fetchImpl = async () => jsonResponse(200, { data: [{ b64_json: PNG_1X1 }, { b64_json: PNG_1X1 }] });
  const result = await runOperation("generate", options(dir, { n: 2 }), { env: AZURE, fetchImpl });
  assert.deepEqual(result.outputs.map((item) => path.basename(item.file)), ["out-1.png", "out-2.png"]);
});

test("edit sends multipart image[] parts, an optional mask and records input hashes", async (t) => {
  const dir = await temp(t);
  const reference = path.join(dir, "ref.png");
  const mask = path.join(dir, "mask.png");
  await writeFile(reference, Buffer.from(PNG_1X1, "base64"));
  await writeFile(mask, Buffer.from(PNG_1X1, "base64"));
  let form;
  const fetchImpl = async (_url, init) => { form = init.body; return jsonResponse(200, { data: [{ b64_json: PNG_1X1 }] }); };
  await runOperation("edit", options(dir, { images: [reference], mask, inputFidelity: "high" }), { env: AZURE, fetchImpl });
  assert.ok(form instanceof FormData);
  assert.equal(form.getAll("image[]").length, 1);
  assert.equal(form.get("input_fidelity"), "high");
  assert.equal(form.get("model"), "gpt-image-2.5-test");
  assert.ok(form.get("mask"));
  const record = JSON.parse(await readFile(`${path.join(dir, "out.png")}.json`, "utf8"));
  assert.equal(record.request.input_images[0].sha256.length, 64);
  await assert.rejects(runOperation("edit", options(dir), { env: AZURE, fetchImpl }), /at least one --image/);
});

test("a 429 is retried once and then succeeds; a 400 is not retried", async (t) => {
  const dir = await temp(t);
  let attempts = 0;
  const flaky = async () => {
    attempts += 1;
    return attempts === 1 ? jsonResponse(429, { error: { message: "slow down" } }, { "retry-after": "0.01" }) : jsonResponse(200, { data: [{ b64_json: PNG_1X1 }] });
  };
  await runOperation("generate", options(dir, { retries: 1 }), { env: AZURE, fetchImpl: flaky });
  assert.equal(attempts, 2);
  let bad = 0;
  const rejecting = async () => { bad += 1; return jsonResponse(400, { error: { message: "Transparent background is not supported for this model." } }); };
  await assert.rejects(runOperation("generate", options(dir, { retries: 3, background: "transparent" }), { env: AZURE, fetchImpl: rejecting }), (error) => {
    assert.match(error.message, /400/);
    assert.match(error.hint, /key color/);
    return true;
  });
  assert.equal(bad, 1);
});

test("dry run builds the request but never calls the network and redacts the key", async (t) => {
  const dir = await temp(t);
  const fetchImpl = async () => { throw new Error("must not be called"); };
  const result = await runOperation("generate", options(dir, { dryRun: true }), { env: AZURE, fetchImpl });
  assert.equal(result.dry_run, true);
  assert.equal(result.headers["api-key"], "<redacted>");
  assert.ok(!JSON.stringify(result).includes(SECRET));
});

test("transparent backgrounds cannot be combined with jpeg", async (t) => {
  const dir = await temp(t);
  await assert.rejects(runOperation("generate", options(dir, { background: "transparent", format: "jpeg" }), { env: AZURE, fetchImpl: async () => jsonResponse(200, {}) }), /png or webp/);
});

test("the CLI reads prompt files, returns exit codes and honours --dry-run", async (t) => {
  const dir = await temp(t);
  const promptFile = path.join(dir, "p.txt");
  await writeFile(promptFile, "prompt from file");
  let printed = "";
  const code = await main(["generate", "--prompt-file", promptFile, "--dry-run", "--size", "1024x1024"], { env: AZURE, stdout: (text) => { printed += text; } });
  assert.equal(code, 0);
  assert.equal(JSON.parse(printed).prompt, "prompt from file");
  assert.equal(await main(["generate", "--dry-run"], { env: AZURE, stdout: () => {} }), 2, "missing prompt");
  assert.equal(await main(["status"], { env: {}, stdout: () => {} }), 1);
});

test("a real HTTP round trip carries the api-key header and the JSON body", async (t) => {
  const dir = await temp(t);
  let seen;
  const server = createServer((request, response) => {
    let body = "";
    request.on("data", (chunk) => { body += chunk; });
    request.on("end", () => {
      seen = { url: request.url, key: request.headers["api-key"], body: JSON.parse(body) };
      response.setHeader("content-type", "application/json");
      response.end(JSON.stringify({ data: [{ b64_json: PNG_1X1 }] }));
    });
  });
  await new Promise((resolve) => server.listen(0, "127.0.0.1", resolve));
  t.after(() => server.close());
  const { port } = server.address();
  const env = { ...AZURE, AZURE_OPENAI_ENDPOINT: `http://127.0.0.1:${port}/openai/v1` };
  await runOperation("generate", options(dir), { env });
  assert.equal(seen.url, "/openai/v1/images/generations");
  assert.equal(seen.key, SECRET);
  assert.equal(seen.body.prompt, "flat sheet");
});

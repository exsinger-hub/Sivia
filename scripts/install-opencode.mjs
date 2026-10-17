#!/usr/bin/env node
// Install Sivia into OpenCode / OpenWork.
//
// OpenCode (and OpenWork, which embeds it) discovers skills from <config>/skills/<name>/SKILL.md and MCP
// servers from the `mcp` map of opencode.json. This script wires a Sivia checkout into both without
// touching anything else:
//
//   node scripts/install-opencode.mjs                       # user-wide (~/.config/opencode)
//   node scripts/install-opencode.mjs --scope project --project <workspace>   # one OpenWork workspace
//   node scripts/install-opencode.mjs status | uninstall
//
// Skills are linked (junction on Windows, symlink elsewhere) so `git pull` updates them in place and the
// repository-relative paths used by the skills (knowledge-base/, scripts/) keep resolving.
import { existsSync, realpathSync } from "node:fs";
import { cp, copyFile, lstat, mkdir, readdir, readFile, readlink, realpath, rm, symlink, writeFile } from "node:fs/promises";
import os from "node:os";
import path from "node:path";
import { fileURLToPath } from "node:url";

const SCRIPT_DIR = path.dirname(fileURLToPath(import.meta.url));
export const SIVIA_ROOT = path.resolve(SCRIPT_DIR, "..");
const INSTALL_MARKER = ".sivia-installed.json";

export const SERVERS = {
  "drawio-live": { script: "scripts/live-server.mjs", profile: "drawio" },
  "drawio-file-utils": { script: "scripts/server.mjs", profile: "drawio" },
  "powerpoint-live": { script: "scripts/powerpoint-server.mjs", profile: "powerpoint" },
};
const PROFILES = {
  all: Object.keys(SERVERS),
  drawio: Object.keys(SERVERS).filter((name) => SERVERS[name].profile === "drawio"),
  powerpoint: Object.keys(SERVERS).filter((name) => SERVERS[name].profile === "powerpoint"),
  none: [],
};

// ---------------------------------------------------------------------------------------------
// JSONC helpers: opencode.jsonc may hold comments and trailing commas; opencode.json normally does not.
// ---------------------------------------------------------------------------------------------
export function stripJsonc(text) {
  let out = "";
  let inString = false;
  let comments = false;
  for (let i = 0; i < text.length; i += 1) {
    const char = text[i];
    const next = text[i + 1];
    if (inString) {
      out += char;
      if (char === "\\") { out += next ?? ""; i += 1; } else if (char === '"') inString = false;
    } else if (char === '"') {
      inString = true;
      out += char;
    } else if (char === "/" && next === "/") {
      comments = true;
      while (i < text.length && text[i] !== "\n") i += 1;
      out += "\n";
    } else if (char === "/" && next === "*") {
      comments = true;
      i += 2;
      while (i < text.length && !(text[i] === "*" && text[i + 1] === "/")) i += 1;
      i += 1;
    } else {
      out += char;
    }
  }
  // Remove trailing commas outside strings.
  let cleaned = "";
  inString = false;
  for (let i = 0; i < out.length; i += 1) {
    const char = out[i];
    if (inString) {
      cleaned += char;
      if (char === "\\") { cleaned += out[i + 1] ?? ""; i += 1; } else if (char === '"') inString = false;
    } else if (char === '"') {
      inString = true;
      cleaned += char;
    } else if (char === ",") {
      let j = i + 1;
      while (j < out.length && /\s/.test(out[j])) j += 1;
      if (out[j] === "}" || out[j] === "]") { comments = comments || false; continue; }
      cleaned += char;
    } else {
      cleaned += char;
    }
  }
  return { text: cleaned, hadComments: comments };
}

export function parseConfigText(text) {
  const { text: stripped, hadComments } = stripJsonc(text.replace(/^\uFEFF/, ""));
  const trimmed = stripped.trim();
  return { value: trimmed ? JSON.parse(trimmed) : {}, hadComments };
}

// ---------------------------------------------------------------------------------------------
// Locations
// ---------------------------------------------------------------------------------------------
export function resolveTargets({ scope = "user", project, configDir, env = process.env, homeDir = os.homedir(), cwd = process.cwd() } = {}) {
  if (scope === "project") {
    const projectDir = path.resolve(project || cwd);
    return {
      scope,
      skillsDir: path.join(projectDir, ".opencode", "skills"),
      configDir: projectDir,
      configCandidates: ["opencode.json", "opencode.jsonc"].map((name) => path.join(projectDir, name)),
    };
  }
  const base = configDir
    || env.OPENCODE_CONFIG_DIR?.trim()
    || path.join(env.XDG_CONFIG_HOME?.trim() || path.join(homeDir, ".config"), "opencode");
  return {
    scope: "user",
    skillsDir: path.join(base, "skills"),
    configDir: base,
    configCandidates: ["opencode.json", "opencode.jsonc"].map((name) => path.join(base, name)),
  };
}

export async function listSkills(root = SIVIA_ROOT) {
  const skillsRoot = path.join(root, "skills");
  const entries = await readdir(skillsRoot, { withFileTypes: true });
  const names = [];
  for (const entry of entries) {
    if (entry.isDirectory() && existsSync(path.join(skillsRoot, entry.name, "SKILL.md"))) names.push(entry.name);
  }
  return names.sort();
}

export function mcpEntry(serverName, { root = SIVIA_ROOT, node = "node", stateHome = path.join(os.homedir(), ".sivia"), extraEnvironment = {} } = {}) {
  const server = SERVERS[serverName];
  if (!server) throw new Error(`Unknown MCP server: ${serverName}`);
  return {
    type: "local",
    command: [node, path.join(root, server.script)],
    enabled: true,
    environment: { SIVIA_HOME: stateHome, ...extraEnvironment },
    timeout: 15000,
  };
}

async function pathInfo(target) {
  try {
    const stats = await lstat(target);
    let linkTarget = null;
    if (stats.isSymbolicLink()) linkTarget = await readlink(target);
    return { exists: true, isLink: stats.isSymbolicLink(), isDirectory: stats.isDirectory(), linkTarget };
  } catch (error) {
    if (error.code === "ENOENT") return { exists: false };
    throw error;
  }
}

function samePath(a, b) {
  const normalize = (value) => path.resolve(value).replace(/[\\/]+$/, "");
  return process.platform === "win32" ? normalize(a).toLowerCase() === normalize(b).toLowerCase() : normalize(a) === normalize(b);
}

async function isOurs(dest, source) {
  const info = await pathInfo(dest);
  if (!info.exists) return false;
  if (info.isLink) {
    // Junction targets may carry a \\?\ prefix or a trailing separator.
    const cleaned = String(info.linkTarget).replace(/^\\\\\?\\/, "");
    return samePath(cleaned, source);
  }
  return existsSync(path.join(dest, INSTALL_MARKER));
}

// ---------------------------------------------------------------------------------------------
// Planning and execution
// ---------------------------------------------------------------------------------------------
export async function planInstall(options = {}) {
  const root = path.resolve(options.root || SIVIA_ROOT);
  const targets = options.targets || resolveTargets(options);
  const mode = options.mode || "link";
  const skills = options.skills === false ? [] : await listSkills(root);
  const servers = options.servers ?? PROFILES.all;
  const prefix = options.prefix ?? "sivia-";
  const actions = [];

  for (const name of skills) {
    const source = path.join(root, "skills", name);
    const dest = path.join(targets.skillsDir, name);
    const info = await pathInfo(dest);
    let action = mode === "copy" ? "copy" : "link";
    let note = "";
    if (info.exists) {
      if (await isOurs(dest, source)) { action = "refresh"; note = "already installed by Sivia"; }
      else if (options.force) { action = `replace-${mode}`; note = "existing entry will be replaced (--force)"; }
      else { action = "skip"; note = "a different skill with this name exists; use --force to replace it"; }
    }
    actions.push({ kind: "skill", name, source, dest, action, note });
  }

  const configFile = pickConfigFile(targets, options.config);
  for (const serverName of servers) {
    const key = `${prefix}${serverName}`;
    actions.push({
      kind: "mcp",
      name: key,
      server: serverName,
      file: configFile,
      entry: mcpEntry(serverName, { root, node: options.node || "node" }),
      action: "write",
    });
  }
  return { root, targets, mode, actions, configFile, prefix };
}

export function pickConfigFile(targets, explicit) {
  if (explicit) return path.resolve(explicit);
  const existing = targets.configCandidates.find((candidate) => existsSync(candidate));
  // Prefer a populated opencode.json; otherwise use whichever exists; otherwise create opencode.json.
  const json = targets.configCandidates[0];
  if (existsSync(json)) return json;
  return existing || json;
}

async function writeConfig(file, mutate, { dryRun, rewriteJsonc }) {
  let value = {};
  let hadComments = false;
  let existed = false;
  if (existsSync(file)) {
    existed = true;
    const parsed = parseConfigText(await readFile(file, "utf8"));
    value = parsed.value;
    hadComments = parsed.hadComments;
  }
  const before = JSON.stringify(value);
  const next = mutate(structuredClone(value));
  const changed = JSON.stringify(next) !== before;
  const result = { file, changed, written: false, existed, blockedByComments: false, snippet: null };
  if (!changed) return result;
  if (existed && hadComments && !rewriteJsonc) {
    result.blockedByComments = true;
    result.snippet = next.mcp;
    return result;
  }
  if (dryRun) return result;
  const output = !existed && !next.$schema ? { $schema: "https://opencode.ai/config.json", ...next } : next;
  await mkdir(path.dirname(file), { recursive: true });
  if (existed) {
    const backup = `${file}.sivia-backup`;
    if (!existsSync(backup)) await copyFile(file, backup);
  }
  await writeFile(file, `${JSON.stringify(output, null, 2)}\n`, "utf8");
  result.written = true;
  return result;
}

async function installSkill(action, mode) {
  await mkdir(path.dirname(action.dest), { recursive: true });
  if (action.action === "skip") return "skipped";
  if (action.action !== "link" && action.action !== "copy") {
    await rm(action.dest, { recursive: true, force: true });
  }
  if (mode === "copy") {
    await cp(action.source, action.dest, { recursive: true });
    await writeFile(path.join(action.dest, INSTALL_MARKER), `${JSON.stringify({ source: action.source, installed_at: new Date().toISOString() }, null, 2)}\n`, "utf8");
    return "copied";
  }
  // Junctions need no elevation on Windows; POSIX uses a directory symlink.
  await symlink(action.source, action.dest, process.platform === "win32" ? "junction" : "dir");
  return "linked";
}

export async function runInstall(options = {}) {
  const plan = await planInstall(options);
  const report = { root: plan.root, scope: plan.targets.scope, skills_dir: plan.targets.skillsDir, config_file: plan.configFile, dry_run: !!options.dryRun, skills: [], mcp: null, notes: [] };
  for (const action of plan.actions.filter((item) => item.kind === "skill")) {
    let outcome = action.action;
    if (!options.dryRun) outcome = await installSkill(action, plan.mode);
    report.skills.push({ name: action.name, dest: action.dest, outcome, note: action.note });
  }
  const mcpActions = plan.actions.filter((item) => item.kind === "mcp");
  if (mcpActions.length && !options.mcpSkip) {
    report.mcp = await writeConfig(plan.configFile, (config) => {
      config.mcp = { ...(config.mcp || {}) };
      for (const action of mcpActions) config.mcp[action.name] = action.entry;
      return config;
    }, { dryRun: options.dryRun, rewriteJsonc: options.rewriteJsonc });
    report.mcp.servers = mcpActions.map((action) => action.name);
    if (report.mcp.blockedByComments) {
      report.notes.push(`${plan.configFile} contains comments, so it was left untouched. Merge the printed "mcp" entries by hand or re-run with --rewrite-jsonc (a .sivia-backup copy is kept).`);
    }
  }
  return report;
}

export async function runUninstall(options = {}) {
  const root = path.resolve(options.root || SIVIA_ROOT);
  const targets = options.targets || resolveTargets(options);
  const prefix = options.prefix ?? "sivia-";
  const report = { scope: targets.scope, skills_dir: targets.skillsDir, dry_run: !!options.dryRun, skills: [], mcp: null, notes: [] };
  for (const name of await listSkills(root)) {
    const source = path.join(root, "skills", name);
    const dest = path.join(targets.skillsDir, name);
    if (await isOurs(dest, source)) {
      if (!options.dryRun) await rm(dest, { recursive: true, force: true });
      report.skills.push({ name, dest, outcome: "removed" });
    } else {
      report.skills.push({ name, dest, outcome: (await pathInfo(dest)).exists ? "kept (not installed by Sivia)" : "absent" });
    }
  }
  const file = pickConfigFile(targets, options.config);
  if (existsSync(file)) {
    const owned = Object.keys(SERVERS).map((name) => `${prefix}${name}`);
    report.mcp = await writeConfig(file, (config) => {
      if (config.mcp) {
        config.mcp = Object.fromEntries(Object.entries(config.mcp).filter(([key]) => !owned.includes(key)));
        if (!Object.keys(config.mcp).length) delete config.mcp;
      }
      return config;
    }, { dryRun: options.dryRun, rewriteJsonc: options.rewriteJsonc });
    if (report.mcp.blockedByComments) report.notes.push(`${file} contains comments; remove the sivia-* entries from "mcp" by hand or use --rewrite-jsonc.`);
  }
  return report;
}

export async function runStatus(options = {}) {
  const root = path.resolve(options.root || SIVIA_ROOT);
  const targets = options.targets || resolveTargets(options);
  const prefix = options.prefix ?? "sivia-";
  const skills = [];
  for (const name of await listSkills(root)) {
    const dest = path.join(targets.skillsDir, name);
    const info = await pathInfo(dest);
    skills.push({ name, installed: info.exists && await isOurs(dest, path.join(root, "skills", name)), exists: info.exists });
  }
  const file = pickConfigFile(targets, options.config);
  let servers = {};
  if (existsSync(file)) {
    const { value } = parseConfigText(await readFile(file, "utf8"));
    for (const name of Object.keys(SERVERS)) {
      const entry = value.mcp?.[`${prefix}${name}`];
      servers[`${prefix}${name}`] = entry ? { configured: true, enabled: entry.enabled !== false, script_exists: existsSync(String(entry.command?.[1] ?? "")) } : { configured: false };
    }
  }
  return { root, scope: targets.scope, skills_dir: targets.skillsDir, config_file: file, skills, servers };
}

// ---------------------------------------------------------------------------------------------
// CLI
// ---------------------------------------------------------------------------------------------
export function parseArgs(argv) {
  const options = { command: "install" };
  const args = [...argv];
  if (args[0] && !args[0].startsWith("-")) options.command = args.shift();
  while (args.length) {
    const arg = args.shift();
    const value = () => {
      const next = args.shift();
      if (next === undefined) throw new Error(`${arg} needs a value`);
      return next;
    };
    switch (arg) {
      case "--scope": options.scope = value(); break;
      case "--project": options.project = value(); break;
      case "--config-dir": options.configDir = value(); break;
      case "--config": options.config = value(); break;
      case "--mode": options.mode = value(); break;
      case "--profile": options.profile = value(); break;
      case "--servers": options.servers = value().split(",").map((item) => item.trim()).filter(Boolean); break;
      case "--prefix": options.prefix = value(); break;
      case "--node": options.node = value(); break;
      case "--skills-only": options.mcpSkip = true; break;
      case "--mcp-only": options.skills = false; break;
      case "--dry-run": options.dryRun = true; break;
      case "--force": options.force = true; break;
      case "--rewrite-jsonc": options.rewriteJsonc = true; break;
      case "--json": options.json = true; break;
      case "-h": case "--help": options.help = true; break;
      default: throw new Error(`Unknown option: ${arg}`);
    }
  }
  if (options.scope && !["user", "project"].includes(options.scope)) throw new Error("--scope must be user or project");
  if (options.mode && !["link", "copy"].includes(options.mode)) throw new Error("--mode must be link or copy");
  if (options.profile) {
    if (!PROFILES[options.profile]) throw new Error(`--profile must be one of ${Object.keys(PROFILES).join(", ")}`);
    options.servers = options.servers ?? PROFILES[options.profile];
  }
  for (const name of options.servers ?? []) if (!SERVERS[name]) throw new Error(`Unknown server "${name}". Known: ${Object.keys(SERVERS).join(", ")}`);
  return options;
}

const HELP = `Install Sivia into OpenCode / OpenWork

Usage: node scripts/install-opencode.mjs [install|status|uninstall] [options]

  --scope user|project     user: ~/.config/opencode (default); project: <project>/.opencode + opencode.json
  --project <dir>          project/workspace directory for --scope project (default: current directory)
  --mode link|copy         link skills to this checkout (default) or copy them
  --profile all|drawio|powerpoint|none   which MCP servers to register (default: all)
  --servers a,b            explicit MCP server list (${Object.keys(SERVERS).join(", ")})
  --skills-only | --mcp-only
  --prefix <text>          MCP key prefix (default "sivia-" -> sivia-drawio-live)
  --node <path>            node executable written into MCP commands (default "node")
  --config <file>          edit this opencode config file instead of the default
  --rewrite-jsonc          allow rewriting a config that contains comments (a .sivia-backup copy is kept)
  --force                  replace skills with the same name that Sivia did not install
  --dry-run                show what would change; write nothing
  --json                   machine-readable output
`;

function printReport(title, report) {
  const lines = [`${title}${report.dry_run ? " (dry run)" : ""}`];
  lines.push(`  skills dir : ${report.skills_dir}`);
  if (report.config_file) lines.push(`  config file: ${report.config_file}`);
  for (const skill of report.skills ?? []) lines.push(`  skill ${skill.name.padEnd(38)} ${skill.outcome}${skill.note ? ` - ${skill.note}` : ""}`);
  if (report.mcp) {
    if (report.mcp.servers) lines.push(`  mcp        : ${report.mcp.servers.join(", ")} -> ${report.mcp.written ? "written" : report.mcp.blockedByComments ? "NOT written (comments)" : report.mcp.changed ? "would write" : "unchanged"}`);
    if (report.mcp.blockedByComments && report.mcp.snippet) lines.push(JSON.stringify({ mcp: report.mcp.snippet }, null, 2));
  }
  for (const note of report.notes ?? []) lines.push(`  note: ${note}`);
  return lines.join("\n");
}

export async function main(argv = process.argv.slice(2)) {
  const options = parseArgs(argv);
  if (options.help) { process.stdout.write(HELP); return 0; }
  options.servers = options.servers ?? PROFILES.all;
  let report;
  let title;
  if (options.command === "install") { report = await runInstall(options); title = "Sivia install"; }
  else if (options.command === "uninstall") { report = await runUninstall(options); title = "Sivia uninstall"; }
  else if (options.command === "status") { report = await runStatus(options); title = "Sivia status"; }
  else throw new Error(`Unknown command: ${options.command}`);

  if (options.json) {
    process.stdout.write(`${JSON.stringify(report, null, 2)}\n`);
  } else if (options.command === "status") {
    const lines = [title, `  root       : ${report.root}`, `  skills dir : ${report.skills_dir}`, `  config file: ${report.config_file}`];
    for (const skill of report.skills) lines.push(`  skill ${skill.name.padEnd(38)} ${skill.installed ? "installed" : skill.exists ? "name taken by another skill" : "missing"}`);
    for (const [name, info] of Object.entries(report.servers)) lines.push(`  mcp   ${name.padEnd(38)} ${info.configured ? (info.enabled ? "configured" : "configured (disabled)") : "missing"}`);
    process.stdout.write(`${lines.join("\n")}\n`);
  } else {
    process.stdout.write(`${printReport(title, report)}\n`);
    if (options.command === "install" && !options.dryRun) {
      process.stdout.write("\nRestart OpenCode / OpenWork, then verify with `opencode debug skill` and `opencode mcp list`.\n");
    }
  }
  const blocked = report.mcp?.blockedByComments;
  return blocked ? 3 : 0;
}

// Compare real paths: Node resolves links for the entry module but not for process.argv[1].
function isEntryPoint() {
  try {
    return Boolean(process.argv[1]) && realpathSync.native(process.argv[1]) === realpathSync.native(fileURLToPath(import.meta.url));
  } catch {
    return false;
  }
}

if (isEntryPoint()) {
  main().then((code) => { process.exitCode = code; }, (error) => {
    process.stderr.write(`install-opencode: ${error.message}\n`);
    process.exitCode = 2;
  });
}

import { spawnSync } from "node:child_process";

// Some contract tests execute real bridge functions through pwsh; skip them where PowerShell 7 is not installed.
const probe = spawnSync("pwsh", ["-NoProfile", "-NonInteractive", "-Command", "exit 0"], { windowsHide: true });

export const requiresPwsh = { skip: probe.error ? "pwsh (PowerShell 7) is not installed" : false };

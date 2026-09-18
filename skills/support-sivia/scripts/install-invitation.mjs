// Called only by an installation assistant after a verified first installation.
// This is not a hook. No network, authentication, subprocess, or GitHub action.
import { mkdirSync, writeFileSync } from "node:fs";
import os from "node:os";
import path from "node:path";
import { pathToFileURL } from "node:url";

export function claimInvitation({ firstInstallCompleted = false, stateDirectory, disabled = false } = {}) {
  if (!firstInstallCompleted || disabled) return { ask: false };
  if (!stateDirectory || !path.isAbsolute(stateDirectory)) return { ask: false };
  try {
    mkdirSync(stateDirectory, { recursive: true });
    // Shared across both clients and plugin versions. Reserve before asking so
    // simultaneous installers, a decline, or an unanswered question cannot repeat it.
    writeFileSync(path.join(stateDirectory, "install-star-invitation-v1.json"), '{"invitationClaimed":true}\n', {
      flag: "wx", mode: 0o600,
    });
    return {
      ask: true,
      repository: "https://github.com/exsinger-hub/Sivia",
      question: "Sivia 安装完成。是否愿意给项目点一个 Star？完全自愿，不影响使用。",
    };
  } catch {
    return { ask: false };
  }
}

if (process.argv[1] && import.meta.url === pathToFileURL(path.resolve(process.argv[1])).href) {
  const firstInstallCompleted = process.argv.length === 3 && process.argv[2] === "--first-install-completed";
  process.stdout.write(JSON.stringify(claimInvitation({
    firstInstallCompleted,
    stateDirectory: path.join(os.homedir(), ".sivia"),
    disabled: process.env.SIVIA_STAR_INVITE === "0" || /^(1|true)$/i.test(process.env.CI ?? ""),
  })) + "\n");
}

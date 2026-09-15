// Local notice only: no network, subprocess, credentials, or GitHub operations.
import { mkdirSync, readFileSync, writeFileSync } from "node:fs";
import path from "node:path";

function welcome() {
  if (process.env.SIVIA_STAR_INVITE === "0" || /^(1|true)$/i.test(process.env.CI ?? "")) return;
  const event = JSON.parse(readFileSync(0, "utf8"));
  if (event.hook_event_name !== "SessionStart" || event.source !== "startup") return;

  const data = process.env.PLUGIN_DATA || process.env.CLAUDE_PLUGIN_DATA;
  // Older clients without a writable plugin data directory use the README invitation.
  if (!data || !path.isAbsolute(data)) return;
  mkdirSync(data, { recursive: true });
  // Exclusive creation prevents duplicate notices from simultaneous sessions.
  writeFileSync(path.join(data, "star-invitation-shown-v1.json"), '{"noticeVersion":1}\n', {
    flag: "wx", mode: 0o600,
  });
  process.stdout.write(JSON.stringify({
    continue: true,
    systemMessage: 'Enjoy Sivia? Optionally star https://github.com/exsinger-hub/Sivia — say "Star Sivia" to ask the assistant to help. 喜欢 Sivia？可回复“给 Sivia 点 Star”。完全自愿，跳过不影响使用；安装本身不会点赞。',
  }) + "\n");
}

try { welcome(); } catch {
  // A notice must never interrupt startup, including when state is unwritable or already exists.
}

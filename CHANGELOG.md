# Changelog / 更新日志

## 1.1.3 — 2026-09-17

- Removed the Star `SessionStart` hook. Startup, resumption and normal figure workflows never solicit Stars.
- Limited the optional invitation to an assistant-led, verified first successful installation. A local marker shared across clients prevents repeat invitations; updates, reinstalls and uncertain installation history skip it.
- 删除 Star 启动钩子；仅安装助手在确认首次安装成功后询问一次，使用阶段不询问、不补问。升级、重装和无法确认安装历史时跳过。

## 1.1.2 — 2026-09-16

- Added one optional welcome invitation for Codex and Claude Code through a shared `SessionStart` hook. It only writes a local notice marker and displays a message; it does not contact GitHub or change an account.
- Added `support-sivia` for explicit Star requests, with account selection, existing-state checks, verification and a manual-link fallback. Updated the bilingual installation instructions.
- 新增 Codex / Claude Code 共用的首次启动邀请，仅保存本地提示标记、展示自愿 Star 邀请，不自动登录或点赞。
- 新增 `support-sivia` 规则：安装者明确要求后才协助点 Star，并检查账号和操作结果；同步更新中英文安装说明。

## 1.1.1 — 2026-09-09

### English

- Reorganized the README into English and Simplified Chinese editions with matching installation, quick-start prompts, capabilities, gallery and limitations.
- Added bilingual end-to-end workflow guides, from source-grounded ImageGen drafts through explicit approval to editable reconstruction and packaging.
- Connected demonstrated recovery rules to the drawing/review skills: actual host identity, stalled or ineffective operations, isolated native-file candidates, post-grouping arrow visibility, exact-file rendering and truthful pending gates.
- Fixed Windows COM's swapped `triangle` / `open` arrowhead values, with a pure-function regression test that does not launch Office.
- Added documentation-link/version checks and ignored generated Python caches. No private manuscripts or local reconstruction outputs are included.

### 中文

- README 改为相互切换的英文与简体中文版本，安装、快速开始、能力、知识库和限制保持对应。
- 新增双语完整工作流，覆盖有科学依据的 ImageGen 视觉稿、明确确认、可编辑复刻与最终打包。
- 将实践恢复规则接入绘制/审阅 skills：实际宿主识别、阻塞与无效操作、独立原生文件候选稿、分组后的箭头层叠、实际文件渲染及如实保留待核验项。
- 修正 Windows COM 中 `triangle` / `open` 箭头枚举写反的问题，并加入不启动 Office 的纯函数回归测试。
- 增加文档链接/版本检查，忽略 Python 缓存；未包含私有论文或本地复刻输出。

## 1.1.0 — 2026-09-09

- Asset classification, retained-pixel/placement and actual-alpha inspection, and authorized contour-mask recovery for suitable illustrations.
- 素材分类、保留像素/放置尺寸与实际透明度检查，以及适用于特定插画的获授权轮廓遮罩恢复。
- Existing release tag / 已有版本标签：[v1.1](https://github.com/exsinger-hub/Sivia/tree/v1.1).

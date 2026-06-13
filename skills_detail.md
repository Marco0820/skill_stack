# gstack Skills 详细文档

> 来源：https://github.com/garrytan/gstack
> 作者：Garry Tan (Y Combinator CEO)
> 许可：MIT | Stars: 109k | Forks: 16.3k

## 安装

```bash
git clone --single-branch --depth 1 https://github.com/garrytan/gstack.git ~/.claude/skills/gstack && cd ~/.claude/skills/gstack && ./setup
```

## 工作流理念

gstack 围绕 **Think → Plan → Build → Review → Test → Ship → Reflect** 流程组织，每个 skill 依次衔接。

---

## 完整 Skill 一览表

| # | Skill | 角色 | 详细介绍 | 使用方法 | 示例 |
|---|-------|------|----------|----------|------|
| 1 | `/office-hours` | YC Office Hours | 推荐的起点。使用 6 个"强制性问题"在写代码之前重新审视你的产品。挑战前提假设、生成实现方案，输出设计文档供下游 skill 使用。 | 直接输入 `/office-hours`，描述你的产品想法，Claude 会通过 6 个问题帮你重新思考。 | `/office-hours 我想做一个AI驱动的日程管理工具` → Claude 会质疑你的假设，提出替代方案，输出设计文档。 |
| 2 | `/plan-ceo-review` | CEO / 创始人 | 从战略层面重新思考问题。运行 10 段式评审，支持 4 种模式：Expansion（扩展）、Selective Expansion（选择性扩展）、Hold Scope（保持范围）、Reduction（精简）。目标是"找到隐藏在需求中的 10 星产品"。 | 输入 `/plan-ceo-review`，Claude 会以 CEO 视角审视你的计划。 | `/plan-ceo-review` → 分析产品方向，可能建议你削减功能聚焦核心价值，或发现扩展机会。 |
| 3 | `/plan-eng-review` | 工程经理 | 锁定架构设计，生成 ASCII 数据流图、状态机、错误路径。覆盖测试矩阵、失败模式和安全问题。"将隐藏的假设暴露出来"。 | 输入 `/plan-eng-review`，附上架构或功能描述。 | `/plan-eng-review` → 输出数据流图、API 设计、错误处理策略、测试计划。 |
| 4 | `/plan-design-review` | 高级设计师 | 对每个设计维度打 0-10 分，解释 10 分是什么样子，然后据此修改计划。包含 AI Slop 检测（识别 AI 生成的低质量设计）。每个设计选择只问一个问题。 | 输入 `/plan-design-review`，Claude 会评估 UI/UX 设计。 | `/plan-design-review` → 评估配色、布局、交互模式，给出分数和改进建议。 |
| 5 | `/plan-devex-review` | 开发者体验负责人 | 交互式 DX 评审：探索开发者画像、对标竞品的"Hello World"时间、设计"魔法时刻"、追踪摩擦点。3 种模式：DX EXPANSION / DX POLISH / DX TRIAGE。使用 20-45 个强制性问题。 | 输入 `/plan-devex-review`，描述你的 API/SDK/CLI 产品。 | `/plan-devex-review` → 分析开发者上手体验，建议减少配置步骤，优化文档结构。 |
| 6 | `/autoplan` | 评审流水线 | 一条命令自动运行 CEO → 设计 → 工程评审，内置"编码决策原则"。只浮出需要用户拍板的品味决策。 | 输入 `/plan-ceo-review` 后接 `/autoplan`，自动串联所有评审。 | `/autoplan` → 自动完成战略、设计、工程三层评审，只在关键决策点暂停等你确认。 |
| 7 | `/design-consultation` | 设计合伙人 | 从零构建完整设计系统。研究行业景观、提出创意冒险方案、生成逼真的产品原型。输出 `DESIGN.md` 文件。 | 输入 `/design-consultation`，描述你要构建的产品。 | `/design-consultation` → 输出完整的品牌色板、字体系统、组件库规范到 DESIGN.md。 |
| 8 | `/design-shotgun` | 设计探索者 | 使用 GPT Image 生成 4-6 个 AI 原型变体，在浏览器中打开比较面板。用户选择最喜欢的并留下反馈进行迭代。包含"品味记忆"功能，学习你的偏好。 | 输入 `/design-shotgun`，描述要设计的界面。 | `/design-shotgun 一个现代风格的登录页面` → 生成 6 个不同风格的设计稿，你在浏览器中选择最佳方案。 |
| 9 | `/design-html` | 设计工程师 | 将批准的原型转换为生产级 HTML/CSS。使用"Pretext 计算布局"：文本在调整大小时自动回流，高度随内容调整。30KB 开销，零依赖。自动检测 React/Svelte/Vue 并输出对应格式。 | 先用 `/design-shotgun` 选定设计，再输入 `/design-html` 转为代码。 | `/design-html` → 将选中的设计稿转为响应式 HTML/CSS 组件，自动适配你的前端框架。 |
| 10 | `/review` | Staff 工程师 | 找出"能通过 CI 但在生产环境爆炸的 bug"。自动修复明显问题，标记完整性缺失。 | 输入 `/review`，Claude 会审查当前代码变更。 | `/review` → 发现未处理的 null 异常、竞态条件、缺少错误边界等问题并自动修复。 |
| 11 | `/ship` | 发布工程师 | 同步 main 分支、运行测试、审计覆盖率、推送代码、创建 PR。"如果你没有测试框架，会帮你搭建"。在 checkpoint 模式下会过滤压缩 WIP 提交。 | 代码完成后输入 `/ship`。 | `/ship` → 自动 rebase、跑测试、生成 PR，包含变更摘要和测试结果。 |
| 12 | `/land-and-deploy` | 发布工程师 | 合并 PR、等待 CI 和部署、验证生产环境健康。一条命令从"已批准"到"生产验证"。 | PR 获批后输入 `/land-and-deploy`。 | `/land-and-deploy` → merge PR → 等 CI 绿灯 → 部署 → 验证生产环境 URL 返回 200。 |
| 13 | `/canary` | SRE | 部署后监控循环，观察控制台错误、性能回归和页面故障。 | 部署完成后输入 `/canary`。 | `/canary` → 持续监控生产环境，发现 JS 错误或性能下降时立即告警。 |
| 14 | `/benchmark` | 性能工程师 | 建立页面加载时间、Core Web Vitals 和资源大小的基线。支持每次 PR 的前后对比。 | 输入 `/benchmark`，可选对比模式。 | `/benchmark` → 输出 LCP、FID、CLS 等指标，与上次部署对比标注变化。 |
| 15 | `/browse` | QA 工程师 | 给 agent 一个真实的 Chromium 浏览器，支持真实点击和截图。每条命令约 100ms。 | 输入 `/browse` 后描述要浏览的页面或操作。 | `/browse 打开 localhost:3000 并截图首页` → 启动浏览器访问页面并返回截图。 |
| 16 | `/connect-chrome` | 浏览器连接 | 连接到已运行的 Chrome 实例，复用现有会话和 cookies。 | 输入 `/connect-chrome`。 | `/connect-chrome` → 连接到你已登录的 Chrome，可以直接测试需要登录的页面。 |
| 17 | `/qa` | QA 负责人 | 使用真实浏览器测试应用，发现 bug，用原子提交修复，重新验证。为每个修复自动生成回归测试。 | 输入 `/qa`，Claude 会自动测试你的应用。 | `/qa` → 打开浏览器测试所有页面，发现表单提交失败的 bug，修复并生成测试用例。 |
| 18 | `/qa-only` | QA 报告者 | 与 `/qa` 相同的方法论，但只报告不修改代码。纯 bug 报告。 | 输入 `/qa-only`。 | `/qa-only` → 输出一份详细的 bug 列表，包含截图和复现步骤，不修改任何代码。 |
| 19 | `/design-review` | 会写代码的设计师 | 用与 `/plan-design-review` 相同的方法审计线上代码，然后用原子提交修复发现的问题，附带前后截图对比。 | 输入 `/design-review`。 | `/design-review` → 审计线上 UI，发现间距不一致问题，修复并生成 before/after 截图。 |
| 20 | `/setup-browser-cookies` | 会话管理器 | 从真实浏览器（Chrome、Arc、Brave、Edge）导入 cookies 到无头会话，用于测试需要登录的页面。 | 输入 `/setup-browser-cookies`。 | `/setup-browser-cookies` → 导入 Chrome 的 cookies，之后 `/browse` 可以访问需要登录的页面。 |
| 21 | `/setup-deploy` | 部署配置器 | `/land-and-deploy` 的一次性设置。自动检测平台、生产 URL 和部署命令。 | 首次使用 `/land-and-deploy` 前运行。 | `/setup-deploy` → 检测到 Vercel，配置部署命令和生产 URL。 |
| 22 | `/setup-gbrain` | GBrain 入门 | 5 分钟内设置持久化知识库。4 种路径：PGLite 本地、Supabase 现有 URL、自动配置 Supabase、远程 gbrain MCP。 | 输入 `/setup-gbrain`。 | `/setup-gbrain` → 选择 PGLite 本地模式，30 秒完成知识库搭建。 |
| 23 | `/retro` | 工程经理 | 团队感知的周回顾：按人分解、发布连胜记录、测试健康趋势、成长机会。`/retro global` 跨所有项目和 AI 工具运行。 | 周末或 sprint 结束时输入 `/retro`。 | `/retro` → 输出本周：完成了 12 个 PR，测试覆盖率从 78% 提升到 85%，建议关注性能优化。 |
| 24 | `/investigate` | 调试器 | 系统化的根因调试，遵循"铁律：没有调查就没有修复"。追踪数据流、测试假设，3 次修复失败后自动停止。自动冻结到被调查的模块。 | 遇到 bug 时输入 `/investigate`。 | `/investigate 用户登录后偶尔 500 错误` → 追踪请求链路，定位到数据库连接池耗尽的根因。 |
| 25 | `/document-release` | 技术作家 | 更新所有项目文档以匹配刚发布的内容。构建"Diataxis 覆盖图"（参考/教程/操作指南/解释），让文档缺口可见。自动捕获过时的 README。 | 发布后输入 `/document-release`。 | `/document-release` → 更新 README、API 文档、CHANGELOG，标注仍缺失的教程文档。 |
| 26 | `/document-generate` | 文档作者 | 使用 Diataxis 框架从零生成缺失文档。先研究代码库，再编写与代码匹配的文档。可独立使用或从 `/document-release` 链式调用。 | 输入 `/document-generate`。 | `/document-generate` → 为你的 CLI 工具生成完整的使用教程和 API 参考文档。 |
| 27 | `/codex` | 第二意见 | 来自 OpenAI Codex CLI 的独立代码审查。3 种模式：review（通过/失败门禁）、adversarial challenge（对抗性挑战）、open consultation（开放咨询）。当 `/review`（Claude）和 `/codex`（OpenAI）都运行后，生成跨模型分析。 | 输入 `/codex`。 | `/codex` → OpenAI 独立审查代码，与 Claude 的 `/review` 结果交叉验证。 |
| 28 | `/cso` | 首席安全官 | OWASP Top 10 + STRIDE 威胁模型。"零噪音：17 个误报排除规则、8/10+ 置信度门禁、独立发现验证"。每个发现包含具体漏洞利用场景。 | 输入 `/cso`。 | `/cso` → 发现 SQL 注入风险，给出具体的攻击 payload 示例和修复方案。 |
| 29 | `/careful` | 安全护栏 | 在执行破坏性命令（rm -rf、DROP TABLE、force-push）前发出警告。说"be careful"即可激活。警告可被覆盖。 | 输入 `/careful` 或说"be careful"。 | `/careful` → 之后执行 `rm -rf` 时会先弹出确认提示。 |
| 30 | `/freeze` | 编辑锁定 | 将文件编辑限制在一个目录内。防止调试时意外修改范围外的文件。 | 输入 `/freeze`。 | `/freeze src/components/` → 之后只能编辑 src/components/ 下的文件。 |
| 31 | `/guard` | 完全安全 | 一条命令组合 `/careful` + `/freeze`，生产工作时的最大安全保障。 | 输入 `/guard`。 | `/guard` → 同时激活破坏性命令警告和目录锁定。 |
| 32 | `/unfreeze` | 解锁 | 移除 `/freeze` 的目录边界限制。 | 输入 `/unfreeze`。 | `/unfreeze` → 解除文件编辑的目录限制。 |
| 33 | `/gstack-upgrade` | 自更新器 | 升级 gstack 到最新版本。检测全局 vs 供应商安装，同步两者，显示变更内容。 | 输入 `/gstack-upgrade`。 | `/gstack-upgrade` → 检测到新版本，显示 changelog，询问是否升级。 |
| 34 | `/learn` | 记忆管理 | 管理 gstack 跨会话学到的内容。查看、搜索、修剪和导出项目特定的模式、陷阱和偏好。"学习成果跨会话累积"。 | 输入 `/learn`。 | `/learn` → 查看历史学习记录，如"这个项目偏好使用 Tailwind 而非 CSS Modules"。 |

---

## 快速选择指南

| 构建目标 | 规划阶段 | 线上审计 |
|----------|----------|----------|
| 终端用户（UI、Web、移动端） | `/plan-design-review` | `/design-review` |
| 开发者（API、CLI、SDK、文档） | `/plan-devex-review` | `/devex-review` |
| 架构（数据流、性能、测试） | `/plan-eng-review` | `/review` |
| 以上全部 | `/autoplan` | — |

---

## 典型工作流示例

### 从零开始构建一个 Web 应用

```bash
# 1. 产品思考
/office-hours 我想做一个团队协作白板工具

# 2. CEO 级战略评审
/plan-ceo-review

# 3. 设计系统
/design-consultation

# 4. 生成设计变体
/design-shotgun 现代风格的协作白板界面

# 5. 转为生产代码
/design-html

# 6. 代码审查
/review

# 7. QA 测试
/qa

# 8. 性能基线
/benchmark

# 9. 安全审计
/cso

# 10. 发布
/ship

# 11. 部署验证
/land-and-deploy

# 12. 部署后监控
/canary

# 13. 更新文档
/document-release

# 14. 周回顾
/retro
```

### 快速 Bug 修复流程

```bash
# 1. 调查根因
/investigate 用户报告页面加载卡死

# 2. 修复并测试
/qa

# 3. 发布
/ship
```

### API/SDK 开发流程

```bash
# 1. DX 设计评审
/plan-devex-review

# 2. 工程架构评审
/plan-eng-review

# 3. 构建完成后审查
/devex-review

# 4. 文档生成
/document-generate

# 5. 发布
/ship
```

---

## 安装平台支持

| AI Agent | 安装标志 | 安装位置 |
|----------|----------|----------|
| Claude Code | 默认 | `~/.claude/skills/gstack/` |
| OpenAI Codex CLI | `--host codex` | `~/.codex/skills/gstack-*/` |
| OpenCode | `--host opencode` | `~/.config/opencode/skills/gstack-*/` |
| Cursor | `--host cursor` | `~/.cursor/skills/gstack-*/` |
| Factory Droid | `--host factory` | `~/.factory/skills/gstack-*/` |
| Slate | `--host slate` | `~/.slate/skills/gstack-*/` |
| Kiro | `--host kiro` | `~/.kiro/skills/gstack-*/` |
| Hermes | `--host hermes` | `~/.hermes/skills/gstack-*/` |

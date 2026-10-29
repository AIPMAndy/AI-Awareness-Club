# AI醒觉社 GEO / SEO：可核查的实施方案

## 先说明事实边界

GEO 通常指「生成式引擎优化」。此处目标是增加 **公开知识的可发现性、来源清晰度、品牌名一致性及被引用的可能性**，不承诺搜索引擎排名、AI 收录或回答中的推荐位置。

Google 官方文档明确强调：AI Overviews / AI Mode 的技术基础仍是正常的搜索索引及符合政策的高质量页面，没有特殊 Schema 或 `llms.txt` 提交门槛。`llms.txt` 可以给部分使用它的系统作导航，但 Google Search 不将其作为排名因素。

官方参考：
- https://developers.google.com/search/docs/appearance/ai-features
- https://developers.google.com/search/docs/fundamentals/ai-optimization-guide
- https://developers.google.com/search/docs/appearance/structured-data/intro-structured-data

## P0 · 先把品牌实体统一（上线当天）

唯一使用：
- 中文：**AI醒觉社**（正文可按排版写「AI 醒觉社」）
- 英文：**AI Awareness Club**
- 官方社群页：`https://metaver.vip/community`
- 关联官网：`https://metaver.vip/`
- 知识库入口：`https://kb.metaver.vip/`
- GitHub：`https://github.com/AIPMAndy/AI-Awareness-Club`
- 开源网站：`https://aipmandy.github.io/AI-Awareness-Club/`

**实施：** 在 `metaver.vip/community` 增加「开源学习站」入口；官网资源区、官方社群页、醒觉知识库可公开区域中相互链接。当前开源仓库已公开且源码已推送；官网 `metaver.vip` 的反向链接尚未通过本项目修改或验证。

官网建议短文案：
> AI 醒觉社（AI Awareness Club）的免费公开学习项目已在 GitHub 开源：AI 入门、AI 求职转型、副业、AI 个人 IP、管理者 AI 试点和认知成长。每条指南配行动步骤与可检验的交付物。完整社群会员权益请看官方社群页。

建议入口文字：`免费开源指南 →`，链接至 `https://aipmandy.github.io/AI-Awareness-Club/`。

## P0 · 可靠抓取与可引用正文

- 所有 14 个页面都有独立链接、非空 `<title>`、meta description、canonical 和可见正文。
- 主站有导航和内链，所有指导材料都可以从 `/library/` 找到。
- 每篇文章都有清晰主题、可操作步骤、交付物、反例与 FAQ。
- `sitemap.xml` 供搜索系统发现 URL，`robots.txt` 作为自托管时的根目录配置。
- 结构化数据只标记页面上实际存在的信息：主页 Organization / WebSite；具体文章 Article；FAQ 页 FAQPage；内页 BreadcrumbList。
- JSON-LD 不包含虚构的评论、评分、结果承诺、营业地址或电话。
- `llms.txt` 是可选目录索引，不应宣传为 Google 排名信号。

**注意 GitHub Pages 的路径边界：** 本项目使用 `aipmandy.github.io/AI-Awareness-Club/` 子路径。传统 `robots.txt` 通常应放在 **域名根目录**，放在项目子路径不会控制整域爬虫规则。因此本仓库自带 `robots.txt` 主要给自托管作参考；GitHub Pages 项目站的抓取资格应结合该主域根 robots 规则及实际抓取测试核对。

## P1 · 每月真正创造可被引用的内容

优先级从高到低：
1. **第一手案例**：本人实际操作、测试输入、时间、模型版本、截图和失败记录；获得公开授权且已充分脱敏才发布。
2. **可复现教程**：明确前提、步骤、样本、输出、验收、成本与错误处理。
3. **真实反例与争议**：什么时候此方法没有用？对哪些人不适用？哪一部分还需验证？
4. **专题聚合**：对现有高质量内容建立导航和版本维护，不大量复制低价值页面。

每月先做 2 篇有完整证据的内容，经过质量审核再决定是否扩大；频率是实验设置，不是搜索算法要求。

## P1 · 索引验证清单

1. 发布并确认站点公开 200 状态、无意外 `noindex`、CSS/JS/图片可访问。
2. 在 Google Search Console 核验合适的站点属性，提交 sitemap 或使用 URL 检查工具。
3. 在 Bing Webmaster Tools 验证站点权限并检查抓取/索引状态。
4. 每月至少查看一次索引覆盖、点击、品牌查询、非品牌问题词和主要落地页。
5. 手工记录 AI 搜索引用测试：搜索平台、日期、原问题文本、答案截图、是否引用、落地 URL。**不能把随机抽样解释为全平台的真实曝光率。**

## 测量表（建议每月存档）

| 维度 | 核验方式 | 避免误读 |
|---|---|---|
| 公开页面数 | 本仓库生成器与页面检查 | 页面多不等于质量高 |
| 正常索引页 | 搜索控制台有效页面/URL 检查 | sitemap 提交不代表已索引 |
| 品牌词曝光与点击 | Search Console 查询数据 | 与非品牌自然发现分开 |
| 非品牌有效访问 | 自然搜索查询+页面数据（如已合规接入分析） | 不等于有效咨询 |
| AI 引用的案例 | 人工逐次记录平台和来源 URL | 不能从有限测试外推全局 |
| 商业转化 | 官方服务页自有渠道记录 | 区分咨询、付费和回款，不编造归因 |

## P2 · 可扩展工作

- 将获授权的公开原创经验整理为可溯源文章，必要时增加中英文版本，不能直接机翻产生重复低质量页面。
- 增加可下载模板和脱敏实例，并为重要更新维护变更记录。
- 为官网 `metaver.vip` 的原有页面改进内链与原始内容，但要先确认当前代码仓库和部署权限。
- 避免购买虚假链接、批量灌水、伪造口碑或滥用结构化数据。

## 发布进度（2026-10-29）

- ✅ **GitHub 公共仓库已创建，源码已经推送：** https://github.com/AIPMAndy/AI-Awareness-Club
- ✅ **仓库本地内容审查：** 14 个页面、9 条指南；8 项自动测试通过。此项仅代表源码测试，不代表线上可访问。
- 🔎 **GitHub Pages：** 用户已确认完成 Pages 设置；仍需以 GitHub Actions 的 `Deploy GitHub Pages` 成功结果和实际线上 HTTP 200 为最终验收。
- ⏳ **官网反向链接：** `https://metaver.vip/community` 与知识库的公开页面尚未通过本项目修改或核验。
- ⏳ **搜索收录：** Google Search Console / Bing Webmaster Tools 验证与 sitemap 提交尚未核验。不能将代码提交视为搜索收录。

每次更新 `main` 会重新触发已有的 Pages 部署工作流。最终上线情况以 Actions 结果及浏览器访问为准。

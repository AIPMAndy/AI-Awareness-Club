# 首次发布 AI-Awareness-Club · 保姆级清单

目标：公开 GitHub 仓库 `AIPMAndy/AI-Awareness-Club`，之后让静态站显示在 `https://aipmandy.github.io/AI-Awareness-Club/`。

## 一、先检查本地包

```bash
python3 scripts/build.py
python3 -m unittest discover -s tests -v
```

确认 `docs/index.html` 与 `docs/sitemap.xml` 已生成。

## 二、创建公开 GitHub 仓库

> 当前 GitHub 连接能操作已有仓库，但没有「新建仓库」能力。完成以下任一种方式即可；在未完成前请勿宣传为已上线。

### 方式 A：最少操作，创建后交给已连接的 GitHub 继续处理

1. 用 AIPMAndy 登录 `https://github.com/new`。
2. Repository name 填 `AI-Awareness-Club`；Visibility 选 **Public**。
3. 勾选 **Add a README file**，让新仓库有初始的 `main` 分支；然后创建。
4. 在对话中告诉 AI「仓库已创建」。如果当前 GitHub 连接能访问新仓库，即可继续写入并替换初始化 README；若 GitHub App 只授权了部分仓库，需在 GitHub 授权设置中把新仓库加入可访问列表。

### 方式 B：自己一次性把这个 ZIP 推送上去

1. 用 AIPMAndy 登录 `https://github.com/new`。
2. Repository name 填 `AI-Awareness-Club`，Description 可填：`AI醒觉社 · AI Awareness Club — 开放学习、AI 实践与价值共创的免费开源知识站。`
3. Visibility 选 **Public**。**不要**勾选自动生成 README、LICENSE、.gitignore，因为项目包已有这些文件。
4. 在下载并解压的 `AI-Awareness-Club` 目录执行：

```bash
git init
git add .
git commit -m "feat: launch AI Awareness Club open knowledge hub"
git branch -M main
git remote add origin https://github.com/AIPMAndy/AI-Awareness-Club.git
git push -u origin main
```

若已初始化 Git，跳过 `git init`；若远端已设置，请先运行 `git remote -v` 核对。认证使用正常 GitHub 账号登录流程，不要向任何人发送 Token。

有 GitHub CLI 的电脑也可以在完成本地初始提交后使用 `gh repo create AIPMAndy/AI-Awareness-Club --public --source=. --remote=origin --push`。

## 三、启用 GitHub Pages

1. 打开仓库 **Settings → Pages**。
2. 找到 **Build and deployment → Source**，选择 **GitHub Actions**。
3. 进入 **Actions**，检查 `Deploy GitHub Pages` 成功；若出现授权确认，按 GitHub 账户界面提示处理。
4. 打开：`https://aipmandy.github.io/AI-Awareness-Club/`，测试首页、知识库、九篇指南、主题切换、搜索及勾选导出。
5. 若 Pages 尚未完成首次部署，等 Actions 日志给出成功结果后再公开传播链接；不要在验证前声称上线。

## 四、验证 GEO 基础

- 打开 `/sitemap.xml`，检查全部 14 个 URL。
- 打开 `/llms.txt`，验证列出的 9 篇指南能访问。
- 在浏览器检查 canonical、OG 图片及 JSON-LD（例如 Google Rich Results Test 或 Schema Validator）。
- 使用移动设备测试首页、搜索、指南勾选和下载。
- 在 `https://metaver.vip/community` 加入开源仓库/站点入口，使官方品牌页面与 GitHub 形成双向链接。
- 向 Search Console 提交站点地图，并用 URL 检查确认可抓取；不能保证即时收录。

## 五、GitHub 仓库装修

- About 描述：`AI醒觉社 · AI Awareness Club：让 AI 成为利人利己的力量。免费开源的 AI 实战、职业转型、副业、个人 IP、MBTI 成长与价值共创指南。`
- Website：`https://aipmandy.github.io/AI-Awareness-Club/`（成功部署后再填）
- Topics：`ai-awareness-club`, `ai-learning`, `open-source-education`, `career-growth`, `personal-branding`, `ai-agent`, `chinese`
- 社交预览图：仓库 **Settings → General → Social preview** 手动上传 `site/assets/social-preview.png`。
- Readme 首屏已内嵌原创 SVG banner；请确认手机上显示正确。

## 六、上线后的首轮检查

| 验收项 | 通过标准 |
|---|---|
| 内容 | 免费和付费边界明确；无私密资料；9 条指南都有交付物 |
| 结构 | `README` 首屏清晰，所有内链可打开 |
| 网站 | 桌面与手机导航可用，按钮有真实操作 |
| GEO | 独立标题、canonical、sitemap 与可见正文一致 |
| 自动化 | `CI` 和 `Deploy GitHub Pages` 通过 |
| 官方入口 | 官网和知识库链接真实，会员权益以官网为准 |

没有验证就保留为待完成，不宣称通过。

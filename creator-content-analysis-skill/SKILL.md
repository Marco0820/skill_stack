# SKILL.md — creator-content-analysis-skill

## Skill 名称

`creator-content-analysis-skill`

## 何时触发

当用户的请求包含以下意图时，应触发本 Skill：

- 分析某个自媒体博主/达人/KOL 的内容
- 拆解某个账号的内容策略、爆款规律
- 评估某个账号的商业化潜力
- 对标分析同赛道竞品账号
- 生成 KOL 筛选分析报告
- 用户提供了博主内容数据并要求分析
- 用户提到了 "分析博主"、"分析达人"、"KOL分析"、"内容拆解"、"账号拆解"、"爆款分析" 等关键词

## 触发关键词

```
分析博主, 分析达人, 分析账号, KOL分析, 内容分析, 博主拆解, 账号拆解,
爆款分析, 商业化分析, creator analysis, content analysis, KOL review,
达人评估, 内容策略分析, 赛道分析
```

## 使用流程

### 1. 收集数据

引导用户提供以下任意一种输入：

| 输入类型 | 说明 |
|----------|------|
| 主页链接 | 抖音/小红书/B站/视频号/微博/TikTok/YouTube/Instagram 主页（提示用户手动整理数据） |
| 单条/多条链接 | 视频或图文链接（提示用户提供关键数据） |
| 文件 | CSV / JSON / Markdown / TXT / Excel 文件 |
| 数据列表 | 视频标题、文案、转写稿、评论、互动数据 |
| 手动粘贴 | 用户直接粘贴的博主内容样本 |

**重要**：本 Skill 不包含爬虫，不直接抓取平台数据。如用户提供链接，应提示其通过合法方式导出数据。

### 2. 数据标准化

将用户输入转换为标准 JSON 结构（参见 `templates/input_schema.json`）。

必要字段：
- `creator.name` — 账号名称
- `creator.platform` — 平台
- `contents[]` — 内容列表

每条内容建议包含：
- `title` — 标题
- `transcript` — 转写稿（如有）
- `likes/comments/shares/favorites` — 互动数据

### 3. 执行分析

按以下模块依次分析：

1. **账号基础画像** → 使用 `prompts/account_analysis_prompt.md`
2. **单条内容拆解** → 使用 `prompts/video_analysis_prompt.md`
3. **内容标签提取** → 使用 `prompts/tag_extraction_prompt.md`
4. **爆款规律分析** → 使用 `prompts/viral_pattern_prompt.md`
5. **商业化潜力分析** → 使用 `prompts/commercial_analysis_prompt.md`

### 4. 生成报告

使用 `templates/report_template.md` 作为报告骨架，填充分析结果。

输出两个版本：
- **Markdown 报告** — 运营人员可直接用于会议讨论
- **JSON 结构化数据** — 程序化处理使用

## 输入规范

```json
{
  "creator": {
    "name": "string (必填)",
    "platform": "string (必填)",
    "profile_url": "string",
    "bio": "string",
    "followers": "string",
    "following": "string",
    "total_posts": "string"
  },
  "contents": [
    {
      "id": "string",
      "title": "string (建议必填)",
      "url": "string",
      "publish_time": "string (YYYY-MM-DD)",
      "description": "string",
      "transcript": "string (强烈建议提供)",
      "cover_text": "string",
      "hashtags": ["string"],
      "likes": "number",
      "comments": "number",
      "shares": "number",
      "favorites": "number",
      "duration": "string (MM:SS)",
      "raw_comments": ["string"]
    }
  ]
}
```

## 输出规范

### Markdown 报告结构

```markdown
# 自媒体博主内容分析报告

## 1. 账号一句话定位
## 2. 账号基础画像
## 3. 内容赛道分析
## 4. 内容调性分析
## 5. 内容风格分析
## 6. 内容标签总结
## 7. 高频选题与关键词
## 8. 爆款内容规律
## 9. 单条内容拆解
## 10. 商业化潜力分析
## 11. 对标复刻建议
## 12. 风险与不足
## 13. 后续内容选题建议
```

### JSON 输出结构

参见 `templates/output_schema.json`

## 注意事项

1. **数据质量依赖**：分析质量取决于输入数据的完整性和准确性。数据越详细，分析越精准。
2. **不包含爬虫**：本 Skill 不提供任何数据抓取功能，所有数据需用户自行准备。
3. **人工判断优先**：分析结果作为决策参考，建议结合人工经验综合判断。
4. **隐私合规**：处理用户数据时注意隐私保护，不存储或传播用户原始数据。
5. **报告语言**：默认输出中文报告，如需其他语言请在 prompt 中指定。

## 关联文件

- 主入口：`scripts/analyze_creator.py`
- Prompt 模板：`prompts/*.md`
- 数据模板：`templates/*.json`
- 示例数据：`examples/`

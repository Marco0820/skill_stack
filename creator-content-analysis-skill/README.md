# creator-content-analysis-skill

> 自媒体博主/达人/KOL 内容分析 Skill —— 自动生成账号分析报告，适用于 MCN、品牌投放、KOL 筛选、内容策划、账号孵化。

---

## 功能概述

本 Skill 用于分析某个自媒体博主/达人/KOL/账号的所有已发布内容，自动总结：

- 账号基础画像
- 内容赛道定位与竞争分析
- 内容调性与风格拆解
- 内容标签体系
- 爆款内容规律提炼
- 商业化潜力评估
- 对标复刻建议与选题库

输出为**运营人员可以直接拿去开会讨论**的专业分析报告（Markdown + JSON）。

---

## 安装方式

### 环境要求

- Python >= 3.8
- 无强制第三方依赖（仅使用 Python 标准库）

### 安装步骤

```bash
# 1. 克隆或下载本目录到本地
# 2. 进入项目目录
cd creator-content-analysis-skill

# 3. （可选）安装 Excel 支持
pip install openpyxl

# 4. 直接运行
python scripts/analyze_creator.py --input examples/sample_input.json --output report.md
```

---

## 使用方式

### 方式一：命令行运行

```bash
# 从 JSON 文件分析
python scripts/analyze_creator.py --input data.json --output report.md

# 从 CSV 文件分析
python scripts/analyze_creator.py --input data.csv --output report.md

# 同时输出 JSON 结构化结果
python scripts/analyze_creator.py --input data.json --output report.md --json-output result.json
```

### 方式二：Python 代码调用

```python
from scripts.analyze_creator import CreatorAnalyzer

analyzer = CreatorAnalyzer()
analyzer.load_input("data.json")
report_md, report_json = analyzer.analyze()

with open("report.md", "w", encoding="utf-8") as f:
    f.write(report_md)

with open("result.json", "w", encoding="utf-8") as f:
    import json
    json.dump(report_json, f, ensure_ascii=False, indent=2)
```

### 方式三：在 Claude Code / Codex 中使用

直接对 Claude 说：

> "请用 creator-content-analysis-skill 分析这个博主的内容"
> "帮我分析一下这个账号的爆款规律和商业化潜力"

---

## 输入格式

### JSON 格式（推荐）

```json
{
  "creator": {
    "name": "博主名称",
    "platform": "抖音",
    "profile_url": "https://...",
    "bio": "个人简介",
    "followers": "100万",
    "following": "500",
    "total_posts": "300"
  },
  "contents": [
    {
      "id": "1",
      "title": "视频标题",
      "url": "https://...",
      "publish_time": "2024-01-15",
      "description": "视频描述",
      "transcript": "转写稿全文...",
      "cover_text": "封面文字",
      "hashtags": ["标签1", "标签2"],
      "likes": 50000,
      "comments": 3000,
      "shares": 1000,
      "favorites": 8000,
      "duration": "03:45",
      "raw_comments": ["评论1", "评论2"]
    }
  ]
}
```

### CSV 格式

CSV 文件需包含以下列（表头）：

```
id, title, url, publish_time, description, transcript, cover_text, hashtags, likes, comments, shares, favorites, duration
```

### 手动输入

也可以直接在对话中粘贴博主信息和内容数据，Skill 会自动解析。

---

## 输出格式

### Markdown 报告

输出包含以下章节的完整分析报告：

1. 账号一句话定位
2. 账号基础画像
3. 内容赛道分析
4. 内容调性分析
5. 内容风格分析
6. 内容标签总结
7. 高频选题与关键词
8. 爆款内容规律
9. 单条内容拆解
10. 商业化潜力分析
11. 对标复刻建议
12. 风险与不足
13. 后续内容选题建议

### JSON 结构化数据

包含与报告对应的完整结构化数据，方便程序化处理。

---

## 项目结构

```
creator-content-analysis-skill/
├── README.md                  # 本文件
├── SKILL.md                   # Skill 触发与使用规范
├── skill.json                 # Skill 元数据
├── prompts/                   # 大模型 Prompt 模板
│   ├── account_analysis_prompt.md
│   ├── video_analysis_prompt.md
│   ├── tag_extraction_prompt.md
│   ├── viral_pattern_prompt.md
│   └── commercial_analysis_prompt.md
├── templates/                 # 数据模板
│   ├── input_schema.json
│   ├── output_schema.json
│   ├── report_template.md
│   └── video_item_template.md
├── examples/                  # 示例数据
│   ├── sample_input.json
│   ├── sample_output.md
│   └── sample_creator_dataset.csv
└── scripts/                   # Python 脚本
    ├── analyze_creator.py     # 主入口
    ├── parse_input.py         # 数据解析
    ├── generate_report.py     # 报告生成
    └── tag_classifier.py      # 标签分类
```

---

## 分析维度说明

| 维度 | 说明 |
|------|------|
| 账号画像 | 名称、平台、粉丝、内容量、目标人群 |
| 赛道分析 | 一级/二级赛道、竞争强度、商业化潜力 |
| 内容调性 | 专业理性/情绪共鸣/犀利观点/幽默搞笑等 |
| 内容风格 | 标题、封面、开头钩子、叙事结构、剪辑节奏 |
| 内容标签 | 赛道/人群/主题/情绪/商业化/传播潜力标签 |
| 爆款规律 | 高频主题、标题句式、情绪触发点、共性 |
| 商业化 | 广告合作、带货、知识付费、私域转化 |
| 对标复刻 | 可复刻选题、标题模板、优化建议 |

---

## 扩展方式

### 接入大模型 API

在 `scripts/analyze_creator.py` 中替换 `generate_analysis()` 函数，接入你的大模型 API：

```python
def generate_analysis(self, data: dict) -> dict:
    # 替换为调用你的大模型 API
    import requests
    response = requests.post("YOUR_API_ENDPOINT", json={
        "prompt": self.build_prompt(data),
        "model": "your-model"
    })
    return response.json()
```

### 接入数据采集

在 `scripts/parse_input.py` 中添加新的数据源解析器：

```python
def parse_from_api(self, api_response: dict) -> dict:
    """从合法 API 采集结果解析数据"""
    # 你的解析逻辑
    pass
```

---

## 适用团队

- 互联网营销公司
- MCN 机构
- 品牌投放团队
- KOL 筛选与评估
- 内容策划团队
- 账号孵化团队

---

## 注意事项

1. 本 Skill 不包含任何爬虫或平台破解代码，所有数据需用户手动提供或通过合法渠道获取。
2. 分析结果基于提供的数据质量，数据越完整，分析越准确。
3. 建议结合人工判断使用，分析报告作为决策参考而非唯一依据。
4. 所有 Prompt 模板可直接用于大模型 API 调用。

---

## License

MIT

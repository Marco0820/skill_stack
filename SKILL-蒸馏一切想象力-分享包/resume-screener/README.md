# resume-screener — 简历批量筛选技能

从本地文件夹读取多个 PDF 求职简历，依据公司招聘标准（销售 / 开发）逐条打分，参照本地报告模板生成中文筛选报告；**仅当用户明确要求时**才通过 SMTP 邮件发送报告。

## 目录结构

本技能遵循 Claude 官方 Skill 规范：元信息全部写在 `SKILL.md` 顶部的 YAML frontmatter（`name` + `description`）中，不再单列 `skill.json`；招聘标准作为「按需加载的参考文档」放 `references/`，报告模板作为「输出时使用的文件」放 `assets/`。

```
resume-screener/
├── SKILL.md                       # 技能说明与使用流程（含 frontmatter 元信息，主入口）
├── requirements.txt               # 可选 Python 依赖
├── scripts/                       # 确定性脚本
│   ├── extract_pdfs.py            # 批量提取 PDF 简历文本
│   ├── generate_report.py         # 按模板生成筛选报告
│   └── send_report.py             # SMTP 发送报告邮件
├── references/                    # 按需加载的参考文档
│   ├── sales_hiring_criteria.md   # 销售人员招聘标准（占位）
│   └── dev_hiring_criteria.md     # 开发人员招聘标准（占位）
└── assets/                        # 输出时使用的文件
    └── report_template.md         # 报告模板
```

## 使用流程

1. **确认输入**：简历文件夹路径、招聘标准文件（默认用内置占位）、是否发送邮件。
2. **提取文本**：`python scripts/extract_pdfs.py "<简历文件夹>" --output resumes.json`
3. **评估打分**：由模型对照 `references/` 下招聘标准逐份打分，输出 `evaluations.json`。
4. **生成报告**：
   ```bash
   python scripts/generate_report.py \
     --evals evaluations.json \
     --template assets/report_template.md \
     --output 简历筛选报告.md
   ```
5. **发送邮件（可选）**：仅当用户明确要求时执行：
   ```bash
   python scripts/send_report.py \
     --report 简历筛选报告.md \
     --to hr@example.com \
     --config smtp_config.json
   ```

## 安装依赖（可选）

```bash
pip install -r requirements.txt
```

未安装依赖时，技能会自动回退让 Claude 用 Read 工具直接读取 PDF。

## 邮件配置

SMTP 配置通过配置文件或环境变量提供，**不硬编码在脚本中**。配置文件示例（`smtp_config.json`）：

```json
{
  "SMTP_HOST": "smtp.qq.com",
  "SMTP_PORT": 465,
  "SMTP_USER": "your_account@qq.com",
  "SMTP_PASS": "你的授权码",
  "SMTP_FROM": "your_account@qq.com",
  "SMTP_USE_SSL": true
}
```

## 注意事项

- 内置的销售 / 开发招聘标准为**占位模板**，正式使用前请替换为真实公司文档。
- **默认不发邮件**，发送需用户明确授权。
- 评分均附依据，仅供参考，最终录用请结合人工判断。

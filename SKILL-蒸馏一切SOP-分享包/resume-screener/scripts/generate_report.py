#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
generate_report.py — 简历筛选报告生成脚本

作用：
    读取评估结果 JSON（由模型对每份简历打分后生成），按报告模板填充统计概览、
    候选人排名总表与每位候选人的评分明细，输出最终的中文 Markdown 报告。

用法：
    python generate_report.py \
        --evals evaluations.json \
        --template templates/report_template.md \
        --output 简历筛选报告.md

模板占位标记（在 templates/report_template.md 中使用）：
    {{report_title}}    报告标题
    {{generated_at}}    生成时间
    {{summary}}         概览统计段落
    {{candidate_table}} 候选人排名总表（Markdown 表格）
    {{details}}         每位候选人的评分明细段落

评估 JSON 结构（数组）：
    [
      {
        "filename": "张三-销售.pdf",
        "candidate_name": "张三",
        "position_type": "销售",
        "items": [
          {"criterion": "沟通表达能力", "score": 4, "max": 5, "evidence": "……"}
        ],
        "total_score": 23,
        "max_score": 30,
        "highlights": ["……"],
        "risks": ["……"],
        "conclusion": "推荐进入面试"
      }
    ]
"""

import argparse     # 命令行参数解析
import json         # 读取评估 JSON
from datetime import datetime  # 生成时间
from pathlib import Path       # 路径处理


def load_evals(evals_path: str):
    """读取评估结果 JSON 文件，返回列表。"""
    with open(evals_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    if not isinstance(data, list):
        raise ValueError("评估文件应是一个 JSON 数组。")
    return data


def build_summary(evals):
    """根据评估结果生成概览统计段落。"""
    total = len(evals)
    # 按岗位类别统计
    position_counts = {}
    for item in evals:
        pos = item.get("position_type", "未分类")
        position_counts[pos] = position_counts.get(pos, 0) + 1
    # 按结论统计
    conclusion_counts = {}
    for item in evals:
        conc = item.get("conclusion", "未结论")
        conclusion_counts[conc] = conclusion_counts.get(conc, 0) + 1

    pos_line = "、".join(f"{k} {v} 份" for k, v in position_counts.items())
    conc_line = "、".join(f"{k} {v} 人" for k, v in conclusion_counts.items())

    return (
        f"本次共筛选简历 **{total}** 份。"
        f"岗位分布：{pos_line}。"
        f"结论分布：{conc_line}。"
    )


def build_candidate_table(evals):
    """生成候选人排名总表（按总分降序）。"""
    # 按总分降序排列；缺失总分视为 0
    sorted_evals = sorted(
        evals,
        key=lambda x: x.get("total_score", 0),
        reverse=True,
    )
    lines = [
        "| 排名 | 姓名 | 岗位类别 | 总分 | 满分 | 结论 |",
        "|------|------|----------|------|------|------|",
    ]
    for idx, item in enumerate(sorted_evals, start=1):
        name = item.get("candidate_name") or item.get("filename", "未知")
        pos = item.get("position_type", "未分类")
        total = item.get("total_score", 0)
        max_score = item.get("max_score", 0)
        conc = item.get("conclusion", "未结论")
        lines.append(f"| {idx} | {name} | {pos} | {total} | {max_score} | {conc} |")
    return "\n".join(lines)


def build_details(evals):
    """生成每位候选人的评分明细段落。"""
    sorted_evals = sorted(
        evals,
        key=lambda x: x.get("total_score", 0),
        reverse=True,
    )
    blocks = []
    for item in sorted_evals:
        name = item.get("candidate_name") or item.get("filename", "未知")
        pos = item.get("position_type", "未分类")
        total = item.get("total_score", 0)
        max_score = item.get("max_score", 0)
        conc = item.get("conclusion", "未结论")

        # 候选人标题
        block = [f"### {name}（{pos}）", ""]
        block.append(f"- **总分**：{total} / {max_score}")
        block.append(f"- **结论**：{conc}")
        block.append("")

        # 逐项评分明细
        items = item.get("items", [])
        if items:
            block.append("| 评分项 | 得分 | 满分 | 依据 |")
            block.append("|--------|------|------|------|")
            for it in items:
                crit = it.get("criterion", "")
                score = it.get("score", 0)
                mx = it.get("max", 0)
                ev = it.get("evidence", "").replace("\n", " ").replace("|", "\\|")
                block.append(f"| {crit} | {score} | {mx} | {ev} |")
            block.append("")

        # 亮点
        highlights = item.get("highlights", [])
        if highlights:
            block.append("**亮点**：")
            for h in highlights:
                block.append(f"- {h}")
            block.append("")

        # 风险点
        risks = item.get("risks", [])
        if risks:
            block.append("**风险点**：")
            for r in risks:
                block.append(f"- {r}")
            block.append("")

        blocks.append("\n".join(block))
    return "\n---\n\n".join(blocks)


def render_template(template_path: str, evals):
    """读取模板并替换占位标记，返回最终报告字符串。"""
    with open(template_path, "r", encoding="utf-8") as f:
        template = f.read()

    replacements = {
        "{{report_title}}": "简历筛选报告",
        "{{generated_at}}": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "{{summary}}": build_summary(evals),
        "{{candidate_table}}": build_candidate_table(evals),
        "{{details}}": build_details(evals),
    }
    for marker, value in replacements.items():
        template = template.replace(marker, value)
    return template


def main():
    parser = argparse.ArgumentParser(description="按模板生成简历筛选报告。")
    parser.add_argument("--evals", required=True, help="评估结果 JSON 文件路径")
    parser.add_argument("--template", required=True, help="报告模板 Markdown 文件路径")
    parser.add_argument("--output", required=True, help="输出报告 Markdown 文件路径")
    args = parser.parse_args()

    evals = load_evals(args.evals)
    report = render_template(args.template, evals)

    output_path = Path(args.output).expanduser().resolve()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(report)

    print(f"报告已生成：{output_path}")


if __name__ == "__main__":
    main()

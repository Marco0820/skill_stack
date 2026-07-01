#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
from datetime import datetime
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    KeepTogether,
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)


ROOT = Path("/Users/lyz/wby/技术文档/wby_skill_stack")
EVALS_PATH = ROOT / "tmp/pdfs/resume-screener/evaluations.json"
OUTPUT_PATH = ROOT / "output/pdf/简历筛选报告.pdf"
FONT_NAME = "ArialUnicodeMS"
FONT_PATH = "/Library/Fonts/Arial Unicode.ttf"


def load_evals():
    with EVALS_PATH.open("r", encoding="utf-8") as f:
        return json.load(f)


def p(text):
    return str(text).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def conclusion_counts(evals):
    counts = {}
    for item in evals:
        key = item["conclusion"]
        counts[key] = counts.get(key, 0) + 1
    return counts


def draw_footer(canvas, doc):
    canvas.saveState()
    canvas.setFont(FONT_NAME, 8)
    canvas.setFillColor(colors.HexColor("#6B7280"))
    canvas.drawString(18 * mm, 12 * mm, "resume-screener | 简历筛选报告")
    canvas.drawRightString(192 * mm, 12 * mm, f"第 {doc.page} 页")
    canvas.restoreState()


def build_pdf(evals):
    pdfmetrics.registerFont(TTFont(FONT_NAME, FONT_PATH))

    styles = getSampleStyleSheet()
    base = ParagraphStyle(
        "BaseCN",
        parent=styles["Normal"],
        fontName=FONT_NAME,
        fontSize=10,
        leading=15,
        textColor=colors.HexColor("#111827"),
        alignment=TA_LEFT,
        spaceAfter=4,
    )
    title = ParagraphStyle(
        "TitleCN",
        parent=base,
        fontSize=22,
        leading=30,
        alignment=TA_CENTER,
        textColor=colors.HexColor("#0F172A"),
        spaceAfter=10,
    )
    h1 = ParagraphStyle(
        "H1CN",
        parent=base,
        fontSize=15,
        leading=22,
        textColor=colors.HexColor("#0F172A"),
        spaceBefore=8,
        spaceAfter=8,
    )
    h2 = ParagraphStyle(
        "H2CN",
        parent=base,
        fontSize=13,
        leading=19,
        textColor=colors.HexColor("#0F172A"),
        spaceBefore=10,
        spaceAfter=6,
    )
    small = ParagraphStyle(
        "SmallCN",
        parent=base,
        fontSize=8.5,
        leading=12,
        textColor=colors.HexColor("#374151"),
    )
    table_header_dark = ParagraphStyle(
        "TableHeaderDarkCN",
        parent=small,
        textColor=colors.white,
    )
    note = ParagraphStyle(
        "NoteCN",
        parent=base,
        fontSize=9,
        leading=13,
        textColor=colors.HexColor("#4B5563"),
    )

    doc = SimpleDocTemplate(
        str(OUTPUT_PATH),
        pagesize=A4,
        leftMargin=16 * mm,
        rightMargin=16 * mm,
        topMargin=16 * mm,
        bottomMargin=18 * mm,
        title="简历筛选报告",
        author="resume-screener",
    )

    story = []
    generated_at = datetime.now().strftime("%Y-%m-%d %H:%M")
    sorted_evals = sorted(evals, key=lambda x: x["total_score"], reverse=True)
    counts = conclusion_counts(evals)

    story.append(Paragraph("简历筛选报告", title))
    story.append(Paragraph(f"生成时间：{generated_at}", note))
    story.append(
        Paragraph(
            "评估口径：用户指定岗位主要为销售，本报告统一按内置销售人员招聘标准打分。"
            "候选人简历实际求职意向多为产品经理/AI 产品经理，因此销售结论重点考察其对销售场景、客户资源、商业指标和抗压目标的适配度。",
            note,
        )
    )
    story.append(Spacer(1, 8))

    summary_data = [
        [
            Paragraph("简历总数", small),
            Paragraph("推荐进入面试", small),
            Paragraph("备选", small),
            Paragraph("不推荐", small),
        ],
        [
            Paragraph(str(len(evals)), base),
            Paragraph(str(counts.get("推荐进入面试", 0)), base),
            Paragraph(str(counts.get("备选", 0)), base),
            Paragraph(str(counts.get("不推荐", 0)), base),
        ],
    ]
    summary_table = Table(summary_data, colWidths=[40 * mm, 42 * mm, 35 * mm, 35 * mm])
    summary_table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#EEF2F7")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.HexColor("#374151")),
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("FONTNAME", (0, 0), (-1, -1), FONT_NAME),
                ("FONTSIZE", (0, 0), (-1, -1), 10),
                ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#D1D5DB")),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
                ("TOPPADDING", (0, 0), (-1, -1), 7),
            ]
        )
    )
    story.append(summary_table)
    story.append(Spacer(1, 10))

    story.append(Paragraph("一、候选人排名总表", h1))
    ranking = [
        [
            Paragraph("排名", table_header_dark),
            Paragraph("姓名", table_header_dark),
            Paragraph("岗位类别", table_header_dark),
            Paragraph("总分", table_header_dark),
            Paragraph("结论", table_header_dark),
            Paragraph("核心判断", table_header_dark),
        ]
    ]
    for idx, item in enumerate(sorted_evals, start=1):
        headline = "；".join(item["highlights"][:2])
        ranking.append(
            [
                Paragraph(str(idx), small),
                Paragraph(p(item["candidate_name"]), small),
                Paragraph(p(item["position_type"]), small),
                Paragraph(f"{item['total_score']} / {item['max_score']}", small),
                Paragraph(p(item["conclusion"]), small),
                Paragraph(p(headline), small),
            ]
        )
    ranking_table = Table(
        ranking,
        colWidths=[13 * mm, 20 * mm, 20 * mm, 22 * mm, 27 * mm, 76 * mm],
        repeatRows=1,
    )
    ranking_table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#0F172A")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("FONTNAME", (0, 0), (-1, -1), FONT_NAME),
                ("FONTSIZE", (0, 0), (-1, -1), 8.5),
                ("GRID", (0, 0), (-1, -1), 0.35, colors.HexColor("#CBD5E1")),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("BACKGROUND", (0, 1), (-1, -1), colors.HexColor("#FFFFFF")),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#F8FAFC")]),
                ("TOPPADDING", (0, 0), (-1, -1), 5),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
            ]
        )
    )
    story.append(ranking_table)
    story.append(Spacer(1, 10))

    story.append(Paragraph("二、评分明细", h1))
    for idx, item in enumerate(sorted_evals):
        story.append(
            KeepTogether(
                [
                    Paragraph(
                        f"{item['candidate_name']}：{item['total_score']} / {item['max_score']}，{item['conclusion']}",
                        h2,
                    ),
                    Paragraph(f"来源文件：{p(item['filename'])}", note),
                ]
            )
        )
        score_rows = [
            [
                Paragraph("评分项", small),
                Paragraph("得分", small),
                Paragraph("依据", small),
            ]
        ]
        for scoring in item["items"]:
            score_rows.append(
                [
                    Paragraph(p(scoring["criterion"]), small),
                    Paragraph(f"{scoring['score']} / {scoring['max']}", small),
                    Paragraph(p(scoring["evidence"]), small),
                ]
            )
        scores_table = Table(score_rows, colWidths=[34 * mm, 18 * mm, 126 * mm], repeatRows=1)
        scores_table.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#EEF2F7")),
                    ("FONTNAME", (0, 0), (-1, -1), FONT_NAME),
                    ("FONTSIZE", (0, 0), (-1, -1), 8.5),
                    ("GRID", (0, 0), (-1, -1), 0.35, colors.HexColor("#CBD5E1")),
                    ("VALIGN", (0, 0), (-1, -1), "TOP"),
                    ("TOPPADDING", (0, 0), (-1, -1), 4),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
                ]
            )
        )
        story.append(scores_table)
        story.append(Spacer(1, 5))
        story.append(Paragraph("亮点", h2))
        for value in item["highlights"]:
            story.append(Paragraph(f"- {p(value)}", base))
        story.append(Paragraph("风险点", h2))
        for value in item["risks"]:
            story.append(Paragraph(f"- {p(value)}", base))
        if idx < len(sorted_evals) - 1:
            story.append(PageBreak())

    story.append(Spacer(1, 8))
    story.append(Paragraph("附：说明", h1))
    story.append(
        Paragraph(
            "本报告由 resume-screener 技能依据内置销售招聘标准生成。评分仅作为初筛参考，最终是否进入面试或录用请结合人工判断与面试表现综合决策。未按用户要求执行任何邮件发送动作。",
            note,
        )
    )

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    doc.build(story, onFirstPage=draw_footer, onLaterPages=draw_footer)


def main():
    build_pdf(load_evals())
    print(f"PDF 已生成：{OUTPUT_PATH}")


if __name__ == "__main__":
    main()

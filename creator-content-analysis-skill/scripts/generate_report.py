#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
报告生成模块 — 将分析结果转换为 Markdown 报告和 JSON 输出
"""

import json
from datetime import datetime
from typing import Dict, List, Optional


class ReportGenerator:
    """分析报告生成器"""

    def __init__(self, template_path: Optional[str] = None):
        self.template_path = template_path
        self.report_data = {}

    def generate(self, analysis_result: Dict) -> tuple:
        """
        生成报告

        Args:
            analysis_result: 完整的分析结果

        Returns:
            (markdown_report, json_report) 元组
        """
        self.report_data = analysis_result

        md_report = self._generate_markdown()
        json_report = self._generate_json()

        return md_report, json_report

    def _generate_markdown(self) -> str:
        """生成 Markdown 报告"""
        d = self.report_data
        creator = d.get("creator", {})
        account = d.get("account_profile", {})
        track = d.get("track_analysis", {})
        tone = d.get("tone_analysis", {})
        style = d.get("style_analysis", {})
        tags = d.get("tags", {})
        viral = d.get("viral_patterns", {})
        content_items = d.get("content_items", [])
        commercial = d.get("commercial_potential", {})
        benchmark = d.get("benchmark_recommendations", {})
        risks = d.get("risks_and_issues", [])
        future_topics = d.get("future_topics", [])

        md = []
        md.append("# 自媒体博主内容分析报告\n")
        md.append(f"> **分析对象**：{creator.get('name', '未知')}")
        md.append(f"> **所属平台**：{creator.get('platform', '未知')}")
        md.append(f"> **分析时间**：{datetime.now().strftime('%Y-%m-%d %H:%M')}")
        md.append(f"> **数据完整度**：{d.get('meta', {}).get('data_completeness', 'N/A')}%\n")
        md.append("---\n")

        # 1. 一句话定位
        md.append("## 1. 账号一句话定位\n")
        md.append(d.get("summary", "数据不足，无法判断") + "\n")
        md.append("---\n")

        # 2. 账号基础画像
        md.append("## 2. 账号基础画像\n")
        md.append("| 字段 | 内容 |")
        md.append("|------|------|")
        md.append(f"| 账号名称 | {creator.get('name', '未知')} |")
        md.append(f"| 所属平台 | {creator.get('platform', '未知')} |")
        md.append(f"| 主页链接 | {creator.get('profile_url', '无')} |")
        md.append(f"| 粉丝量级 | {account.get('followers_tier', '数据不足')} |")
        md.append(f"| 粉丝数 | {account.get('followers_count', '数据不足')} |")
        md.append(f"| 内容总数 | {account.get('total_posts', '数据不足')} |")
        md.append(f"| 主要内容类型 | {account.get('content_type', '数据不足')} |")
        md.append(f"| 目标用户人群 | {account.get('target_audience', '数据不足')} |")
        md.append(f"| 账号发展阶段 | {account.get('account_stage', '数据不足')} |")
        md.append(f"| 互动率 | {account.get('engagement_rate', '数据不足')} |")
        md.append("")

        if creator.get("bio"):
            md.append("### 账号简介\n")
            md.append(creator["bio"] + "\n")

        if account.get("user_persona"):
            md.append("### 用户画像推测\n")
            md.append(account["user_persona"] + "\n")

        md.append("---\n")

        # 3. 赛道分析
        md.append("## 3. 内容赛道分析\n")
        md.append("| 维度 | 分析结论 |")
        md.append("|------|----------|")
        md.append(f"| 一级赛道 | {track.get('primary_track', '数据不足')} |")
        md.append(f"| 二级细分赛道 | {track.get('secondary_track', '数据不足')} |")
        md.append(f"| 赛道竞争强度 | {track.get('competition_level', '数据不足')} |")
        md.append(f"| 赛道商业化潜力 | {track.get('commercial_potential', '数据不足')} |")
        md.append(f"| 赛道用户需求 | {track.get('user_needs', '数据不足')} |")
        md.append(f"| 差异化定位 | {track.get('differentiation', '数据不足')} |")
        md.append("")

        if track.get("trends"):
            md.append("### 赛道趋势与机会\n")
            md.append(track["trends"] + "\n")

        md.append("---\n")

        # 4. 调性分析
        md.append("## 4. 内容调性分析\n")
        md.append(f"### 主导调性：{tone.get('primary_tone', '数据不足')}\n")

        if tone.get("tone_scores"):
            md.append("| 调性类型 | 匹配度 | 判断依据 |")
            md.append("|----------|--------|----------|")
            for t, score in tone["tone_scores"].items():
                stars = "★" * score + "☆" * (5 - score)
                md.append(f"| {t} | {stars} | 基于内容分析 |")
            md.append("")

        if tone.get("tone_summary"):
            md.append("### 调性特征总结\n")
            md.append(tone["tone_summary"] + "\n")

        md.append("---\n")

        # 5. 风格分析
        md.append("## 5. 内容风格分析\n")
        md.append("| 维度 | 分析 |")
        md.append("|------|------|")
        md.append(f"| 标题风格 | {style.get('title_style', '数据不足')} |")
        md.append(f"| 封面风格 | {style.get('cover_style', '数据不足')} |")
        md.append(f"| 开头3秒钩子 | {style.get('hook_type', '数据不足')} |")
        md.append(f"| 叙事结构 | {style.get('narrative_structure', '数据不足')} |")
        md.append(f"| 语言表达习惯 | {style.get('language_habits', '数据不足')} |")
        md.append(f"| 剪辑节奏 | {style.get('editing_rhythm', '数据不足')} |")
        md.append(f"| 结尾引导方式 | {style.get('ending_guide', '数据不足')} |")
        md.append(f"| 是否具有强人设 | {'是' if style.get('has_strong_persona') else '否'} |")
        md.append(f"| 是否适合矩阵化复制 | {'是' if style.get('is_replicable') else '否'} |")
        md.append("")
        md.append("---\n")

        # 6. 标签总结
        md.append("## 6. 内容标签总结\n")

        account_tags = tags.get("account_tags", {})
        if account_tags:
            md.append("### 账号核心标签\n")
            all_tags = []
            for dim_tags in account_tags.values():
                all_tags.extend(dim_tags)
            md.append(" ".join([f"`#{t}`" for t in all_tags[:15]]) + "\n")

        tag_dist = tags.get("tag_distribution", [])
        if tag_dist:
            md.append("### 标签分布统计\n")
            md.append("| 标签维度 | 标签 | 出现次数 | 占比 |")
            md.append("|----------|------|----------|------|")
            for item in tag_dist[:20]:
                md.append(f"| {item['dimension']} | {item['tag']} | {item['count']} | {item['percentage']}% |")
            md.append("")

        insights = tags.get("insights", [])
        if insights:
            md.append("### 标签洞察\n")
            for insight in insights:
                md.append(f"- {insight}")
            md.append("")

        md.append("---\n")

        # 7. 高频选题
        md.append("## 7. 高频选题与关键词\n")
        topics = viral.get("high_frequency_topics", [])
        if topics:
            md.append("### 高频选题 TOP 10\n")
            md.append("| 排名 | 选题方向 | 出现次数 | 爆款率 |")
            md.append("|------|----------|----------|--------|")
            for i, t in enumerate(topics[:10], 1):
                md.append(f"| {i} | {t.get('topic', '')} | {t.get('count', 0)} | {t.get('viral_rate', 'N/A')} |")
            md.append("")

        keywords = viral.get("keywords", [])
        if keywords:
            md.append("### 高频关键词\n")
            md.append("、".join(keywords[:20]) + "\n")

        md.append("---\n")

        # 8. 爆款规律
        md.append("## 8. 爆款内容规律\n")
        md.append(f"### 爆款率：{viral.get('viral_rate', 'N/A')}\n")

        formulas = viral.get("title_formulas", [])
        if formulas:
            md.append("### 高频标题句式 TOP 10\n")
            md.append("| 排名 | 句式 | 示例 | 使用次数 |")
            md.append("|------|------|------|----------|")
            for i, f in enumerate(formulas[:10], 1):
                md.append(f"| {i} | {f.get('formula', '')} | {f.get('example', '')} | {f.get('frequency', 0)} |")
            md.append("")

        hooks = viral.get("hook_types", [])
        if hooks:
            md.append("### 高频开头方式\n")
            for h in hooks:
                md.append(f"- {h}")
            md.append("")

        emotions = viral.get("emotion_triggers", [])
        if emotions:
            md.append("### 高频情绪触发点\n")
            for e in emotions:
                md.append(f"- {e}")
            md.append("")

        commonalities = viral.get("viral_commonalities", [])
        if commonalities:
            md.append("### 爆款内容共性\n")
            for c in commonalities:
                md.append(f"- {c}")
            md.append("")

        issues = viral.get("non_viral_issues", [])
        if issues:
            md.append("### 非爆款内容问题\n")
            for issue in issues:
                md.append(f"- {issue}")
            md.append("")

        md.append("---\n")

        # 9. 单条内容拆解
        md.append("## 9. 单条内容拆解\n")
        if content_items:
            for i, item in enumerate(content_items, 1):
                md.append(f"### {i}. {item.get('title', '未知标题')}\n")
                md.append(f"- **爆款等级**：{item.get('viral_level', 'N/A')}")
                md.append(f"- **核心主题**：{item.get('core_topic', 'N/A')}")
                md.append(f"- **钩子**：{item.get('hook', 'N/A')}")
                md.append(f"- **痛点**：{item.get('pain_point', 'N/A')}")
                md.append(f"- **情绪触发**：{item.get('emotion_trigger', 'N/A')}")
                replicable = item.get("replicable_elements", [])
                if replicable:
                    md.append(f"- **可复刻元素**：{'、'.join(replicable)}")
                risks = item.get("risks", [])
                if risks:
                    md.append(f"- **风险**：{'、'.join(risks)}")
                md.append("")
        else:
            md.append("数据不足，无法进行单条内容拆解\n")

        md.append("---\n")

        # 10. 商业化潜力
        md.append("## 10. 商业化潜力分析\n")
        md.append(f"### 商业化成熟度：{commercial.get('maturity', 'N/A')}\n")

        ad_cats = commercial.get("ad_categories", [])
        if ad_cats:
            md.append("### 适合广告合作的品类\n")
            md.append("| 品类 | 匹配度 | 理由 |")
            md.append("|------|--------|------|")
            for cat in ad_cats:
                stars = "★" * cat.get("match_score", 0) + "☆" * (5 - cat.get("match_score", 0))
                md.append(f"| {cat.get('category', '')} | {stars} | {cat.get('reason', '')} |")
            md.append("")

        ecom_cats = commercial.get("ecommerce_categories", [])
        if ecom_cats:
            md.append("### 适合带货的品类\n")
            md.append("| 品类 | 匹配度 | 带货方式 |")
            md.append("|------|--------|----------|")
            for cat in ecom_cats:
                stars = "★" * cat.get("match_score", 0) + "☆" * (5 - cat.get("match_score", 0))
                md.append(f"| {cat.get('category', '')} | {stars} | {cat.get('method', '')} |")
            md.append("")

        revenue = commercial.get("revenue_estimate", {})
        if revenue:
            md.append("### 月收入预估\n")
            md.append("| 变现方式 | 预估月收入 |")
            md.append("|----------|-----------|")
            md.append(f"| 广告合作 | {revenue.get('ad_revenue', 'N/A')} |")
            md.append(f"| 带货佣金 | {revenue.get('ecommerce_revenue', 'N/A')} |")
            md.append(f"| 知识付费 | {revenue.get('knowledge_revenue', 'N/A')} |")
            md.append(f"| **合计** | **{revenue.get('total_estimate', 'N/A')}** |")
            md.append("")

        commercial_risks = commercial.get("risks", [])
        if commercial_risks:
            md.append("### 商业化风险\n")
            md.append("| 风险类型 | 风险等级 | 说明 |")
            md.append("|----------|----------|------|")
            for r in commercial_risks:
                md.append(f"| {r.get('type', '')} | {r.get('level', '')} | {r.get('description', '')} |")
            md.append("")

        md.append("---\n")

        # 11. 对标复刻建议
        md.append("## 11. 对标复刻建议\n")

        best = benchmark.get("best_practices", [])
        if best:
            md.append("### 最值得学习的地方\n")
            for b in best:
                md.append(f"- {b}")
            md.append("")

        structures = benchmark.get("replicable_structures", [])
        if structures:
            md.append("### 可复刻的内容结构\n")
            for s in structures:
                md.append(f"- {s}")
            md.append("")

        templates = benchmark.get("title_templates", [])
        if templates:
            md.append("### 可复用的标题模板\n")
            for t in templates:
                md.append(f"- {t}")
            md.append("")

        strategy = benchmark.get("imitation_strategy", "")
        if strategy:
            md.append("### 模仿策略（非抄袭）\n")
            md.append(strategy + "\n")

        rep_topics = benchmark.get("replicable_topics", [])
        if rep_topics:
            md.append("### 10 个可复刻选题\n")
            md.append("| 序号 | 选题 | 切入角度 | 参考内容 |")
            md.append("|------|------|----------|----------|")
            for i, t in enumerate(rep_topics[:10], 1):
                md.append(f"| {i} | {t.get('topic', '')} | {t.get('angle', '')} | {t.get('reference_content', '')} |")
            md.append("")

        suggestions = benchmark.get("optimization_suggestions", [])
        if suggestions:
            md.append("### 5 条账号优化建议\n")
            for i, s in enumerate(suggestions[:5], 1):
                md.append(f"{i}. {s}")
            md.append("")

        md.append("---\n")

        # 12. 风险与不足
        md.append("## 12. 风险与不足\n")
        if risks:
            md.append("| 风险类型 | 严重程度 | 说明 | 建议 |")
            md.append("|----------|----------|------|------|")
            for r in risks:
                md.append(f"| {r.get('type', '')} | {r.get('severity', '')} | {r.get('description', '')} | {r.get('suggestion', '')} |")
            md.append("")
        else:
            md.append("暂无明显风险\n")

        md.append("---\n")

        # 13. 后续选题建议
        md.append("## 13. 后续内容选题建议\n")
        if future_topics:
            md.append("| 序号 | 选题 | 切入角度 | 目标痛点 | 预期爆款潜力 | 建议标题 |")
            md.append("|------|------|----------|----------|-------------|----------|")
            for i, t in enumerate(future_topics[:10], 1):
                md.append(f"| {i} | {t.get('topic', '')} | {t.get('angle', '')} | {t.get('target_pain_point', '')} | {t.get('expected_viral_potential', '')} | {t.get('suggested_title', '')} |")
            md.append("")
        else:
            md.append("数据不足，无法生成选题建议\n")

        md.append("---\n")

        # 附录
        md.append("## 附录\n")
        md.append("### A. 免责声明\n")
        md.append("本报告基于提供的数据分析生成，分析结论仅供参考。数据质量直接影响分析准确度。建议结合人工判断综合决策。\n")
        md.append(f"---\n\n*报告生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}*")
        md.append(f"*Skill 版本：1.0.0*")

        return "\n".join(md)

    def _generate_json(self) -> Dict:
        """生成 JSON 结构化报告"""
        d = self.report_data

        json_report = {
            "meta": {
                "analysis_time": datetime.now().isoformat(),
                "skill_version": "1.0.0",
                "data_completeness": d.get("meta", {}).get("data_completeness", 0),
                "confidence_score": d.get("meta", {}).get("confidence_score", 0)
            },
            "summary": d.get("summary", ""),
            "account_profile": d.get("account_profile", {}),
            "track_analysis": d.get("track_analysis", {}),
            "tone_analysis": d.get("tone_analysis", {}),
            "style_analysis": d.get("style_analysis", {}),
            "tags": d.get("tags", {}),
            "viral_patterns": d.get("viral_patterns", {}),
            "content_items": d.get("content_items", []),
            "commercial_potential": d.get("commercial_potential", {}),
            "benchmark_recommendations": d.get("benchmark_recommendations", {}),
            "risks_and_issues": d.get("risks_and_issues", []),
            "future_topics": d.get("future_topics", [])
        }

        return json_report


def generate_report(analysis_result: Dict) -> tuple:
    """
    便捷函数：生成报告

    Args:
        analysis_result: 分析结果

    Returns:
        (markdown_report, json_report) 元组
    """
    generator = ReportGenerator()
    return generator.generate(analysis_result)


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        with open(sys.argv[1], "r", encoding="utf-8") as f:
            data = json.load(f)
        md, js = generate_report(data)
        print(md)
    else:
        print("用法: python generate_report.py <分析结果JSON文件路径>")

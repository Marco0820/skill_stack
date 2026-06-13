#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
creator-content-analysis-skill 主入口
自媒体博主/达人/KOL 内容分析工具

使用方式：
    python analyze_creator.py --input data.json --output report.md
    python analyze_creator.py --input data.csv --output report.md --json-output result.json
    python analyze_creator.py --input data.json  # 输出到控制台
"""

import argparse
import json
import os
import sys
from datetime import datetime
from typing import Dict, List, Tuple, Optional

# 添加当前目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from parse_input import InputParser, parse_input
from tag_classifier import TagClassifier, classify_tags
from generate_report import ReportGenerator, generate_report


class CreatorAnalyzer:
    """自媒体博主内容分析器"""

    def __init__(self):
        self.parser = InputParser()
        self.classifier = TagClassifier()
        self.generator = ReportGenerator()
        self.data = None
        self.analysis_result = None

    def load_input(self, input_source: str, format_hint: Optional[str] = None) -> Dict:
        """
        加载输入数据

        Args:
            input_source: 文件路径或文本内容
            format_hint: 格式提示

        Returns:
            标准化的数据
        """
        self.data = self.parser.load(input_source, format_hint)
        return self.data

    def analyze(self) -> Tuple[str, Dict]:
        """
        执行完整分析

        Returns:
            (markdown_report, json_report) 元组
        """
        if not self.data:
            raise ValueError("请先调用 load_input() 加载数据")

        # 执行分析
        analysis_result = self._run_analysis()

        # 生成报告
        md_report, json_report = self.generator.generate(analysis_result)

        self.analysis_result = analysis_result
        return md_report, json_report

    def _run_analysis(self) -> Dict:
        """执行所有分析模块"""
        data = self.data
        creator = data.get("creator", {})
        contents = data.get("contents", [])

        # 计算数据完整度
        completeness = self._calculate_completeness(data)

        # 1. 账号画像分析
        account_profile = self._analyze_account_profile(creator, contents)

        # 2. 赛道分析
        track_analysis = self._analyze_track(contents, creator)

        # 3. 调性分析
        tone_analysis = self._analyze_tone(contents)

        # 4. 风格分析
        style_analysis = self._analyze_style(contents)

        # 5. 标签分析
        tags = self.classifier.classify_account(contents, creator)

        # 6. 爆款规律分析
        viral_patterns = self._analyze_viral_patterns(contents)

        # 7. 单条内容分析
        content_items = self._analyze_content_items(contents)

        # 8. 商业化潜力分析
        commercial = self._analyze_commercial(contents, creator, account_profile)

        # 9. 对标复刻建议
        benchmark = self._generate_benchmark(contents, viral_patterns)

        # 10. 风险分析
        risks = self._analyze_risks(contents, creator)

        # 11. 未来选题建议
        future_topics = self._suggest_future_topics(contents, viral_patterns, track_analysis)

        # 12. 一句话总结
        summary = self._generate_summary(creator, account_profile, track_analysis)

        return {
            "meta": {
                "data_completeness": completeness,
                "confidence_score": min(completeness + 10, 100)
            },
            "creator": creator,
            "summary": summary,
            "account_profile": account_profile,
            "track_analysis": track_analysis,
            "tone_analysis": tone_analysis,
            "style_analysis": style_analysis,
            "tags": tags,
            "viral_patterns": viral_patterns,
            "content_items": content_items,
            "commercial_potential": commercial,
            "benchmark_recommendations": benchmark,
            "risks_and_issues": risks,
            "future_topics": future_topics
        }

    def _calculate_completeness(self, data: Dict) -> int:
        """计算数据完整度"""
        score = 0
        creator = data.get("creator", {})
        contents = data.get("contents", [])

        # 基础信息
        if creator.get("name"): score += 5
        if creator.get("platform"): score += 5
        if creator.get("followers"): score += 5
        if creator.get("bio"): score += 5

        # 内容数据
        if contents:
            score += 10
            sample = contents[0] if contents else {}
            if sample.get("title"): score += 10
            if sample.get("transcript"): score += 20
            if sample.get("likes"): score += 10
            if sample.get("comments"): score += 5
            if sample.get("shares"): score += 5
            if sample.get("hashtags"): score += 5
            if sample.get("publish_time"): score += 5

            # 数据量加分
            if len(contents) >= 10: score += 10
            elif len(contents) >= 5: score += 5

        return min(score, 100)

    def _analyze_account_profile(self, creator: Dict, contents: List[Dict]) -> Dict:
        """分析账号基础画像"""
        name = creator.get("name", "未知")
        platform = creator.get("platform", "未知")
        followers = creator.get("followers", "")
        bio = creator.get("bio", "")
        total_posts = creator.get("total_posts", str(len(contents)))

        # 解析粉丝量级
        followers_tier = self._parse_followers_tier(followers)

        # 计算互动率
        total_engagement = sum(
            c.get("likes", 0) + c.get("comments", 0) + c.get("shares", 0) + c.get("favorites", 0)
            for c in contents
        )
        avg_engagement = total_engagement / len(contents) if contents else 0
        followers_num = self._parse_followers_num(followers)
        engagement_rate = f"{(avg_engagement / followers_num * 100):.1f}%" if followers_num > 0 else "数据不足"

        # 判断主要内容类型
        content_types = [c.get("content_type", "短视频") for c in contents]
        main_type = max(set(content_types), key=content_types.count) if content_types else "短视频"

        # 判断账号阶段
        if followers_num >= 1000000:
            stage = "成熟期（百万粉以上）"
        elif followers_num >= 100000:
            stage = "爆发期（十万级）"
        elif followers_num >= 10000:
            stage = "成长期（万粉级）"
        else:
            stage = "起步期"

        # 推测目标人群
        target_audience = self._infer_target_audience(contents, creator)

        # 用户画像
        user_persona = self._infer_user_persona(contents, creator)

        return {
            "name": name,
            "platform": platform,
            "profile_url": creator.get("profile_url", ""),
            "followers_tier": followers_tier,
            "followers_count": followers if followers else "数据不足",
            "total_posts": total_posts,
            "content_type": main_type,
            "target_audience": target_audience,
            "account_stage": stage,
            "engagement_rate": engagement_rate,
            "user_persona": user_persona
        }

    def _parse_followers_tier(self, followers: str) -> str:
        """解析粉丝量级"""
        if not followers:
            return "数据不足"

        followers = str(followers).replace(",", "").replace(" ", "")

        if "千万" in followers or (followers.replace("万", "").replace("w", "").replace("W", "").isdigit() and int(followers.replace("万", "").replace("w", "").replace("W", "")) >= 1000):
            return "千万级"
        elif "百万" in followers or "M" in followers.upper():
            return "百万级"
        elif "万" in followers or "w" in followers.lower():
            num = followers.replace("万", "").replace("w", "").replace("W", "")
            try:
                if int(num) >= 10:
                    return "十万级"
                else:
                    return "万级"
            except ValueError:
                return "万级"
        else:
            try:
                num = int(followers)
                if num >= 1000000:
                    return "百万级"
                elif num >= 100000:
                    return "十万级"
                elif num >= 10000:
                    return "万级"
                elif num >= 1000:
                    return "千级"
                else:
                    return "百级"
            except ValueError:
                return "数据不足"

    def _parse_followers_num(self, followers: str) -> int:
        """解析粉丝数为数字"""
        if not followers:
            return 0

        followers = str(followers).replace(",", "").replace(" ", "")

        try:
            if "万" in followers or "w" in followers.lower():
                num = float(followers.replace("万", "").replace("w", "").replace("W", ""))
                return int(num * 10000)
            elif "百万" in followers:
                num = float(followers.replace("百万", ""))
                return int(num * 1000000)
            elif "千万" in followers:
                num = float(followers.replace("千万", ""))
                return int(num * 10000000)
            elif "亿" in followers:
                num = float(followers.replace("亿", ""))
                return int(num * 100000000)
            else:
                return int(float(followers))
        except (ValueError, TypeError):
            return 0

    def _infer_target_audience(self, contents: List[Dict], creator: Dict) -> str:
        """推测目标用户人群"""
        # 合并所有文本
        all_text = " ".join([
            str(c.get("title", "")) + " " + str(c.get("description", "")) + " " + str(c.get("transcript", ""))
            for c in contents
        ])

        audiences = []
        audience_keywords = {
            "互联网从业者": ["互联网", "程序员", "产品经理", "运营", "技术"],
            "职场人": ["职场", "打工人", "上班族", "工作", "上班"],
            "创业者": ["创业", "老板", "生意", "副业"],
            "学生": ["学生", "大学生", "考研", "毕业"],
            "宝妈": ["宝妈", "带娃", "育儿", "妈妈"],
            "科技爱好者": ["AI", "科技", "数码", "极客"],
            "想赚钱的普通人": ["赚钱", "副业", "收入", "变现"],
        }

        for audience, keywords in audience_keywords.items():
            if any(kw in all_text for kw in keywords):
                audiences.append(audience)

        if not audiences:
            audiences = ["泛人群"]

        return "、".join(audiences[:3])

    def _infer_user_persona(self, contents: List[Dict], creator: Dict) -> str:
        """推测用户画像"""
        audience = self._infer_target_audience(contents, creator)

        personas = []
        if "互联网从业者" in audience or "科技爱好者" in audience:
            personas.append("25-40岁，一二线城市，对新技术敏感，有学习焦虑")
        if "职场人" in audience:
            personas.append("有职场晋升需求，关注效率工具和职业技能")
        if "想赚钱的普通人" in audience:
            personas.append("有副业/赚钱需求，愿意尝试新事物")

        if not personas:
            personas.append("基于内容推测为对新事物感兴趣的年轻群体")

        return "；".join(personas)

    def _analyze_track(self, contents: List[Dict], creator: Dict) -> Dict:
        """分析内容赛道"""
        all_text = " ".join([
            str(c.get("title", "")) + " " + str(c.get("description", "")) + " " + str(c.get("transcript", ""))
            for c in contents
        ])

        # 一级赛道判断
        track_scores = {}
        track_mapping = {
            "科技": ["AI", "人工智能", "ChatGPT", "科技", "技术", "编程", "代码"],
            "职场": ["职场", "工作", "面试", "简历", "升职"],
            "财经": ["赚钱", "副业", "投资", "理财", "收入"],
            "教育": ["学习", "教程", "课程", "知识", "培训"],
            "美妆": ["美妆", "护肤", "化妆", "穿搭"],
            "情感": ["情感", "恋爱", "婚姻"],
        }

        for track, keywords in track_mapping.items():
            score = sum(all_text.count(kw) for kw in keywords)
            track_scores[track] = score

        primary_track = max(track_scores, key=track_scores.get) if track_scores else "综合"

        # 二级赛道
        secondary_tracks = []
        if "AI" in all_text or "人工智能" in all_text:
            secondary_tracks.append("AI/人工智能")
        if "赚钱" in all_text or "副业" in all_text:
            secondary_tracks.append("AI赚钱/副业")
        if "工具" in all_text or "推荐" in all_text:
            secondary_tracks.append("AI工具推荐")
        secondary_track = " + ".join(secondary_tracks[:2]) if secondary_tracks else "综合"

        # 竞争强度
        competition = "高" if primary_track in ["科技", "职场", "财经"] else "中"

        # 商业化潜力
        commercial_potential = "极高" if primary_track in ["科技", "财经", "美妆"] else "高"

        # 用户需求
        user_needs = "学习AI工具、了解行业趋势、获取赚钱方法、缓解职场焦虑"

        # 差异化定位
        differentiation = self._analyze_differentiation(contents)

        return {
            "primary_track": primary_track,
            "secondary_track": secondary_track,
            "competition_level": competition,
            "commercial_potential": commercial_potential,
            "user_needs": user_needs,
            "differentiation": differentiation,
            "trends": "AI赛道仍处于快速增长期，用户需求旺盛，商业化潜力巨大"
        }

    def _analyze_differentiation(self, contents: List[Dict]) -> str:
        """分析差异化定位"""
        all_titles = " ".join([str(c.get("title", "")) for c in contents])

        if "赚钱" in all_titles and "AI" in all_titles:
            return "'AI+赚钱'双标签，兼顾资讯和实用变现，比纯科普更有吸引力"
        elif "教程" in all_titles:
            return "以教程为核心，强调实操性和可复制性"
        else:
            return "基于内容分析推测的差异化定位"

    def _analyze_tone(self, contents: List[Dict]) -> Dict:
        """分析内容调性"""
        all_text = " ".join([
            str(c.get("title", "")) + " " + str(c.get("transcript", ""))
            for c in contents
        ])

        # 调性评分
        tone_scores = {
            "专业理性型": 0,
            "情绪共鸣型": 0,
            "犀利观点型": 0,
            "幽默搞笑型": 0,
            "干货教学型": 0,
            "个人陪伴型": 0,
            "反差人设型": 0,
            "强销售转化型": 0,
            "故事叙事型": 0,
            "观点输出型": 0,
            "热点借势型": 0,
        }

        # 关键词匹配评分
        if any(kw in all_text for kw in ["教程", "方法", "技巧", "工具", "手把手"]):
            tone_scores["干货教学型"] += 3
        if any(kw in all_text for kw in ["焦虑", "淘汰", "取代", "害怕", "担心"]):
            tone_scores["情绪共鸣型"] += 3
        if any(kw in all_text for kw in ["我认为", "我觉得", "说实话", "不建议"]):
            tone_scores["观点输出型"] += 2
            tone_scores["犀利观点型"] += 2
        if any(kw in all_text for kw in ["我", "自己", "经历", "分享"]):
            tone_scores["故事叙事型"] += 2
        if any(kw in all_text for kw in ["最新", "更新", "发布", "热点"]):
            tone_scores["热点借势型"] += 2
        if any(kw in all_text for kw in ["哈哈", "搞笑", "笑死"]):
            tone_scores["幽默搞笑型"] += 2

        # 找出主导调性
        primary_tone = max(tone_scores, key=tone_scores.get)

        # 调性总结
        tone_summary = f"账号以'{primary_tone}'为核心调性"
        if tone_scores["情绪共鸣型"] > 1:
            tone_summary += "，配合焦虑驱动获取流量"
        if tone_scores["干货教学型"] > 1:
            tone_summary += "，内容以干货教学为主"

        return {
            "primary_tone": primary_tone,
            "tone_scores": {k: v for k, v in tone_scores.items() if v > 0},
            "tone_evidence": "基于标题、文案关键词分析",
            "tone_summary": tone_summary
        }

    def _analyze_style(self, contents: List[Dict]) -> Dict:
        """分析内容风格"""
        titles = [str(c.get("title", "")) for c in contents]

        # 标题风格分析
        title_features = []
        if any("！" in t for t in titles):
            title_features.append("感叹号强化情绪")
        if any(any(c.isdigit() for c in t) for t in titles):
            title_features.append("数字型标题")
        if any("？" in t for t in titles):
            title_features.append("疑问句引发好奇")
        if any("千万" in t or "别" in t for t in titles):
            title_features.append("否定警示型")

        title_style = "、".join(title_features) if title_features else "标准标题"

        # 钩子类型
        transcripts = [str(c.get("transcript", ""))[:100] for c in contents if c.get("transcript")]
        hook_types = []
        for t in transcripts:
            if any(kw in t for kw in ["你敢相信", "你猜", "竟然", "居然"]):
                hook_types.append("悬念型")
            if any(kw in t for kw in ["今天", "最新", "重磅"]):
                hook_types.append("热点型")
            if any(kw in t for kw in ["我用", "我试", "我花了"]):
                hook_types.append("个人经历型")

        hook_type = max(set(hook_types), key=hook_types.count) if hook_types else "标准开头"

        return {
            "title_style": title_style,
            "cover_style": "大字标题+信息量密集",
            "hook_type": hook_type,
            "narrative_structure": "问题-方案型、数字清单型、个人经历型",
            "language_habits": "口语化、通俗易懂、善用反问和设问",
            "editing_rhythm": "快节奏，信息密度高",
            "ending_guide": "引导关注，强调持续价值",
            "has_strong_persona": False,
            "is_replicable": True
        }

    def _analyze_viral_patterns(self, contents: List[Dict]) -> Dict:
        """分析爆款规律"""
        if not contents:
            return {"viral_rate": "N/A", "high_frequency_topics": [], "title_formulas": []}

        # 计算平均互动
        engagements = []
        for c in contents:
            eng = c.get("likes", 0) + c.get("comments", 0) + c.get("shares", 0) + c.get("favorites", 0)
            engagements.append(eng)

        avg_engagement = sum(engagements) / len(engagements) if engagements else 0

        # 识别爆款（>=2倍平均值）
        viral_threshold = avg_engagement * 2
        viral_contents = [c for c, e in zip(contents, engagements) if e >= viral_threshold]
        viral_rate = f"{len(viral_contents)}/{len(contents)} ({len(viral_contents)/len(contents)*100:.0f}%)" if contents else "N/A"

        # 高频主题
        topic_counter = {}
        for c in contents:
            title = str(c.get("title", ""))
            # 简单的主题提取
            for keyword in ["AI", "赚钱", "工具", "方法", "教程", "避坑", "选题", "自媒体"]:
                if keyword in title:
                    topic_counter[keyword] = topic_counter.get(keyword, 0) + 1

        high_freq_topics = [
            {"topic": k, "count": v, "viral_rate": "待计算"}
            for k, v in sorted(topic_counter.items(), key=lambda x: -x[1])[:10]
        ]

        # 标题句式
        title_formulas = []
        for c in contents:
            title = str(c.get("title", ""))
            if "实测" in title or "揭秘" in title:
                title_formulas.append({"formula": "揭秘/实测型", "example": title[:30], "frequency": 1})
            elif any(c.isdigit() for c in title) and ("个" in title or "招" in title or "件" in title):
                title_formulas.append({"formula": "数字清单型", "example": title[:30], "frequency": 1})
            elif "千万别" in title or "不要" in title:
                title_formulas.append({"formula": "否定警示型", "example": title[:30], "frequency": 1})
            elif "为什么" in title:
                title_formulas.append({"formula": "疑问观点型", "example": title[:30], "frequency": 1})

        # 去重统计
        formula_counts = {}
        for f in title_formulas:
            key = f["formula"]
            if key not in formula_counts:
                formula_counts[key] = {"formula": key, "example": f["example"], "frequency": 0}
            formula_counts[key]["frequency"] += 1

        return {
            "viral_rate": viral_rate,
            "high_frequency_topics": high_freq_topics,
            "title_formulas": sorted(formula_counts.values(), key=lambda x: -x["frequency"])[:10],
            "hook_types": ["数据冲击型", "悬念型", "否定型", "热点型"],
            "emotion_triggers": ["焦虑触发", "好奇触发", "利益诱导", "紧迫感"],
            "keywords": [k for k, _ in sorted(topic_counter.items(), key=lambda x: -x[1])[:15]],
            "viral_commonalities": [
                "标题必须有数字或具体利益点",
                "前3秒必须有强钩子",
                "内容必须击中用户痛点",
                "结尾必须有明确的行动引导",
                "信息密度要高，避免拖沓"
            ],
            "non_viral_issues": [
                "选题偏离核心标签",
                "标题缺乏具体数字或利益点",
                "开头钩子不够强",
                "内容深度一般，缺乏独特观点"
            ]
        }

    def _analyze_content_items(self, contents: List[Dict]) -> List[Dict]:
        """分析单条内容"""
        items = []

        # 计算平均互动用于爆款判断
        engagements = []
        for c in contents:
            eng = c.get("likes", 0) + c.get("comments", 0) + c.get("shares", 0) + c.get("favorites", 0)
            engagements.append(eng)
        avg_engagement = sum(engagements) / len(engagements) if engagements else 1

        for i, c in enumerate(contents):
            eng = engagements[i] if i < len(engagements) else 0

            # 爆款等级
            if eng >= avg_engagement * 3:
                viral_level = "S"
            elif eng >= avg_engagement * 2:
                viral_level = "A"
            elif eng >= avg_engagement:
                viral_level = "B"
            elif eng >= avg_engagement * 0.5:
                viral_level = "C"
            else:
                viral_level = "D"

            title = str(c.get("title", ""))
            transcript = str(c.get("transcript", ""))

            # 核心主题提取
            core_topic = "AI科技"
            for kw in ["赚钱", "工具", "教程", "避坑", "趋势"]:
                if kw in title or kw in transcript[:200]:
                    core_topic = f"AI{kw}"
                    break

            # 钩子分析
            hook = transcript[:100] if transcript else title

            # 痛点分析
            pain_point = "想了解AI但不知从何入手"
            if "赚钱" in title:
                pain_point = "想用AI赚钱但没有方向"
            elif "淘汰" in title or "取代" in title:
                pain_point = "担心被AI取代的职场焦虑"
            elif "工具" in title:
                pain_point = "不知道哪个AI工具好用"

            items.append({
                "id": c.get("id", str(i + 1)),
                "title": title,
                "url": c.get("url", ""),
                "publish_time": c.get("publish_time", ""),
                "core_topic": core_topic,
                "summary": transcript[:200] + "..." if len(transcript) > 200 else transcript,
                "hook": hook[:80],
                "pain_point": pain_point,
                "core_viewpoint": f"关于{core_topic}的核心观点",
                "emotion_trigger": "焦虑+好奇",
                "structure": "问题-方案型",
                "conversion_point": "引导关注",
                "viral_level": viral_level,
                "replicable_elements": ["选题角度", "标题句式", "钩子设计"],
                "risks": [],
                "tags": []
            })

        return items

    def _analyze_commercial(self, contents: List[Dict], creator: Dict, account_profile: Dict) -> Dict:
        """分析商业化潜力"""
        followers_num = self._parse_followers_num(creator.get("followers", ""))

        # 商业化成熟度
        if followers_num >= 1000000:
            maturity = "成熟期"
        elif followers_num >= 100000:
            maturity = "成长期"
        else:
            maturity = "萌芽期"

        # 广告品类
        ad_categories = [
            {"category": "AI工具/SaaS", "match_score": 5, "reason": "内容与产品高度匹配"},
            {"category": "在线教育/课程", "match_score": 4, "reason": "用户有学习需求"},
            {"category": "科技硬件", "match_score": 3, "reason": "科技属性匹配"},
            {"category": "职场服务", "match_score": 3, "reason": "用户有职场焦虑"},
        ]

        # 带货品类
        ecom_categories = [
            {"category": "AI课程/训练营", "match_score": 5, "method": "视频挂车+私域转化"},
            {"category": "效率工具会员", "match_score": 4, "method": "视频挂车"},
            {"category": "科技数码产品", "match_score": 3, "method": "视频挂车+直播"},
        ]

        # 收入预估
        base_income = followers_num * 0.01 if followers_num > 0 else 10000
        revenue = {
            "ad_revenue": f"¥{int(base_income * 0.3):,} - ¥{int(base_income * 0.8):,}",
            "ecommerce_revenue": f"¥{int(base_income * 0.1):,} - ¥{int(base_income * 0.3):,}",
            "knowledge_revenue": f"¥{int(base_income * 0.5):,} - ¥{int(base_income * 1.5):,}",
            "total_estimate": f"¥{int(base_income * 0.9):,} - ¥{int(base_income * 2.6):,}"
        }

        # 风险
        commercial_risks = [
            {"type": "内容翻车风险", "level": "中", "description": "AI赚钱类内容容易被质疑夸大"},
            {"type": "舆情风险", "level": "中", "description": "焦虑营销可能引发负面评价"},
            {"type": "平台政策风险", "level": "低", "description": "内容合规，无明显违规"},
        ]

        return {
            "maturity": maturity,
            "ad_categories": ad_categories,
            "ecommerce_categories": ecom_categories,
            "knowledge_monetization": "适合AI实战训练营，定价999-2999元",
            "private_domain_potential": "通过视频引导私信，建立AI学习社群",
            "brand_collaboration": "AI工具品牌深度合作，在线教育平台课程分销",
            "revenue_estimate": revenue,
            "risks": commercial_risks
        }

    def _generate_benchmark(self, contents: List[Dict], viral_patterns: Dict) -> Dict:
        """生成对标复刻建议"""
        return {
            "best_practices": [
                "选题精准，100%围绕核心标签",
                "标题公式成熟：数字+利益+焦虑",
                "开头钩子强，前3秒必有冲击性信息",
                "信息密度高，每15-20秒一个信息点",
                "引导关注自然，结尾价值承诺"
            ],
            "replicable_structures": [
                "数字清单型：X个工具/X个方法",
                "个人经历型：我用AI做了XX",
                "避坑指南型：千万别做这X件事",
                "观点输出型：为什么我不建议...",
                "揭秘型：揭秘XX是怎么做的"
            ],
            "title_templates": [
                "实测！用AI一天赚了XXX块，方法公开",
                "千万别用AI做这X件事，否则你会后悔",
                "2025年最值得学的X个AI工具",
                "为什么我不建议你现在学XXX",
                "这个AI工具免费用，99%的人不知道"
            ],
            "expandable_topics": ["AI+教育", "AI+电商", "AI+设计", "AI+写作", "AI+创业"],
            "imitation_strategy": "换赛道（AI+其他行业）、换角度（不同切入方向）、换深度（更专业或更通俗）、换形式（图文/直播）、换人设（不同身份标签）",
            "replicable_topics": [
                {"topic": "用AI做PPT", "angle": "效率工具", "reference_content": "ChatGPT更新"},
                {"topic": "AI写爆文", "angle": "内容创作", "reference_content": "AI做自媒体"},
                {"topic": "AI工具对比", "angle": "工具测评", "reference_content": "免费AI工具"},
            ],
            "optimization_suggestions": [
                "强化人设，打造更鲜明的个人IP",
                "深化变现，系统化知识付费产品",
                "增加深度内容，提升专业度",
                "多平台分发，扩大影响力",
                "建立私域社群，沉淀核心用户"
            ]
        }

    def _analyze_risks(self, contents: List[Dict], creator: Dict) -> List[Dict]:
        """分析风险"""
        risks = []

        # 检查夸大宣传风险
        all_text = " ".join([str(c.get("title", "")) + str(c.get("transcript", "")) for c in contents])
        if any(kw in all_text for kw in ["一天赚", "月入10万", "替代90%", "99%不知道"]):
            risks.append({
                "type": "夸大宣传风险",
                "severity": "中",
                "description": "标题和内容中存在夸大表述，可能被质疑",
                "suggestion": "增加免责声明，使用'可能'、'有机会'等措辞"
            })

        # 焦虑营销风险
        if any(kw in all_text for kw in ["淘汰", "取代", "焦虑", "害怕"]):
            risks.append({
                "type": "焦虑营销风险",
                "severity": "中",
                "description": "过度使用焦虑驱动可能引发负面评价",
                "suggestion": "降低焦虑浓度，增加正向价值内容"
            })

        # 内容同质化风险
        if len(contents) > 5:
            risks.append({
                "type": "内容同质化风险",
                "severity": "低",
                "description": "选题和风格高度相似，可能审美疲劳",
                "suggestion": "增加内容形式创新，如访谈、实操直播"
            })

        return risks

    def _suggest_future_topics(self, contents: List[Dict], viral_patterns: Dict, track_analysis: Dict) -> List[Dict]:
        """建议未来选题"""
        topics = [
            {
                "topic": "AI+教育应用",
                "angle": "教育赛道家长焦虑",
                "target_pain_point": "家长担心孩子落后",
                "expected_viral_potential": "★★★★★",
                "suggested_title": "用AI辅导孩子作业，成绩提升30分"
            },
            {
                "topic": "AI副业矩阵",
                "angle": "多种AI赚钱方式",
                "target_pain_point": "想增加收入",
                "expected_viral_potential": "★★★★★",
                "suggested_title": "5个AI副业，月入过万不是梦"
            },
            {
                "topic": "AI+职场晋升",
                "angle": "用AI提升工作效率",
                "target_pain_point": "职场竞争力焦虑",
                "expected_viral_potential": "★★★★☆",
                "suggested_title": "用AI写周报，领导直接给我升职"
            },
            {
                "topic": "AI工具深度测评",
                "angle": "工具对比评测",
                "target_pain_point": "不知道选哪个工具",
                "expected_viral_potential": "★★★★☆",
                "suggested_title": "ChatGPT vs Claude vs Kimi，到底哪个最好用？"
            },
            {
                "topic": "AI学习路线图",
                "angle": "系统学习AI的路径",
                "target_pain_point": "想学但不知从何入手",
                "expected_viral_potential": "★★★★☆",
                "suggested_title": "2025年AI学习路线图，从入门到精通"
            },
        ]
        return topics

    def _generate_summary(self, creator: Dict, account_profile: Dict, track_analysis: Dict) -> str:
        """生成一句话总结"""
        name = creator.get("name", "该账号")
        platform = creator.get("platform", "")
        audience = account_profile.get("target_audience", "用户")
        track = track_analysis.get("primary_track", "综合")
        secondary = track_analysis.get("secondary_track", "")

        return f"{name}是一个面向{audience}的{platform}{track}类账号，主要聚焦{secondary}方向，通过干货教学+焦虑驱动的内容策略吸引用户关注。"


def main():
    """命令行入口"""
    parser = argparse.ArgumentParser(
        description="自媒体博主/达人/KOL 内容分析工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用示例：
  python analyze_creator.py --input data.json --output report.md
  python analyze_creator.py --input data.csv --output report.md --json-output result.json
  python analyze_creator.py --input data.json  # 输出到控制台
        """
    )

    parser.add_argument("--input", "-i", required=True, help="输入文件路径（支持 JSON/CSV/Markdown/TXT/Excel）")
    parser.add_argument("--output", "-o", help="Markdown 报告输出路径")
    parser.add_argument("--json-output", "-j", help="JSON 结构化输出路径")
    parser.add_argument("--format", "-f", choices=["json", "csv", "md", "txt"], help="强制指定输入格式")

    args = parser.parse_args()

    # 检查输入文件
    if not os.path.exists(args.input):
        print(f"错误：输入文件不存在: {args.input}")
        sys.exit(1)

    # 执行分析
    print(f"正在加载数据: {args.input}")
    analyzer = CreatorAnalyzer()
    analyzer.load_input(args.input, args.format)

    stats = analyzer.parser.get_stats()
    print(f"数据加载完成: {stats.get('total_contents', 0)} 条内容")

    print("正在执行分析...")
    md_report, json_report = analyzer.analyze()
    print("分析完成！")

    # 输出结果
    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(md_report)
        print(f"Markdown 报告已保存: {args.output}")
    else:
        print("\n" + "=" * 60)
        print(md_report)
        print("=" * 60)

    if args.json_output:
        with open(args.json_output, "w", encoding="utf-8") as f:
            json.dump(json_report, f, ensure_ascii=False, indent=2)
        print(f"JSON 报告已保存: {args.json_output}")

    print("\n分析完成！")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
标签分类模块 — 基于规则和关键词的自动标签提取
可独立使用，也可作为分析流程的一部分
"""

import json
import re
from collections import Counter
from typing import Dict, List, Set, Tuple


class TagClassifier:
    """内容标签分类器"""

    # 赛道标签关键词映射
    TRACK_KEYWORDS = {
        "科技": ["科技", "技术", "AI", "人工智能", "ChatGPT", "GPT", "大模型", "机器学习", "深度学习", "编程", "代码", "Python", "算法", "互联网", "数字化"],
        "职场": ["职场", "工作", "面试", "简历", "升职", "加薪", "跳槽", "求职", "职业规划", "管理", "领导力"],
        "财经": ["财经", "投资", "理财", "股票", "基金", "赚钱", "收入", "副业", "创业", "商业", "商业模式"],
        "教育": ["教育", "学习", "考试", "考研", "留学", "培训", "课程", "知识", "成长"],
        "情感": ["情感", "恋爱", "婚姻", "分手", "脱单", "相亲", "两性", "爱情"],
        "美妆": ["美妆", "护肤", "化妆", "穿搭", "时尚", "美容", "化妆品"],
        "母婴": ["母婴", "育儿", "宝宝", "孕期", "辅食", "早教", "带娃"],
        "汽车": ["汽车", "买车", "驾驶", "车评", "新能源", "电动车"],
        "房产": ["房产", "买房", "租房", "装修", "房价", "楼市"],
        "旅游": ["旅游", "旅行", "攻略", "景点", "酒店", "机票", "自驾"],
        "美食": ["美食", "做饭", "菜谱", "餐厅", "小吃", "烘焙", "烹饪"],
        "健身": ["健身", "减肥", "运动", "瑜伽", "增肌", "跑步", "塑形"],
        "知识科普": ["科普", "知识", "原理", "为什么", "冷知识", "真相"],
        "娱乐": ["娱乐", "明星", "综艺", "八卦", "热搜", "搞笑", "段子"],
        "影视解说": ["电影", "电视剧", "影视", "解说", "影评", "剧评"],
        "带货种草": ["种草", "推荐", "好物", "测评", "开箱", "拔草"],
        "本地生活": ["本地", "同城", "探店", "周边", "附近"],
    }

    # 人群标签关键词
    AUDIENCE_KEYWORDS = {
        "年轻人": ["大学生", "毕业", "00后", "95后", "Z世代", "年轻人"],
        "职场人": ["打工人", "上班族", "职场", "加班", "通勤", "996"],
        "宝妈": ["宝妈", "带娃", "育儿", "宝宝", "妈妈"],
        "创业者": ["创业", "老板", "生意", "开店", "副业"],
        "学生": ["学生", "考研", "考试", "校园", "大学"],
        "男性": ["男人", "男生", "男性", "兄弟", "哥们"],
        "女性": ["女人", "女生", "女性", "姐妹", "闺蜜"],
        "中年人": ["中年", "40岁", "50岁", "上有老下有小"],
        "科技爱好者": ["极客", "数码", "科技", "程序员", "开发者"],
        "焦虑人群": ["焦虑", "迷茫", "内卷", "躺平", "压力"],
    }

    # 情绪标签关键词
    EMOTION_KEYWORDS = {
        "焦虑": ["焦虑", "担心", "害怕", "恐惧", "淘汰", "取代", "失业", "落后", "错过"],
        "共鸣": ["共鸣", "感同身受", "说到心坎", "太真实", "扎心"],
        "好奇": ["揭秘", "秘密", "真相", "为什么", "原来", "竟然", "居然"],
        "愤怒": ["愤怒", "气愤", "过分", "无语", "离谱", "恶心"],
        "感动": ["感动", "泪目", "暖心", "温暖", "正能量"],
        "激励": ["加油", "坚持", "努力", "奋斗", "逆袭", "改变"],
        "轻松": ["搞笑", "哈哈", "笑死", "有趣", "好玩"],
        "紧迫": ["赶紧", "马上", "立刻", "最后", "错过", "再等一年"],
    }

    # 表达风格标签
    STYLE_KEYWORDS = {
        "口语化": ["哈哈", "嗯", "吧", "呢", "啊", "嘛", "你懂的"],
        "专业化": ["数据显示", "研究表明", "根据", "分析", "报告"],
        "故事化": ["我有个朋友", "之前", "有一次", "记得", "故事"],
        "数据化": ["90%", "10倍", "100万", "数据", "统计", "百分比"],
        "犀利": ["说实话", "不客气", "真相是", "别再", "千万别"],
        "温和": ["建议", "可以", "试试", "分享", "希望"],
        "幽默": ["笑死", "哈哈", "离谱", "绝了", "绝绝子"],
    }

    # 商业化标签
    COMMERCIAL_KEYWORDS = {
        "适合广告": ["推荐", "好用", "神器", "必备", "强烈推荐"],
        "适合带货": ["购买", "链接", "下单", "优惠", "折扣", "同款"],
        "适合知识付费": ["教程", "课程", "学习", "方法", "技巧", "秘籍"],
        "适合私域": ["私信", "关注", "社群", "群", "加我"],
    }

    # 热点标签
    HOTSPOT_KEYWORDS = {
        "追热点": ["热搜", "热点", "最新", "刚刚", "突发", "重磅"],
        "蹭热度": ["XXX", "那个", "最近很火", "大家都在说"],
        "常青内容": ["永久", "经典", "必看", "收藏", "干货"],
    }

    # 内容形式标签
    FORMAT_KEYWORDS = {
        "教程类": ["教程", "教你", "手把手", "步骤", "方法"],
        "测评类": ["测评", "评测", "对比", "实测", "体验"],
        "资讯类": ["新闻", "资讯", "更新", "发布", "最新"],
        "观点类": ["我认为", "我觉得", "观点", "看法", "建议"],
        "故事类": ["故事", "经历", "分享", "真实", "案例"],
        "清单类": ["X个", "X招", "X种", "Top", "排行榜"],
    }

    def __init__(self):
        self.stats = Counter()

    def classify_content(self, content: Dict) -> Dict:
        """
        对单条内容进行标签分类

        Args:
            content: 内容字典

        Returns:
            标签字典
        """
        # 合并所有文本用于分析
        text = " ".join([
            str(content.get("title", "")),
            str(content.get("description", "")),
            str(content.get("transcript", "")),
            str(content.get("cover_text", "")),
            " ".join(content.get("hashtags", []))
        ])

        tags = {
            "track": self._match_tags(text, self.TRACK_KEYWORDS),
            "audience": self._match_tags(text, self.AUDIENCE_KEYWORDS),
            "topic": self._extract_topics(content),
            "emotion": self._match_tags(text, self.EMOTION_KEYWORDS),
            "style": self._match_tags(text, self.STYLE_KEYWORDS),
            "commercial": self._match_tags(text, self.COMMERCIAL_KEYWORDS),
            "hotspot": self._match_tags(text, self.HOTSPOT_KEYWORDS),
            "format": self._match_tags(text, self.FORMAT_KEYWORDS),
            "platform": self._detect_platform_style(content),
            "virality": self._assess_virality(content),
        }

        return tags

    def classify_account(self, contents: List[Dict], creator_info: Dict = None) -> Dict:
        """
        对整个账号进行标签分类

        Args:
            contents: 内容列表
            creator_info: 账号信息

        Returns:
            账号级标签字典
        """
        all_tags = {
            "track": Counter(),
            "audience": Counter(),
            "topic": Counter(),
            "emotion": Counter(),
            "style": Counter(),
            "commercial": Counter(),
            "hotspot": Counter(),
            "format": Counter(),
            "platform": Counter(),
            "virality": Counter(),
        }

        # 对每条内容打标签并统计
        content_tags_list = []
        for content in contents:
            tags = self.classify_content(content)
            content_tags_list.append({"content_id": content.get("id", ""), "tags": tags})
            for dim, tag_list in tags.items():
                for tag in tag_list:
                    all_tags[dim][tag] += 1

        # 生成账号级标签（取 Top N）
        account_tags = {}
        for dim, counter in all_tags.items():
            account_tags[dim] = [tag for tag, _ in counter.most_common(10)]

        # 生成标签分布统计
        tag_distribution = []
        total = len(contents) if contents else 1
        for dim, counter in all_tags.items():
            for tag, count in counter.most_common():
                tag_distribution.append({
                    "dimension": dim,
                    "tag": tag,
                    "count": count,
                    "percentage": round(count / total * 100, 1)
                })

        # 生成标签洞察
        insights = self._generate_insights(account_tags, tag_distribution, contents)

        return {
            "account_tags": account_tags,
            "content_tags": content_tags_list,
            "tag_distribution": tag_distribution,
            "insights": insights
        }

    def _match_tags(self, text: str, keyword_map: Dict[str, List[str]]) -> List[str]:
        """根据关键词匹配标签"""
        matched = []
        text_lower = text.lower()
        for tag, keywords in keyword_map.items():
            for kw in keywords:
                if kw.lower() in text_lower:
                    matched.append(tag)
                    break
        return matched

    def _extract_topics(self, content: Dict) -> List[str]:
        """提取内容主题标签"""
        topics = []
        title = content.get("title", "")
        hashtags = content.get("hashtags", [])

        # 从标签中提取
        topics.extend(hashtags)

        # 从标题中提取关键短语
        # 简单的关键词提取（实际应用中可以用NLP）
        keywords = ["AI", "ChatGPT", "赚钱", "副业", "工具", "教程", "方法", "技巧",
                     "Python", "编程", "自媒体", "职场", "学习", "效率", "提效"]
        for kw in keywords:
            if kw in title:
                topics.append(kw)

        return list(set(topics))[:10]  # 去重，最多10个

    def _detect_platform_style(self, content: Dict) -> List[str]:
        """检测平台风格"""
        styles = []
        title = content.get("title", "")
        duration = content.get("duration", "")

        # 短视频特征
        if duration:
            try:
                parts = duration.split(":")
                total_seconds = int(parts[0]) * 60 + int(parts[1]) if len(parts) == 2 else 0
                if total_seconds <= 60:
                    styles.append("短视频")
                elif total_seconds <= 300:
                    styles.append("中视频")
                else:
                    styles.append("长视频")
            except (ValueError, IndexError):
                pass

        # 标题风格
        if "！" in title or "？" in title:
            styles.append("强情绪标题")
        if any(c.isdigit() for c in title):
            styles.append("数字标题")

        return styles if styles else ["标准"]

    def _assess_virality(self, content: Dict) -> List[str]:
        """评估传播潜力"""
        tags = []
        likes = content.get("likes", 0)
        comments = content.get("comments", 0)
        shares = content.get("shares", 0)
        favorites = content.get("favorites", 0)

        total_engagement = likes + comments + shares + favorites

        if total_engagement > 100000:
            tags.append("高传播力")
        elif total_engagement > 30000:
            tags.append("中传播力")
        else:
            tags.append("低传播力")

        # 分享率高说明有传播价值
        if likes > 0 and shares / likes > 0.1:
            tags.append("高分享率")

        # 收藏率高说明有实用价值
        if likes > 0 and favorites / likes > 0.2:
            tags.append("高收藏率")

        # 评论率高说明有互动性
        if likes > 0 and comments / likes > 0.05:
            tags.append("高互动性")

        return tags

    def _generate_insights(self, account_tags: Dict, tag_distribution: List[Dict], contents: List[Dict]) -> List[str]:
        """生成标签洞察"""
        insights = []

        # 核心标签画像
        core_tags = []
        for dim in ["track", "audience", "emotion"]:
            if account_tags.get(dim):
                core_tags.extend(account_tags[dim][:2])
        if core_tags:
            insights.append(f"核心标签画像：{'、'.join(core_tags[:5])}")

        # 标签集中度
        track_tags = account_tags.get("track", [])
        if len(track_tags) <= 2:
            insights.append("标签集中度高：账号内容高度聚焦，垂直度强")
        elif len(track_tags) <= 4:
            insights.append("标签集中度中等：账号有一定聚焦，但也有扩展")
        else:
            insights.append("标签集中度低：账号内容较分散，建议聚焦核心赛道")

        # 商业化标签
        commercial_tags = account_tags.get("commercial", [])
        if commercial_tags:
            insights.append(f"商业化方向：{', '.join(commercial_tags[:3])}")

        # 情绪标签
        emotion_tags = account_tags.get("emotion", [])
        if "焦虑" in emotion_tags:
            insights.append("情绪策略：大量使用焦虑驱动，需注意负面情绪累积风险")
        if "好奇" in emotion_tags:
            insights.append("情绪策略：善于激发好奇心，有利于完播率")

        return insights


def classify_tags(data: Dict) -> Dict:
    """
    便捷函数：对数据进行标签分类

    Args:
        data: 标准化数据字典

    Returns:
        标签分类结果
    """
    classifier = TagClassifier()
    return classifier.classify_account(
        data.get("contents", []),
        data.get("creator", {})
    )


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        with open(sys.argv[1], "r", encoding="utf-8") as f:
            data = json.load(f)
        result = classify_tags(data)
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print("用法: python tag_classifier.py <输入JSON文件路径>")

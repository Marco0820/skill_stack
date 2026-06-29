#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
send_report.py — 通过 SMTP 发送简历筛选报告

作用：
    把生成的简历筛选报告以邮件附件形式发送给指定收件人。
    仅在用户明确要求发送时才由上层调用本脚本。

安全说明（重要）：
    SMTP 账号密码等敏感信息【绝不硬编码】在本脚本中，统一通过以下两种方式之一提供：
      1) 配置文件（推荐）：--config 指向一个 JSON 文件，字段见下；
      2) 环境变量：未提供 --config 时，从环境变量读取。
    配置文件 / 环境变量字段：
      SMTP_HOST      SMTP 服务器地址，如 smtp.qq.com
      SMTP_PORT      SMTP 端口，如 465（SSL）或 587（STARTTLS）
      SMTP_USER      发件账号
      SMTP_PASS      发件账号密码 / 授权码（QQ/163 等多为授权码）
      SMTP_FROM      发件人地址（缺省时取 SMTP_USER）
      SMTP_USE_TLS   是否使用 STARTTLS（true/false）；端口为 465 时走 SSL
      SMTP_USE_SSL   是否使用 SSL（true/false）；默认端口 465 时为 true

用法：
    python send_report.py \
        --report 简历筛选报告.md \
        --to hr@example.com \
        --subject "简历筛选报告" \
        --config smtp_config.json

    也可用环境变量：
    SMTP_HOST=smtp.qq.com SMTP_PORT=465 SMTP_USER=xxx SMTP_PASS=xxx \
        python send_report.py --report 简历筛选报告.md --to hr@example.com
"""

import argparse        # 命令行参数解析
import json            # 读取配置文件
import os              # 读取环境变量
import smtplib         # SMTP 发送
from email.mime.multipart import MIMEMultipart  # 多部分邮件（正文 + 附件）
from email.mime.text import MIMEText            # 纯文本正文
from email.utils import formataddr, formatdate  # 发件人格式化、日期


def load_config(config_path):
    """
    加载 SMTP 配置。优先读配置文件，缺失字段回退到环境变量。
    返回字典。
    """
    config = {}
    if config_path:
        with open(config_path, "r", encoding="utf-8") as f:
            config = json.load(f)

    # 环境变量回退
    env_keys = ["SMTP_HOST", "SMTP_PORT", "SMTP_USER", "SMTP_PASS",
                "SMTP_FROM", "SMTP_USE_TLS", "SMTP_USE_SSL"]
    for key in env_keys:
        if key not in config or config[key] in (None, ""):
            env_val = os.environ.get(key)
            if env_val is not None:
                config[key] = env_val

    # 必填校验
    required = ["SMTP_HOST", "SMTP_USER", "SMTP_PASS"]
    missing = [k for k in required if not config.get(k)]
    if missing:
        raise ValueError(
            f"缺少 SMTP 配置：{missing}。"
            f"请通过 --config 配置文件或环境变量提供。"
        )

    # 端口与加密方式默认值
    port = int(config.get("SMTP_PORT") or 0)
    if not port:
        # 未指定端口时，按是否 SSL 给默认值
        port = 465 if _as_bool(config.get("SMTP_USE_SSL")) else 587
    config["SMTP_PORT"] = port
    config["SMTP_FROM"] = config.get("SMTP_FROM") or config["SMTP_USER"]
    return config


def _as_bool(value):
    """把字符串 / 布尔值统一解析为布尔。"""
    if isinstance(value, bool):
        return value
    if value is None:
        return False
    return str(value).strip().lower() in ("1", "true", "yes", "on")


def build_message(report_path, sender, recipients, subject):
    """构建带附件的邮件对象。"""
    msg = MIMEMultipart()
    msg["From"] = formataddr(("简历筛选技能", sender))
    msg["To"] = ", ".join(recipients)
    msg["Subject"] = subject
    msg["Date"] = formatdate(localtime=True)

    # 正文：简要说明 + 附件同名提示
    body = (
        "您好，\n\n"
        "附件为本次简历筛选报告，请查收。\n"
        "报告由 resume-screener 技能自动生成，评分仅供参考，最终录用请结合人工判断。\n"
    )
    msg.attach(MIMEText(body, "plain", "utf-8"))

    # 附件：报告 Markdown 文件
    with open(report_path, "rb") as f:
        report_content = f.read()
    attachment = MIMEText(report_content, "base64", "utf-8")
    attachment.add_header(
        "Content-Disposition",
        "attachment",
        filename=("utf-8", "", os.path.basename(report_path)),
    )
    msg.attach(attachment)
    return msg


def send(config, recipients, subject, report_path):
    """根据配置连接 SMTP 服务器并发送邮件。"""
    host = config["SMTP_HOST"]
    port = config["SMTP_PORT"]
    user = config["SMTP_USER"]
    password = config["SMTP_PASS"]
    sender = config["SMTP_FROM"]
    use_ssl = _as_bool(config.get("SMTP_USE_SSL")) or port == 465
    use_tls = _as_bool(config.get("SMTP_USE_TLS")) and not use_ssl

    msg = build_message(report_path, sender, recipients, subject)

    # 根据加密方式选择连接
    if use_ssl:
        server = smtplib.SMTP_SSL(host, port, timeout=30)
    else:
        server = smtplib.SMTP(host, port, timeout=30)
        if use_tls:
            server.starttls()

    try:
        server.login(user, password)
        server.sendmail(sender, recipients, msg.as_string())
    finally:
        server.quit()


def main():
    parser = argparse.ArgumentParser(description="通过 SMTP 发送简历筛选报告邮件。")
    parser.add_argument("--report", required=True, help="报告文件路径（作为附件）")
    parser.add_argument("--to", required=True, help="收件人邮箱（多个用逗号分隔）")
    parser.add_argument("--cc", default="", help="抄送邮箱（多个用逗号分隔，可选）")
    parser.add_argument("--subject", default="简历筛选报告", help="邮件主题")
    parser.add_argument("--config", help="SMTP 配置文件路径（JSON），可选")
    args = parser.parse_args()

    config = load_config(args.config)
    recipients = [addr.strip() for addr in args.to.split(",") if addr.strip()]
    if args.cc:
        recipients += [addr.strip() for addr in args.cc.split(",") if addr.strip()]

    send(config, recipients, args.subject, args.report)
    print(f"邮件已发送至：{', '.join(recipients)}")


if __name__ == "__main__":
    main()

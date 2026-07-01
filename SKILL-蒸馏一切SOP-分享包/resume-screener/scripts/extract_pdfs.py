#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
extract_pdfs.py — 简历 PDF 批量文本提取脚本

作用：
    扫描指定文件夹下的所有 PDF 简历，逐份提取文本，统一输出为一个 JSON 文件，
    供后续的招聘标准评估环节使用。

提取策略（按优先级自动回退）：
    1. 优先使用 pdfplumber 提取（对排版复杂的简历效果较好）；
    2. 若 pdfplumber 不可用或提取失败，回退到 PyPDF2；
    3. 若两者都不可用，或提取到的文本过少（可能是扫描件 / 图片型 PDF），
       则把该简历标记为 needs_manual_read=True，提示上层改用 Read 工具直接读取。

用法：
    python extract_pdfs.py <简历文件夹路径> --output resumes.json
    python extract_pdfs.py <简历文件夹路径> --output resumes.json --min-chars 20

输出 JSON 结构：
    [
      {
        "filename": "张三-销售.pdf",
        "path": "/abs/path/张三-销售.pdf",
        "text": "提取到的简历正文……",
        "extracted_by": "pdfplumber | pypdf2 | none",
        "needs_manual_read": false,
        "error": ""
      },
      ...
    ]
"""

import argparse          # 命令行参数解析
import json              # 输出 JSON
import os                # 路径处理
from pathlib import Path  # 跨平台路径操作


def find_pdf_files(folder: str):
    """递归查找文件夹下所有 PDF 文件，返回绝对路径列表。"""
    folder_path = Path(folder).expanduser().resolve()
    if not folder_path.is_dir():
        raise NotADirectoryError(f"指定的简历文件夹不存在或不是目录：{folder_path}")
    # rglob 递归匹配，统一小写比较以兼容 .PDF 后缀
    pdfs = [p for p in folder_path.rglob("*.pdf") if p.is_file()]
    pdfs += [p for p in folder_path.rglob("*.PDF") if p.is_file()]
    # 去重并排序，保证输出稳定
    seen = set()
    unique = []
    for p in pdfs:
        if p not in seen:
            seen.add(p)
            unique.append(p)
    return sorted(unique)


def extract_with_pdfplumber(pdf_path: str) -> str:
    """用 pdfplumber 提取文本。失败时抛出异常交由上层回退。"""
    import pdfplumber  # 延迟导入，避免未安装时整个脚本崩溃
    text_parts = []
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text() or ""
            text_parts.append(page_text)
    return "\n".join(text_parts).strip()


def extract_with_pypdf2(pdf_path: str) -> str:
    """用 PyPDF2 / pypdf 提取文本，作为回退方案。"""
    try:
        # 新版包名是 pypdf
        from pypdf import PdfReader
    except ImportError:
        # 旧版包名 PyPDF2
        from PyPDF2 import PdfReader  # type: ignore
    reader = PdfReader(pdf_path)
    text_parts = []
    for page in reader.pages:
        try:
            text_parts.append(page.extract_text() or "")
        except Exception:
            # 某一页解析失败不阻塞其它页
            text_parts.append("")
    return "\n".join(text_parts).strip()


def extract_one(pdf_path: str, min_chars: int):
    """
    对单份 PDF 执行提取，返回一个结果字典。
    extracted_by 标记最终用了哪种方式；needs_manual_read 提示是否需要人工补读。
    """
    result = {
        "filename": os.path.basename(pdf_path),
        "path": pdf_path,
        "text": "",
        "extracted_by": "none",
        "needs_manual_read": False,
        "error": "",
    }

    # 第一优先级：pdfplumber
    try:
        text = extract_with_pdfplumber(pdf_path)
        if text and len(text) >= min_chars:
            result["text"] = text
            result["extracted_by"] = "pdfplumber"
            return result
        # 提取到的文本太少，先记下，继续尝试回退方案
        result["text"] = text
    except ImportError:
        # pdfplumber 未安装，直接进入回退
        pass
    except Exception as e:
        result["error"] = f"pdfplumber 提取失败：{e}"

    # 第二优先级：PyPDF2 / pypdf
    try:
        text = extract_with_pypdf2(pdf_path)
        if text and len(text) >= min_chars:
            result["text"] = text
            result["extracted_by"] = "pypdf2"
            return result
        # 两种方式都没拿到足够文本，标记为需要人工补读（多为扫描件 / 图片型 PDF）
        result["text"] = text or result["text"]
        result["needs_manual_read"] = True
        if not result["error"]:
            result["error"] = "提取到的文本过少，疑似扫描件或图片型 PDF"
    except ImportError:
        # 两个库都没装：无法自动提取，交给上层用 Read 工具读取
        result["needs_manual_read"] = True
        result["error"] = "未安装 pdfplumber / pypdf2，请用 Read 工具直接读取该 PDF"
    except Exception as e:
        result["needs_manual_read"] = True
        result["error"] = f"pypdf2 提取失败：{e}"

    return result


def main():
    parser = argparse.ArgumentParser(description="批量提取 PDF 简历文本，输出 JSON。")
    parser.add_argument("folder", help="存放 PDF 简历的文件夹路径")
    parser.add_argument("--output", "-o", default="resumes.json",
                        help="输出 JSON 文件路径（默认 resumes.json）")
    parser.add_argument("--min-chars", type=int, default=20,
                        help="判定提取成功的最小字符数阈值（默认 20）")
    args = parser.parse_args()

    pdf_files = find_pdf_files(args.folder)
    print(f"共发现 {len(pdf_files)} 份 PDF 简历。")

    results = []
    for pdf in pdf_files:
        print(f"  提取中：{pdf.name}")
        results.append(extract_one(str(pdf), args.min_chars))

    # 确保输出目录存在
    output_path = Path(args.output).expanduser().resolve()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    # 汇总提示
    auto_ok = sum(1 for r in results if not r["needs_manual_read"])
    need_manual = sum(1 for r in results if r["needs_manual_read"])
    print(f"提取完成：自动成功 {auto_ok} 份，需人工补读 {need_manual} 份。")
    print(f"结果已写入：{output_path}")
    if need_manual:
        print("提示：需人工补读的简历，请改用 Read 工具直接读取对应 PDF。")


if __name__ == "__main__":
    main()

#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
測試情感分析功能
"""

import sys

sys.path.insert(0, ".")

from app import analyze_sentiment, classify_sentiment, analyze_news_sentiment
import pandas as pd

# 測試文本
test_texts = [
    "台灣經濟持續成長，前景看好",  # 正面
    "股市大跌，投資者損失慘重",  # 負面
    "今天天氣不錯",  # 中立
    "新產品發布會圓滿成功",  # 正面
    "公司裁員計畫引發員工不滿",  # 負面
]

print("=" * 60)
print("🧪 情感分析功能測試")
print("=" * 60)

# 測試單個文本的情感分析
print("\n📝 測試單個文本的情感分析：")
print("-" * 60)

for text in test_texts:
    score = analyze_sentiment(text)
    sentiment = classify_sentiment(score)
    print(f"文本: {text}")
    score_str = f"{score:.4f}" if score is not None else "N/A"
    print(f"情感分數: {score_str}")
    print(f"情感分類: {sentiment}")
    print()

# 測試 DataFrame 的情感分析
print("\n📊 測試 DataFrame 的情感分析：")
print("-" * 60)

df = pd.DataFrame(
    {
        "標題": test_texts,
        "連結": ["http://example.com"] * len(test_texts),
        "發布時間": ["2025-10-27 12:00:00"] * len(test_texts),
        "來源": ["測試來源"] * len(test_texts),
        "關鍵字": ["測試"] * len(test_texts),
    }
)

print("原始 DataFrame:")
print(df)
print()

df_analyzed = analyze_news_sentiment(df)

print("分析後的 DataFrame:")
print(df_analyzed[["標題", "情感分數", "情感分類"]])
print()

# 統計情感分佈
print("情感分佈統計:")
print(df_analyzed["情感分類"].value_counts())

print("\n✅ 測試完成！")

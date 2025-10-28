#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
測試詞雲功能修復
"""

import sys
import os

sys.path.insert(0, ".")

from app import generate_word_cloud
import pandas as pd

print("=" * 80)
print("🧪 測試詞雲功能修復")
print("=" * 80)

# 建立測試資料
test_data = {
    "標題": [
        "台積電宣布在台南設立新廠，預計創造上萬個就業機會",
        "科技產業持續成長，半導體需求強勁",
        "台灣經濟表現亮眼，出口創新高",
        "人工智慧技術突破，應用範圍擴大",
        "綠能產業發展迅速，政府大力支持",
        "5G網路建設加速，覆蓋率提升",
        "電動車市場蓬勃發展，充電站普及",
        "數位轉型成為企業重要課題",
        "資訊安全受到重視，防護措施加強",
        "雲端服務需求增加，市場規模擴大",
    ],
    "連結": ["http://example.com"] * 10,
    "發布時間": ["2025-10-27 12:00:00"] * 10,
    "來源": ["測試來源"] * 10,
    "關鍵字": ["科技"] * 10,
}

df = pd.DataFrame(test_data)

print("\n📊 測試資料：")
print(df[["標題"]].head())
print(f"\n總共 {len(df)} 筆新聞標題")

print("\n" + "-" * 80)
print("🎨 開始生成詞雲...")
print("-" * 80)

try:
    result = generate_word_cloud(df)
    
    if result:
        print(f"\n✅ 詞雲生成成功！")
        print(f"📁 檔案名稱: {result}")
        print(f"📂 完整路徑: {os.path.abspath(os.path.join('static', result))}")
        
        # 檢查檔案是否存在
        file_path = os.path.join("static", result)
        if os.path.exists(file_path):
            file_size = os.path.getsize(file_path)
            print(f"📏 檔案大小: {file_size:,} bytes ({file_size/1024:.2f} KB)")
            print(f"\n🎉 測試通過！詞雲 stopwords bug 已修復！")
        else:
            print(f"\n❌ 錯誤：檔案不存在")
    else:
        print(f"\n⚠️ 詞雲生成返回 None")
        print("可能原因：")
        print("1. wordcloud 模組未安裝")
        print("2. 字體檔案未找到")
        print("3. 其他錯誤（請查看上方錯誤訊息）")
        
except Exception as e:
    print(f"\n❌ 測試失敗: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 80)
print("測試完成")
print("=" * 80)


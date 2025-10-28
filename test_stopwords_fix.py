#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
測試 stopwords 修復邏輯（不需要安裝 wordcloud）
"""

print("=" * 80)
print("🧪 測試 Stopwords 修復邏輯")
print("=" * 80)

# 模擬原本的錯誤寫法
print("\n❌ 原本的錯誤寫法：")
print("-" * 80)

try:
    from wordcloud import STOPWORDS
    
    # 錯誤的寫法：update() 返回 None
    wrong_stopwords = STOPWORDS.update(["的", "是", "在", "了"])
    print(f"STOPWORDS.update() 的返回值: {wrong_stopwords}")
    print(f"類型: {type(wrong_stopwords)}")
    print("⚠️ 這會導致 WordCloud 的 stopwords 參數接收到 None！")
    
except ImportError:
    print("⚠️ wordcloud 未安裝，使用模擬測試")
    
    # 模擬 STOPWORDS 行為
    class MockStopwords(set):
        def __init__(self):
            super().__init__(["a", "the", "is", "are"])
    
    STOPWORDS = MockStopwords()
    
    # 錯誤的寫法
    wrong_stopwords = STOPWORDS.update(["的", "是", "在", "了"])
    print(f"STOPWORDS.update() 的返回值: {wrong_stopwords}")
    print(f"類型: {type(wrong_stopwords)}")
    print("⚠️ 這會導致 WordCloud 的 stopwords 參數接收到 None！")

print("\n" + "=" * 80)
print("✅ 修復後的正確寫法：")
print("-" * 80)

try:
    from wordcloud import STOPWORDS as WC_STOPWORDS
    
    # 正確的寫法：使用集合運算
    chinese_stopwords = {
        "的", "是", "在", "了", "和", "有", "也", "為", "與",
        "等", "將", "及", "或", "但", "而", "對", "於", "以"
    }
    
    correct_stopwords = WC_STOPWORDS | chinese_stopwords
    print(f"使用集合運算 (|) 的返回值類型: {type(correct_stopwords)}")
    print(f"是否為集合: {isinstance(correct_stopwords, set)}")
    print(f"總共包含 {len(correct_stopwords)} 個停用詞")
    print(f"前 10 個停用詞: {list(correct_stopwords)[:10]}")
    print("✅ 這樣可以正確傳遞給 WordCloud！")
    
except ImportError:
    print("⚠️ wordcloud 未安裝，使用模擬測試")
    
    # 模擬 STOPWORDS
    STOPWORDS = {"a", "the", "is", "are"}
    
    # 正確的寫法
    chinese_stopwords = {
        "的", "是", "在", "了", "和", "有", "也", "為", "與",
        "等", "將", "及", "或", "但", "而", "對", "於", "以"
    }
    
    correct_stopwords = STOPWORDS | chinese_stopwords
    print(f"使用集合運算 (|) 的返回值類型: {type(correct_stopwords)}")
    print(f"是否為集合: {isinstance(correct_stopwords, set)}")
    print(f"總共包含 {len(correct_stopwords)} 個停用詞")
    print(f"停用詞內容: {correct_stopwords}")
    print("✅ 這樣可以正確傳遞給 WordCloud！")

print("\n" + "=" * 80)
print("📝 修復總結：")
print("-" * 80)
print("1. ❌ 錯誤：stopwords=STOPWORDS.update([...])  → 返回 None")
print("2. ✅ 正確：stopwords=STOPWORDS | set([...])   → 返回合併後的集合")
print("3. ✅ 正確：stopwords=STOPWORDS | {...}        → 返回合併後的集合")
print("\n💡 Python 集合的 update() 方法會就地修改集合並返回 None")
print("💡 使用 | 運算符可以創建新的合併集合")
print("=" * 80)

print("\n🎉 Stopwords bug 修復邏輯驗證完成！")


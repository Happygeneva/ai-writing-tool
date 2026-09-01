import streamlit as st

from core.gemini_client import generate
from core.ui import api_key_warning, page_header, render_result

st.set_page_config(page_title="翻訳", page_icon="🌐", layout="wide")
page_header("🌐 翻訳", "日本語・英語を中心に文章を翻訳します。")

if not api_key_warning():
    st.stop()

source_text = st.text_area("翻訳したい文章", height=240, placeholder="翻訳したい文章を貼り付けてください")

col1, col2 = st.columns(2)
with col1:
    target_lang = st.selectbox("翻訳先言語", ["英語", "日本語", "中国語（簡体字）", "韓国語", "スペイン語", "フランス語", "その他（自由入力）"])
    if target_lang == "その他（自由入力）":
        target_lang = st.text_input("翻訳先言語を入力してください", placeholder="例: ドイツ語")
with col2:
    tone = st.selectbox("トーン", ["自然・標準", "ビジネスフォーマル", "カジュアル"])

if st.button("翻訳する", type="primary", use_container_width=True):
    if not source_text:
        st.warning("翻訳したい文章を入力してください。")
    else:
        prompt = f"""以下の文章を{target_lang}に翻訳してください。

# トーン
{tone}

# 対象の文章
{source_text}

# 出力形式
翻訳結果のみを出力してください。
"""
        with st.spinner("翻訳しています..."):
            result = generate(
                prompt,
                system_instruction="あなたはプロの翻訳者です。自然で文脈に合った訳文を作成します。",
                temperature=0.3,
            )
        render_result(result, key="translation")

import streamlit as st

from core.gemini_client import generate
from core.ui import api_key_warning, page_header, render_result

st.set_page_config(page_title="文章要約", page_icon="📄", layout="wide")
page_header("📄 文章要約", "長文を指定した長さ・形式で要約します。")

if not api_key_warning():
    st.stop()

source_text = st.text_area("要約したい文章", height=280, placeholder="要約したい文章を貼り付けてください")

col1, col2 = st.columns(2)
with col1:
    style = st.selectbox("出力形式", ["1段落の文章", "箇条書き（3〜5点）", "一文で要約", "見出し付き要約"])
with col2:
    length = st.select_slider("要約の分量", options=["超短め", "短め", "標準", "やや詳しく"], value="標準")

if st.button("要約する", type="primary", use_container_width=True):
    if not source_text:
        st.warning("要約したい文章を入力してください。")
    else:
        prompt = f"""以下の文章を要約してください。

# 出力形式
{style}

# 分量
{length}

# 要約対象の文章
{source_text}
"""
        with st.spinner("要約しています..."):
            result = generate(
                prompt,
                system_instruction="あなたは文章要約の専門家です。原文の要点を漏らさず、簡潔で分かりやすい日本語に要約します。",
                temperature=0.3,
            )
        render_result(result, key="summary")

import streamlit as st

from core.gemini_client import generate
from core.ui import api_key_warning, page_header, render_result

st.set_page_config(page_title="タイトル・見出し生成", page_icon="🏷️", layout="wide")
page_header("🏷️ タイトル・見出し生成", "記事内容からタイトルや見出し案を複数提案します。")

if not api_key_warning():
    st.stop()

source_text = st.text_area(
    "記事の内容 or テーマ", height=220, placeholder="タイトルを付けたい記事本文、または簡単なテーマ説明を入力してください"
)

col1, col2 = st.columns(2)
with col1:
    style = st.selectbox("スタイル", ["SEOを意識した検索されやすいタイトル", "クリックしたくなるキャッチーなタイトル", "シンプルで分かりやすいタイトル", "数字を使ったタイトル"])
with col2:
    count = st.slider("提案数", min_value=3, max_value=10, value=5)

if st.button("タイトル案を生成する", type="primary", use_container_width=True):
    if not source_text:
        st.warning("記事の内容またはテーマを入力してください。")
    else:
        prompt = f"""以下の記事内容・テーマに合うタイトル案を{count}個提案してください。

# スタイル
{style}

# 記事内容・テーマ
{source_text}

# 出力形式
番号付きリストでタイトル案のみを列挙してください。
"""
        with st.spinner("タイトル案を生成しています..."):
            result = generate(
                prompt,
                system_instruction="あなたは編集者・コピーライターです。読者の興味を引きつつ内容を正確に反映したタイトルを考えます。",
                temperature=0.9,
            )
        render_result(result, key="titles")

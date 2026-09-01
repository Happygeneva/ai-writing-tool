import streamlit as st

from core.gemini_client import generate
from core.ui import api_key_warning, page_header, render_result

st.set_page_config(page_title="トーン変換", page_icon="🔄", layout="wide")
page_header("🔄 トーン変換", "文章の口調（丁寧・カジュアル・ビジネスなど）を変換します。")

if not api_key_warning():
    st.stop()

source_text = st.text_area("変換したい文章", height=240, placeholder="トーンを変えたい文章を貼り付けてください")

target_tone = st.selectbox(
    "変換後のトーン",
    [
        "丁寧語（です・ます調）",
        "ビジネスフォーマル",
        "カジュアル・フランク",
        "簡潔・端的",
        "熱意が伝わる表現",
        "謙虚・控えめな表現",
    ],
)
keep_meaning = st.checkbox("意味・事実関係は変えずニュアンスのみ変換する", value=True)

if st.button("変換する", type="primary", use_container_width=True):
    if not source_text:
        st.warning("変換したい文章を入力してください。")
    else:
        prompt = f"""以下の文章のトーンを「{target_tone}」に変換してください。
{"元の意味や事実関係は変えず、言い回しのみを変換してください。" if keep_meaning else ""}

# 対象の文章
{source_text}

# 出力形式
変換後の文章のみを出力してください。
"""
        with st.spinner("変換しています..."):
            result = generate(
                prompt,
                system_instruction="あなたは文章のトーン・文体変換の専門家です。自然な日本語で書き直します。",
                temperature=0.5,
            )
        render_result(result, key="tone_converted")

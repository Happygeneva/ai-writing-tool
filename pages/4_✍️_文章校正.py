import streamlit as st

from core.gemini_client import generate
from core.ui import api_key_warning, page_header, render_result

st.set_page_config(page_title="文章校正・添削", page_icon="✍️", layout="wide")
page_header("✍️ 文章校正・添削", "誤字脱字や表現の違和感をチェックし、改善案を提示します。")

if not api_key_warning():
    st.stop()

source_text = st.text_area("校正したい文章", height=280, placeholder="校正・添削したい文章を貼り付けてください")

checkpoints = st.multiselect(
    "チェックしてほしい観点",
    ["誤字脱字", "文法・言い回しの不自然さ", "敬語の適切さ", "分かりやすさ・簡潔さ", "重複表現"],
    default=["誤字脱字", "文法・言い回しの不自然さ", "分かりやすさ・簡潔さ"],
)

if st.button("校正する", type="primary", use_container_width=True):
    if not source_text:
        st.warning("校正したい文章を入力してください。")
    else:
        prompt = f"""以下の文章を校正・添削してください。

# チェック観点
{"、".join(checkpoints) if checkpoints else "全般"}

# 対象の文章
{source_text}

# 出力形式
1. 「指摘事項」として、問題箇所と理由を箇条書きで列挙する
2. 「修正後の全文」として、修正を反映した文章全体を提示する
"""
        with st.spinner("校正しています..."):
            result = generate(
                prompt,
                system_instruction="あなたはプロの日本語校閲者です。的確かつ簡潔に指摘し、自然な文章に修正します。",
                temperature=0.3,
            )
        render_result(result, key="proofread")

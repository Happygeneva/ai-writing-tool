import streamlit as st

from core.gemini_client import generate
from core.ui import api_key_warning, page_header, render_result

st.set_page_config(page_title="アイデア出し", page_icon="💡", layout="wide")
page_header("💡 アイデア出し", "テーマに沿った切り口・構成案をブレインストーミングします。")

if not api_key_warning():
    st.stop()

theme = st.text_area("テーマ・お題", height=140, placeholder="例: 副業に興味がある会社員向けのブログ")

col1, col2 = st.columns(2)
with col1:
    idea_type = st.selectbox(
        "アイデアの種類",
        ["ブログ記事の切り口", "SNS投稿のネタ", "動画・コンテンツの企画案", "記事の構成案（見出し案）", "商品・サービスの企画案"],
    )
with col2:
    count = st.slider("提案数", min_value=3, max_value=15, value=8)

extra = st.text_area("条件・制約（任意）", placeholder="例: 初心者向け、費用をかけずにできるもの、を優先してほしい")

if st.button("アイデアを出す", type="primary", use_container_width=True):
    if not theme:
        st.warning("テーマ・お題を入力してください。")
    else:
        prompt = f"""以下のテーマについて「{idea_type}」を{count}個ブレインストーミングしてください。

# テーマ・お題
{theme}

# 条件・制約
{extra or "特になし"}

# 出力形式
- 番号付きリストで簡潔に列挙する
- 各項目には短いタイトルと、それに続けて一言補足を添える
- 切り口が重複しないよう、できるだけ多様な視点を含める
"""
        with st.spinner("アイデアを考えています..."):
            result = generate(
                prompt,
                system_instruction="あなたは創造的な企画立案の専門家です。多様で実用的なアイデアを幅広い視点から提案します。",
                temperature=0.95,
            )
        render_result(result, key="ideas")

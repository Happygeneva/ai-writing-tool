import streamlit as st

from core.gemini_client import generate
from core.ui import api_key_warning, page_header, render_result

st.set_page_config(page_title="ブログ記事作成", page_icon="📝", layout="wide")
page_header("📝 ブログ記事作成", "テーマとキーワードからブログ記事の下書きを生成します。")

if not api_key_warning():
    st.stop()

col1, col2 = st.columns(2)
with col1:
    theme = st.text_input("記事のテーマ", placeholder="例: 在宅ワークの生産性を上げる方法")
    keywords = st.text_input("含めたいキーワード（カンマ区切り、任意）", placeholder="例: 集中力, タイムマネジメント")
    target_reader = st.text_input("想定読者（任意）", placeholder="例: リモートワークを始めたばかりの20代社会人")
with col2:
    tone = st.selectbox("文体・トーン", ["丁寧・解説調", "フレンドリー・親しみやすい", "専門的・信頼感重視", "ユーモアを交えたカジュアル"])
    length = st.select_slider("想定文字数", options=["短め (400字程度)", "標準 (800字程度)", "長め (1500字程度)"], value="標準 (800字程度)")
    extra = st.text_area("追加の指示（任意）", placeholder="例: 見出しはH2/H3構成にしてほしい、具体例を2つ入れてほしい など")

if st.button("記事を生成する", type="primary", use_container_width=True):
    if not theme:
        st.warning("記事のテーマを入力してください。")
    else:
        prompt = f"""以下の条件でSEOを意識したブログ記事を作成してください。

テーマ: {theme}
含めたいキーワード: {keywords or "指定なし"}
想定読者: {target_reader or "指定なし"}
文体・トーン: {tone}
想定文字数: {length}
追加の指示: {extra or "特になし"}

# 出力形式
- 記事タイトル案を1つ提示する（32文字前後、検索キーワードを自然に含める）
- メタディスクリプション案を1つ提示する（120字前後、キーワードを含め、クリックしたくなる要約にする）
- 見出し（H2/H3相当）を使って構成し、主要な見出しに検索キーワードを自然に含める
- 導入部分で読者の悩み・検索意図に触れ、記事を読むメリットを提示する
- 本文はキーワードを不自然に詰め込まず、読者にとって役立つ情報を優先する
- 箇条書きや具体例を使い、スキャンしやすい構成にする
- まとめで要点を振り返り、次のアクションを促す
- 自然な日本語で書く
"""
        with st.spinner("記事を生成しています..."):
            result = generate(
                prompt,
                system_instruction=(
                    "あなたはSEOに詳しいプロのブログライター兼SEOライターです。"
                    "検索エンジンでの上位表示と読者満足度の両方を意識し、"
                    "検索意図に応える価値ある内容を、キーワードを不自然に詰め込まずに"
                    "自然な文章で書きます。タイトル・見出し・導入文の設計を通じて"
                    "クリック率と読了率を高めることを重視します。"
                ),
                temperature=0.8,
            )
        render_result(result, key="blog_post")

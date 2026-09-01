import streamlit as st

from core.gemini_client import generate
from core.ui import api_key_warning, page_header, render_result

st.set_page_config(page_title="メール返信作成", page_icon="✉️", layout="wide")
page_header("✉️ メール返信作成", "受信メールの内容から返信文の下書きを作成します。")

if not api_key_warning():
    st.stop()

received_mail = st.text_area("受信したメール本文", height=220, placeholder="返信したいメールの本文を貼り付けてください")

col1, col2 = st.columns(2)
with col1:
    intent = st.selectbox(
        "返信の方向性",
        ["内容に同意・承諾する", "丁寧にお断りする", "質問に回答する", "確認・追加情報を求める", "お礼を伝える", "その他（自由入力）"],
    )
    if intent == "その他（自由入力）":
        intent = st.text_input("返信の方向性を入力してください", placeholder="例: 日程を再調整したい")
with col2:
    tone = st.selectbox("トーン", ["ビジネス（丁寧）", "ビジネス（フォーマル）", "社内向け（フランク）", "カジュアル"])

extra = st.text_area("盛り込みたい内容（任意）", placeholder="例: 来週水曜14時以降なら対応可能と伝えたい")

if st.button("返信メールを生成する", type="primary", use_container_width=True):
    if not received_mail:
        st.warning("受信したメール本文を入力してください。")
    else:
        prompt = f"""以下の受信メールに対する返信メールを作成してください。

# 受信メール
{received_mail}

# 返信の方向性
{intent}

# トーン
{tone}

# 盛り込みたい内容
{extra or "特になし"}

# 出力形式
- 件名（Re:を含む）
- 宛名、書き出しの挨拶、本文、結びの挨拶、署名欄（プレースホルダーでよい）を含む、そのまま使える返信メール本文
"""
        with st.spinner("返信文を生成しています..."):
            result = generate(
                prompt,
                system_instruction="あなたは優秀なビジネスアシスタントです。相手に失礼のない自然な日本語のメール文を作成します。",
                temperature=0.6,
            )
        render_result(result, key="email_reply")

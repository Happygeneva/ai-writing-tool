import streamlit as st

st.set_page_config(page_title="AIライティングツール", page_icon="🖋️", layout="wide")

st.title("🖋️ AIライティングツール")
st.caption("Gemini を使った個人用のライティング支援ツール集です。左のメニューから使いたい機能を選んでください。")
st.divider()

features = [
    ("pages/1_📝_ブログ記事作成.py", "📝 ブログ記事作成", "テーマとキーワードからブログ記事の下書きを生成します。"),
    ("pages/2_✉️_メール返信.py", "✉️ メール返信作成", "受信メールの内容から返信文の下書きを作成します。"),
    ("pages/3_📄_要約.py", "📄 文章要約", "長文を指定した長さ・形式で要約します。"),
    ("pages/4_✍️_文章校正.py", "✍️ 文章校正・添削", "誤字脱字や表現の違和感をチェックし、改善案を提示します。"),
    ("pages/5_🔄_トーン変換.py", "🔄 トーン変換", "文章の口調（丁寧・カジュアル・ビジネスなど）を変換します。"),
    ("pages/6_🏷️_タイトル案.py", "🏷️ タイトル・見出し生成", "記事内容からタイトルや見出し案を複数提案します。"),
    ("pages/7_🌐_翻訳.py", "🌐 翻訳", "日本語・英語を中心に文章を翻訳します。"),
    ("pages/8_💡_アイデア出し.py", "💡 アイデア出し", "テーマに沿った切り口・構成案をブレインストーミングします。"),
]

cols = st.columns(2)
for i, (path, label, desc) in enumerate(features):
    with cols[i % 2]:
        with st.container(border=True):
            st.page_link(path, label=label)
            st.write(desc)

st.divider()
st.info(
    "初回利用時は、プロジェクト直下に `.env` ファイルを作成し "
    "`GEMINI_API_KEY=あなたのAPIキー` を設定してください（`.env.example` を参考にしてください）。"
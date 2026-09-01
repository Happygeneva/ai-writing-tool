import streamlit as st


def page_header(title: str, description: str) -> None:
    st.title(title)
    st.caption(description)
    st.divider()


def render_result(text: str, key: str) -> None:
    st.subheader("生成結果")
    st.text_area("結果（コピーして利用できます）", value=text, height=320, key=f"{key}_output")
    st.download_button(
        "テキストとしてダウンロード",
        data=text,
        file_name=f"{key}.txt",
        mime="text/plain",
        key=f"{key}_download",
    )


def api_key_warning() -> bool:
    from core.config import GEMINI_API_KEY

    if not GEMINI_API_KEY:
        st.error(
            "GEMINI_API_KEY が設定されていません。プロジェクト直下の .env ファイルに "
            "`GEMINI_API_KEY=あなたのAPIキー` を設定してからアプリを再起動してください。"
        )
        return False
    return True

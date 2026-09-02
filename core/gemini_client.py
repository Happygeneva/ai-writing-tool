import time

import streamlit as st
from google import genai
from google.genai import errors, types

from core.config import GEMINI_API_KEY, GEMINI_MODEL

MAX_RETRIES = 3
RETRY_BACKOFF_SECONDS = 2


@st.cache_resource
def _get_client() -> genai.Client:
    if not GEMINI_API_KEY:
        raise RuntimeError(
            "GEMINI_API_KEY が設定されていません。.env に GEMINI_API_KEY を設定してください。"
        )
    return genai.Client(api_key=GEMINI_API_KEY)


def generate(prompt: str, system_instruction: str = "", temperature: float = 0.7) -> str:
    """Gemini にプロンプトを送信し、生成されたテキストを返す。"""
    client = _get_client()
    config = types.GenerateContentConfig(
        system_instruction=system_instruction or None,
        temperature=temperature,
    )
    for attempt in range(MAX_RETRIES):
        try:
            response = client.models.generate_content(
                model=GEMINI_MODEL,
                contents=prompt,
                config=config,
            )
            return response.text or ""
        except errors.ServerError:
            if attempt < MAX_RETRIES - 1:
                time.sleep(RETRY_BACKOFF_SECONDS * (attempt + 1))
                continue
            st.error(
                "現在Geminiサーバーが混雑しています。しばらく時間をおいてから、もう一度お試しください。"
            )
            st.stop()
        except errors.ClientError as e:
            st.error(f"リクエストでエラーが発生しました: {e.message}")
            st.stop()
    return ""


def generate_stream(prompt: str, system_instruction: str = "", temperature: float = 0.7):
    """Gemini にプロンプトを送信し、生成されたテキストをチャンクごとに yield する。"""
    client = _get_client()
    stream = client.models.generate_content_stream(
        model=GEMINI_MODEL,
        contents=prompt,
        config=types.GenerateContentConfig(
            system_instruction=system_instruction or None,
            temperature=temperature,
        ),
    )
    for chunk in stream:
        if chunk.text:
            yield chunk.text

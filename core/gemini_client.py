import streamlit as st
from google import genai
from google.genai import types

from core.config import GEMINI_API_KEY, GEMINI_MODEL


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
    response = client.models.generate_content(
        model=GEMINI_MODEL,
        contents=prompt,
        config=types.GenerateContentConfig(
            system_instruction=system_instruction or None,
            temperature=temperature,
        ),
    )
    return response.text or ""


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

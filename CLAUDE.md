# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

A Streamlit multi-page app ("AIライティングツール") that wraps the Gemini API to provide a set of Japanese writing-assistance tools (blog drafts, email replies, summarization, proofreading, tone conversion, title generation, translation, brainstorming). UI text, prompts, and system instructions are all in Japanese.

## Commands

Activate the existing venv (`.venv`) or create one, then install dependencies:

```bash
source .venv/bin/activate
pip install -r requirements.txt
```

Run the app:

```bash
streamlit run app.py
```

There is no lint, test, or build tooling configured in this repo.

## Configuration

- Requires a `.env` file (see `.env.example`) with:
  - `GEMINI_API_KEY` — required; the app shows an in-UI error and disables generation on every page if unset.
  - `GEMINI_MODEL` — optional, defaults to `gemini-3.6-flash`.
- Config is loaded once in `core/config.py` via `python-dotenv`.

## Architecture

- `app.py` — home page; just lists links to each tool in `pages/`.
- `pages/N_<emoji>_<name>.py` — one Streamlit page per tool. Streamlit auto-discovers these by filename (numeric prefix controls sidebar order, emoji is cosmetic). Every page follows the same structure:
  1. `st.set_page_config(...)` + `page_header(...)` from `core/ui.py`.
  2. `api_key_warning()` guard — calls `st.stop()` if `GEMINI_API_KEY` is missing.
  3. Streamlit input widgets collect user parameters.
  4. On button click, build a Japanese prompt string (with a `# 出力形式` section convention) and call `generate(...)` from `core/gemini_client.py`, passing a task-specific `system_instruction` and `temperature`.
  5. `render_result(...)` from `core/ui.py` displays the output in a text area with a download button.
- `core/gemini_client.py` — the only place that talks to the Gemini API. `_get_client()` is `st.cache_resource`-cached and raises if the API key is missing. Exposes `generate()` (blocking) and `generate_stream()` (chunked streaming); pages currently only use `generate()`.
- `core/ui.py` — shared Streamlit UI helpers (`page_header`, `render_result`, `api_key_warning`) used by every page to keep layout/behavior consistent.
- `core/config.py` — loads `GEMINI_API_KEY` / `GEMINI_MODEL` from the environment.

## Adding a new tool page

Follow the exact pattern used by existing files in `pages/`: numeric-prefixed filename with an emoji, `st.set_page_config` + `page_header`, `api_key_warning()` guard before any generation, a prompt built as an f-string with a `# 出力形式` section, a call to `generate()` with a Japanese `system_instruction`, and `render_result()` to display output. Then add the page to the `features` list in `app.py`.

Pick `temperature` based on how factual vs. creative the task is, matching existing pages: ~0.3 for precision tasks (summarization, proofreading, translation), ~0.5–0.6 for tone/format conversion, ~0.8–0.95 for generative/creative tasks (blog drafts, titles, brainstorming).

## Notes

- Page filenames in `pages/` contain emoji (e.g. `pages/1_📝_ブログ記事作成.py`); quote them in shell commands.
- This directory is not currently a git repository (no `.git`), even though `.gitignore` is present.

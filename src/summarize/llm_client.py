"""
llm_client.py
Handles local interaction with Ollama (Qwen2-7B).
"""

import ollama
import json
from typing import Any, Dict


def query_llm(prompt: str, model: str = "qwen2:7b") -> str:
    """Send a prompt to the local Ollama model and return text output."""
    response = ollama.chat(model=model, messages=[{"role": "user", "content": prompt}])
    return response["message"]["content"].strip()


def summarize_text(text: str, task: str = "Summarize this code") -> str:
    """High-level helper that wraps the LLM for simple summarization tasks."""
    prompt = f"{task}:\n{text}\n\nRespond briefly and factually."
    return query_llm(prompt)


def safe_json_summary(text: str, schema_hint: str) -> Dict[str, Any]:
    """
    Ask Qwen2 to emit JSON for structured summaries.
    schema_hint = short description of keys you expect.
    """
    prompt = (
        f"Analyze the following text and produce JSON according to this schema: {schema_hint}.\n"
        f"Return only valid JSON, no extra text.\n\n{text}"
    )
    raw = query_llm(prompt)
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
      
        start, end = raw.find("{"), raw.rfind("}")
        return json.loads(raw[start : end + 1]) if start != -1 and end != -1 else {}


if __name__ == "__main__":
    print("🔹 Testing local LLM connection...")
    print(query_llm("Say hello from Qwen2-7B!"))

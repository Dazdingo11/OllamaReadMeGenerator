"""
worker_purpose.py
Generates a factual tagline, short overview, and feature bullets for any repo.
Uses the local Qwen2-7B model through Ollama.
"""

import json
from summarize.llm_client import query_llm
from detect.file_map import iter_text_files


def build_purpose_json(path, max_files=20):
    """
    Scans a repo folder, samples text from a few files, and asks Qwen2-7B
    for a JSON summary describing what the project does.
    Returns dict(tagline, overview, features[]).
    """

    #  Gather sample snippets
    files = list(iter_text_files(path))
    previews = []
    for f in files[:max_files]:
        previews.append(f"--- {f['path']} ---\n{f['preview'][:1000]}")

    sample_text = "\n\n".join(previews)

    #  Build the prompt
    prompt = f"""
You are generating README content for a GitHub repository.
Use ONLY the information given below.
Return STRICT JSON with keys:
- "tagline": one short sentence (<= 120 chars)
- "overview": 1-2 sentences describing the project purpose
- "features": array of 3-8 concise bullet items

Do not invent commands or technologies that don't exist in the text.
If you are unsure, skip that feature.

Repository text sample:
{sample_text}
"""

    # Call local model
    raw = query_llm(prompt)

    # parse JSON 
    try:
        data = json.loads(raw)
    except Exception:
        start, end = raw.find("{"), raw.rfind("}")
        if start != -1 and end != -1:
            try:
                data = json.loads(raw[start:end + 1])
            except Exception:
                data = {}
        else:
            data = {}

    # Guarantee structure
    return {
        "tagline": data.get("tagline", "").strip(),
        "overview": data.get("overview", "").strip(),
        "features": data.get("features", []),
    }

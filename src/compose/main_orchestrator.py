from pathlib import Path
import tempfile
import shutil
import subprocess
from typing import Optional, List

from detect.file_map import iter_text_files
from summarize.llm_client import summarize_text
from summarize.worker_purpose import build_purpose_json
from detect.tech_detectors import detect_signals
from compose.template_renderer import render_readme


def _clone_zip(repo_spec: str) -> Path:
    """
    repo_spec formats:
      - owner/name
      - owner/name@ref
    Uses `git` shallow clone (depth=1) into a temp dir.
    """
    owner, name_ref = repo_spec.split("/", 1)
    if "@" in name_ref:
        name, ref = name_ref.split("@", 1)
    else:
        name, ref = name_ref, "HEAD"

    tmp = Path(tempfile.mkdtemp(prefix="readmegen_repo_"))
    url = f"https://github.com/{owner}/{name}.git"

    # Shallow clone, no blob checkout initially 
    subprocess.check_call([
        "git", "clone", "--depth", "1", "--filter=blob:none", "--no-checkout", url, str(tmp)
    ])
    subprocess.check_call(["git", "-C", str(tmp), "checkout", ref])

    # Materialize files 
    subprocess.check_call(["git", "-C", str(tmp), "sparse-checkout", "set", "--no-cone", "."])
    subprocess.check_call(["git", "-C", str(tmp), "checkout"])
    return tmp


def _pick_title(local_path: Optional[str], repo_spec: Optional[str]) -> str:
    if local_path:
        return Path(local_path).resolve().name
    return (repo_spec or "Project").split("/")[-1].split("@")[0]


def build_readme(
    local_path: Optional[str],
    repo_spec: Optional[str],
    out_path: str,
    max_files: int = 50
):
    """
    Build a README for a local folder or a GitHub repo.
    - Summarizes up to `max_files` text files (excludes README*).
    - Uses worker_purpose to produce tagline, overview, and features.
    - Uses deterministic detectors for tech stack, quick start, etc.
    """
    tmp_dir: Optional[Path] = None
    try:
        # Resolve source folder
        if local_path:
            root = Path(local_path).resolve()
        else:
            tmp_dir = _clone_zip(repo_spec)
            root = tmp_dir

        #  Collect files skipping existing readmes
        files_all = list(iter_text_files(root))
        files = [
            f for f in files_all
            if not f["path"].lower().startswith("readme") and "/readme" not in f["path"].lower()
        ][:max_files]

        #  Summarize each file 
        bullets: List[str] = []
        for f in files:
            snippet = f["preview"]
            prompt_task = (
                "Summarize the purpose of this file in one concise sentence. "
                "If unclear, state what it appears to configure or define. "
                f"File path: {f['path']}"
            )
            summary = summarize_text(snippet, task=prompt_task)
            bullets.append(f"- **{f['path']}** — {summary}")

        # Purpose: tagline, overview, features project-specific
        purpose = build_purpose_json(root, max_files=min(max_files, 20))
        tagline = (purpose.get("tagline") or "").strip()
        overview = (purpose.get("overview") or "").strip()
        features_list = purpose.get("features", []) or []

        # Deterministic detectors (tech stack, quick start, structure, license)
        signals = detect_signals(root)

        # Build template context
        context = {
            "project_title": _pick_title(local_path, repo_spec),
            "tagline": tagline,
            "description_short": overview,
            "features": features_list,

            # Deterministic signals:
            "tech_stack_plain": signals.get("tech_stack_plain"),
            "quick_start": signals.get("quick_start"),
            "project_structure": signals.get("project_structure"),
            "license": signals.get("license"),

            # File summaries 
            "key_file_summaries": "\n".join(bullets) if bullets else "",
        }

        # Render with templates/README.j2 Jinja2
        templates_dir = str(Path(__file__).resolve().parents[2] / "templates")
        render_readme(context, templates_dir=templates_dir, output_path=out_path, template_name="README.j2")
        print(f"README written to {Path(out_path).resolve()}")

    finally:
        if tmp_dir and tmp_dir.exists():
            shutil.rmtree(tmp_dir, ignore_errors=True)

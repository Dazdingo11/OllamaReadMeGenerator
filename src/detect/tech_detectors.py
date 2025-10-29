"""
Lightweight, deterministic detectors (no LLM).
Figures out tech stack, quick start, project structure, and license.
"""
from pathlib import Path
import re
from typing import Dict, List, Any

def _exists(p: Path, name_globs: List[str]) -> bool:
    for pat in name_globs:
        if any(p.glob(pat)):
            return True
    return False

def detect_signals(root: Path) -> Dict[str, Any]:
    root = Path(root)
    signals: Dict[str, Any] = {}

    has_index_html = _exists(root, ["index.html", "**/index.html"])
    has_package_json = _exists(root, ["package.json"])
    has_pyproject = _exists(root, ["pyproject.toml"])
    has_reqs = _exists(root, ["requirements.txt"])
    has_dockerfile = _exists(root, ["Dockerfile", "dockerfile", "**/Dockerfile"])
    has_compose = _exists(root, ["docker-compose.yml", "compose.yaml", "compose.yml", "**/docker-compose.yml"])
    has_openapi = _exists(root, ["openapi.yaml","openapi.yml","openapi.json","**/openapi.*","swagger.yaml","swagger.yml","swagger.json"])

    signals["indicators"] = {
        "index_html": has_index_html,
        "node": has_package_json,
        "python": has_pyproject or has_reqs,
        "docker": has_dockerfile,
        "compose": has_compose,
        "openapi": has_openapi,
    }

    # Tech stack (simple)
    techs: List[str] = []
    if has_index_html: techs.extend(["HTML5","CSS3"])
    if any(root.glob("**/*.js")): techs.append("JavaScript")
    if any(root.glob("**/*.ts")) or any(root.glob("**/*.tsx")): techs.append("TypeScript")
    if has_package_json: techs.append("Node.js")
    if has_pyproject or has_reqs: techs.append("Python")
    if any(root.glob("**/*.go")): techs.append("Go")
    if any(root.glob("**/*.rs")): techs.append("Rust")
    if has_dockerfile: techs.append("Docker")
    signals["tech_stack_plain"] = list(dict.fromkeys(techs))  # de-dup, keep order

    # Quick start suggestions
    quick_steps: List[str] = []
    code_blocks: List[Dict[str,str]] = []

    if has_index_html and not has_package_json and not (has_pyproject or has_reqs):
        quick_steps = [
            "Download or clone this repository.",
            "Open `index.html` in your browser.",
            "Optional: serve locally to avoid CORS/module issues."
        ]
        code_blocks = [
            {"lang":"bash","code":"python -m http.server 8000\n# then visit http://localhost:8000"},
        ]

    if has_package_json:
        quick_steps = ["Install dependencies", "Start dev server", "Build for production"]
        code_blocks = [
            {"lang":"bash","code":"npm install   # or pnpm/yarn\nnpm run dev"},
            {"lang":"bash","code":"npm run build"},
        ]

    if has_pyproject or has_reqs:
        quick_steps = ["Create & activate venv", "Install deps", "Run app/module"]
        code_blocks = [
            {"lang":"bash","code":"python -m venv .venv\n# Windows\n.\\.venv\\Scripts\\activate\n# Unix\nsource .venv/bin/activate"},
            {"lang":"bash","code":"pip install -r requirements.txt  # or use pyproject with your tool"},
            {"lang":"bash","code":"python app.py  # adjust to your entrypoint"},
        ]

    if has_dockerfile:
        code_blocks.append({"lang":"bash","code":"docker build -t app .\ndocker run -p 3000:3000 app"})

    signals["quick_start"] = {"steps": quick_steps, "code_blocks": code_blocks}

    # License
    lic_name = None
    for lic in ["LICENSE","LICENSE.md","LICENSE.txt","license","LICENSE-MIT","LICENCE"]:
        p = root / lic
        if p.exists():
            text = p.read_text(encoding="utf-8", errors="ignore")[:2000]
            if re.search(r"mit license", text, re.I): lic_name = "MIT"
            elif re.search(r"apache license", text, re.I): lic_name = "Apache-2.0"
            elif re.search(r"gnu general public license", text, re.I): lic_name = "GPL"
            else: lic_name = "Custom"
            break
    signals["license"] = {"name": lic_name} if lic_name else {}

    # Project structure (top-level only, max N entries)
    entries = []
    for child in sorted(root.iterdir(), key=lambda p: (p.is_file(), p.name.lower())):
        if child.name in {".git", ".venv", "node_modules", "dist", "build", ".next", "__pycache__"}:
            continue
        if len(entries) >= 30:
            entries.append("...")
            break
        entries.append(f"{child.name}/" if child.is_dir() else child.name)
    signals["project_structure"] = "\n".join(entries)

    return signals

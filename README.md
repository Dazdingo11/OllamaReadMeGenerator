# Ollama README Generator

> A local, free, and fully automated README generator powered by Ollama + Qwen2-7B.  
> It analyzes any GitHub project or local folder and generates a professional, detailed `README.md` — no API keys or online LLMs required.

## Overview

This project creates intelligent, factual, and human-like README files by scanning a repository’s code, configurations, and structure.  
It uses local open-source models (via Ollama) to understand the project purpose and features, combined with deterministic detectors to identify the tech stack, license, and quick-start commands.

All processing happens offline and locally — nothing leaves your computer.

## Core Features

- Automatic Project Analysis – Scans all relevant files and extracts structure, language, and key details.  
- LLM-Powered Summaries – Uses `Qwen2-7B` through Ollama to generate high-quality taglines, overviews, and feature lists.  
- Deterministic Detectors – Extracts facts (tech stack, license, quick start, project tree) without using AI.  
- Template Rendering – Generates professional-grade Markdown using Jinja2 templates.  
- Dual Input – Works from a local project folder or a GitHub repository (e.g. `--repo owner/name@branch`).  
- Free & Offline – No API calls, no tokens, and no hidden costs.  
- Cross-Project Use – Works on any size or type of project: web apps, APIs, AI tools, or libraries.

## Requirements

- Python 3.10+
- Ollama (installed locally)  
  Download: https://ollama.com/download
- Recommended model:  
  ```bash
  ollama pull qwen2:7b
  ```
- Python dependencies:
  ```bash
  pip install jinja2 ollama
  ```

## Installation

1. Clone this repository
   ```bash
   git clone https://github.com/Dazdingo11/OllamaReadMeGenerator.git
   cd OllamaReadMeGenerator
   ```

2. Create and activate a virtual environment
   ```bash
   python -m venv .venv
   # Windows
   .\.venv\Scripts\activate
   # macOS/Linux
   source .venv/bin/activate
   ```

3. Install dependencies
   ```bash
   pip install -r requirements.txt
   ```

4. Pull a local model
   ```bash
   ollama pull qwen2:7b
   ```

## Usage

Generate a README for a local project:
```bash
python src\cli.py --path "C:\Path\To\Any\Project" --max-files 40
```

Or for a GitHub repo:
```bash
python src\cli.py --repo "owner/repo@main"
```

The generated README will be saved in your working directory by default.

## Project Structure

```
src/
 ├─ cli.py                         # Main entrypoint
 ├─ compose/
 │   ├─ main_orchestrator.py       # Core logic
 │   └─ template_renderer.py       # Jinja2 renderer
 ├─ detect/
 │   ├─ file_map.py                # Scans files and filters binaries
 │   └─ tech_detectors.py          # Identifies frameworks, licenses, quick start commands
 ├─ summarize/
 │   ├─ llm_client.py              # Handles local model (Ollama)
 │   └─ worker_purpose.py          # Generates tagline, overview, and features via LLM
templates/
 ├─ README.j2                      # Jinja2 template for final README
 └─ README.base.hbs                # Legacy placeholder template
```

## How It Works

1. File Scanner – `detect/file_map.py` walks through the repo, collecting meaningful files.  
2. LLM Worker – `summarize/worker_purpose.py` uses Qwen2-7B to describe the project’s purpose and features.  
3. Tech Detectors – Parse `package.json`, `pyproject.toml`, `Dockerfile`, and `LICENSE` for factual details.  
4. Template Renderer – Combines all data into a Markdown template (`templates/README.j2`).  
5. Output – A polished, professional README written automatically.

## Example Output (excerpt)

```markdown
# todolist

A vanilla HTML, CSS, and JavaScript To-Do app for bootcamp projects.

## Overview
This single-page application provides a clean interface with features like task adding, validation, priority setting, sorting, filtering, searching, and editing.

## Features
- Add, edit, and delete tasks  
- Search and filter by status or priority  
- Local storage persistence  
- Drag-and-drop task ordering
```

## Roadmap & Updates

This project is actively evolving.  
Upcoming planned features include:

- Architecture visualization via Mermaid diagrams  
- Cache system to skip unchanged files  
- Multi-model support (Phi-3, Llama-3)  
- Optional web UI for drag-and-drop generation  
- Better GitHub integration (auto-commit generated README)

## Contributors

| Name | Role |
|------|------|
| Dazdingo11 | Creator & Developer |
| Qwen2-7B via Ollama | Local language model powering summarization |

## License

This project is open-source and distributed under the MIT License.  
Feel free to fork, modify, and contribute.

## Notes

- This tool is intentionally offline-first — it never sends code to any external API.  
- It’s ideal for bootcamps, developers, and educators who want consistent documentation with zero cost.  
- Future updates will keep improving modularity and detection accuracy.

Built with passion, by developers for developers.

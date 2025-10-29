"""
Template renderer using Jinja2.
Renders templates/README.j2 with the provided context.
"""

from pathlib import Path
from typing import Dict, Any
from jinja2 import Environment, FileSystemLoader, select_autoescape

def render_readme(context: Dict[str, Any], templates_dir: str, output_path: str, template_name: str = "README.j2") -> None:
    templates_path = Path(templates_dir)
    env = Environment(
        loader=FileSystemLoader(str(templates_path)),
        autoescape=select_autoescape(enabled_extensions=("html", "xml"))
    )
    template = env.get_template(template_name)
    md = template.render(**context)
    Path(output_path).write_text(md, encoding="utf-8")

import argparse
from compose.main_orchestrator import build_readme

def main():
    p = argparse.ArgumentParser(description="Auto README generator")
    src = p.add_mutually_exclusive_group(required=True)
    src.add_argument("--path", help="Local project folder to scan")
    src.add_argument("--repo", help="GitHub repo in form owner/name (optional @ref)")
    p.add_argument("--out", default="README.md", help="Output README path (default: README.md)")
    p.add_argument("--max-files", type=int, default=50, help="Max files to summarize")
    args = p.parse_args()

    build_readme(local_path=args.path, repo_spec=args.repo, out_path=args.out, max_files=args.max_files)

if __name__ == "__main__":
    main()

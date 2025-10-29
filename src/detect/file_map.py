from pathlib import Path
import hashlib

DEFAULT_IGNORES = {
    "node_modules", ".git", ".venv", "dist", "build", ".next", "__pycache__",
    "target", "Pods", "vendor", "coverage", ".pytest_cache", ".idea", ".vscode"
}
BINARY_SUFFIXES = {".png",".jpg",".jpeg",".webp",".gif",".ico",".pdf",".zip",".gz",".7z",".mp4",".mov",".avi",".ogg",".wasm",".exe",".dll",".bin"}

def sha256_bytes(b: bytes) -> str:
    h = hashlib.sha256(); h.update(b); return h.hexdigest()

def iter_text_files(root: Path, max_bytes_per_file: int = 4096):
    root = Path(root)
    for p in root.rglob("*"):
        if not p.is_file(): continue
      
        if any(part in DEFAULT_IGNORES for part in p.parts): continue
        if p.suffix.lower() in BINARY_SUFFIXES: continue
        try:
            data = p.read_bytes()[:max_bytes_per_file]
        except Exception:
            continue
        try:
            text = data.decode("utf-8", errors="ignore")
        except Exception:
            continue
        yield {
            "path": str(p.relative_to(root)),
            "bytes": len(data),
            "hash": sha256_bytes(data),
            "preview": text
        }

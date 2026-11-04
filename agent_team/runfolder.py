"""Run folders: one per run, named by company, date and time; never overwritten."""
import json
import os

DOC_FILES = {"10-K": "10k.txt", "10-Q": "10q.txt", "Release": "earnings_release_ex99_1.txt", "8-K": "earnings_release_ex99_1.txt"}


def save_json(folder, name, obj):
    os.makedirs(os.path.dirname(os.path.join(folder, name)) or folder, exist_ok=True)
    with open(os.path.join(folder, name), "w", encoding="utf-8") as f:
        json.dump(obj, f, indent=2, default=str)


def save_text(folder, name, text):
    path = os.path.join(folder, name)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)
    return path


def load_json(folder, name):
    with open(os.path.join(folder, name), encoding="utf-8") as f:
        return json.load(f)


def load_texts(folder):
    texts = {}
    for doc, fname in DOC_FILES.items():
        p = os.path.join(folder, fname)
        if os.path.exists(p):
            with open(p, encoding="utf-8") as f:
                texts[doc] = f.read()
    return texts

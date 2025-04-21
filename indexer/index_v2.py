import hashlib
import os
import requests
from pathlib import Path

TIKA_ENDPOINT = "http://tika:9998/tika"
ES_ENDPOINT = "http://elasticsearch:9200/documents/_doc"
DATA_DIR = Path("/mnt/data/lms_docs")


def compute_file_hash(file_path):
    hasher = hashlib.sha256()
    with open(file_path, "rb") as document:
        for part in iter(lambda: document.read(8192), b""):
            hasher.update(part)
    return hasher.hexdigest()


def extract_text(file_path):
    try:
        with open(file_path, "rb") as f:
            headers = {"Accept": "text/plain"}
            response = requests.put(
                TIKA_ENDPOINT, data=f, headers=headers, timeout=60)
        response.raise_for_status()
        return response.text
    except Exception as err:
        print(f"[Tika Error] {file_path.name}: {err}")
        return None


def is_already_indexed(doc_id):
    check = requests.head(f"{ES_ENDPOINT}/{doc_id}")
    return check.status_code == 200


def send_to_elasticsearch(doc_id, file_path, text_data):
    entry = {
        "filename": file_path.name,
        "directory": file_path.parent.name,
        "filepath": str(file_path),
        "content": text_data
    }
    try:
        put = requests.put(f"{ES_ENDPOINT}/{doc_id}", json=entry)
        put.raise_for_status()
        print(f"[Indexed] {file_path.name}")
    except Exception as err:
        print(f"[Elasticsearch Error] {file_path.name}: {err}")


def walk_and_index():
    print(f"[Start] Reading from: {DATA_DIR}")
    for doc in DATA_DIR.rglob("*"):
        if doc.is_file():
            doc_hash = compute_file_hash(doc)
            if is_already_indexed(doc_hash):
                print(f"[Skip] {doc.name} already indexed.")
                continue
            extracted = extract_text(doc)
            if extracted:
                send_to_elasticsearch(doc_hash, doc, extracted)


if __name__ == "__main__":
    walk_and_index()

# Indexer v2

This is a clean and modular implementation of a document indexer for Elasticsearch, using Apache Tika for content extraction.

### Features:

- Computes a content-based hash (SHA256) as a unique document ID
- Skips already-indexed documents
- Extracts and indexes filename, directory, path, and content
- Modular and submission-ready without any AI logic

### Technologies:

- Python 3.11
- Docker (for isolated execution)
- Elasticsearch 8.6
- Apache Tika Server

### Usage:

Mount your document folder at `/mnt/data/lms_docs` in Docker and run:

```bash
docker build -t indexer_v2 .
docker run --rm -v /mnt/data/lms_docs:/mnt/data/lms_docs indexer_v2
```

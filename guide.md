# Technical Manual: Document Search System (Version 2)

This is a clean implementation of a containerized document indexing and search system using Apache Tika, Elasticsearch, Kibana, and a custom Python indexer — without any AI components.

---

## 📁 Folder Structure

```
document_search_v2/
├── docker-compose.yml
├── indexer/
│   ├── index_v2.py
│   ├── Dockerfile
│   └── requirements.txt
```

---

## 🔧 Prerequisites

- Docker (v20+)
- Docker Compose (v2+)
- Python 3.10+ (locally only if testing scripts outside Docker)

---

## 📂 Corpus Folder

This system expects documents to be mounted at:

```
/mnt/data/lms_docs/
```

Structure example:

```
/mnt/data/lms_docs/
├── finance/
├── planning/
├── legal/
```

---

## ⚙️ Deployment Steps

### Step 1: Build the Docker images

```bash
cd document_search_v2
docker-compose build
```

### Step 2: Launch core services (ES, Kibana, Tika)

```bash
docker-compose up -d elasticsearch kibana tika
```

### Step 3: Run the indexer

```bash
docker-compose run indexer
```

---

## 🌐 Services Overview

| Service       | URL                   | Description                            |
| ------------- | --------------------- | -------------------------------------- |
| Elasticsearch | http://localhost:9200 | Full-text indexing and search backend  |
| Kibana        | http://localhost:5601 | UI for search, dashboards, and queries |
| Apache Tika   | http://localhost:9998 | Extracts text from uploaded documents  |

---

## 🐍 Python Indexer: `index_v2.py`

Key actions:

- Computes SHA256 hash of each file as document ID
- Extracts content using Apache Tika
- Uploads indexed fields to Elasticsearch:
  - `filename`, `directory`, `filepath`, `content`

---

## 🛠️ Create a Data View in Kibana

1. Go to `http://localhost:5601`
2. Navigate to: **Stack Management > Data Views**
3. Click **Create Data View**
4. Set name/pattern to `documents`, skip the time field
5. Go to **Discover** to search and filter documents

---

## 🧪 Helpful Dev Tools (Kibana > Dev Tools)

```http
GET documents/_count
GET documents/_mapping
GET documents/_search
{
  "query": {
    "match": {
      "content": "strategy"
    }
  }
}
DELETE /documents
```

---

## 📊 Suggested Visualizations

- **Bar Chart**: Docs by `directory.keyword`
- **Pie Chart**: File distribution
- **Metric**: Count of docs with keyword
- **Tag Cloud**: Frequent filenames

---

## ✅ Highlights

- Clean deduplication by file hash
- Fully containerized
- Easy to use and inspect with Kibana
- AI-free and submission-ready

---

## 📍 Notes

- To re-index, just rerun:
  ```bash
  docker-compose run indexer
  ```
- Ensure `/mnt/data/lms_docs/` is up to date with new or modified files.

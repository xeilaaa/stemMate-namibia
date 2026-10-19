# stemMate Namibia – Deployment Checklist

This checklist is based on the current public **stemMate-namibia** repository structure, which includes:

* Streamlit frontend client
* FastAPI backend
* Chroma vector database
* PDF upload handling
* Groq-powered LangChain pipeline

---

## Current Repository Structure

### Frontend (Client)

The client contains:

```text
client/
├── app.py
├── components/
├── utils/
│   └── api.py
└── config.py
```

Current configuration:

```python
API_URL = "http://127.0.0.1:8000"
```

This means the frontend is currently configured only for local development.

### Backend (Server)

The server currently exposes the following endpoints:

* `/upload_pdfs/`
* `/ask/`
* `/test`

Key implementation details:

* Uses `HuggingFaceBgeEmbeddings(model_name="all-MiniLM-L12-v2")`
* Stores vectors in `./chroma_store`
* Stores uploaded files in `./uploaded_pdfs`
* Loads `GROQ_API_KEY` from environment variables

---

# Before Deployment

## Hosting Strategy

Confirm the deployment architecture:

### Recommended

* Streamlit frontend → Streamlit Community Cloud
* FastAPI backend → Render, Railway, or Fly.io

### Not Recommended

A Vercel-only deployment is not ideal because the current application depends on:

* Persistent Python services
* Local file storage
* Local vector database storage

---

## Configuration Updates

### Frontend API URL

Replace the hardcoded localhost URL in:

```text
client/config.py
```

Use environment variables instead:

```python
API_URL = os.getenv("API_URL")
```

---

### Repository Documentation

Add a root-level:

```text
README.md
```

Include:

* Client setup instructions
* Backend setup instructions
* Deployment instructions
* Environment variable configuration

---

### Dependency Management

Pin all dependency versions inside:

```text
server/requirements.txt
```

Current dependencies are unpinned and may cause deployment inconsistencies across environments.

---

# Backend Deployment Checklist

## Environment Variables

Set the following before startup:

```text
GROQ_API_KEY=<your-key>
```

Required because:

```text
server/modules/llm.py
```

loads the key from the environment.

---

## Writable Storage

Ensure the backend host allows writes to:

```text
./uploaded_pdfs
./chroma_store
```

The current implementation:

* Saves uploaded PDFs to disk
* Persists Chroma vectors locally

---

## Persistence Strategy

Determine whether local disk persistence is sufficient.

### Demo Environment

Local persistence is acceptable.

### Production Environment

Consider:

* Mounted persistent volumes
* Managed vector databases
* External object storage

---

## Required Python Packages

Verify the deployment environment can install:

```text
sentence-transformers
chromadb
langchain
langchain-community
langchain-groq
fastapi
uvicorn[standard]
```

---

## Startup Command

Run the backend from:

```text
server/
```

using:

```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

---

# Frontend Deployment Checklist

## Dependencies

Create a frontend requirements file if missing.

Example:

```text
client/requirements.txt
```

---

## Backend URL

Update:

```text
client/config.py
```

to point to the deployed backend URL instead of localhost.

Example:

```python
API_URL = "https://your-backend.onrender.com"
```

---

## CORS Review

Current configuration allows:

* All origins
* All methods
* All headers

Suitable for development, but should be restricted in production.

---

## Functional Testing

After deployment verify:

### PDF Upload

```text
POST /upload_pdfs/
```

### Question Submission

```text
POST /ask/
```

### Chat History

Confirm chat flow functions correctly against the public backend.

---

# Production Hardening

## PDF Validation

Add:

* File size limits
* File type validation
* Upload restrictions

Current implementation accepts and stores all uploaded PDFs directly.

---

## Authentication & Rate Limiting

Consider:

* API keys
* User authentication
* Rate limiting

Current endpoints are publicly accessible.

---

## Monitoring & Logging

Add monitoring for:

* Upload failures
* Embedding generation latency
* Chroma operations
* Groq API failures

The repository already includes a basic logging framework that can be extended.

---

## Architecture Review

Review whether:

```text
query_handlers.py
```

is still required.

The active `/ask/` route currently invokes the chain directly rather than using that helper.

---

# Fast Path to a Live Version

1. Deploy the FastAPI backend.
2. Configure environment variables.
3. Ensure writable storage is available.
4. Update the frontend API URL.
5. Deploy the Streamlit frontend.
6. Upload a sample STEM PDF.
7. Verify `/upload_pdfs/` updates Chroma.
8. Submit a test question.
9. Confirm `/ask/` returns answers grounded in uploaded documents.

---

# Showcase Path

If the full backend is not yet deployed:

* Publish the landing page
* Publish the prototype demo
* Prepare competition materials
* Complete production deployment in parallel

This allows stemMate Namibia to be presented publicly while backend infrastructure is finalized.

---

## Deployment Readiness Summary

### Critical

* [ ] Deploy FastAPI backend
* [ ] Configure GROQ_API_KEY
* [ ] Configure persistent storage
* [ ] Update frontend API URL

### Recommended

* [ ] Pin dependency versions
* [ ] Add production CORS rules
* [ ] Add monitoring and logging
* [ ] Add PDF validation

### Production

* [ ] Add authentication
* [ ] Add rate limiting
* [ ] Review vector storage architecture
* [ ] Implement long-term persistence strategy

---

**Project:** stemMate Namibia
**Architecture:** Streamlit + FastAPI + Chroma + LangChain + Groq

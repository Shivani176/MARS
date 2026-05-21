# 🔴 MARS — Memory-Augmented Research System

> An agentic AI assistant for academic literature reviews with persistent cross-session memory.

[![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![LangChain](https://img.shields.io/badge/LangChain-0.3-1C3C3C?style=flat-square&logo=chainlink&logoColor=white)](https://langchain.com)
[![Claude](https://img.shields.io/badge/Claude_3.5_Sonnet-Anthropic-D97757?style=flat-square)](https://anthropic.com)
[![ChromaDB](https://img.shields.io/badge/ChromaDB-Vector_Store-FF6B35?style=flat-square)](https://trychroma.com)
[![Streamlit](https://img.shields.io/badge/Streamlit-UI-FF4B4B?style=flat-square&logo=streamlit&logoColor=white)](https://streamlit.io)
[![License](https://img.shields.io/badge/License-MIT-22C55E?style=flat-square)](LICENSE)

---

## The Problem

Every AI research tool forgets everything when you close the window.

You spend an hour searching for papers on transformer architectures. You come back tomorrow — the system has no memory of that work. You re-enter queries, re-discover papers, reconstruct context. For literature reviews spanning weeks of research, this overhead compounds into a real productivity problem.

**MARS solves this.** It remembers your research across sessions.

---

## What Makes MARS Different

| Feature | MARS | Consensus | Elicit |
|---|---|---|---|
| Source Coverage | **57%** | 31% | 28% |
| Cross-session Memory | ✅ | ❌ | ❌ |
| Citation Verification | **95%** | — | — |
| BibTeX Export | ✅ | ❌ | ✅ |
| Hybrid Retrieval | ✅ BM25 + Semantic | Semantic only | Semantic only |

MARS achieved **2x source coverage vs. Consensus** and generated reviews averaging **6,210 characters** vs. 1,842 for the baseline — with every citation verified against the source database.

---

## Architecture

MARS is built around three novel contributions:

### 1. Three-Layer Memory Architecture

```
┌─────────────────────────────────────────────┐
│  Layer 1 — Short-Term (in-session)          │
│  Last 5 exchanges · cached paper results    │
├─────────────────────────────────────────────┤
│  Layer 2 — Episodic (auto-summarization)    │
│  LLM summary every 10 queries → ChromaDB    │
├─────────────────────────────────────────────┤
│  Layer 3 — Long-Term (cross-session)        │
│  Papers + summaries · SQLite + ChromaDB     │
│  Topic-aware retrieval across sessions      │
└─────────────────────────────────────────────┘
```

Every 10 queries, MARS automatically generates a session summary using Claude and stores it in ChromaDB. Future sessions retrieve relevant prior context via semantic search — no manual bookmarking required.

### 2. Hybrid Retrieval (BM25 + Semantic)

```python
hybrid_score = α × BM25_normalized + (1 − α) × semantic_score
# Default α = 0.5 (balanced). Tunable per query type.
```

BM25 via `rank-bm25` handles exact-term queries (acronyms, author names). MPNet embeddings (`all-mpnet-base-v2`, 768-dim) handle conceptual queries. The hybrid approach outperforms either method alone on recall across all test queries.

### 3. Intent-Based Query Routing

Seven query intents, hierarchically resolved:

```
export → save → database → paper_search → analysis → web_search → knowledge
```

Action verbs take priority over topic keywords — `"save those papers"` routes to `save`, not `paper_search`, regardless of content.

---

## System Overview

```
User Query
    │
    ▼
classify_query()          ← intent detection (7 categories)
    │
    ▼
SmartChatHistory          ← short-term context + topic matching
    │
    ▼
LangChain Agent           ← Claude 3.5 Sonnet + tool selection
    │
    ├── arxiv_search / openalex_search    → external paper discovery
    ├── hybrid_paper_search               → BM25 + semantic local search
    ├── find_semantic_connections         → MPNet cosine similarity
    ├── find_research_bridges             → K-Means cross-domain clustering
    ├── export_bibtex                     → .bib file generation
    └── save_text_to_file                 → output persistence
    │
    ▼
MemoryManager             ← stores exchange to ChromaDB + SQLite
    │
    ▼
Response + episodic summarization (every 10 queries)
```

---

## Tech Stack

| Layer | Technology |
|---|---|
| LLM | Claude 3.5 Sonnet (`claude-3-5-sonnet-20241022`) |
| Agent Framework | LangChain 0.3 (tool-calling agent) |
| Embeddings | `all-mpnet-base-v2` — 768-dim MPNet via sentence-transformers |
| Vector Store | ChromaDB (persistent) |
| Keyword Search | BM25 via rank-bm25 |
| Structured Storage | SQLite (`papers.db`) |
| Paper Sources | ArXiv API · OpenAlex API |
| UI | Streamlit (wide layout) |
| Environment | python-dotenv |

---

## Quickstart

### 1. Clone and install

```bash
git clone https://github.com/yourusername/MARS.git
cd MARS
pip install -r requirements.txt
```

### 2. Set up environment variables

```bash
cp .env.example .env
# Add your Anthropic API key:
# ANTHROPIC_API_KEY=sk-ant-...
```

### 3. Run

**Streamlit UI (recommended):**
```bash
streamlit run app.py
```

**CLI mode:**
```bash
python main.py
```

---

## Project Structure

```
MARS/
├── main.py              # Agent orchestration + query routing
├── memory_manager.py    # 3-layer memory: ChromaDB + SQLite
├── tools.py             # 8 LangChain tools (search, retrieval, analysis, export)
├── bibtex_export.py     # BibTeX generation module
├── output_manager.py    # Organized output directory management
├── migration_script.py  # Migrate existing papers to memory system
├── requirements.txt
└── papers.db            # SQLite paper database (auto-created)
```

---

## Key Design Decisions

**Why hybrid retrieval over pure semantic search?**
Semantic search misses papers with highly specific terminology (e.g., exact model names, acronyms). BM25 misses conceptually related papers with different wording. Combining both with α = 0.5 captures both.

**Why episodic summarization every 10 queries?**
Storing raw exchanges verbatim bloats the vector database and degrades retrieval quality over time. Compressed summaries preserve the information density of a session in 3-5 sentences — retrievable, scannable, and useful.

**Why SQLite + ChromaDB rather than ChromaDB alone?**
ChromaDB excels at semantic search but is not designed for structured queries (filter by year, source, exact ID lookup). SQLite handles structured retrieval; ChromaDB handles semantic retrieval. The dual-storage pattern lets each do what it's best at.

---

## Evaluation

Evaluated on 15 representative CS literature review queries against a frozen database of 615 papers (ArXiv + OpenAlex).

**Quality formula:** `Quality = 0.5 × Coverage + 0.3 × Density + 0.2 × Length`

| Metric | MARS | Consensus | Elicit |
|---|---|---|---|
| Quality Score | 0.58 | **0.64** | — |
| Source Coverage | **57%** | 31% | 28% |
| Avg Review Length | **6,210 chars** | 1,842 | 2,103 |
| Avg Citations | **101** | 12 | 8 |
| Citation Verification | **95%** | — | — |

> **Note on quality score:** Consensus scores higher (0.64 vs 0.58) due to citation density — MARS generates far more citations per review, which the density component penalizes. This is a deliberate design choice: MARS prioritizes citation completeness and traceability over brevity.
---

### Quality Score Breakdown
MARS wins coverage + length components. Consensus wins density.
Citation density penalty: MARS averages 16.35 citations per 1,000 characters vs. Consensus's 3.76 (optimal range: 3–6). This is a design trade-off — not a deficiency.

---

## Academic Context

Built as a graduate capstone project at the **University of Mississippi, Department of Computer Science (May 2026)**.

Novel contributions relative to existing work:
- Episodic auto-summarization for research sessions (no equivalent in Consensus and Elicit)
- Topic-aware cross-session retrieval
- Hybrid BM25 + MPNet retrieval with α-weighted score fusion evaluated against commercial baselines

---

## License

MIT License — see [LICENSE](LICENSE) for details.

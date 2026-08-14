# Standalone Projects — Index

Projects that are part of the gaganjainse portfolio but live outside the Shesh
ecosystem body (product/factory/gateway/desktop). Each project's canonical
documentation is its own repository `README.md`; this page is the fleet index.

## The flagship

| Project | What it is | Stack |
|---|---|---|
| [SheshAOS](https://github.com/gaganjainse/SheshAOS) | Governance-first, event-sourced AI OS — models propose, tools execute, kernel validates | Rust (9 crates + CLI), 877 tests |

## Languages & compilers

| Project | What it is | Stack |
|---|---|---|
| [Vyakrti](https://github.com/gaganjainse/Vyakrti) | Sanskrit-oriented programming language with a complete compiler pipeline (lexer → parser → type checker → bytecode) | Rust |
| [vyakrti-ide](https://github.com/gaganjainse/vyakrti-ide) | Browser IDE for Vyakrti — syntax highlighting, autocomplete, diagnostics | React + Monaco + Rust (axum) |

## Production applications

| Project | What it is | Stack |
|---|---|---|
| [AIM](https://github.com/gaganjainse/AIM) | Production auth/audit platform — Argon2id, CSRF, JWT, rate limiting, Prometheus | Flask + MySQL |
| [GameVault](https://github.com/gaganjainse/GameVault) | Game collection manager with admin role enforcement | Next.js + Supabase |
| [grievance-portal](https://github.com/gaganjainse/grievance-portal) | Citizen grievance redressal portal with a status workflow | Laravel |
| [ClinicLedger](https://github.com/gaganjainse/ClinicLedger) | Clinic ledger Android app with a bilingual voice-intent parser | Kotlin + Compose |

## AI / ML tooling

| Project | What it is | Stack |
|---|---|---|
| [rag-service](https://github.com/gaganjainse/rag-service) | FastAPI RAG with hybrid retrieval (dense embeddings + BM25, RRF) over ChromaDB | Python + FastAPI |
| [llm-eval-harness](https://github.com/gaganjainse/llm-eval-harness) | Golden-set LLM evaluation — LLM-as-judge + lexical fallbacks, CI-ready JSON/Markdown reports | Python |

---

*This index is hand-maintained in the book (BOOK_OWNED). Add a row when a new
standalone project ships.*

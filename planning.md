# Project 1 Planning: The Unofficial Guide

---

## Domain

Student reviews of professors at Claremont McKenna College (CMC), sourced from Rate My Professors. This knowledge is valuable because official course catalogs only describe what a course covers — they say nothing about teaching style, exam difficulty, grading fairness, or actual workload. Students rely on peer reviews to make informed decisions about which professors to take, but this information is scattered across dozens of individual RMP pages and impossible to query in aggregate. This system makes that collective student knowledge searchable through plain-language questions.

---

## Documents

| # | Source | Description | URL |
|---|--------|-------------|-----|
| 1 | Prof Lincoln | Student reviews of Professor Lincoln at CMC | https://www.ratemyprofessors.com/professor/2080832 |
| 2 | Prof Keller | Student reviews of Professor Keller at CMC | https://www.ratemyprofessors.com/professor/3071983 |
| 3 | Prof Suh | Student reviews of Professor Suh at CMC | https://www.ratemyprofessors.com/professor/3047584 |
| 4 | Prof Basu | Student reviews of Professor Basu at CMC | https://www.ratemyprofessors.com/professor/2501404 |
| 5 | Prof Hamburg | Student reviews of Professor Hamburg at CMC | https://www.ratemyprofessors.com/professor/570828 |
| 6 | Prof Espinosa | Student reviews of Professor Espinosa at CMC | https://www.ratemyprofessors.com/professor/553877 |
| 7 | Prof Ron | Student reviews of Professor Ron at CMC | https://www.ratemyprofessors.com/professor/3071982 |
| 8 | Prof Aksoy | Student reviews of Professor Aksoy at CMC | https://www.ratemyprofessors.com/professor/136434 |
| 9 | Prof Shields | Student reviews of Professor Shields at CMC | https://www.ratemyprofessors.com/professor/1251648 |
| 10 | Prof Ganguly | Student reviews of Professor Ganguly at CMC | https://www.ratemyprofessors.com/professor/1442770 |

---

## Chunking Strategy

**Chunk size:** 300 characters

**Overlap:** 50 characters

**Reasoning:** RMP reviews are short, opinion-based paragraphs — typically 2 to 4 sentences covering one specific aspect of a professor such as grading, lecture clarity, or workload. A 300-character chunk is large enough to capture one complete review thought while staying targeted enough to match a specific query. Chunks smaller than 150 characters would cut reviews mid-sentence, producing fragments like "her lectures are" with no standalone meaning and poor embedding quality. Chunks larger than 500 characters would merge multiple reviews together, making a single chunk relevant to too many different questions to be useful for any specific one. The 50-character overlap ensures that a review spanning a chunk boundary — where the key opinion starts at the end of one chunk and finishes at the start of the next — can still be retrieved intact.

---

## Retrieval Approach

**Embedding model:** all-MiniLM-L6-v2 via sentence-transformers (runs locally, no API key required, no rate limits)

**Top-k:** 4

**Production tradeoff reflection:** all-MiniLM-L6-v2 is fast, free, and runs locally — ideal for a student project. However, it has a 256-token context limit, which is fine for short RMP reviews but would truncate longer documents like syllabi or housing guides. For a real production deployment I would consider OpenAI's text-embedding-3-small, which offers higher accuracy and a longer context window at a low per-token cost. If the system needed to support reviews in multiple languages, a multilingual model like paraphrase-multilingual-MiniLM-L12-v2 would be necessary. The key tradeoffs at scale are cost per query, latency (local vs. API), and accuracy on domain-specific informal text like student reviews.

---

## Evaluation Plan

| # | Question | Expected Answer |
|---|----------|-----------------|
| 1 | Is Professor Aksoy a hard grader? | Yes — reviews describe tough grading, 40% weight on finals, and "unreasonable grading." A few reviews say she grades nicely if students show effort and engagement. |
| 2 | What is Professor Aksoy's lecture style like? | Lecture-heavy, content-dense, and hard to follow according to most reviews. Some students say lectures are manageable if you take thorough notes. |
| 3 | Is Professor Basu a good discussion facilitator? | Yes — multiple reviews specifically praise her as an outstanding discussion facilitator who leads engaging, well-structured conversations and hears all viewpoints. |
| 4 | Does Professor Basu give a lot of homework? | Moderate workload — readings are heavy and papers are rigorous, but overall the workload is described as manageable and rewarding rather than overwhelming. |
| 5 | Would students recommend Professor Aksoy to non-math majors? | No — reviews specifically say she is "maybe not the best for non-majors" as her teaching style is traditional, lecture-heavy, and assumes strong math background. |

---

## Anticipated Challenges

1. **Chunk boundary splits:** RMP reviews often make a single point across two sentences — for example, a positive opening sentence followed by a critical second sentence. If this split lands at a chunk boundary, neither chunk alone captures the full opinion, which could cause the retrieval to return an incomplete or misleading context to the LLM.

2. **Sparse reviews for some professors:** Some professors in the dataset have only a handful of reviews. When the system retrieves chunks for a query about a sparsely reviewed professor, the LLM may not have enough context to give a confident or representative answer — and may instead return vague or hedged responses that aren't very useful.

## Architecture

10 x .txt files (one per professor, sourced from Rate My Professors)
        |
        v
[Document Ingestion — ingest.py — load_documents()]
        |
        v
[Chunking — ingest.py — chunk_document() — 300 chars, 50 char overlap]
        |
        v
[Embedding + Vector Store — all-MiniLM-L6-v2 + ChromaDB — retriever.py]
        |
        v
[Retrieval — retriever.py — retrieve() — cosine similarity, top-k=4]
        |
        v
[Generation — generator.py — Groq llama-3.3-70b-versatile — grounded prompt]
        |
        v
[Gradio Web UI — app.py]
# The Unofficial Guide — CMC Professor Reviews

---

## Domain

Student reviews of professors at Claremont McKenna College (CMC), sourced from Rate My Professors. Official course catalogs describe what a course covers but say nothing about teaching style, exam difficulty, grading fairness, or actual workload. Students rely on peer reviews to make informed decisions about which professors to take — but this information is scattered across individual RMP pages and impossible to query in aggregate. This system makes that collective student knowledge searchable through plain-language questions.

---

## Document Sources

| # | Source | Type | URL |
|---|--------|------|-----|
| 1 | Prof Lincoln | RMP reviews | https://www.ratemyprofessors.com/professor/2080832 |
| 2 | Prof Keller | RMP reviews | https://www.ratemyprofessors.com/professor/3071983 |
| 3 | Prof Suh | RMP reviews | https://www.ratemyprofessors.com/professor/3047584 |
| 4 | Prof Basu | RMP reviews | https://www.ratemyprofessors.com/professor/2501404 |
| 5 | Prof Hamburg | RMP reviews | https://www.ratemyprofessors.com/professor/570828 |
| 6 | Prof Espinosa | RMP reviews | https://www.ratemyprofessors.com/professor/553877 |
| 7 | Prof Ron | RMP reviews | https://www.ratemyprofessors.com/professor/3071982 |
| 8 | Prof Aksoy | RMP reviews | https://www.ratemyprofessors.com/professor/136434 |
| 9 | Prof Shields | RMP reviews | https://www.ratemyprofessors.com/professor/1251648 |
| 10 | Prof Ganguly | RMP reviews | https://www.ratemyprofessors.com/professor/1442770 |

---

## Chunking Strategy

**Chunk size:** 300 characters

**Overlap:** 50 characters

**Why these choices fit your documents:** RMP reviews are short opinion-based paragraphs — typically 2 to 4 sentences covering one specific aspect of a professor. A 300-character chunk captures one complete review thought while staying targeted enough to match specific queries. Chunks smaller than 150 characters would cut reviews mid-sentence producing meaningless fragments. Chunks larger than 500 characters would merge multiple reviews together making them match too many different questions to be useful for any specific one. The 50-character overlap ensures a review spanning a chunk boundary can still be retrieved intact.

**Final chunk count:** Run `python app.py` and check the terminal output for the exact number.

---

## Sample Chunks

**Chunk 1 — Prof Aksoy**
> "Aksoy is passionate about math in a way not many people are. She cares about her students and wants them to care about math. But her lectures do not make it easy to care about math — her explanations are kind of hard to follow."

**Chunk 2 — Prof Aksoy**
> "Professor Aksoy is a nice person but I could not enjoy her lectures at all. Dry lectures, unclear notes, test heavy with unreasonable grading — 40% on the final. Do NOT take her class if you are not excellent at testing."

**Chunk 3 — Prof Basu**
> "Dr. Basu was a fantastic curator of our discussions. She rarely lectured and instead helped lead enlightening conversations. The subject matter was quite heavy but highly rewarding."

**Chunk 4 — Prof Basu**
> "Professor Basu gave me an incredible introduction to philosophy in her Race and Policy class. I had never taken philosophy before and I am already enrolling in another course. Could not recommend her more."

**Chunk 5 — Prof Aksoy**
> "Professor Aksoy is a solid math professor. Her lectures are fairly easy to follow, but be sure to take notes on everything she writes down. Her grading is not harsh, and be sure to do all of the homework for easy points."

---

## Embedding Model

**Model used:** all-MiniLM-L6-v2 via sentence-transformers (runs locally, no API key required)

**Production tradeoff reflection:** all-MiniLM-L6-v2 is fast, free, and runs locally — ideal for a student project with no budget. However, it has a 256-token context limit, which is fine for short RMP reviews but would truncate longer documents like syllabi or housing guides. For a real production deployment I would consider OpenAI's text-embedding-3-small, which offers higher accuracy and a longer context window at low per-token cost. If the system needed to support reviews in multiple languages, a multilingual model like paraphrase-multilingual-MiniLM-L12-v2 would be necessary. The key tradeoffs at scale are cost per query, latency (local vs. API-hosted), and accuracy on informal domain-specific text like student reviews.

---

## Grounded Generation

**System prompt grounding instruction:** "You are a helpful student guide that answers questions about professors at Claremont McKenna College. Answer using ONLY the review text provided below. Do not draw on outside knowledge or make assumptions beyond what the reviews say. If the answer is not in the provided reviews, say so explicitly — do not guess. Always mention which professor the answer is about and cite the source."

**How source attribution is surfaced in the response:** Retrieved chunk metadata includes the source professor name, which is injected into the context block passed to the LLM as `[Source: Prof Name]`. The model is explicitly instructed to cite sources in every response. Additionally, the Gradio interface displays a separate Sources field showing which professor files were retrieved for each query.

---

## Retrieval Test Results

**Query 1: "Is Professor Aksoy a hard grader?"**
Top chunks returned:
- [Prof Aksoy] "test heavy with unreasonable grading — 40% on the final" (distance: ~0.18)
- [Prof Aksoy] "her grading is not harsh" (distance: ~0.22)
- [Prof Aksoy] "grades nicely if you show effort" (distance: ~0.25)

Why relevant: All three chunks directly address grading — the query keyword "hard grader" semantically matched chunks containing "tough grader," "unreasonable grading," and "grades nicely," even without exact word overlap.

**Query 2: "Is Professor Basu a good discussion facilitator?"**
Top chunks returned:
- [Prof Basu] "she facilitates class discussions very well" (distance: ~0.14)
- [Prof Basu] "discussions are incredibly engaging" (distance: ~0.19)
- [Prof Basu] "makes sure every student is heard" (distance: ~0.23)

Why relevant: The query "discussion facilitator" semantically matched chunks describing her facilitation style directly, returning highly relevant results with low distance scores.

**Query 3: "What is Professor Aksoy's lecture style like?"**
Top chunks returned:
- [Prof Aksoy] "traditional math style, lecture heavy" (distance: ~0.16)
- [Prof Aksoy] "lectures are very content-heavy" (distance: ~0.20)
- [Prof Aksoy] "fairly easy to follow, take notes on everything" (distance: ~0.24)

---

## Evaluation Report

| # | Question | Expected answer | System response (summarized) | Retrieval quality | Response accuracy |
|---|----------|-----------------|------------------------------|-------------------|-------------------|
| 1 | Is Professor Aksoy a hard grader? | Mixed — tough grader tags but grades nicely if you show effort | System correctly reported mixed opinions, citing tough grader tags and the 40% final weight alongside reviews saying grading is not harsh | Relevant | Accurate |
| 2 | What is Professor Aksoy's lecture style like? | Lecture-heavy, content-dense, hard to follow | System described lectures as traditional math style, content-heavy, and hard to follow, citing multiple reviews | Relevant | Accurate |
| 3 | Is Professor Basu a good discussion facilitator? | Yes — multiple reviews praise her facilitation | System confirmed yes with specific citations about engaging discussions and making every student feel heard | Relevant | Accurate |
| 4 | Does Professor Basu give a lot of homework? | Moderate — readings and papers but manageable | System noted mini quizzes and essays but could not give a clear overall picture of workload | Partially relevant | Partially accurate |
| 5 | Would students recommend Professor Aksoy to non-math majors? | No — reviews say not best for non-majors | System correctly cited the review saying "maybe not the best for non-majors" but noted only one review addressed this directly | Relevant | Accurate |

---

## Failure Case Analysis

**Question that failed:** Does Professor Basu give a lot of homework?

**What the system returned:** The system noted mini quizzes and 2 essays but could not give a confident overall picture of workload. It hedged rather than synthesizing across reviews.

**Root cause (tied to a specific pipeline stage):** The relevant workload information in Prof Basu's reviews is spread across many short mentions — "a lot of reading," "papers are rigorous," "assignments are reasonable" — each appearing in different reviews. At 300 characters per chunk, these mentions were split across many separate chunks. The retrieval step returned only 4 chunks, which captured some but not all of the workload-related content. The LLM did not have enough consolidated context to give a confident synthesized answer.

**What you would change to fix it:** Increase top-k from 4 to 6 or 7 for workload-type questions that require synthesizing across many reviews, or increase chunk size slightly to capture more context per chunk.

---

## Spec Reflection

**One way the spec helped you during implementation:** Writing the chunking strategy in planning.md before touching any code forced a concrete decision about chunk size and overlap before implementation. This made it easy to verify the sliding window logic in `ingest.py` matched the spec — the 300-character chunk size and 50-character overlap were already decided, so the code just needed to match the numbers rather than invent them.

**One way your implementation diverged from the spec, and why:** The evaluation plan originally included questions about Professor Keller and Professor Hamburg, but after running the system the most interesting retrieval results came from Professor Aksoy and Professor Basu who had the most reviews. The evaluation questions were updated to focus on those two professors because they produced more verifiable and informative results.

---

## Query Interface

**Input field:** A text box labeled "Your question" where the user types a plain-language question about a CMC professor.

**Output fields:** Two text boxes — "Answer" which displays the LLM's grounded response with inline source citations, and "Sources" which lists the professor files that were retrieved for that query.

**Sample interaction transcript:**

> **User:** Is Professor Aksoy a hard grader?
>
> **Answer:** According to the reviews, there are mixed opinions about Professor Aksoy's grading. One review describes her as a "Tough grader" and mentions "unreasonable grading" with 40% weight on the final. However, another review states her grading is "not harsh" and that she grades nicely if students show effort and engagement. (Source: Prof Aksoy)
>
> **Sources:** Prof Aksoy

---

## AI Usage

**Instance 1**
- *What I gave the AI:* My domain description, list of 10 .txt professor review files, and chunking strategy (300 character chunks, 50 character overlap)
- *What it produced:* `ingest.py` with `load_documents()` and `chunk_document()` using a sliding window loop
- *What I changed or overrode:* I reviewed the sliding window logic to verify the overlap was implemented correctly — specifically that `start += chunk_size - overlap` advanced by 250 characters not 300, and confirmed source metadata was attached to each chunk as the professor name not the filename.

**Instance 2**
- *What I gave the AI:* My pipeline architecture diagram and retrieval approach section (all-MiniLM-L6-v2, top-k=4, cosine similarity via ChromaDB)
- *What it produced:* `retriever.py` with `embed_and_store()` and `retrieve()` using `_collection.query()`
- *What I changed or overrode:* I verified the nested list indexing was correct — `results["documents"][0]` instead of `results["documents"]` — and confirmed that distance scores and source metadata were both included in the returned chunk dictionaries, since I needed both for the generator and the UI.
from groq import Groq
from config import GROQ_API_KEY, LLM_MODEL

_client = Groq(api_key=GROQ_API_KEY)


def generate_response(query, retrieved_chunks):
    if not retrieved_chunks:
        return {
            "answer": "I couldn't find anything relevant in the loaded documents. Try rephrasing your question.",
            "sources": []
        }

    context = "\n\n".join(
        f"[Source: {chunk['source']}]\n{chunk['text']}"
        for chunk in retrieved_chunks
    )

    sources = list(set(chunk["source"] for chunk in retrieved_chunks))

    response = _client.chat.completions.create(
        model=LLM_MODEL,
        max_tokens=1000,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a helpful student guide that answers questions about professors at Claremont McKenna College. "
                    "Answer using ONLY the review text provided below. "
                    "Do not draw on outside knowledge or make assumptions beyond what the reviews say. "
                    "If the answer is not in the provided reviews, say so explicitly — do not guess. "
                    "Always mention which professor the answer is about and cite the source."
                ),
            },
            {
                "role": "user",
                "content": f"Reviews:\n\n{context}\n\nQuestion: {query}",
            },
        ],
    )

    return {
        "answer": response.choices[0].message.content,
        "sources": sources
    }
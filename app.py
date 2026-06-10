import gradio as gr
from ingest import load_documents, chunk_document
from retriever import embed_and_store, retrieve, get_collection
from generator import generate_response

def setup():
    collection = get_collection()
    if collection.count() == 0:
        print("Ingesting documents...")
        documents = load_documents()
        all_chunks = []
        for doc in documents:
            chunks = chunk_document(doc["text"], doc["source"])
            all_chunks.extend(chunks)
        embed_and_store(all_chunks)
        print(f"Ingestion complete. {collection.count()} chunks stored.")
    else:
        print(f"Vector store already populated ({collection.count()} chunks). Skipping ingestion.")

def ask(question):
    chunks = retrieve(question)
    result = generate_response(question, chunks)
    sources = "\n".join(f"• {s}" for s in result["sources"])
    return result["answer"], sources

setup()

with gr.Blocks(title="CMC Unofficial Guide") as demo:
    gr.Markdown("# 🎓 CMC Unofficial Professor Guide")
    gr.Markdown("Ask anything about professors at Claremont McKenna College based on student reviews.")
    
    inp = gr.Textbox(label="Your question", placeholder="e.g. Is Professor Keller a hard grader?")
    btn = gr.Button("Ask")
    answer = gr.Textbox(label="Answer", lines=8)
    sources = gr.Textbox(label="Sources", lines=3)
    
    btn.click(ask, inputs=inp, outputs=[answer, sources])
    inp.submit(ask, inputs=inp, outputs=[answer, sources])

demo.launch()
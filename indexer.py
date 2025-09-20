import faiss, numpy as np, joblib
from sentence_transformers import SentenceTransformer
from datap import load_datasets

def build_indexes():
    exchanges, traci = load_datasets('detailed_exchanges_harmonized.csv','traci_2_2.xlsx')
    model = SentenceTransformer("all-MiniLM-L6-v2")

    # process embeddings
    process_names = exchanges['process_name'].dropna().unique().tolist()
    proc_emb = model.encode(process_names, convert_to_numpy=True, show_progress_bar=True)
    faiss.normalize_L2(proc_emb)

    index_proc = faiss.IndexFlatIP(proc_emb.shape[1])
    index_proc.add(proc_emb)

    # TRACI embeddings
    traci_names = traci.index.tolist()
    traci_emb = model.encode(traci_names, convert_to_numpy=True, show_progress_bar=True)
    faiss.normalize_L2(traci_emb)

    index_traci = faiss.IndexFlatIP(traci_emb.shape[1])
    index_traci.add(traci_emb)

    # save everything
    joblib.dump({
        "model": model,
        "process_names": process_names,
        "index_proc": index_proc,
        "proc_emb": proc_emb,
        "traci_names": traci_names,
        "index_traci": index_traci,
        "traci_emb": traci_emb
    }, "indexes.pkl")

    print("✅ Indexes saved to indexes.pkl")

if __name__ == "__main__":
    build_indexes()

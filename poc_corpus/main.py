from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
from pathlib import Path

# -------- Configuration --------
BASE_DIR = Path(__file__).resolve().parent
CSV_PATH = BASE_DIR / "data" / "corpus.csv"
PARTIE_COL = "Partie"
SOUS_PARTIE_COL = "Sous Partie"
SUJET_COL = "Sujet"
CITATION_COLS = ["Citations 1", "Citation 2", "Citation 3"]
FONCTION_COLS = ["Fonction 1", "Fonction 2", "Fonction 3"]

# -------- App setup --------
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------- Chargement automatique --------
DATA: pd.DataFrame | None = None

def load_data():
    global DATA
    if not CSV_PATH.exists():
        raise RuntimeError(f"Fichier CSV non trouvé : {CSV_PATH}")
    df = pd.read_csv(str(CSV_PATH), encoding="utf-8-sig", sep=None, engine="python")
    df.columns = df.columns.str.strip().str.replace('\ufeff', '', regex=True)
    for col in [PARTIE_COL, SOUS_PARTIE_COL, SUJET_COL]:
        if col not in df.columns:
            raise RuntimeError(f"Colonne manquante : {col}")
    DATA = df

load_data()
print("Colonnes chargées :", DATA.columns.tolist())
print("Premières lignes :", DATA.head(2).to_dict())

@app.get("/parties")
def get_parties():
    if DATA is None:
        raise HTTPException(400, "Aucune donnée chargée.")
    counts = (
        DATA[PARTIE_COL]
        .value_counts()
        .rename_axis("partie")
        .reset_index(name="size")
    )
    return counts.to_dict(orient="records")

@app.get("/parties/{partie}/sous-parties")
def get_sous_parties(partie: str):
    subset = DATA[DATA[PARTIE_COL] == partie]
    if subset.empty:
        raise HTTPException(404, f"Aucune sous-partie pour {partie}")
    counts = (
        subset[SOUS_PARTIE_COL]
        .value_counts()
        .rename_axis("sous_partie")
        .reset_index(name="size")
    )
    return counts.to_dict(orient="records")

@app.get("/parties/{partie}/{sous_partie}/sujets")
def get_sujets(partie: str, sous_partie: str):
    subset = DATA[
        (DATA[PARTIE_COL] == partie) &
        (DATA[SOUS_PARTIE_COL] == sous_partie)
    ]
    if subset.empty:
        raise HTTPException(404, "Aucun sujet trouvé.")
    counts = (
        subset[SUJET_COL]
        .value_counts()
        .rename_axis("sujet")
        .reset_index(name="size")
    )
    return {"sujets": counts["sujet"].tolist()}

@app.get("/parties/{partie}/{sous_partie}/{sujet}/citations")
def get_citations(partie: str, sous_partie: str, sujet: str):
    subset = DATA[
        (DATA[PARTIE_COL] == partie) &
        (DATA[SOUS_PARTIE_COL] == sous_partie) &
        (DATA[SUJET_COL] == sujet)
    ]
    if subset.empty:
        raise HTTPException(404, "Aucune citation trouvée.")

    results = []
    for _, row in subset.iterrows():
        for citation_col, fonction_col in zip(CITATION_COLS, FONCTION_COLS):
            citation = row.get(citation_col)
            fonction = row.get(fonction_col)
            if pd.notna(citation) and citation.strip():
                results.append({
                    "citation": citation.strip(),
                    "fonction": fonction.strip() if pd.notna(fonction) else ""
                })
    return results

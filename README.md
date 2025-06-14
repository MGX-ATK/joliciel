# Joliciel

This repository provides a small proof of concept for exploring maintenance documentation. A FastAPI backend serves data from a CSV file and a D3.js powered web page consumes this API.

## Starting the project

1. Install the required Python packages (e.g. `fastapi`, `uvicorn`, `pandas`).
2. Launch the API:
   ```bash
   cd poc_corpus
   uvicorn main:app --reload
   ```
3. In another terminal, serve the front-end files:
   ```bash
   cd poc_corpus
   python -m http.server 9000
   ```
4. Visit [http://127.0.0.1:9000/index.html](http://127.0.0.1:9000/index.html) in your browser.

The API automatically loads its content from the CSV file located under `poc_corpus/data/`.

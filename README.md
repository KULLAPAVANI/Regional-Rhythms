# AccentCuisineProject_v2

This version includes HuBERT feature extraction support, MFCC baseline, Flask backend and React frontend with colorful cuisine suggestions and playback.

Important: Dataset not included. Run `backend/download_dataset.sh` to fetch IndicAccentDb from Hugging Face (requires git-lfs).

Backend:
- python -m venv venv
- source venv/bin/activate  # or venv\Scripts\activate on Windows
- pip install -r backend/requirements.txt
- (optional) bash backend/download_dataset.sh
- python backend/src/train.py --feature hubert
- python backend/src/api.py

Frontend:
- cd frontend
- npm install
- npm run dev

Open http://localhost:5173

https://drive.google.com/file/d/1ZfvmKb-GuGn1InqAzbjvp8kArHjoAGHG/view?usp=sharing

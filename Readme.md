python3.12 -m venv venv
.\venv\Scripts\activate
pip install pip --upgrade
python -m pip install pip --upgrade
uvicorn src.main:app --reload
docker build -t analytics-api:latest -f Dockerfile.web .
docker run analytics-api:latest
docker compose up
docker compose up --watch
docker compose up --build
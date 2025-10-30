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
docker compose up --build --watch
docker compose down -v
Go to railway https://railway.com/
Create db on https://console.cloud.timescale.com/ 
Add DATABASE_URL with prefix: postgresql+psycopg:// in Railway Variables
Set PORT 8080 in Railway Variables
Deploy on Railway
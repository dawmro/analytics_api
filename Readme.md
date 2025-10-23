python3.12 -m venv venv
.\venv\Scripts\activate
pip install pip --upgrade
python -m pip install pip --upgrade
uvicorn src.main:app --reload
docker ps
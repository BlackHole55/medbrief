### Quickstart

1. Install requirements
```
pip install -r requirements.txt
```

2. Run docker compose
```
docker compose up -d
```

3. Start celery worker
```
celery -A app.celery_app worker --pool=solo --loglevel=info 
```

4. Start service
```
uvicorn app.main:app
```

To access Swager UI, use ```/docs``` endpoint 
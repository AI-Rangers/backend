FROM tiangolo/uvicorn-gunicorn:python3.8

COPY ./app /app
COPY requirements.txt .
RUN pip install --upgrade pip setuptools && \
    pip --no-cache-dir install -r requirements.txt
 
# COPY requirements.txt /tmp/requirements.txt
# RUN pip install --no-cache-dir -r /tmp/requirements.txt
# CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]

# If running behind a proxy like Nginx or Traefik add --proxy-headers
# CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80", "--proxy-headers"]

# CMD exec gunicorn --bind :$PORT --workers 2 --threads 8 --timeout 0 app.main:app
CMD exec gunicorn --bind :$PORT app.main:app --workers 2 --worker-class uvicorn.workers.UvicornWorker

FROM tiangolo/uvicorn-gunicorn:python3.9

COPY ./app /app
COPY requirements.txt .
RUN pip --no-cache-dir install -r requirements.txt

# COPY requirements.txt /tmp/requirements.txt
# RUN pip install --no-cache-dir -r /tmp/requirements.txt
# CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]

# If running behind a proxy like Nginx or Traefik add --proxy-headers
# CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80", "--proxy-headers"]
FROM tiangolo/uvicorn-gunicorn:python3.8

ENV PYTHONUNBUFFERED True

ENV APP_HOME /app
WORKDIR $APP_HOME
COPY . ./
 
# COPY ./app /app
# COPY requirements.txt .
RUN pip install --upgrade pip setuptools && \
    pip --no-cache-dir install -r requirements.txt
 
RUN apt-get update
RUN apt-get install ffmpeg libsm6 libxext6 libgl1-mesa-glx libgl1 -y
RUN pip install opencv-python-headless

# COPY requirements.txt /tmp/requirements.txt
# RUN pip install --no-cache-dir -r /tmp/requirements.txt
# CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]

# If running behind a proxy like Nginx or Traefik add --proxy-headers
# CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80", "--proxy-headers"]

# CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 app.main:app
CMD exec gunicorn --preload --bind :$PORT app.main:app --workers 1 --worker-class uvicorn.workers.UvicornWorker

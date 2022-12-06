FROM tiangolo/uvicorn-gunicorn:python3.8

ENV PYTHONUNBUFFERED True

ENV APP_HOME /app
WORKDIR $APP_HOME
COPY . ./
 
# COPY ./app /app
# COPY requirements.txt .
RUN pip install --upgrade pip setuptools && \
    pip --no-cache-dir install -r requirements.txt

# 解決 cv2 缺少相依性套件的問題 ImportError: libGL.so.1: cannot open shared object file: No such file or directory
RUN apt-get update
RUN apt-get install ffmpeg libsm6 libxext6 -y
RUN apt-get install libgl1
# RUN pip install install h5py
# RUN pip install versioned-hdf5

# 安裝 opencv-python-headless 會導致 imshow 等涉及UI的方法不能用。
# RUN pip install opencv-python-headless

# COPY requirements.txt /tmp/requirements.txt
# RUN pip install --no-cache-dir -r /tmp/requirements.txt
# CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]

# If running behind a proxy like Nginx or Traefik add --proxy-headers
# CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80", "--proxy-headers"]

# CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 app.main:app
CMD exec gunicorn --preload --bind :$PORT app.main:app --workers 1 --worker-class uvicorn.workers.UvicornWorker

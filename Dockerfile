FROM python:3.9-slim
WORKDIR /app
COPY . /app

RUN apt-get update && apt-get install -y \
    build-essential libsndfile1 \
    && rm -rf /var/lib/apt/lists/*

RUN pip install -e .
RUN python -m unidic download
RUN wget http://192.168.1.76:9008/test/checkpoint.pth -O /app/melo/model/zh/checkpoint.pth
#RUN python melo/init_downloads.py
CMD ["python", "./melo/service.py"]
#CMD ["python", "./melo/app.py", "--host", "0.0.0.0", "--port", "8888"]
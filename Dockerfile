FROM 192.168.1.76:8099/evtrain/melo:v1.0
WORKDIR /app
RUN rm -rf /app/*
COPY . /app
RUN pip install flask && wget http://192.168.1.76:9008/test/checkpoint.pth -O /app/melo/model/zh/checkpoint.pth
CMD ["python", "./melo/service.py"]
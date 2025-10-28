FROM python:3.11-slim

RUN apt-get update 

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python3", "app.py", "--host=0.0.0.0", "--port=9000"]
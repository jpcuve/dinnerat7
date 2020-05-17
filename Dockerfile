FROM python:3.7-slim
COPY . /code
WORKDIR /code
RUN pip install --no-cache-dir -r requirements.txt
ENTRYPOINT python run.py
EXPOSE 5000
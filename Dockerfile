FROM python:3.10
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y
EXPOSE $PORT
CMD gunicorn --workers=4 --preload -b 0.0.0.0:$PORT app:app

FROM python:3.8-slim
COPY . /app
WORKDIR /app
RUN apt-get update && export DEBIAN_FRONTEND=noninteractive \
    && apt-get -y install --no-install-recommends libsndfile1
RUN python3 -m pip install --upgrade pip \
    && pip3 --disable-pip-version-check --no-cache-dir install -r requirements.txt
CMD exec gunicorn --bind :5000 --workers 1 --threads 8 --timeout 0 application:application
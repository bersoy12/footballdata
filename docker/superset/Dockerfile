FROM apache/superset:3.0.2

USER root
RUN apt-get update && apt-get upgrade -y && apt-get clean

COPY requirements.txt /tmp/
RUN pip install --no-cache-dir -r /tmp/requirements.txt

USER superset
FROM python:3.8-slim-buster

MAINTAINER Steven Bambling <smbambling@gmail.com>

# Metadata
LABEL Remarks="Check Kubernetes Job Status"

RUN pip install --upgrade pip && \
    pip install --no-cache-dir prettytable && \
    pip install --no-cache-dir kubernetes

WORKDIR /usr/local/sbin/app

COPY app .
COPY VERSION .

ENTRYPOINT [ "python", "./check_kubernetes_cronjobs.py" ]
CMD [ "--help" ]

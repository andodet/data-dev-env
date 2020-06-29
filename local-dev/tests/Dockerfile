FROM python:3.8.3-alpine3.12

COPY . /
RUN pip install -r requirements.txt

RUN ["chmod", "+x", "./entrypoint.sh"]

ENTRYPOINT [ "/bin/sh", "-c", "./entrypoint.sh" ]
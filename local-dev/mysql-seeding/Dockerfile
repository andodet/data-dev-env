FROM python:3.8.3-alpine3.12

COPY . /
RUN pip install -r requirements.txt

CMD chmod +x seed_mysql.sh

ENTRYPOINT [ "/bin/sh", "seed_mysql.sh" ]

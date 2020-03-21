FROM python:3.7.2

WORKDIR /usr/src/services/web

COPY . .

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

EXPOSE 8091

ENTRYPOINT ["./run.sh"]
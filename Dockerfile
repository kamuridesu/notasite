FROM python:3-alpine
WORKDIR /app
COPY ./requirements.txt .
RUN pip install -r requirements.txt
COPY . .
RUN pelican -o output -s pelicanconf.py
ENTRYPOINT [ "pelican", "content", "-o", "output", "-s", "publishconf.py", "--listen", "-p", "80", "-b", "0.0.0.0" ]
FROM python:3-alpine as build
WORKDIR /app
COPY ./requirements.txt .
RUN pip install -r requirements.txt
COPY . .
RUN pelican -o output -s pelicanconf.py

FROM nginx:1.25.2
COPY --from=build /app/output /usr/share/nginx/html
COPY ./nginx.conf /etc/nginx/conf.d/default.conf
# ---- Base python ----
FROM python:3.8.6 AS base
# Create app directory
WORKDIR "/usr/src/app"

# ---- Dependencies ----
COPY . /usr/src/app

RUN pip3 install --upgrade pip &&\
 pip3 install -r requirements.txt --no-cache-dir

HEALTHCHECK --interval=60s --timeout=5s \
 CMD curl -fs http://localhost:5010/healthyCheck || exit 1

ENTRYPOINT ["sh", "/usr/src/app/entrypoint.sh"]

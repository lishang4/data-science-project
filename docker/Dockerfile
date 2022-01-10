# ---- Base python ----
FROM python:3.8.1 AS base
# Create app directory
WORKDIR "/usr/src/app"

# ---- Dependencies ----
FROM base AS dependencies  
COPY ./requirements.txt ./
# install app dependencies if needed

# ---- Copy Files/Build ----
FROM dependencies AS build  
WORKDIR "/usr/src/app"
COPY . /usr/src/app

# --- Release with Alpine ----
FROM python:3.8.1-alpine AS release  
# Create app directory
WORKDIR "/usr/src/app"
COPY --from=dependencies /usr/src/app/requirements.txt ./

# Install app dependencies
RUN apk --update add python py-pip openssl ca-certificates py-openssl curl&& \
 apk --update add --virtual build-dependencies libffi-dev freetype-dev libpng-dev openssl-dev python3-dev libc-dev py-pip build-base && \
 pip3 install --upgrade pip &&\
 pip3 install -r requirements.txt &&\
 apk del build-dependencies
HEALTHCHECK --interval=60s --timeout=5s \
 CMD curl -fs http://localhost:5010/healthyCheck || exit 1

COPY --from=build /usr/src/app/ ./
ENTRYPOINT ["sh", "/usr/src/app/entrypoint.sh"]

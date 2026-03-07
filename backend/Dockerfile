FROM node:22-slim

WORKDIR /backend

COPY package.json pnpm-lock.yaml ./

RUN apt update -y && apt upgrade -y 

RUN pnpm install --freeze-lockfile

EXPOSE 8000
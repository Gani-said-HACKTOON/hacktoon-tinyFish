# build
FROM node:22-slim AS builder

ARG DATABASE_URL

RUN apt update -y && apt upgrade -y && apt install openssl -y 

RUN corepack enable && corepack prepare pnpm@latest --activate

WORKDIR /backend-app

RUN mkdir backend packages

COPY package.json pnpm-lock.yaml pnpm-workspace.yaml ./

COPY ./backend ./backend

COPY ./packages ./packages

RUN pnpm install --frozen-lockfile

RUN echo "${DATABASE_URL}" > ./packages/database/.env

RUN pnpm --prefix=./packages/database prisma generate

RUN pnpm --filter backend build

# deploy 
FROM node:22-slim

RUN corepack enable && corepack prepare pnpm@latest --activate

WORKDIR /backend-app

RUN mkdir -p packages/database backend

# depedencies
COPY ./package.json ./pnpm-lock.yaml ./pnpm-workspace.yaml ./
COPY ./backend/package.json ./backend/package.json
COPY ./packages/database/package.json ./packages/database/package.json

# app 
COPY --from=builder /backend-app/backend/dist ./backend/dist
COPY --from=builder /backend-app/packages ./packages

EXPOSE 3000

RUN pnpm install --prod --frozen-lockfile

ENV NODE_ENV=production

CMD ["node", "backend/dist/main"]
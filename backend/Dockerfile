# build
FROM node:22-slim AS builder

ARG DATABASE_URL

RUN apt update -y && apt upgrade -y && apt install openssl -y 

RUN corepack enable && corepack prepare pnpm@latest --activate

WORKDIR /backend-build

RUN mkdir backend packages

COPY package.json pnpm-lock.yaml pnpm-workspace.yaml ./

COPY ./backend ./backend

COPY ./packages ./packages

RUN pnpm install --frozen-lockfile

RUN echo "${DATABASE_URL}" > ./packages/database/.env

RUN pnpm --prefix=/backend-build/packages/database prisma generate

RUN pnpm --filter backend build

# deploy 
FROM node:22-slim

RUN corepack enable && corepack prepare pnpm@latest --activate

WORKDIR /backend-deploy 

RUN mkdir -p packages/database backend

# depedencies
COPY ./package.json ./pnpm-lock.yaml ./pnpm-workspace.yaml ./
COPY ./backend/package.json ./backend/package.json
COPY ./packages/database/package.json ./packages/database/package.json

# app 
COPY --from=builder /backend-build/backend/dist ./backend/dist
COPY --from=builder /backend-build/packages ./packages

RUN pnpm install --prod --frozen-lockfile

EXPOSE 3000

ENV NODE_ENV=production

# CMD ["node", "backend/dist/main"]
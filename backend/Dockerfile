# build

FROM node:22-slim as builder

RUN npm install -g pnpm

WORKDIR /backend-build

COPY package.json pnpm-lock.yaml pnpm-workspace.yaml ./

COPY backend .

COPY packages .

RUN apt update -y && apt upgrade -y 

RUN pnpm install --force

COPY . .

RUN pnpm build

# deploy 
FROM node:22-slim

WORKDIR /backend-deploy 

COPY --from=builder /backend-build/dist ./dist

COPY package.json .

RUN pnpm install --only=production

CMD ["node", "./dist/main.js"]

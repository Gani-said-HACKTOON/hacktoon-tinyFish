import dotenv from 'dotenv'
import path from "path";
import { fileURLToPath } from 'url';
import { PrismaClient } from "./generated/prisma/client/client.js";
import { PrismaPg } from "@prisma/adapter-pg";

const __filename = fileURLToPath(import.meta.url)
const __dirname = path.dirname(__filename)

dotenv.config({
    path: path.resolve(__dirname,".env")
})

const adapter = new PrismaPg({
    connectionString: process.env.DATABASE_URL
})

export const prisma = new PrismaClient({
    adapter
});

export * from './lib/refresh_token.ts'
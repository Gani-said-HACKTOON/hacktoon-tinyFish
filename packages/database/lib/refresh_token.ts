import { prisma } from "../index.ts";
import { type refreshToken } from "../generated/prisma/client/index.js";

interface refreshTokenType{
    id: number,
    refresh_token: string,
    createdAt: Date,
    expiredAt: Date
} 

async function readRefreshTokenByUserId(userId: number): Promise<refreshToken | null>{
    return await prisma.refreshToken.findUnique({
        where:{
            user_id: userId
        }
    })
}

async function createRefreshTokenDb(dbData: refreshTokenType){
        await prisma.refreshToken.create({
        data: {
            user_id: dbData.id,
            token: dbData.refresh_token,
            expired_at: dbData.expiredAt,
            created_at: dbData.createdAt   
        }
    })
}

async function updateRefreshTokenDb(userId: number, data: {refresh_token: string, expiredAt: Date, createdAt: Date}){
    await prisma.refreshToken.update({
        where:{
            user_id: userId
        },
        data:{
            token: data.refresh_token,
            expired_at: data.expiredAt,
        }
    })
}                                                                                                                                   

export { updateRefreshTokenDb, createRefreshTokenDb, readRefreshTokenByUserId }
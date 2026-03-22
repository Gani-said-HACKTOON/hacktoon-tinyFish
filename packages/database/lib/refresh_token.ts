import { prisma } from "../index.ts";

interface refreshTokenType{
    id: number,
    refresh_token: string,
    createdAt: Date,
    expiredAt: Date
} 

async function createRefreshTokenDb(dbData: refreshTokenType){
        await prisma.refresh_token.create({
        data: {
            user_id: dbData.id,
            token: dbData.refresh_token,
            expired_at: dbData.expiredAt,
            created_at: dbData.createdAt   
        }
    })
}

async function updateRefreshTokenDb(userId: number, data: {refresh_token: string, expiredAt: Date, createdAt: Date}){
    await prisma.refresh_token.update({
        where:{
            user_id: userId
        },
        data:{
            token: data.refresh_token,
            expired_at: data.expiredAt,
            created_at: data.createdAt
        }
    })
}

export { updateRefreshTokenDb, createRefreshTokenDb }
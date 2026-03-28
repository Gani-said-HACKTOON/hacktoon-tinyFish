import { prisma } from '../index.ts'
import { User } from '../generated/prisma/client/index.js'

async function readUserByEmail(email: string):  Promise<User | null>{
    return await prisma.user.findUnique({
        where:{
            email: email
        }
    })
}

async function readUserById(userId: number): Promise<User | null>{
    return await prisma.user.findUnique({
        where:{
            id: userId
        }
    })
}


async function createUserTable(data: {
    username: string,
    email: string,
    password: string
}){
    await prisma.user.create({
        data: data
    })
}

export { createUserTable, readUserByEmail, readUserById }
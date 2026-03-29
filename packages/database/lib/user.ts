import { prisma } from '../index.ts'
import { type User } from '../generated/prisma/client/index.js'

interface userType{
    first_name: string,
    last_name: string,
    company_name: string,
    email: string,
    password: string
}

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


async function createUserTable(data: userType): Promise<User>{
    return await prisma.user.create({
        data: data
    })
}

export { createUserTable, readUserByEmail, readUserById , type userType}
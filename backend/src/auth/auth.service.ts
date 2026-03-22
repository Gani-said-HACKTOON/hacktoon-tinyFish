import { Injectable, UnauthorizedException, NotFoundException, ConflictException, InternalServerErrorException } from "@nestjs/common"
import { prisma, createRefreshTokenDb, updateRefreshTokenDb } from "@hackathon/database"
import { Prisma, User as userTypeDB } from "@hackathon/database/generated/prisma/client";
import bcrypt from 'bcrypt';
import ms  from 'ms';
import { JwtService } from "@nestjs/jwt";

interface HttpRes{
    message: string
}

interface HttpAuth{
    access_token: string,
    refresh_token: string
}

@Injectable()
class AuthService{
    constructor(private JwtServ: JwtService){}

    async createUser(data: {
        username: string,
        email: string,
        password: string
    }): Promise<HttpRes>{
        const hashpass = await bcrypt.hash(data.password, 10);

        data.password = hashpass;
        
        try{
            await prisma.user.create({
                    data: data
            })
            return {
                message: "create account has been succesful"
            };

        }catch(err){
            if (err instanceof Prisma.PrismaClientKnownRequestError){
                if (err.code === "P2002"){
                    throw new ConflictException("Email already exists")
                }
            }

            throw new InternalServerErrorException()
        }
    }


    async emailLogin(loginData:{
        email: string
        password: string
    }): Promise<HttpAuth>{
        const dbData = await prisma.user.findUnique({
            where : { email: loginData.email}
        })

        if (!dbData){
            throw new NotFoundException("Email not found");
        }

        if(! await this.#comparePassword(loginData.password, dbData.password)){
            throw new  UnauthorizedException("Invalid Password");
        }

       return this.generateToken(dbData)

    }

    async refresh(userId: number): Promise<HttpAuth>{
        const userData = await prisma.user.findUnique({
            where: { id: userId }
        })

        if (!userData){
            throw new NotFoundException()
        }

        
        return {
            access_token: await this.generateAccessToken(userData),
            refresh_token: await this.updateRefreshToken(userId)
        }
    }

    async generateToken(userData: userTypeDB): Promise<HttpAuth>{
        return {
            access_token: await this.generateAccessToken(userData),
            refresh_token: await this.generateRefreshToken(userData)
        }
        
    }

    async generateAccessToken(userData: userTypeDB): Promise<string> {
         const access_token_payload = {
            email: userData.email,
            sub: userData.id
        }
        return await this.JwtServ.signAsync(access_token_payload)
    }

    async generateRefreshToken(userData: userTypeDB): Promise<string>{
        const createdAt = Date.now() 
        const expiresIn = "7d"
        const expiredAt = createdAt + ms(expiresIn)
3
        const refresh_token_payload = {
            sub: userData.id
        }

        const refresh_token = await this.JwtServ.signAsync(refresh_token_payload,{
            expiresIn: expiresIn
        })

         createRefreshTokenDb({
            id: userData.id,
            refresh_token:  await bcrypt.hash(refresh_token,10),
            expiredAt: new Date(expiredAt),
            createdAt: new Date(createdAt)
        }).catch(async err => {
            if (err instanceof Prisma.PrismaClientKnownRequestError){
                if (err.code === "P2002"){
                    await updateRefreshTokenDb(userData.id,{
                        refresh_token:  await bcrypt.hash(refresh_token,10),
                        expiredAt: new Date(expiredAt),
                        createdAt: new Date(createdAt)
                    })
                }
            }
        })

        return refresh_token
    }

    async updateRefreshToken(userId: number): Promise<string>{
        const createdAt = Date.now() 
        const expiresIn = "7d"
        const expiredAt = createdAt + ms(expiresIn)
3
        const refresh_token_payload = {
            sub: userId
        }

        const refresh_token = await this.JwtServ.signAsync(refresh_token_payload,{
            expiresIn: expiresIn
        })

        updateRefreshTokenDb(userId, {
            refresh_token: refresh_token,
            expiredAt: new Date(expiredAt),
            createdAt: new Date(createdAt)
        })

        return refresh_token
    }

    async #comparePassword(inputPassword: string, dbPassword: string){
        return await bcrypt.compare(inputPassword, dbPassword)
    }
}

export {AuthService, type HttpRes, type HttpAuth }
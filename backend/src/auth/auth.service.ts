import { Injectable, UnauthorizedException, NotFoundException, ConflictException, InternalServerErrorException } from "@nestjs/common"
import { prisma } from "@hackathon/database"
import { Prisma } from "@hackathon/database/generated/prisma/client"
import bcrypt from 'bcrypt';
import { JwtService } from "@nestjs/jwt";
import { type Response } from "express";

interface HttpRes{
    message: string
}

interface HttpAuth{
    access_token: string
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
    }, response_handler: Response): Promise<HttpAuth>{
        const dbData = await prisma.user.findUnique({
            where : { email: loginData.email}
        })

        if (!dbData){
            throw new NotFoundException("Email not found");
        }

        if(! await this.#comparePassword(loginData.password, dbData.password)){
            throw new  UnauthorizedException("Invalid Password");
        }

        // response_handler.cookie()

        const payload = {
            email: dbData.email,
            sub: dbData.id
        }
        
       return {
            access_token: await this.JwtServ.signAsync(payload )
       } 

    }

    async #comparePassword(inputPassword: string, dbPassword: string){
        return await bcrypt.compare(inputPassword, dbPassword)
    }
}

export {AuthService, type HttpRes, type HttpAuth }
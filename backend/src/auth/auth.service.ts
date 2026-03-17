import { Injectable, UnauthorizedException, NotFoundException, ConflictException, InternalServerErrorException } from "@nestjs/common"
import { prisma } from "@hackathon/database"
import { Prisma } from "@hackathon/database/generated/prisma/client"
import bcrypt from 'bcrypt';

interface HttpRes{
    message: string
}

@Injectable()
class AuthService{
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

            throw new InternalServerErrorException(err)
        }
    }


    async emailLogin(loginData:{
        email: string
        password: string
    }): Promise<HttpRes>{
        const dbData = await prisma.user.findUnique({
            where : { email: loginData.email}
        })

        if (!dbData){
            throw new NotFoundException("Email not found");
        }

        if(! await this.#comparePassword(loginData.password, dbData.password)){
            throw new  UnauthorizedException("Invalid Password");
        }

        return {
            message: "login succesful"
        }

    }

    async #comparePassword(inputPassword: string, dbPassword: string){
        return await bcrypt.compare(inputPassword, dbPassword)
    }
}

export {AuthService, type HttpRes}
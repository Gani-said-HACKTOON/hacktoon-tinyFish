import { Injectable, UnauthorizedException, NotFoundException, ConflictException, InternalServerErrorException } from "@nestjs/common"
import { prisma } from "@hackathon/database"
import { Prisma, User as userTypeDB } from "@hackathon/database/generated/prisma/client"
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

    async generateToken(userData: userTypeDB): Promise<HttpAuth>{
           const access_token_payload = {
            email: userData.email,
            sub: userData.id
        }

        return {
            access_token: await this.JwtServ.signAsync(access_token_payload),
            refresh_token: await this.generateRefreshToken(userData)
        }
        
    }

    async generateRefreshToken(userData: userTypeDB): Promise<string>{
        const createdAt = Date.now() 
        const expiresIn = "7d"
        const expiredAt = createdAt + ms(expiresIn)

        const refresh_token_payload = {
            sub: userData.id
        }

        const refresh_token = await this.JwtServ.signAsync(refresh_token_payload,{
            expiresIn: expiresIn
        })

        await prisma.refresh_token.create({
            data: {
                user_id: userData.id,
                token: await bcrypt.hash(refresh_token,10),
                expired_at: new Date(expiredAt),
                created_at: new Date(createdAt)    
            }
        })

        return refresh_token
    }

    async #comparePassword(inputPassword: string, dbPassword: string){
        return await bcrypt.compare(inputPassword, dbPassword)
    }
}

export {AuthService, type HttpRes, type HttpAuth }
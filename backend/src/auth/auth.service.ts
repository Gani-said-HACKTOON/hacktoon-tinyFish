import { Injectable } from "@nestjs/common"
import { prisma } from "@hackathon/database" 
import bcrypt from 'bcrypt';

interface HttpRes{
    message: string,
    status: number
}

class HttpErr extends Error{
    status: number
    constructor(message: string, status: number){
        super(message)
        this.status = status
    }
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
                message: "create account has been succesful",
                status: 201
            };

        }catch(err){
            throw new HttpErr("error",500)
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
            throw new HttpErr("Email not found", 404);
        }

        if(! await this.#comparePassword(loginData.password, dbData.password)){
            throw new HttpErr("Invalid Password",401);
        }

        return {
            message: "login succesfull",
            status: 200
        }

    }

    async #comparePassword(inputPassword: string, dbPassword: string){
        return await bcrypt.compare(inputPassword, dbPassword)
    }
}

export {AuthService, type HttpRes, type HttpErr}
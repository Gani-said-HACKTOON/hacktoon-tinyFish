import { Injectable } from "@nestjs/common"
import { prisma } from "@hackathon/database" 
import bcrypt from 'bcrypt';


@Injectable()
export class AuthService{
    async createUser(data: {
        username: string,
        email: string,
        password: string
    }){
        const hashpass = await bcrypt.hash(data.password, 10);

        data.password = hashpass;

        const user = await prisma.user.create({
            data: data
        })
        console.log(user)
    }


}
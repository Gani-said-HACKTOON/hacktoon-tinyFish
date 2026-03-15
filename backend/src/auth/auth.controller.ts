import { Controller, Post, Body, Res } from '@nestjs/common'
import { AuthService, type HttpRes, type HttpErr } from './auth.service';
import { CreateUserDto } from './dto/create-user.dto';      
import { login_with_email } from './dto/login-user.dto';
import { type Response } from "express";


@Controller("/auth")
export class AuthController{
    constructor(private readonly authService: AuthService){}

    
    @Post("registration")
    async Registration(@Res() res: Response, @Body() createUser: CreateUserDto){
        this.authService.createUser({
            username: createUser.username,
            email: createUser.email,
            password: createUser.password
        })
        .then((serverresponse: HttpRes)=>res.status(serverresponse.status).json({
            message: serverresponse.message
        }))
        .catch((servererr: HttpErr)=>res.status(servererr.status).json({
            message: servererr.message
        }))
    }
    
    @Post("loginwithemail")
    async loginWithEmail(@Res({passthrough:  true}) res: Response, @Body() loginData: login_with_email){
        this.authService.emailLogin({
            email: loginData.email,
            password: loginData.password
        })
        .then((serverresponse: HttpRes)=>res.status(serverresponse.status).json({
            message: serverresponse.message
        }))
        .catch((servererr: HttpErr)=> res.status(servererr.status).json({
            message: servererr.message
        }))
        
    }
}
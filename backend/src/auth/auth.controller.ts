import { Controller, Post, Body, Res, HttpCode } from '@nestjs/common'
import { AuthService, type HttpRes } from './auth.service';
import { CreateUserDto } from './dto/create-user.dto';      
import { login_with_email } from './dto/login-user.dto';
import { type Response } from "express";


@Controller("/auth")
export class AuthController{
    constructor(private readonly authService: AuthService){}

    
    @Post("registration")
    @HttpCode(201)
    Registration(@Body() createUser: CreateUserDto){
        return this.authService.createUser({
            username: createUser.username,
            email: createUser.email,
            password: createUser.password
        })
    }
    
    @Post("loginwithemail")
    @HttpCode(200)
    loginWithEmail(@Body() loginData: login_with_email){
        return this.authService.emailLogin({
            email: loginData.email,
            password: loginData.password
        })
    }
}
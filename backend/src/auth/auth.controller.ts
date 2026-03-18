import { Controller, Post, Body, HttpCode , Res, Req } from '@nestjs/common'
import { AuthService } from './auth.service';
import { type Response, type Request } from 'express';
import { CreateUserDto } from './dto/create-user.dto';      
import { login_with_email } from './dto/login-user.dto';


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
    loginWithEmail(@Res({passthrough: true}) res: Response,  @Body() loginData: login_with_email){  
        return this.authService.emailLogin({
            email: loginData.email,
            password: loginData.password
        },res)
    }

    @Post("refresh")
    refresh(@Req() req: Request){

    }
}
import { Controller, Get, Post, Body, HttpCode , Res, Req, UseGuards } from '@nestjs/common'
import { AuthService, HttpAuth } from './auth.service';
import { type Response, type Request } from 'express';
import { CreateUserDto } from './dto/create-user.dto';      
import { login_with_email } from './dto/login-user.dto';
import { AuthGuard } from '@nestjs/passport';


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
    
    @UseGuards(AuthGuard('login'))
    @Post("loginwithemail")
    @HttpCode(200)
    loginWithEmail(@Res({passthrough: true}) res: Response, @Req() req: Request){  
        const user = req.user as HttpAuth
        res.cookie('refresh_token', user.refresh_token, {
            httpOnly: true,
        })

        return {
            access_token: user.access_token
        }

    }

    @Post("refresh")
    refresh(@Req() req: Request){

    }

    @UseGuards(AuthGuard("jwt"))
    @Get("profile")
    profile(@Req() req: Request){

    }
}
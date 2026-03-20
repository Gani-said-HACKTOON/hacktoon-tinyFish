import { Strategy as LocalStrategy } from 'passport-local';
import { PassportStrategy } from '@nestjs/passport';
import { Injectable } from '@nestjs/common';
import { AuthService, HttpAuth } from './auth.service';


@Injectable()
export class loginStrategy extends PassportStrategy(LocalStrategy,'login'){
    constructor(private authServ: AuthService){
        super({
            usernameField: "email",
            passwordField: "password"
        })
    }
    async validate(email: string,password: string): Promise<HttpAuth>{
        return this.authServ.emailLogin({
            email: email,
            password: password
        })
    }
}
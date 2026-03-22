import { Injectable } from "@nestjs/common";
import { PassportStrategy } from "@nestjs/passport";
import { ExtractJwt, Strategy } from 'passport-jwt';
import { ConfigService } from "@nestjs/config";
import { AuthService } from "./auth.service";
import { type Request } from 'express'

interface refreshTokenType{
    sub: number
}

@Injectable()
class accessToken extends PassportStrategy(Strategy, "access_token"){
    constructor(private authService: AuthService, config: ConfigService){
        super({ 
            jwtFromRequest: ExtractJwt.fromAuthHeaderAsBearerToken(),
            ignoreExpiration: false,
            secretOrKey: config.get<string>("SECRET_JWT_KEY") || "whatever_fallback"
        })
    }
    async validate(payload: any){
        console.log(payload)
    }
}

@Injectable()
class refreshToken extends PassportStrategy(Strategy, "refresh_token"){
    constructor(private authService: AuthService, config: ConfigService){
        super({
            jwtFromRequest: ExtractJwt.fromExtractors([
                (req: Request) => (req.headers.cookie ?? "").split('=')[1]
            ]),
            ignoreExpiration: false,
            secretOrKey: config.get<string>("SECRET_JWT_KEY") || "whatever_fallback"
        })
    }
    async validate(payload: refreshTokenType){
        return this.authService.refresh(payload.sub)
    }
}

export { accessToken, refreshToken }
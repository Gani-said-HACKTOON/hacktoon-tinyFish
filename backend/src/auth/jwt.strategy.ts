import { Injectable, UnauthorizedException } from "@nestjs/common";
import { PassportStrategy } from "@nestjs/passport";
import { ExtractJwt, Strategy } from 'passport-jwt';
import { ConfigService } from "@nestjs/config";
import { AuthService } from "./auth.service";
import { type Request } from 'express'

interface refreshTokenType{x
    sub: number
}

interface accessTokenType{
    email: string,
    sub: number  
}

@Injectable()
class accessTokenStrategy extends PassportStrategy(Strategy, "access_token"){
    constructor(config: ConfigService){
        super({ 
            jwtFromRequest: ExtractJwt.fromAuthHeaderAsBearerToken(),
            ignoreExpiration: false,
            secretOrKey: config.get<string>("SECRET_JWT_KEY") || "whatever_fallback"
        })
    }
    async validate(payload: accessTokenType){
        return payload
    }
}

@Injectable()
class refreshTokenStrategy extends PassportStrategy(Strategy, "refresh_token"){
    constructor(private authService: AuthService, config: ConfigService){
        console.log(config.get("SECRET_JWT_KEY"))
        super({
            jwtFromRequest: ExtractJwt.fromExtractors([
                (req: Request) => (req.headers.cookie ?? "").split('=')[1] 
            ]),
            ignoreExpiration: false,
            secretOrKey: config.get<string>("SECRET_JWT_KEY") || "whatever_fallback",
            passReqToCallback: true
        })
    }
    async validate(req: Request, payload: refreshTokenType){
        if(!await this.authService.verifyRefreshToken((req.headers.cookie ?? "").split('=')[1], payload.sub)){
            throw new UnauthorizedException("not match in db")
        }
        return this.authService.refresh(payload.sub)
        
    }
}

export { accessTokenStrategy, refreshTokenStrategy }
import { Injectable } from "@nestjs/common";
import { PassportStrategy } from "@nestjs/passport";
import { ExtractJwt, Strategy } from 'passport-jwt';
import { ConfigService } from "@nestjs/config";

@Injectable()
export class jwtStrategy extends PassportStrategy(Strategy, "jwt"){
    constructor(private config: ConfigService){
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
import { PassportStrategy } from "@nestjs/passport";
import { Injectable } from "@nestjs/common";
import { Strategy, VerifyCallback } from "passport-google-oauth20";
import { ConfigService } from "@nestjs/config";

@Injectable()
export class googleStrategy extends PassportStrategy(Strategy, "google"){

    constructor(config: ConfigService){
        super({
            clientID: config.get<string>("GOOGLE_CLIENT_ID")!,
            clientSecret: config.get<string>("GOOGLE.CLIENT_SECRET")!,
            callbackURL: "http://localhost:3000/auth/google/callback",
            scope: ["email","profile"],
        })
    }

    async validate(accessToken: string, refreshToken: string, profile: any, done: VerifyCallback){

    }
}
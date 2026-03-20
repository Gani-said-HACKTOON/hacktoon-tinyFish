import { Module } from '@nestjs/common';
import { AuthController } from './auth.controller';
import { AuthService } from './auth.service';
import { JwtModule } from '@nestjs/jwt';
import { ConfigService } from '@nestjs/config';
import { PassportModule } from '@nestjs/passport';
import { loginStrategy } from './local.strategy';

@Module({
    imports: [JwtModule.registerAsync({
        useFactory: (config: ConfigService)=>({
            secret: config.get<string>("SECRET_JWT_KEY"),
            signOptions: { expiresIn: "30m" }
        }),
        inject: [ConfigService]
    }
    ),PassportModule],
    controllers: [AuthController],
    providers: [AuthService, loginStrategy],

})
export class AuthModule {}

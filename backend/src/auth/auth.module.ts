import { Module } from '@nestjs/common';
import { AuthController } from './auth.controller';
import { AuthService } from './auth.service';
import { JwtModule } from '@nestjs/jwt';
import { ConfigService } from '@nestjs/config';

@Module({
    imports: [JwtModule.registerAsync({
        useFactory: (config: ConfigService)=>({
            secret: config.get<string>("SECRET_JWT_KEY"),
            signOptions: { expiresIn: "30m" }
        }),
        inject: [ConfigService]
    }
    )],
    controllers: [AuthController],
    providers: [AuthService],

})
export class AuthModule {}

import { Controller, Post, Body, Res } from '@nestjs/common'
import { AuthService } from './auth.service';
import { CreateUserDto } from './dto/create-user.dto';  


@Controller("/auth")
export class AuthController{
    constructor(private readonly authService: AuthService){}

    
    @Post("registration")
    Registration(@Body() createUser: CreateUserDto){
        this.authService.createUser(createUser);
        return "success full created"
    }
    
    @Post("test1")
    Test1(@Res() res: Response){
        return res
    }
    
    comparePassword(userPass: string, dbPass: string): boolean{
        return userPass === dbPass
    }
}
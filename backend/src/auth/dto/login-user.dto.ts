import { IsEmail, IsString } from "class-validator";

export class login_with_email{
    @IsEmail()
    email!: string;

    @IsString()
    password!: string;
}
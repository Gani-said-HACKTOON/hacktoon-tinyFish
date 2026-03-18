import { NestFactory } from '@nestjs/core';
import { AppModule } from './app.module';
import { ValidationPipe } from '@nestjs/common'
import "dotenv/config"

export const SECRET_JWT_KEY = process.env.SECRET_JWT_KEY
console.log(SECRET_JWT_KEY)
async function bootstrap() {

  const app = await NestFactory.create(AppModule);
  app.useGlobalPipes(new ValidationPipe({
    whitelist: true,
    forbidNonWhitelisted: true,
    transform: true
  }))

  await app.listen(process.env.PORT ?? 3000);
}
bootstrap();

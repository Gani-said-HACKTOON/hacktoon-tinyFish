import { Module } from '@nestjs/common';
import { AgentController } from './agent.controller';
import { AgentService } from './agent.service';
import { accessTokenStrategy } from '../auth/jwt.strategy';
@Module({
    controllers: [AgentController],
    providers: [AgentService, accessTokenStrategy]

})
export class AgentModule {}

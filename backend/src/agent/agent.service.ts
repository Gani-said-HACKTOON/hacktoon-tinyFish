import { Injectable } from '@nestjs/common'

@Injectable()
export class AgentService{
    hello(){
        return "hello"
    }
}
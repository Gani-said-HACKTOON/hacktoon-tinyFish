import { Injectable } from '@nestjs/common'
import { readComplianceReports, readActivityLog, readDBFromAgent, writeDBFromAgent } from '@hackathon/database'
import { type userData } from '@hackathon/database/generated/prisma/client/client'

@Injectable()
export class AgentService{
    hello(){
        return "hello"
    }

    async readReport(userId: number){
        return await readComplianceReports(userId)
    }

    async readActivity(userId: number){
        return await readActivityLog(userId)
    }

    async readFromAgent(userId: number, key: keyof userData ){
        return await readDBFromAgent(userId, key )
    }

    async writeFromAgent(userId: number, key: keyof userData, data: any){
        const strdata = JSON.stringify(data);
        await writeDBFromAgent(userId, key, strdata);
    }
}
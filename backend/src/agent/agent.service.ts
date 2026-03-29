import { Injectable } from '@nestjs/common'
import { readComplianceReports, readActivityLog } from '@hackathon/database'

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

    async readFromAgent(){
        
    }
}
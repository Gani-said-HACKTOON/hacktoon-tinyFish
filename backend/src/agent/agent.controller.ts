import { Controller, Get, UseGuards, Req } from '@nestjs/common'
import { AgentService } from './agent.service'
import { AuthGuard } from '@nestjs/passport'
import { type Request } from 'express'
import { type accessTokenType } from '../auth/jwt.strategy'

@Controller("/agent")
export class AgentController {
    constructor (private readonly agentService: AgentService){}

    @Get()
    AgentMain(){
        return this.agentService.hello()
    }

    @UseGuards(AuthGuard("access_token"))
    @Get("compliancereports")
    async complianceReports(@Req() req: Request){
        const accessTokenPayload = req.user as accessTokenType
        return await this.agentService.readReport(accessTokenPayload.sub)
    }

    @UseGuards(AuthGuard("access_token"))
    @Get("activitylogs")
    async activityLogs(@Req() req: Request){
        const accessTokenPayload = req.user as accessTokenType
        return await this.agentService.readActivity(accessTokenPayload.sub)
    }

    @UseGuards(AuthGuard("access_token"))
    @Get("readbyagent")
    async readByAgent(@Req() req: Request){
        const accessTokenPayload = req.user as accessTokenType
        
    }

    @UseGuards(AuthGuard("access_token"))
    @Get("writebyagent")
    async writeByAgent(@Req() req: Request){
        const accessTokenPayload = req.user as accessTokenType
        
    }

}
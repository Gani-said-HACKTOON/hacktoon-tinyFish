import { Controller, Get, UseGuards, Req, Body, Patch, Param } from '@nestjs/common'
import { AgentService } from './agent.service'
import { AuthGuard } from '@nestjs/passport'
import { type Request } from 'express'
import { type accessTokenType } from '../auth/jwt.strategy'
import { userData } from '@hackathon/database/generated/prisma/client/client'

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
    async readByAgent(@Req() req: Request, @Param() param: {key: string}){
        console.log(param)

        const accessTokenPayload = req.user as accessTokenType
        return await this.agentService.readFromAgent( accessTokenPayload.sub, param.key as keyof userData )
    }

    @UseGuards(AuthGuard("access_token"))
    @Patch("writebyagent")
    async writeByAgent(@Req() req: Request, @Body() body: {
        key: keyof userData,
        data: any
    } ){

        console.log(body)
        const accessTokenPayload = req.user as accessTokenType
        return await this.agentService.writeFromAgent( accessTokenPayload.sub, body.key, body.data)
    }

}
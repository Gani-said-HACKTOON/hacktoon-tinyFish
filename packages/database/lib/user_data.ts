import { prisma } from "../index.ts"
import { type userData } from "../generated/prisma/client/index.js"

interface agentDBType{
    regulations: string,
    risk_analysis: string,
    compliance_reports: string,
    policy_enforcements: string,
    activity_log: string
}

async function readUserDataById(userId: number): Promise<userData | null>{
    return await prisma.userData.findUnique({
        where:{
            user_id: userId
        }
    })
}

async function createUserDataTable(userId: number){
    await prisma.userData.create({
        data:{
            user_id: userId,
            regulations: "",
            risk_analysis: "",
            compliance_reports: "",
            policy_enforcements: "",
            activity_log: "",
            report_data: ""
        }
    })
}


async function readComplianceReports(userId: number): Promise<string | undefined>{
    return (await readUserDataById(userId))?.compliance_reports
}

async function readActivityLog(userId: number): Promise<string | undefined>{
    return(await readUserDataById(userId))?.activity_log
}

async function readDBFromAgent(userId: number, key: keyof userData ): Promise<any | null>{
    const data = await readUserDataById(userId)
    if (!data ) return null
    return data[key]
}

async function writeDBFromAgent(userId: number, key: keyof userData, data: string){

    await prisma.userData.update({
        where: {
            user_id: userId
        },
        data:{
            [key] : data
        }
    })
}

export { readComplianceReports, readActivityLog, createUserDataTable, readDBFromAgent, writeDBFromAgent}
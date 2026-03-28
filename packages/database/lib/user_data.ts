import { prisma } from "../index.ts"
import { userData } from "../generated/prisma/client/index.js"

async function readUserDataByEmail(email: string): Promise<userData | null>{
    return await prisma.userData.findUnique({
        where:{
            email: email
        }
    })
}

async function readComplianceReports(email: string): Promise<string | undefined>{
    return (await readUserDataByEmail(email))?.compliance_reports
}

async function readActivityLog(email: string): Promise<string | undefined>{
    return(await readUserDataByEmail(email))?.activity_log
}

export { readComplianceReports, readActivityLog }
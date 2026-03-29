from fastapi import APIRouter, Header
import appServices as service

router = APIRouter()

@router.get('/')
def root():
    return {"message": "Compliance Regulator AI — FastAPI is running ✅"}

@router.post("/api/analyze")
async def api_analyze(data: service.RegulationInput, Authorization: str | None = Header(None)):
    userObj = service.appService(token=Authorization)
    return await userObj.analyze_report(data)

@router.get("/api/monitor")
async def api_get_monitor(Authorization: str | None = Header(None)):
    userObj = service.appService(token=Authorization)
    return await userObj.show_monitor()
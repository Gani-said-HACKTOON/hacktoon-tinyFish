import httpx
import os
from typing import TypedDict

class userDataType(TypedDict):
    regulations: str
    risk_analysis: str
    compliance_reports: str
    policy_enforcements: str
    activity_log: str


DATABASE_API: str = os.getenv("DATABASE_API")

async def write_to_db(key: str, data: str | dict, token: str) -> httpx.Response:
    headers= {
        "Authorization" : token
    }
    
    payload = { 
        "key": key,
        "data": data
    }

    url = os.path.join(DATABASE_API, "writebyagent")

    with httpx.Client() as client:
        response = client.patch(url,headers=headers,json=payload)
        return response


async def read_from_db(key: str, token: str) -> dict:
    headers = {
        "Authorization" : token
    }

    payload = {
        "key" : key
    }

    print(payload)

    url = os.path.join(DATABASE_API, "readbyagent")

    with httpx.Client() as client:
        response = client.get(url, headers=headers ,params=payload)
        return response.text

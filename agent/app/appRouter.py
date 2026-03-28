from fastapi import APIRouter
# import appServices as service

router = APIRouter()

@router.get('/')
def hello():
    return "hello"
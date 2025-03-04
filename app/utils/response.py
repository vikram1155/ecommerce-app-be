from fastapi import HTTPException

def success_response(data, message="Request successful", code=200):
    return {
        "data": data,
        "status": {
            "code": code,
            "message": message
        }
    }

def error_response(message="An error occurred", code=400):
    raise HTTPException(
        status_code=code,
        detail={
            "data": None,
            "status": {
                "code": code,
                "message": message
            }
        }
    )

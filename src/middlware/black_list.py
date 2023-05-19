from fastapi import HTTPException, Request, status


BLACK_LIST = [
    # "127.0.0.1",
    "56.24.15.106"
]

async def check_allowed_ip(request: Request):
    def is_ip_banned(headers):
        is_banned = False
        try:
            real_ip = headers["X-REAL-IP"]
            is_banned = real_ip in BLACK_LIST
        except KeyError:
            is_banned = True
        return is_banned

    if is_ip_banned(request.headers):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
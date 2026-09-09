import time
from fastapi import HTTPException, Request
from collections import defaultdict

rate_limit_store = defaultdict(list)

def rate_limiter(request: Request, max_requests: int = 100, window_seconds: int = 60):
    client_ip = request.client.host
    current_time = time.time()
    
    request_times = rate_limit_store[client_ip]
    request_times = [t for t in request_times if current_time - t < window_seconds]
    rate_limit_store[client_ip] = request_times
    
    if len(request_times) >= max_requests:
        raise HTTPException(
            status_code=429,
            detail="Rate limit exceeded. Try again later."
        )
    
    rate_limit_store[client_ip].append(current_time)
    return True

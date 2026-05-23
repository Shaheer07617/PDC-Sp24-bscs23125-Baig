import time
import asyncio
from fastapi import FastAPI, HTTPException, Request, Response
from pydantic import BaseModel

app = FastAPI()


@app.middleware("http")
async def add_student_id_header(request: Request, call_next):
    response = await call_next(request)
    response.headers["X-Student-ID"] = "BSCS23125" 
    return response

# --- CIRCUIT BREAKER STATE ---
class CircuitBreaker:
    def __init__(self):
        self.failure_count = 0
        self.threshold = 3
        self.is_open = False
        self.last_failure_time = 0
        self.recovery_timeout = 10  # Seconds the circuit stays open

    def call(self):
        if self.is_open:
            if time.time() - self.last_failure_time > self.recovery_timeout:
                print("--- Circuit transitioning to HALF-OPEN ---")
                self.is_open = False
            else:
                return False
        return True

    def record_failure(self):
        self.failure_count += 1
        self.last_failure_time = time.time()
        if self.failure_count >= self.threshold:
            self.is_open = True
            print("--- CIRCUIT OPEN: Stopping LLM calls ---")

    def record_success(self):
        self.failure_count = 0
        self.is_open = False

cb = CircuitBreaker()

# --- MOCK LLM SERVICE ---
async def mock_llm_call():
    # Simulating a hanging/failing service
    await asyncio.sleep(5) # Pretend it's slow
    raise Exception("LLM Timeout Error")

@app.get("/generate")
async def generate_text():
    if not cb.call():
        return {"status": "Fallback", "message": "AI is taking a nap. Try again later."}
    
    try:
        await mock_llm_call()
        cb.record_success()
        return {"status": "Success", "data": "AI Response"}
    except Exception as e:
        cb.record_failure()
        raise HTTPException(status_code=503, detail="LLM Failed")

@app.get("/health")
async def health_check():
    return {"status": "Healthy", "message": "I am responsive!"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
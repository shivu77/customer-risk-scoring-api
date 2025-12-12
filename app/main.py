from fastapi import FastAPI
from app.exceptions.handlers import register_exception_handlers
from app.utils.logger import get_logger
from app.routes.customer_routes import router as customer_router
from app.routes.risk_routes import router as risk_router

def create_app():
    app = FastAPI()
    register_exception_handlers(app)
    return app

app = create_app()

@app.get("/health")
def health():
    return {"status": "ok"}

app.include_router(customer_router, prefix="/customer")
app.include_router(risk_router, prefix="/risk")

log = get_logger("app.main")

@app.middleware("http")
async def log_requests(request, call_next):
    log.info(f"Request: {request.method} {request.url}")
    response = await call_next(request)
    log.info(f"Response Status: {response.status_code}")
    return response

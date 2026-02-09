from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from app.core.config import settings
from app.router.auth import router as auth_router
from app.router.user import router as user_router
from app.db.session import init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Starting up...")
    # Initialize the database
    init_db()
    yield
    print("Shutting down...")


app = FastAPI(title=settings.PROJECT_NAME, lifespan=lifespan)

# Rate Limiting Configuration
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)  # type: ignore


# Global Exception Handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={
            "status": "error",
            "detail": str(exc),
            "type": type(exc).__name__,
        },
    )


# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=(
        settings.CORS_ORIGINS.split(",") if settings.CORS_ORIGINS != "*" else ["*"]
    ),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(auth_router)
app.include_router(user_router)


@app.get("/v1/health", tags=["health"])
def health_check():
    return {"status": "ok"}

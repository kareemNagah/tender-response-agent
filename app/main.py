import pydantic_settings
from sqlalchemy.ext.asyncio import create_async_engine , async_sessionmaker 
from asyncio import asynccontextmanager 
from fastapi import FastAPI , APIRouter
from app.config import get_settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    settings = get_settings()
    app.state.engine = create_async_engine(
        url=settings.database_url.get_secret_value(),
        pool_pre_ping=True
    )
    app.state.sessionmaker = async_sessionmaker(
        bind=app.state.engine,
        expire_on_commit=False
    )
    yield 
    await app.state.engine.dispose()


def create_app() -> FastAPI:

    app = FastAPI(
        title="RFP Agent",
        description="RFP Agent API",
        version="0.1.0",
        lifespan=lifespan
    ) 

    app.include_router(health_router)
    app.include_router(api_v1_router,prefix=f"/api/v1")

    return app 



   
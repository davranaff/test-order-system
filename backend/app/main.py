import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.settings import get_settings
from app.logging_config import setup_logging
from app.dependencies import get_db_client, get_connection_manager

from app.apis import products, orders
from app.websocket import endpoints as ws_endpoints

setup_logging()
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting application...")

    try:

        db_client = get_db_client()
        db_client.admin.command('ping')
        logger.info("MongoDB connection established")


        connection_manager = get_connection_manager()
        logger.info("WebSocket connection manager initialized")

        yield

    except Exception as e:
        logger.error(f"Failed to initialize application: {e}")
        raise

    finally:

        logger.info("Shutting down application...")

        try:
            db_client.close()
            logger.info("MongoDB connection closed")
        except:
            pass

def create_app() -> FastAPI:

    settings = get_settings()

    app = FastAPI(
        title="Restaurant Order Management System",
        description="Production-ready система управления заказами ресторана",
        version="1.0.0",
        lifespan=lifespan,
        docs_url="/docs" if settings.debug else None,
        redoc_url="/redoc" if settings.debug else None
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(products.router, prefix="/api/v1")
    app.include_router(orders.router, prefix="/api/v1")

    app.include_router(ws_endpoints.router)

    @app.exception_handler(HTTPException)
    async def http_exception_handler(request, exc):
        logger.warning(f"HTTP {exc.status_code}: {exc.detail}")
        return JSONResponse(
            status_code=exc.status_code,
            content={"error": exc.detail, "success": False}
        )

    @app.exception_handler(Exception)
    async def general_exception_handler(request, exc):
        logger.error(f"Unhandled exception: {exc}", exc_info=True)
        return JSONResponse(
            status_code=500,
            content={"error": "Internal server error", "success": False}
        )

    @app.get("/")
    async def root():
        return {
            "message": "Restaurant Order Management System API",
            "version": "1.0.0",
            "status": "running"
        }

    @app.get("/ready")
    async def ready():

        try:

            db_client = get_db_client()
            db_client.admin.command('ping')

            return {"status": "ready", "message": "Application is ready to serve requests"}
        except Exception as e:
            logger.error(f"Readiness check failed: {e}")
            return JSONResponse(
                status_code=503,
                content={"status": "not ready", "error": str(e)}
            )

    logger.info("FastAPI application created successfully")
    return app


app = create_app()


if __name__ == "__main__":
    import uvicorn

    settings = get_settings()

    uvicorn.run(
        "main:app",
        host=settings.api_host,
        port=settings.api_port,
        reload=settings.debug,
        log_config=None,
    )

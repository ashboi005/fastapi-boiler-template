from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles #remove if not using html css
from fastapi.templating import Jinja2Templates #remove if not using html css
from mangum import Mangum
import os
from fastapi import HTTPException
from fastapi.responses import HTMLResponse
from fastapi.requests import Request
import logging
from app.core.config import ENVIRONMENT, PROJECT_NAME, API_V1_STR, DATABASE_URL
from app.api.api import api_router

#logs the env variables in development mode
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app, includes prod setup for AWS Lambda
app = FastAPI(
    title="Fast API Boilerplate",
    description="Backend API",
    version="0.1.0",
    root_path="" if ENVIRONMENT == "development" else "/Prod",
    docs_url="/apidocs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",  
    servers=[
        {"url": "Enter your prod url here", "description": "Production Server"},
        {"url": "http://localhost:8000", "description": "Local Development Server"},
    ],
)

# Middleware setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Startup func to log environment variables and check db connection
@app.on_event("startup")
async def startup_db_client():
    """
    Check environment variables and database connection at startup
    """
    logger.info(f"Environment: {ENVIRONMENT}")
    
    if DATABASE_URL:
        logger.info(f"Database URL is set. Starts with: {DATABASE_URL[:20]}...")
    else:
        logger.warning("DATABASE_URL is not set! Using fallback database.")
    
    if os.path.isfile(".env"):
        logger.info(".env file found.")
    else:
        logger.warning(".env file not found in working directory!")
        
    logger.info(f"Current working directory: {os.getcwd()}")
    
    if ENVIRONMENT != "production":
        env_vars = {k: v for k, v in os.environ.items() if "SECRET" not in k and "KEY" not in k and "PASSWORD" not in k}
        logger.info(f"Environment variables: {env_vars}")

# Spotlight UI docs setup
@app.get("/docs", include_in_schema=False)
async def api_documentation(request: Request):
    return HTMLResponse(
        """
<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
    <title>DOCS</title>

    <script src="https://unpkg.com/@stoplight/elements/web-components.min.js"></script>
    <link rel="stylesheet" href="https://unpkg.com/@stoplight/elements/styles.min.css">
  </head>
  <body>

    <elements-api
      apiDescriptionUrl="openapi.json"
      router="hash"
      theme="dark"
    />

  </body>
</html>"""
    )

# Static files and templates setup (remove if not using html css)
if ENVIRONMENT == "development":
    app.mount("/static", StaticFiles(directory="app/static"), name="static")
    templates = Jinja2Templates(directory="app/templates")

# Include API routers
app.include_router(api_router)

@app.get("/")
async def root():
    return {"message": "Welcome to YOUR_PROJECT_NAME API"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

# AWS Lambda handler
handler = Mangum(app)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True) 
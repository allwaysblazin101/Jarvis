import os
import asyncio
from datetime import datetime
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

from database.init_db import init_db
from services.owner_seed_service import seed_owner_cognitive_state
from services.self_awareness_loop import continuous_cognition_daemon
from routes.sms_routes import router as sms_router
from services.proactive_scheduler import proactive_check_loop

# NEW: Import the central brain and scheduler
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from core.brain import brain

load_dotenv()

OWNER_NUMBER = os.getenv("OWNER_NUMBER")

if not OWNER_NUMBER:
    raise Exception("OWNER_NUMBER not set in .env")

app = FastAPI()

# Add CORS middleware (your existing one)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include your SMS router
app.include_router(sms_router)

# Global scheduler instance (Toronto timezone)
scheduler = AsyncIOScheduler(timezone="America/Toronto")

@app.on_event("startup")
async def startup():
    print("🚀 Starting Jarvis AI Backend...")

    # Your existing startup tasks
    init_db()
    try:
        seed_owner_cognitive_state()
    except Exception as e:
        print("Owner seed warning:", e)

    # Start AGI cognition daemon (your existing one)
    # Note: If you have a global _consciousness_task, keep it here
    # asyncio.create_task(continuous_cognition_daemon(OWNER_NUMBER))

    # Schedule the central brain's daily cycle at 6:00 AM ET
    scheduler.add_job(
        brain.daily_cycle,
        'cron',
        hour=6,
        minute=0,
    )
    scheduler.start()
    print("🕒 Daily brain cycle scheduled for 6:00 AM ET")

    # for testing (uncomment when needed)
    # asyncio.create_task(brain.daily_cycle())

    print("🧠 Jarvis Central Brain Online")

@app.get("/ping")
async def ping():
    return {"status": "alive", "time": datetime.utcnow().isoformat()}

@app.get("/")
def home():
    return {"status": "running"}
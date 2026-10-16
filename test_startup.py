import sys
import os

# Append current folder to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

print("Testing imports...")
try:
    from app.config import settings
    from app.database import engine, Base
    from app.models.user import User
    from app.models.project import Project
    from app.models.chatbot import Chatbot
    from app.models.evaluation import EvaluationRun
    from app.models.message import Message
    from app.core.security import get_password_hash, encrypt_api_key, decrypt_api_key
    from app.services.connectors import get_connector
    from app.agents.orchestrator import build_evaluation_graph
    from main import app
    print("Success: All imports resolved successfully!")
except Exception as e:
    print(f"Error during imports check: {e}")
    sys.exit(1)

print("Testing database table creation...")
try:
    Base.metadata.create_all(bind=engine)
    print("Success: Database tables created/verified successfully!")
except Exception as e:
    print(f"Error during DB setup: {e}")
    sys.exit(1)

print("Backend configuration is completely sound!")
sys.exit(0)

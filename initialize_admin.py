import asyncio
from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient
from config.config import Settings
from models.admin import Admin
from passlib.context import CryptContext

hash_helper = CryptContext(schemes=["bcrypt"])

async def init_db():
    client = AsyncIOMotorClient(Settings().MONGODB_URI)
    await init_beanie(database=client[Settings().MONGODB_DB], document_models=[Admin])

async def create_admin(username: str, password: str):
    hashed_password = hash_helper.encrypt(password)
    admin = Admin(username=username, password=hashed_password)
    await admin.insert()
    print(f"Admin {username} created successfully")

async def main():
    await init_db()
    
    await create_admin("admin1", "securepass123")
    await create_admin("admin2", "adminNew")

if __name__ == "__main__":
    asyncio.run(main())
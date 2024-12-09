
from fastapi import Body, Depends, FastAPI, HTTPException, Response
from pydantic import BaseModel, Field, field_validator
from dotenv import load_dotenv
import os
from sqlalchemy import Column, select
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy import String

import uvicorn
import asyncio
class Base(DeclarativeBase):
  pass
class UserModel(Base):
    __tablename__ = "users"

    id:Mapped[int] = mapped_column(autoincrement=True, primary_key=True, index=True)
    name:Mapped[int] = mapped_column(unique=True)
    
class UserSchema(BaseModel):
    id: int
    name: str = Field(alias = "username")
    


load_dotenv()
app = FastAPI()
async_engine = create_async_engine(os.getenv("DATABASE_URL"))
async_session = sessionmaker(
    async_engine, class_=AsyncSession, expire_on_commit=False
)
async def get_session():
  async with async_session() as session:
    yield session
        


@app.post("/api/")
async def root(response: Response, user: UserSchema, session: AsyncSession = Depends(get_session) ):
  # raise HTTPException(status_code=404, detail="Item not found")
  res = await session.scalars(select(UserModel).filter(UserModel.name == user.name))
  return res.all()

async def main():
  async with async_engine.connect() as conn:
    await conn.run_sync(Base.metadata.drop_all)
    await conn.run_sync(Base.metadata.create_all)
    await conn.commit()
  uvicorn.run("main:app", host="localhost", port=8000, reload=True)

if __name__ == "__main__":
  asyncio.run(main())

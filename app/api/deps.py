from collections.abc import AsyncIterator 
from typing import Annotated 

from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Request , Depends

from app.config import get_settings , Settings



async def get_db(request: Request) -> AsyncIterator[AsyncSession]:
    async with request.app.state.sessionmaker() as session:
        yield session




    
# Dependencies 

DbSession = Annotated[AsyncSession , Depends(get_db)]
SettingsDep = Annotated[Settings , Depends(get_settings)]
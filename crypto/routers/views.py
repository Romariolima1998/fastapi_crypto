from asyncio import gather

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import select

from crypto.database.connection import get_session
from crypto.database.models import User, Favorite
from crypto.schema import ( UserCreateSchema, UserCreatePublic,
                            UserFavoriteSchema,UserFavoritePublic,
                            MessageSchema, UserListSchema,
                            DaySummarySchema)
from crypto.request import AssetServices

user_router = APIRouter(prefix='/user',tags=['users'])
assets_router = APIRouter(prefix='/assets', tags=['assets'])

@user_router.post('/create/', status_code=status.HTTP_201_CREATED)
async def user_create(dados: UserCreateSchema, session: AsyncSession = Depends(get_session)) -> UserCreatePublic:
    user = User(dados.name)

    try:
        session.add(user)
        await session.commit()
        await session.refresh(user)

    except SQLAlchemyError as e:
        await session.rollback()  # Faz rollback em caso de erro
        raise HTTPException(status_code=500, detail=str(e))
    
    return user


@user_router.get('/list/')
async def user_list(offset:int = 1, limit: int = 10, session: AsyncSession = Depends(get_session)) -> list[UserListSchema]:
    users = await session.scalars(
        select(User).offset(offset).limit(limit)
    )

    return users.all()


@user_router.delete('/delete/{id}')
async def user_delete(id: int, session: AsyncSession = Depends(get_session)) -> MessageSchema:
    user = await session.scalar(
        select(User).where(User.id == id)
    )

    try:
        await session.delete(user)
        await session.commit()

        if user is None:
            raise HTTPException(status_code=404, detail="User not found")

        return {'message': 'Deleted'}
    
    except SQLAlchemyError as error:
        await session.rollback()
        raise HTTPException(status_code=500, detail=str(error))
    

@user_router.post('/favorite/add', status_code=status.HTTP_201_CREATED)
async def user_favorite_add(dados: UserFavoriteSchema, session: AsyncSession = Depends(get_session)) -> UserFavoritePublic:
    
    favorite = Favorite(symbol=dados.symbol,user_id=dados.user_id)

    try:
        session.add(favorite)
        await session.commit()
        await session.refresh(favorite)

        return favorite

    except SQLAlchemyError as error:
        await session.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(error))


@user_router.delete('/favorite/delete/{id}')
async def user_favorite_delete(id: int, session: AsyncSession = Depends(get_session)) -> MessageSchema:
    user = await session.scalar(
        select(Favorite).where(Favorite.id == id)
    )

    try:
        await session.delete(user)
        await session.commit()

        if user is None:
            raise HTTPException(status_code=404, detail="User not found")

        return {'message': 'Deleted'}
    
    except SQLAlchemyError as error:
        await session.rollback()
        raise HTTPException(status_code=500, detail=str(error))
    

@assets_router.get('/days_summary/{id}')
async def days_summary(id: int, session: AsyncSession = Depends(get_session)) -> list[DaySummarySchema]:
    user = await session.scalar(
            select(User).where(User.id == id)
        )

    favorites_symbol = [ favorite.symbol for favorite in user.favorites]

    try:
        # response = []
        # for symbol in favorites_symbol:
        #     result = await AssetServices.day_sumary(symbol)
        #     response.append(result)
        tasks = [AssetServices().day_sumary(symbol) for symbol in favorites_symbol]
        return await gather(*tasks)
    
    except Exception as error:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail=error)

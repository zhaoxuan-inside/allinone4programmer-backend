from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.item import Item
from app.schemas.item import ItemCreate

class ItemService:
    @staticmethod
    async def create_item(db: AsyncSession, item_in: ItemCreate) -> Item:
        db_item = Item(**item_in.model_dump())
        db.add(db_item)
        await db.commit()
        await db.refresh(db_item)
        return db_item

    @staticmethod
    async def get_item(db: AsyncSession, item_id: int) -> Item | None:
        result = await db.execute(select(Item).where(Item.id == item_id))
        return result.scalar_one_or_none()

    @staticmethod
    async def get_all_items(db: AsyncSession, skip: int = 0, limit: int = 100):
        result = await db.execute(select(Item).offset(skip).limit(limit))
        return result.scalars().all()
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.item import Item
from app.schemas.item import ItemCreate


class ItemService:
    @staticmethod
    async def create_item(db: AsyncSession, item_in: ItemCreate) -> Item:
        # ItemCreate 是一个 Pydantic 模型，
        # .model_dump() 会把 Pydantic 模型转成一个普通字典
        # ** 操作符将字典解包，传递给 Item 构造函数
        db_item = Item(**item_in.model_dump())
        # SQLAlchemy 的会话默认工作在“显式事务”模式（是应用层面，不是数据库层面），
        # db.add() 只是将对象标记为“待插入”，并不会立即发送 SQL，更不会自动提交事务
        db.add(db_item)
        await db.commit()

        # 提交后，数据库可能生成一些默认值（如自增 id、当前时间戳等）。
        # refresh 会执行一次 SELECT 把这些最新数据重新加载到 db_item 对象上，保证返回的实例与数据库完全同步。
        await db.refresh(db_item)
        return db_item

    @staticmethod
    async def get_item(db: AsyncSession, item_id: int) -> Item | None:
        # select(Item).where(Item.id == item_id)
        # 构造一个 SELECT ... FROM items WHERE id = ? 查询对象
        result = await db.execute(select(Item).where(Item.id == item_id))
        return result.scalar_one_or_none()

    @staticmethod
    async def get_all_items(db: AsyncSession, skip: int = 0, limit: int = 100):
        # select(Item).offset(skip).limit(limit)
        # 生成带分页的查询：SELECT ... FROM items LIMIT ? OFFSET ?。
        # skip 是跳过的记录数，limit 是返回的最大行数，非常经典的翻页参数
        result = await db.execute(select(Item).offset(skip).limit(limit))
        return result.scalars().all()


"""
注册发生在 SQLAlchemy 的会话（Session）对象内部。
会话本质上是一个内存中的工作单元（Unit of Work），它维护了以下应用层面的数据结构：
Identity Map（标识映射）：一个字典，保存了当前会话中所有已加载或已创建的对象，以主键为键。
待处理列表（pending list）：记录所有 db.add() 添加的新对象，它们尚未触发任何 SQL。
变更追踪集合：记录哪些对象的哪些属性被修改了（用于后续生成 UPDATE 语句）。
删除队列：记录哪些对象被标记为删除。
"""

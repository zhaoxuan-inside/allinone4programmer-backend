from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.services.item_service import ItemService
from app.schemas.item import ItemCreate, ItemResponse
from app.utils.exceptions import BusinessError

# 创建一个路由器，所有注册到这个 router 的路径操作自动加上 /items 前缀
# tags=["items"] 用于 OpenAPI 文档分类，让这些接口归到 "items" 标签下。
router = APIRouter(prefix="/items", tags=["items"])


@router.post("/", response_model=ItemResponse, status_code=status.HTTP_201_CREATED)
async def create_item(
    item_in: ItemCreate,
    # Depends 是 FastAPI 提供的一个函数，它告诉框架：
    # 请不要让调用方直接传这个参数，而是先自动调用 get_db() 这个函数，把它返回的结果赋值给 db。
    db: AsyncSession = Depends(get_db),
):
    if len(item_in.name) < 2:
        raise BusinessError("Name must be at least 2 characters", 422)
    return await ItemService.create_item(db, item_in)


@router.get("/{item_id}", response_model=ItemResponse)
async def get_item(item_id: int, db: AsyncSession = Depends(get_db)):
    item = await ItemService.get_item(db, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item


@router.get("/", response_model=list[ItemResponse])
async def list_items(
    skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)
):
    return await ItemService.get_all_items(db, skip, limit)

from pydantic import BaseModel


class ItemBase(BaseModel):
    name: str
    description: str | None = None


class ItemCreate(ItemBase):
    pass


class ItemResponse(ItemBase):
    id: int
    # from_attributes = True 表示可以从 ORM 对象自动转换
    model_config = {"from_attributes": True}

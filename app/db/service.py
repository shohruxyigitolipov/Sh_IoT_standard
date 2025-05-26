from collections.abc import Sequence
from typing import Generic

from app.db.repository import RepoType
from app.db.obj_types import SchemaType, ModelType


class BaseService(Generic[RepoType]):
    def __init__(self, repo: type[RepoType]):
        self.repo = repo

    async def create(self, schema: SchemaType) -> ModelType | None:
        return await self.repo.create(schema)

    async def get_by_id(self, model_id) -> ModelType | None:
        return await self.repo.get_by_id(model_id)

    async def list_all(self) -> Sequence[ModelType]:
        return await self.repo.list_all()

    async def delete_by_id(self, model_id) -> bool:
        return await self.repo.delete_by_id(model_id)

    async def update_by_id(self, model_id, schema: SchemaType) -> bool:
        return await self.repo.update_by_id(model_id, schema)


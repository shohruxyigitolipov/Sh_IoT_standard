from typing import TypeVar

from pydantic import BaseModel

from app.db.database import Base
from app.events.emitters import event_bus

ModelType = TypeVar('ModelType', bound=Base)
SchemaType = TypeVar('SchemaType', bound=BaseModel)



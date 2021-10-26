from typing import List, Optional, Type

from pydantic import BaseModel
from sqlalchemy import and_, select
from sqlalchemy.orm import Session

from ..database import Base


class DatabaseManager:
    def __init__(self, session: Session):
        self.session = session

    def get_instance(self, class_: Type[Base], instance_id: int) -> Optional[Base]:
        return self.session.get(class_, instance_id)

    def get_instances(
        self,
        class_: Type[Base],
        filters: list = None,
        offset: int = None,
        limit: int = None,
    ) -> List[Base]:
        stmt = select(class_)

        if filters:
            stmt = stmt.where(and_(*filters))

        if offset:
            stmt = stmt.offset(offset)

        if limit:
            stmt = stmt.limit(limit)

        return self.session.execute(stmt).scalars().all()

    def find_instance(self, class_: Type[Base], filters: list = None) -> Base:
        stmt = select(class_)

        if filters:
            stmt = stmt.where(and_(*filters))

        stmt = stmt.limit(1)

        return self.session.execute(stmt).scalars().first()

    def create_instance(self, class_: Type[Base], data: BaseModel) -> Base:
        instance = class_(**data.dict())
        self.session.add(instance)
        self.session.commit()
        self.session.refresh(instance)
        return instance

    def update_instance(self, class_: Type[Base], instance_id: int, data: BaseModel) -> Base:
        if instance := self.get_instance(class_, instance_id):
            for key, value in data:
                if hasattr(instance, key):
                    setattr(instance, key, value)
            self.session.add(instance)
            self.session.commit()
            self.session.refresh(instance)
        return instance

    def delete_instance(self, class_: Type[Base], instance_id: int) -> Base:
        if instance := self.get_instance(class_, instance_id):
            self.session.delete(instance)
            self.session.commit()
        return instance

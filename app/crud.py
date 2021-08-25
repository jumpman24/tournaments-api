from typing import List, Type

from pydantic import BaseModel
from sqlalchemy import and_, select
from sqlalchemy.orm import Session

from .database import Base


def get_instance(db: Session, class_: Type[Base], instance_id: int) -> Base:
    return db.get(class_, instance_id)


def get_instances(
    db: Session,
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

    return db.execute(stmt).scalars().all()


def create_instance(db: Session, class_: Type[Base], data: BaseModel) -> Base:
    instance = class_(**data.dict())
    db.add(instance)
    db.commit()
    db.refresh(instance)
    return instance


def update_instance(db: Session, class_: Type[Base], instance_id: int, data: BaseModel) -> Base:
    if instance := get_instance(db, class_, instance_id):
        for key, value in data:
            if hasattr(instance, key):
                setattr(instance, key, value)
        db.add(instance)
        db.commit()
        db.refresh(instance)
    return instance


def delete_instance(db: Session, class_: Type[Base], instance_id: int) -> Base:
    if instance := get_instance(db, class_, instance_id):
        db.delete(instance)
        db.commit()
    return instance

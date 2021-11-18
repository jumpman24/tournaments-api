from typing import List, Type, TypeVar

from sqlmodel import Session, SQLModel, and_, select

from .loggers import logger


_SQLModel = TypeVar("_SQLModel")


def get_instances(
    db: Session,
    class_: Type[_SQLModel],
    *,
    filters: list = None,
) -> List[_SQLModel]:
    stmt = select(class_)

    if filters:
        stmt = stmt.where(and_(*filters))

    return db.execute(stmt).scalars().all()


def create_instance(db: Session, instance: _SQLModel) -> _SQLModel:
    logger.info(f"Creating instance {repr(instance)}")
    db.add(instance)
    db.commit()
    db.refresh(instance)
    return instance


def update_instance(
    db: Session, class_: Type[_SQLModel], instance_id: int, data: SQLModel
) -> _SQLModel:
    if instance := db.get(class_, instance_id):
        logger.info(f"Updating instance {repr(instance)}")
        for key, value in data:
            if hasattr(instance, key):
                setattr(instance, key, value)
        db.add(instance)
        db.commit()
        db.refresh(instance)
    return instance


def delete_instance(
    db: Session, class_: Type[_SQLModel], instance_id: int
) -> _SQLModel:
    if instance := db.get(class_, instance_id):
        logger.info(f"Deleting instance {repr(instance)}")
        db.delete(instance)
        db.commit()
    return instance

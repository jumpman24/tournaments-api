from sqlalchemy import create_engine
from sqlalchemy.orm import registry, sessionmaker

from app.settings import settings


mapper_reg = registry()
Base = mapper_reg.generate_base()

connect_args = {}
if settings.database_url.startswith("sqlite"):
    connect_args["check_same_thread"] = False

engine = create_engine(settings.database_url, connect_args=connect_args)
SessionLocal = sessionmaker(engine, expire_on_commit=False)

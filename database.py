from typing import Optional
from sqlmodel import Field, SQLModel, create_engine

class Task(SQLModel, table=True):
    __tablename__ = "tasks"

    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(nullable=False)
    due_date: Optional[str] = Field(default=None)
    status: str = Field(default="pending", nullable=False)
    priority: str = Field(nullable=False)


DB_NAME = "to_do.db"
sqlite_url = f"sqlite:///{DB_NAME}"

engine = create_engine(sqlite_url, echo=True)


def create_tables():
    SQLModel.metadata.create_all(engine)


if __name__ == "__main__":
    create_tables()


from datetime import datetime, UTC
from sqlalchemy import DateTime
from sqlalchemy.orm import Mapped, mapped_column
from user_service.app.database import Base

class User(Base):
    __tablename__ = "users"

    email: Mapped[str] = mapped_column(unique=True, index=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(nullable=False)
    username: Mapped[str] = mapped_column(unique=True, nullable=True)
    firstname: Mapped[str] = mapped_column(nullable=True)
    is_admin: Mapped[bool] = mapped_column(nullable=False, default=False, server_default="false")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(UTC))

    def __repr__(self):
        return f"<User(id={self.id}, email={self.email}, username={self.username}, firstname={self.firstname})>"
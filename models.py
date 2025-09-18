from sqlalchemy import Integer, String



from sqlalchemy.orm import Mapped, mapped_column




from database import Base

class Recipe(Base):
    __tablename__ = 'recipes'

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(20), nullable=False)
    ingredients: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(nullable=False)
    cooking_time: Mapped[int] = mapped_column(nullable=False, index=True)
    show_count: Mapped[int] = mapped_column(default=0, index=True)

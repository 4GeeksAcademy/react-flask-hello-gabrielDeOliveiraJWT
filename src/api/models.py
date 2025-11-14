from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, ForeignKey, Column, Table, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship

db = SQLAlchemy()

favorite_character = Table(
    "favorite_character",
    db.Model.metadata,
    Column("user_id", ForeignKey("user.id")),
    Column("character_id", ForeignKey("character.id"))
)

favorite_sith = Table(
    "favorite_sith",
    db.Model.metadata,
    Column("user_id", ForeignKey("user.id")),
    Column("sith_id", ForeignKey("sith.id"))
)

favorite_starship = Table(
    "favorite_starship",
    db.Model.metadata,
    Column("user_id", ForeignKey("user.id")),
    Column("starship_id", ForeignKey("starship.id"))
)

class User(db.Model):
    __tablename__ = "user"
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(80), nullable=False, unique=True)
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean(), nullable=False, default=True)

    characters: Mapped[list["Character"]] = relationship(secondary=favorite_character)
    siths: Mapped[list["Sith"]] = relationship(secondary=favorite_sith)
    starships: Mapped[list["Starship"]] = relationship(secondary=favorite_starship)

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email
        }

class Character(db.Model):
    __tablename__ = "character"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30), nullable=False)
    img: Mapped[str] = mapped_column(String(255), nullable=False)

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "img": self.img
        }

class Starship(db.Model):
    __tablename__ = "starship"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30), nullable=False)
    img: Mapped[str] = mapped_column(String(255), nullable=False)

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "img": self.img
        }

class Sith(db.Model):
    __tablename__ = "sith"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30), nullable=False)
    img: Mapped[str] = mapped_column(String(255), nullable=False)

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "img": self.img
        }
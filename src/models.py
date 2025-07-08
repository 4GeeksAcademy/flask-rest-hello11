from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

db = SQLAlchemy()

class Usuario(db.Model):
    __tablename__= "usuario"
    id: Mapped[int] = mapped_column(Integer, primary_Key=True)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    nickname: Mapped[str] = mapped_column(String(100), nullable=False)

    favoritos: Mapped[list["Favorito"]] = relationship("Favorito", back_populates="usuario")

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
            "nickname": self.nickname
        }


class planeta(db.Model):
    __tablename__= "planeta"
    id: Mapped[int] = mapped_column(primary_Key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str] = mapped_column(String(250), nullable=False)
    rotation: Mapped[int] = mapped_column(Integer)

    personajes: Mapped[list["Personaje"]] = relationship("personaje", back_populates="planeta")

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description
            }

class Personaje(db.Model):
    __tablename__= "personaje"
    id: Mapped[int] = mapped_column(primary_Key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str] = mapped_column(String(500), nullable=False)
    planeta_id:Mapped[int] = mapped_column(Integer, ForeignKey("planeta.id"))

    planeta: Mapped["planeta"] = relationship("planeta", back_populates="personajes")

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "nickname": self.nickname
        }

class Favorito(db.Model):
    __tablename__= "favorito"
    id: Mapped[int] = mapped_column(primary_Key=True)
    usuario_id: Mapped[int] = mapped_column(Integer, ForeignKey("usuario.id"), nullable=False)
    planeta_id : Mapped[int] = mapped_column(Integer, ForeignKey("planeta.id"), nullable=True)
    personaje_id : Mapped[int] = mapped_column(Integer, ForeignKey("personaje.id"), nullable=True)

    usuario: Mapped["Usuario"] = relationship("usuario", back_populates="favoritos")
    planeta: Mapped["planeta"] = relationship("planeta")
    personaje: Mapped["Personaje"] = relationship("personaje")

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "nickname": self.nickname
        }
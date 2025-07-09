from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Integer, String, DateTime, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime

db = SQLAlchemy()

class Usuario(db.Model):
    __tablename__ = "usuario"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    nombre_usuario: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    correo_electronico: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    contraseña_hash: Mapped[str] = mapped_column(String(128), nullable=False)
    nombre_completo: Mapped[str] = mapped_column(String(100), nullable=True)
    biografia: Mapped[str] = mapped_column(Text, nullable=True)
    url_imagen_perfil: Mapped[str] = mapped_column(String(255), nullable=True)
    fecha_creacion: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    publicaciones: Mapped[list["Publicacion"]] = relationship("Publicacion", back_populates="usuario", cascade="all, delete-orphan")
    comentarios: Mapped[list["Comentario"]] = relationship("Comentario", back_populates="usuario", cascade="all, delete-orphan")
    me_gustas: Mapped[list["MeGusta"]] = relationship("MeGusta", back_populates="usuario", cascade="all, delete-orphan")
    siguiendo: Mapped[list["Seguimiento"]] = relationship("Seguimiento", foreign_keys="Seguimiento.seguidor_id", back_populates="seguidor", cascade="all, delete-orphan")
    seguidores: Mapped[list["Seguimiento"]] = relationship("Seguimiento", foreign_keys="Seguimiento.seguido_id", back_populates="seguido", cascade="all, delete-orphan")

    def serialize(self):
        return {
            "id": self.id,
            "nombre_usuario": self.nombre_usuario,
            "correo_electronico": self.correo_electronico,
            "nombre_completo": self.nombre_completo,
            "biografia": self.biografia,
            "url_imagen_perfil": self.url_imagen_perfil,
            "fecha_creacion": self.fecha_creacion.isoformat()
        }


class Publicacion(db.Model):
    __tablename__="publicacion"
    id: Mapped[int] =  mapped_column(Integer, primary_Key=True)
    usuario_id: Mapped[int] = mapped_column(Integer, ForeignKey("usuario.id"), nullable=False)
    url_imagen: Mapped[str] = mapped_column(String(255), nullable=True)
    descripcion: Mapped[str] = mapped_column(Text, nullable=True)
    fecha_creacion: Mapped[datetime] = mapped_column(datetime, default=datetime.utcnow)

    usuario: Mapped[Usuario] =relationship("Usuario", back_populates="publicaciones")
    comentarios: Mapped[list["Comentario"]] = relationship("comentario", back_populates="publicacion", cascade="all, delete-orphan")
    me_gustas: Mapped[list[MeGusta]] =relationship("MeGusta", back_populates="publicacion", cascade="all, delete-orphan")


    def serialize(self):
        return {
            "id": self.id,
            "usuario_id": self.usuario_id,
            "url_imagen": self.url_imagen,
            "description": self.description,
            "fecha_creacion": self.fecha_creacion.isoformat()
            }

class Comentario(db.Model):
    __tablename__= "comentario"
    id: Mapped[int] =  mapped_column(Integer, primary_Key=True)
    publicacion_id: Mapped[int] = mapped_column(Integer, ForeignKey("publicacion.id"), nullable=False)
    usuario_id: Mapped[int] = mapped_column(Integer, ForeignKey("usuario.id"), nullable=False)
    contenido: Mapped[str] = mapped_column(Text, nullable=True)
    fecha_creacion: Mapped[datetime] = mapped_column(datetime, default=datetime.utcnow)

    publicacion: Mapped[Publicacion] = relationship("publicacion",backpopulates="comentarios")
    usuario: Mapped[Usuario] =relationship("Usuario", back_populates="comentarios")

    def serialize(self):
        return {
            "id": self.id,
            "publicacion_id": self.publicacion_id,
            "usuario_id": self.usuario_id,
            "contenido": self.contenido,
            "fecha_creacion": self.fecha_creacion.isoformat()
        }

class MeGusta(db.Model):
    __tablename__= "Me_gusta"
    id: Mapped[int] =  mapped_column(Integer, primary_Key=True)
    publicacion_id: Mapped[int] = mapped_column(Integer, ForeignKey("publicacion.id"), nullable=False)
    usuario_id: Mapped[int] = mapped_column(Integer, ForeignKey("usuario.id"), nullable=False)
    fecha_creacion: Mapped[datetime] = mapped_column(datetime, default=datetime.utcnow)

    publicacion: Mapped[Publicacion] = relationship("publicacion",backpopulates="me_gustas")
    usuario: Mapped[Usuario] =relationship("Usuario", back_populates="me_gustas")

    def serialize(self):
        return {
            "id": self.id,
            "publicacion_id": self.publicacion_id,
            "usuario_id": self.usuario_id,
            "fecha_creacion": self.fecha_creacion.isoformat()
        }
    
class Seguir(db.Model):
    __tablename__="seguir"
    id: Mapped[int] =  mapped_column(Integer, primary_Key=True)
    seguidor_id: Mapped[int] = mapped_column(Integer, ForeignKey("usuario.id"), nullable=False)
    seguido_id: Mapped[int] = mapped_column(Integer, ForeignKey("usuario.id"), nullable=False)
    fecha_creacion: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    seguidor: Mapped[Usuario] = relationship("Usuario", foreign_keys=[seguidor_id], back_populates="siguiendo")
    seguido: Mapped[Usuario] = relationship("Usuario", foreign_keys=[seguidor_id], back_populates="seguidores")

    def serialize(self):
        return {
            "id": self.id,
            "seguidor_id": self.seguidor_id,
            "seguido_id": self.seguido_id,
            "fecha_creacion": self.fecha_creacion.isoformat()
        }

"""DB connection and ORM models for the application."""

from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
    DateTime,
    ForeignKey,
    Enum,
)
from sqlalchemy.orm import sessionmaker, relationship, scoped_session
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.pool import QueuePool

engine = create_engine(
    "mysql+pymysql://cc5002:programacionweb@localhost:3306/tarea2",
    poolclass=QueuePool,
    pool_size=10,
    max_overflow=20,
    pool_pre_ping=True,
    pool_recycle=3600,
)

session_factory = sessionmaker(bind=engine)
Session = scoped_session(session_factory)

Base = declarative_base()


class Region(Base):
    """Modelo ORM para regiones"""

    __tablename__ = "region"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(200), nullable=False)

    # Relationships
    comunas = relationship("Comuna", back_populates="region")


class Comuna(Base):
    """Modelo ORM para comunas"""

    __tablename__ = "comuna"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(200), nullable=False)
    region_id = Column(Integer, ForeignKey("region.id"), nullable=False)

    # Relationships
    region = relationship("Region", back_populates="comunas")
    actividades = relationship("Actividad", back_populates="comuna")


class Actividad(Base):
    """Modelo ORM para actividades"""

    __tablename__ = "actividad"

    id = Column(Integer, primary_key=True, autoincrement=True)
    comuna_id = Column(Integer, ForeignKey("comuna.id"), nullable=False)
    sector = Column(String(100))
    nombre = Column(String(200), nullable=False)
    email = Column(String(100), nullable=False)
    celular = Column(String(15))
    dia_hora_inicio = Column(DateTime, nullable=False)
    dia_hora_termino = Column(DateTime)
    descripcion = Column(String(500))

    # Relationships
    comuna = relationship("Comuna", back_populates="actividades")
    fotos = relationship("Foto", back_populates="actividad")
    temas = relationship("ActividadTema", back_populates="actividad")
    contactos = relationship("ContactarPor", back_populates="actividad")


class Foto(Base):
    """Modelo ORM para fotos"""

    __tablename__ = "foto"

    id = Column(Integer, primary_key=True, autoincrement=True)
    ruta_archivo = Column(String(300), nullable=False)
    nombre_archivo = Column(String(300), nullable=False)
    actividad_id = Column(Integer, ForeignKey("actividad.id"), nullable=False)

    # Relationships
    actividad = relationship("Actividad", back_populates="fotos")


class ContactarPor(Base):
    """Modelo ORM para metodos de contacto"""

    __tablename__ = "contactar_por"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(
        Enum(
            "whatsapp",
            "telegram",
            "X",
            "instagram",
            "tiktok",
            "otra",
            name="contacto_tipo",
        ),
        nullable=False,
    )
    identificador = Column(String(150), nullable=False)
    actividad_id = Column(Integer, ForeignKey("actividad.id"), nullable=False)

    # Relationships
    actividad = relationship("Actividad", back_populates="contactos")


class ActividadTema(Base):
    """Modelo ORM para temas de actividades"""

    __tablename__ = "actividad_tema"

    id = Column(Integer, primary_key=True, autoincrement=True)
    tema = Column(
        Enum(
            "música",
            "deporte",
            "ciencias",
            "religión",
            "política",
            "tecnología",
            "juegos",
            "baile",
            "comida",
            "otro",
            name="tema_tipo",
        ),
        nullable=False,
    )
    glosa_otro = Column(String(15))
    actividad_id = Column(Integer, ForeignKey("actividad.id"), nullable=False)

    # Relationships
    actividad = relationship("Actividad", back_populates="temas")


# Create all tables
Base.metadata.create_all(engine)

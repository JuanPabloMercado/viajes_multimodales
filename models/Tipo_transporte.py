from .imports import * 
from .base import Base 
from .conexion_db import *


class Tipo_transporte(Base):
    __tablename__ = 'Tipo_transporte'
    
    id_tipo_transporte = Column(Integer, primary_key=True, autoincrement=True)
    nombre_tipo = Column(Enum('Avión', 'Tren', 'Colectivo Interurbano', 'Automóvil', 'Taxi', 'Caminata'), nullable=False)
    descripcion = Column(String(200), nullable=True)
    
    #Relación hacia Medios_transporte
    medios_transporte_relacion = relationship('Medios_transporte', back_populates='tipo_transporte_relacion')
    
    
    
    @classmethod
    def insertar_tipo_transporte(cls, nombre_tipo, descripcion=None):
        with SessionLocal() as session: 
            try:
                nuevo_tipo = cls(
                    nombre_tipo=nombre_tipo,
                    descripcion=descripcion
                )
                session.add(nuevo_tipo)
                session.commit()
                return nuevo_tipo.id_tipo_transporte
            except Exception as e:
                session.rollback()
                print(f"Error al insertar tipo de transporte: {e}")
                return None














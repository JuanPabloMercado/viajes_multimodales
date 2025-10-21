from .imports import * 
from .base import Base 
from .conexion_db import *



class Costos_transporte(Base):
    __tablename__ = 'Costos_transporte'
    
    id_costos_transporte = Column(Integer, primary_key=True, autoincrement=True)
    costo_base = Column(Numeric(10, 2), nullable=False)
    
    
    #Relación hacia Medios_transporte
    medios_transporte_relacion = relationship('Medios_transporte', back_populates='costos_transporte_relacion')
    
    
    @classmethod
    def insertar_costo_transporte(cls, costo_base):
        with SessionLocal() as session: 
            try:
                nuevo_costo = cls(
                    costo_base=costo_base
                )
                session.add(nuevo_costo)
                session.commit()
                return nuevo_costo.id_costos_transporte
            except Exception as e:
                session.rollback()
                print(f"Error al insertar costo de transporte: {e}")
                return None
           

















from .imports import * 
from .base import Base 
from .conexion_db import *


class Costos_destinos_especificos(Base):
    __tablename__ = 'Costos_destinos_especificos'
    
    id_costos_destinos_especificos = Column(Integer, primary_key=True, autoincrement=True)
    costo_base = Column(Numeric(10, 2), nullable=False)
    
    #Relación a la tabla Destinos_especificos
    destinos_especificos_relacion = relationship('Destinos_especificos', back_populates='costos_destinos_especificos_relacion')
    
    @classmethod
    def crear_costo_destino_especifico(cls, costo_base: float):
        with SessionLocal() as session:
            try:
                nuevo_costo = Costos_destinos_especificos(costo_base=costo_base)
                session.add(nuevo_costo)
                session.commit()
                print(f'Costo de destino específico creado con éxito. Id: {nuevo_costo.id_costos_destinos_especificos}')
            except Exception as e:
                session.rollback()
                print(f'Error al crear el costo de destino específico. Error: {e}')
























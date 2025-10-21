from .imports import * 
from .base import Base 
from .conexion_db import *



class Costos_destinos_generales(Base):
    __tablename__ = 'Costos_destinos_generales'
    
    id_costos_destinos_generales = Column(Integer, primary_key=True, autoincrement=True)
    costo_base = Column(Numeric(10, 2), nullable=False)
    
    #Relación a la tabla Destinos_generales
    destinos_generales_relacion = relationship('Destinos_generales', back_populates='costos_destinos_generales_relacion')

    @classmethod
    def crear_costo_destino_general(cls, costo_base: float):
        with SessionLocal() as session:
            try:
                nuevo_costo = Costos_destinos_generales(costo_base=costo_base)
                session.add(nuevo_costo)
                session.commit()
                print(f'Costo de destino general creado con éxito. Id: {nuevo_costo.id_costos_destinos_generales}')
            except Exception as e:
                session.rollback()
                print(f'Error al crear el costo de destino general. Error: {e}')

















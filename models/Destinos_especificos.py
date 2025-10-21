from .imports import * 
from .base import Base 
from .conexion_db import *


class Destinos_especificos(Base):
    __tablename__ = 'Destinos_especificos'
    
    id_destinos_especificos = Column(Integer, primary_key=True, autoincrement=True)
    hora_inicio = Column(DateTime, nullable=False)
    hora_fin = Column(DateTime, nullable=False)
    detalles = Column(String(100), nullable=False)
    
    #Definción de las claves foráneas
    id_costos_destinos_especificos = Column(Integer, ForeignKey('Costos_destinos_especificos.id_costos_destinos_especificos'), nullable=False)
    id_destinos_generales = Column(Integer, ForeignKey('Destinos_generales.id_destinos_generales'), nullable=False)
    
    #Relaciones hacia las tablas principales.
    costos_destinos_especificos_relacion = relationship('Costos_destinos_especificos', back_populates='destinos_especificos_relacion')
    destinos_generales_relacion = relationship('Destinos_generales', back_populates='destinos_especificos_relacion')
    
    #Relación a la tabla itinerario_destinos
    itinerario_destinos_relacion = relationship('Itinerario_destinos', back_populates='destinos_especificos_relacion')

    @classmethod
    def crear_destino_especifico(cls, hora_inicio: datetime, hora_fin: datetime, detalles: str, id_costo_destino_especifico: int, id_destino_general: int):
        with SessionLocal() as session:
            try:
                nuevo_destino = Destinos_especificos(
                    hora_inicio=hora_inicio,
                    hora_fin=hora_fin,
                    detalles=detalles,
                    id_costos_destinos_especificos=id_costo_destino_especifico,
                    id_destinos_generales=id_destino_general
                )
                session.add(nuevo_destino)
                session.commit()
                print(f'Destino específico creado con éxito. Id: {nuevo_destino.id_destinos_especificos}')
            except Exception as e:
                session.rollback()
                print(f'Error al crear el destino específico. Error: {e}')



    














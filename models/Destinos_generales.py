from .imports import * 
from .base import Base 
from .conexion_db import *


class Destinos_generales(Base):
    __tablename__ = 'Destinos_generales'
    
    id_destinos_generales = Column(Integer, primary_key=True, autoincrement=True)
    nombre_destino = Column(String(100), nullable=False, unique=True)
    
    #Definción de las claves foráneas
    id_ciudades = Column(Integer, ForeignKey('Ciudades.id_ciudades'), nullable=False)
    id_costos_destinos_generales = Column(Integer, ForeignKey('Costos_destinos_generales.id_costos_destinos_generales'), nullable=False)

    #Relaciones hacia las tablas principales.
    ciudades_relacion = relationship('Ciudades', back_populates='destinos_generales_relacion')
    costos_destinos_generales_relacion = relationship('Costos_destinos_generales', back_populates='destinos_generales_relacion')
    
    #Relación a la tabla Destinos_especificos
    destinos_especificos_relacion = relationship('Destinos_especificos', back_populates='destinos_generales_relacion')
    #Relación a la tabla Itinerario_destinos
    itinerario_destinos_relacion = relationship('Itinerario_destinos', back_populates='destinos_generales_relacion')

    @classmethod
    def crear_destino_general(cls, nombre_destino: str, id_ciudad: int, id_costo_destino_general: int):
        with SessionLocal() as session:
            try:
                nuevo_destino = Destinos_generales(
                    nombre_destino=nombre_destino,
                    id_ciudades=id_ciudad,
                    id_costos_destinos_generales=id_costo_destino_general
                )   
                    
                session.add(nuevo_destino)
                session.commit()
                print(f'Destino general {nombre_destino} creado con éxito. Id: {nuevo_destino.id_destinos_generales}')
            except Exception as e:
                session.rollback()
                print(f'Error al crear el destino general. Error: {e}')










from .imports import * 
from .base import Base 
from .conexion_db import *


class Ciudades(Base):
    __tablename__ = 'Ciudades'
    
    id_ciudades = Column(Integer, primary_key=True, autoincrement=True)
    nombre_ciudad = Column(String(100), nullable=False)
    
    #Definición de las claves foráneas
    id_provincias = Column(Integer, ForeignKey('Provincias.id_provincias'), nullable=False)
    
    #Relación a la tabla Provincias
    provincias_relacion = relationship('Provincias', back_populates='ciudades_relacion')
    #Relación a la tabla Destinos_generales
    destinos_generales_relacion = relationship('Destinos_generales', back_populates='ciudades_relacion')

    @classmethod
    def crear_ciudad(cls, nombre_ciudad: str, id_provincia: int):
        with SessionLocal() as session:
            try:
                nueva_ciudad = Ciudades(
                    nombre_ciudad=nombre_ciudad,
                    id_provincias=id_provincia
                )
                session.add(nueva_ciudad)
                session.commit()
                print(f'Ciudad {nombre_ciudad} creada con éxito. Id: {nueva_ciudad.id_ciudades}')
            except Exception as e:
                session.rollback()
                print(f'Error al crear la ciudad. Error: {e}')
















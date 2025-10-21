from .imports import * 
from .base import Base 
from .conexion_db import *

class Provincias(Base):
    __tablename__ = 'Provincias'
    
    id_provincias = Column(Integer, primary_key=True, autoincrement=True)
    nombre_provincia = Column(String(100), nullable=False, unique=True)
    
    #Definción de las claves foráneas
    id_paises = Column(Integer, ForeignKey('Paises.id_paises'), nullable=False)
    
    #Relación a la tabla Paises
    paises_relacion = relationship('Paises', back_populates='provincias_relacion')
    #Relación a la tabla Ciudades
    ciudades_relacion = relationship('Ciudades', back_populates='provincias_relacion')

    @classmethod
    def crear_provincia(cls, nombre_provincia: str, id_pais: int):
        with SessionLocal() as session:
            try:
                nueva_provincia = Provincias(
                    nombre_provincia=nombre_provincia,
                    id_paises=id_pais
                )
                session.add(nueva_provincia)
                session.commit()
                print(f'Provincia {nombre_provincia} creada con éxito. Id: {nueva_provincia.id_provincias}')
            except Exception as e:
                session.rollback()
                print(f'Error al crear la provincia. Error: {e}')















from .imports import * 
from .base import Base 
from .conexion_db import *


class Paises(Base):
    __tablename__ = 'Paises'
    
    id_paises = Column(Integer, primary_key=True, autoincrement=True)
    nombre_pais = Column(String(100), nullable=False, unique=True)
    
    #Relación a la tabla Provincias
    provincias_relacion = relationship('Provincias', back_populates='paises_relacion')

    @classmethod
    def crear_pais(cls, nombre_pais: str):
        with SessionLocal() as session:
            try:
                nuevo_pais = Paises(nombre_pais=nombre_pais)
                session.add(nuevo_pais)
                session.commit()
                print(f'País {nombre_pais} creado con éxito. Id: {nuevo_pais.id_paises}')
            except Exception as e:
                session.rollback()
                print(f'Error al crear el país. Error: {e}')
    














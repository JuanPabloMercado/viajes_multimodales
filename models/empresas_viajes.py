from .imports import * 
from .base import Base 


class Empresas_viajes(Base):
    __tablename__ = 'Empresas_viajes'
    
    #Definicion de la clave primaria compuesta
    id_viajes = Column(Integer, ForeignKey('Viajes.id_viajes'), primary_key=True, nullable=False)
    id_empresas = Column(Integer, ForeignKey('Empresas.id_empresas'), primary_key=True, nullable=False)

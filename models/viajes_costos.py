from .imports import * 
from .base import Base 

class Viajes_costos(Base):
    __tablename__ = 'Viajes_costos'
    
    #Definicion de la clave primaria compuesta
    id_costos_viajes = Column(Integer, ForeignKey('Costos_viajes.id_costos_viajes'), primary_key=True, nullable=False)
    id_viajes = Column(Integer, ForeignKey('Viajes.id_viajes'), primary_key=True, nullable=False)

    




















from imports import *

class Viajes_costos(Base):
    __tablename__ = 'Viajes_Costos'
    
    #Definicion de la clave primaria compuesta
    id_costos_viajes = Column(Integer, ForeignKey('costos_viajes.id_costos_viajes'), primary_key=True, nullable=False)
    id_viajes = Column(Integer, ForeignKey('viajes.id_viajes'), primary_key=True, nullable=False)

    




















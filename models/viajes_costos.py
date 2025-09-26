from imports import *

class Viajes_costos(Base):
    __tablename__ = 'Viajes_Costos'
    
    #Definicion de la clave primaria compuesta
    id_costos_viajes = Column(Integer, ForeignKey('costos_viajes.id_costos_viajes'), primary_key=True, nullable=False)
    id_viajes = Column(Integer, ForeignKey('viajes.id_viajes'), primary_key=True, nullable=False)

    #Relaciones hacia las tablas principales.
    viajes_relacion = relationship('Viajes', back_populates='viajes_costos_relacion')
    costos_viajes_relacion = relationship('Costos_viajes', back_populates='viajes_costos_relacion')





















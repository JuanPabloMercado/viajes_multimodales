from imports import *


class Destinos_generales(Base):
    __tablename__ = 'Destinos_Generales'
    
    id_destinos_generales = Column(Integer, primary_key=True, autoincrement=True)
    nombre_destino = Column(String(100), nullable=False, unique=True)
    
    #Definción de las claves foráneas
    id_ciudades = Column(Integer, ForeignKey('Ciudades.id_ciudades'), nullable=False)
    id_costos_destinos_generales = Column(Integer, ForeignKey('Costos_destinos_generales.id_costos_destinos_generales'), nullable=False)

    #Relaciones hacia las tablas principales.
    ciudades_relacion = relationship('Ciudades', back_populates='destinos_generales_relacion')
    costos_destinos_generales_relacion = relationship('Costos_destinos_generales', back_populates='destinos_generales_relacion')
    
    #Relación a la tabla Destinos_especificos
    destinos_especificos_relacion = relationship('Destinos_Especificos', back_populates='destinos_generales_relacion')
    #Relación a la tabla Itinerario_destinos
    itinerario_destinos_relacion = relationship('Itinerario_destinos', back_populates='destinos_generales_relacion')












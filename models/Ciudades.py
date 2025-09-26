from imports import *

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



















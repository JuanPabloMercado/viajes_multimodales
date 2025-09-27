from imports import *

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

















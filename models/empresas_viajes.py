from imports import *

class Empresas_viajes(Base):
    __tablename__ = 'Empresas_Viajes'
    
    #Definicion de la clave primaria compuesta
    id_viajes = Column(Integer, ForeignKey('viajes.id_viajes'), primary_key=True, nullable=False)
    id_empresas = Column(Integer, ForeignKey('empresas.id_empresas'), primary_key=True, nullable=False)
    
    #Relaciones hacia las tablas principales.
    viajes_relacion = relationship('Viajes', back_populates='empresas_viajes_relacion')
    empresas_relacion = relationship('Empresas', back_populates='empresas_viajes_relacion')
    
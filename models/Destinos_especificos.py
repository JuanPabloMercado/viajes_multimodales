from imports import *

class Destinos_especificos(Base):
    __tablename__ = 'Destinos_Especificos'
    
    id_destinos_especificos = Column(Integer, primary_key=True, autoincrement=True)
    hora_inicio = Column(DateTime, nullable=False)
    hora_fin = Column(DateTime, nullable=False)
    
    #Definción de las claves foráneas
    id_costos_destinos_especificos = (Integer, ForeignKey('Costos_destinos_especificos.id_costos_destinos_especificos'), nullable=False)
    id_destinos_generales = (Integer, ForeignKey('Destinos_generales.id_destinos_generales'), nullable=False)
    
    #Relaciones hacia las tablas principales.
    costos_destinos_especificos_relacion = relationship('Costos_destinos_especificos', back_populates='destinos_especificos_relacion')
    destinos_generales_relacion = relationship('Destinos_generales', back_populates='destinos_especificos_relacion')
    
    #Relación a la tabla itinerario_destinos
    itinerario_destinos_relacion = relationship('Itinerario_destinos', back_populates='destinos_especificos_relacion')



















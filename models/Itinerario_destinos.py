from imports import *

class Itinerario_destinos(Base):
    __tablename__ = 'Itinerario_Destinos'
    
    #Definicion de la clave primaria compuesta
    id_itinerarios = Column(Integer, ForeignKey('Itinerarios.id_itinerarios'), primary_key=True, nullable=False)
    id_destinos_generales = Column(Integer, ForeignKey('Destinos_Generales.id_destinos_generales'), primary_key=True, nullable=False)

    # Destino específico opcional
    id_destinos_especificos = Column(Integer, ForeignKey('Destinos_Especificos.id_destinos_especificos'), nullable=True)

    #Relaciones hacia las tablas principales.
    itinerarios_relacion = relationship('Itinerarios', back_populates='itinerario_destinos_relacion')
    destinos_generales_relacion = relationship('Destinos_Generales', back_populates='itinerario_destinos_relacion')
    destinos_especificos_relacion = relationship('Destinos_Especificos', back_populates='itinerario_destinos_relacion')

    orden_parada = Column(Integer, nullable=False)

















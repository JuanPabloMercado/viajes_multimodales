from .imports import * 
from .base import Base 


#versión modificada de la clase Itinerario_destinos para corregir el error 
#de restricción al momento de crear destinos especificos multiples relacionados a un destino general.

class Itinerario_destinos(Base):
    
    __tablename__ = 'Itinerario_destinos'
    
    # NUEVA CLAVE PRIMARIA SUSTITUTA (PK)
    id_itinerario_destino = Column(Integer, primary_key=True, autoincrement=True) 
    
   
    id_itinerarios = Column(Integer, ForeignKey('Itinerarios.id_itinerarios'), nullable=False)
    id_destinos_generales = Column(Integer, ForeignKey('Destinos_generales.id_destinos_generales'), nullable=False)

    # Destino específico opcional (no es parte de ninguna PK/Unique)
    id_destinos_especificos = Column(Integer, ForeignKey('Destinos_especificos.id_destinos_especificos'), nullable=True)

    # Relaciones hacia las tablas principales.
    itinerarios_relacion = relationship('Itinerarios', back_populates='itinerario_destinos_relacion')
    destinos_generales_relacion = relationship('Destinos_generales', back_populates='itinerario_destinos_relacion')
    destinos_especificos_relacion = relationship('Destinos_especificos', back_populates='itinerario_destinos_relacion')

    orden_parada = Column(Integer, nullable=False)
    



"""
class Itinerario_destinos(Base):
    __tablename__ = 'Itinerario_destinos'
    
    #Definicion de la clave primaria compuesta
    id_itinerarios = Column(Integer, ForeignKey('Itinerarios.id_itinerarios'), primary_key=True, nullable=False)
    id_destinos_generales = Column(Integer, ForeignKey('Destinos_generales.id_destinos_generales'), primary_key=True, nullable=False)

    # Destino específico opcional
    id_destinos_especificos = Column(Integer, ForeignKey('Destinos_especificos.id_destinos_especificos'), nullable=True)

    #Relaciones hacia las tablas principales.
    itinerarios_relacion = relationship('Itinerarios', back_populates='itinerario_destinos_relacion')
    destinos_generales_relacion = relationship('Destinos_generales', back_populates='itinerario_destinos_relacion')
    destinos_especificos_relacion = relationship('Destinos_especificos', back_populates='itinerario_destinos_relacion')

    orden_parada = Column(Integer, nullable=False)
"""










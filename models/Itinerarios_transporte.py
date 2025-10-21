from .imports import * 
from .base import Base 

"""
class Itinerarios_transporte(Base):
    __tablename__ = 'Itinerarios_transporte'

    #Definicion de la clave primaria compuesta
    id_itinerarios = Column(Integer, ForeignKey('Itinerarios.id_itinerarios'), primary_key=True, nullable=False)
    id_medios_transporte = Column(Integer, ForeignKey('Medios_transporte.id_medios_transporte'), primary_key=True, nullable=False)
"""

#Nueva definción para la clase Itinerarios_transporte 
class Itinerarios_transporte(Base):
    __tablename__ = 'Itinerarios_transporte'

    # ➡️ NUEVA CLAVE PRIMARIA SUSTITUTA (PK) ⬅️
    # Ya no es clave compuesta.
    id_itinerario_transporte = Column(Integer, primary_key=True, autoincrement=True)

    # Claves Foráneas (solo FKs)
    id_itinerarios = Column(Integer, ForeignKey('Itinerarios.id_itinerarios'), nullable=False)
    id_medios_transporte = Column(Integer, ForeignKey('Medios_transporte.id_medios_transporte'), nullable=False)
    
    # Nota: Como es una tabla intermedia con una PK sustituta, 
    # no se requieren campos 'relationship' aquí, ya que la relación N:M
    # se define en las tablas principales (Itinerarios y Medios_transporte).












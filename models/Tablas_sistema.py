from .imports import * 
from .base import Base 


class Tablas_sistema(Base):
    __tablename__ = 'Tablas_sistema'

    id_tabla_sistema = Column(Integer, primary_key=True, autoincrement=True)
    nombre_tabla = Column(String(100), nullable=False, unique=True)
    
    #Relación con Historial_cambios
    historial_cambios = relationship('Historial_cambios', back_populates='tablas_sistema_relacion')





















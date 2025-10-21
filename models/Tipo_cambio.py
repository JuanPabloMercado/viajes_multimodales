from .imports import * 
from .base import Base 


class Tipo_cambio(Base):
    __tablename__ = 'Tipo_cambio'

    id_tipo_cambio = Column(Integer, primary_key=True, autoincrement=True)
    nombre_tipo = Column(String(50), nullable=False, unique=True)

    #Relación con Historial_cambios
    historial_cambios = relationship('Historial_cambios', back_populates='tipo_cambio_relacion')
















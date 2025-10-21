from .imports import * 
from .base import Base 


class Cancelaciones(Base):
    __tablename__ = 'Cancelaciones'
    
    id_cancelaciones = Column(Integer, primary_key = True, autoincrement=True)
    observaciones = Column(String(255), nullable=True)
    fecha_cancelacion = Column(DateTime, nullable=False)
    
    #Claves foráneas
    id_viajes = Column(Integer, ForeignKey('Viajes.id_viajes'), nullable=False)
    id_tipo_cancelacion = Column(Integer, ForeignKey('Tipo_cancelacion.id_tipo_cancelacion'), nullable=False)
    
    #Relaciones hacia las tablas principales.
    viajes_relacion = relationship('Viajes', back_populates='cancelaciones_relacion')
    tipo_cancelacion_relacion = relationship('Tipo_cancelacion', back_populates='cancelaciones_relacion')
from imports import *


class Costos_transporte(Base):
    __tablename__ = 'Costos_Transporte'
    
    id_costos_transporte = Column(Integer, primary_key=True, autoincrement=True)
    costo_base = Column(Numeric(10, 2), nullable=False)
    
    
    #Relación hacia Medios_transporte
    medios_transporte_relacion = relationship('Medios_transporte', back_populates='costos_transporte_relacion')

















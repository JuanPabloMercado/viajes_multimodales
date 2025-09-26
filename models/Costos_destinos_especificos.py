from imports import *

class Costos_destinos_especificos(Base):
    __tablename__ = 'Costos_Destinos_Especificos'
    
    id_costos_destinos_especificos = Column(Integer, primary_key=True, autoincrement=True)
    costo_base = Column(Numeric(10, 2), nullable=False)
    
    #Relación a la tabla Destinos_especificos
    destinos_especificos_relacion = relationship('Destinos_Especificos', back_populates='costos_destinos_especificos_relacion')
    
    
























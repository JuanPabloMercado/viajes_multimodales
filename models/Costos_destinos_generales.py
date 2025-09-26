from imports import *


class Costos_destinos_generales(Base):
    __tablename__ = 'Costos_Destinos_Generales'
    
    id_costos_destinos_generales = Column(Integer, primary_key=True, autoincrement=True)
    costo_base = Column(Numeric(10, 2), nullable=False)
    
    #Relación a la tabla Destinos_generales
    destinos_generales_relacion = relationship('Destinos_generales', back_populates='costos_destinos_generales_relacion')


















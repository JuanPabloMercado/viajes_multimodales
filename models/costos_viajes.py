from imports import *   

class Costos_viajes(Base):
    __tablename__ = 'Costos_Viajes'
    
    id_costos_viajes = Column(Integer, primary_key = True, autoincrement=True)
    costo_base = Column(Numeric(10, 2), nullable=False)

    #Relación con la tabla viajes_costos
    viajes_costos_relacion = relationship('Viajes_Costos', back_populates='costos_viajes_relacion')
    












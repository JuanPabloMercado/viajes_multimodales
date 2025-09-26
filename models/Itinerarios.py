from imports import *

class Itinerario(Base):
    __tablename__ = 'Itinerarios'

    id_itinerario = Column(Integer, primary_key=True, autoincrement=True)
    fecha_inicio = Column(Date, nullable=False)
    fecha_fin = Column(Date, nullable=False)
    detalle = Column(String(200), nullable=True)
    
    #Definción de las claves foráneas
    id_viajes = Column(Integer, ForeignKey('Viajes.id_viaje'), nullable=False)

    #Relación con Medios_transporte a través de la tabla intermedia Itinerarios_transporte
    medios_transporte = relationship('Medios_transporte', secondary='Itinerarios_transporte', back_populates='itinerarios')
    












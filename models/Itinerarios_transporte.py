from imports import *

class Itinerarios_transporte(Base):
    __tablename__ = 'Itinerarios_Transporte'

    #Definicion de la clave primaria compuesta
    id_itinerarios = Column(Integer, ForeignKey(Itinerarios.id_itinerarios), primary_key=True, nullable=False)
    id_medios_transporte = Column(Integer, ForeignKey(Medios_Transporte.id_medios_transporte), primary_key=True, nullable=False)
    
    












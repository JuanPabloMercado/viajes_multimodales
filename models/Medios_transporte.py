from imports import *

class Medios_transporte(Base):
    __tablename__ = 'Medios_Transporte'
    
    id_medios_transporte = Column(Integer, primary_key=True, autoincrement=True)
    
    #Definción de las claves foráneas
    id_costos_transporte = Column(Integer, ForeignKey('Costos_transporte.id_costos_transporte'), nullable=False)
    id_tipo_transporte = Column(Integer, ForeignKey('Tipo_transporte.id_tipo_transporte'), nullable=False)


    #Relaciones hacia la tabla Costos_transporte
    costos_transporte_relacion = relationship('Costos_transporte', back_populates='medios_transporte_relacion')

    #Relación con la tabla Itinerarios, a través de la tabla intermedia Itinerarios_transporte
    itinerarios = relationship('Itinerarios', secondary='Itinerarios_transporte', back_populates='medios_transporte')
    
    #Relación hacia la tabla Tipo_transporte
    tipo_transporte_relacion = relationship('Tipo_transporte', back_populates='medios_transporte_relacion')


















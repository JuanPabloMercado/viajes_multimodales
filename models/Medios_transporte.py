from imports import *

class Medios_transporte(Base):
    __tablename__ = 'Medios_Transporte'
    
    id_medios_transporte = Column(Integer, primary_key=True, autoincrement=True)
    
    #Definción de las claves foráneas
    id_costos_transporte = Column(Integer, ForeignKey('Costos_transporte.id_costos_transporte'), nullable=False)
    id_tipo_transporte = Column(Integer, ForeignKey('Tipo_transporte.id_tipo_transporte'), nullable=False)


    #Relaciones hacia las tablas principales.
    costos_transporte_relacion = relationship('Costos_transporte', back_populates='medios_transporte_relacion')
    tipo_transporte_relacion = relationship('Tipo_transporte', back_populates='medios_transporte_relacion')

















from imports import *   

class Tipo_transporte(Base):
    __tablename__ = 'Tipo_Transporte'
    
    id_tipo_transporte = Column(Integer, primary_key=True, autoincrement=True)
    nombre_tipo = Column(Enum('Avión', 'Tren', 'Colectivo Interurbano', 'Automóvil', 'Taxi', 'Caminata'), nullable=False)
    descripcion = Column(String(200), nullable=True)
    
    #Relación hacia Medios_transporte
    medios_transporte_relacion = relationship('Medios_transporte', back_populates='tipo_transporte_relacion')
    














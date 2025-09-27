from imports import *

class Historial_detalle(Base):
    __tablename__ = 'Historial_detalle'

    id_historial_detalle = Column(Integer, primary_key=True, autoincrement=True)
    campo_modificado = Column(String(100), nullable=False)
    valor_anterior = Column(String(255), nullable=True)
    valor_nuevo = Column(String(255), nullable=True)
    
    #Clave foránea que referencia a Historial_cambios
    id_historial_cambios = Column(Integer, ForeignKey('Historial_cambios.id_historial_cambios'), nullable=False)
    
    #Relación con Historial_cambios
    historial_cambios = relationship('Historial_cambios', backref='historial_detalles')















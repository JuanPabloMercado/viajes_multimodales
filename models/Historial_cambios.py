
from imports import *

class Historial_cambios(Base):
    __tablename__ = 'Historial_cambios'

    id_historial_cambios = Column(Integer, primary_key=True, autoincrement=True)
    registro_afectado = Column(Integer, nullable=False)
    razon_cambio = Column(String(200), nullable=False)
    fecha_cambio = Column(DateTime, default=func.now(), nullable=False)

    #Definición de las claves foráneas
    id_tablas_sistema = Column(Integer, ForeignKey('Tablas_sistema.id_tabla_sistema'), nullable=False)
    id_tipo_cambio = Column(Integer, ForeignKey('Tipo_cambio.id_tipo_cambio'), nullable=False)


    #Definción de las relaciones con las tablas Tablas_sistema y Tipo_cambio
    tablas_sistema_relacion = relationship('Tablas_sistema', backref='historial_cambios')
    tipo_cambio_relacion = relationship('Tipo_cambio', backref='historial_cambios')

    #Relación con Historial_detalle
    historial_detalles = relationship('Historial_detalle', backref='historial_cambios')
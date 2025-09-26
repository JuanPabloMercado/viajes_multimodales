from imports import *

class Tipo_cancelacion(Base):
    __tablename__ = 'Tipo_Cancelacion'
    
    id_tipo_cancelacion = Column(Integer, primary_key = True, autoincrement=True)
    nombre_tipo = Column(
        Enum('Condiciones climaticas adversas', 'Desperfecto técnico', 'Enfermedad', 'Problemas logisticos', 'Otros', name='nombre_tipo_enum'),
        default='Otros',
        nullable=False
    )
    descripcion = Column(String(200), nullable=False)
    
    #Relación con la tabla cancelaciones
    cancelaciones_relacion = relationship('Cancelaciones', back_populates='tipo_cancelacion_relacion')
    
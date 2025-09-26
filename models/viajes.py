from imports import *



class Viajes(Base):
    
    __tablename__ = 'Viajes'

    id_viajes = Column(Integer, primary_key = True, autoincrement=True)
    fecha_inicio = Column(DateTime)
    fecha_fin = Column(DateTime)
    estado = Column(
        Enum('Activo', 'Cancelado', 'Finalizado', name='estado_enum'),
        default='Activo',
        nullable=False
    )

    #Relación con la tabla cancelaciones
    cancelaciones_relacion = relationship('Cancelaciones', back_populates='viajes_relacion')
    #Relación con la tabla viajes_costos
    viajes_costos_relacion = relationship('Viajes_costos', back_populates='viajes_relacion')
    #Relación N:M com la tabla Empresas utilizando la relación intermedia Empresas_viajes
    empresas = relationship('Empresas', secondary='Empresas_viajes', back_populates='viajes')
    






















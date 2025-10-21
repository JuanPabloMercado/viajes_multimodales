from .imports import * 
from .base import Base 
from models.conexion_db import SessionLocal
from models import *
session = SessionLocal()


class Empresas_empleados(Base):
    """
    Clase intermedia que representa la relación N:M entre Empresas y Empleados.
    Incluye atributos adicionales: fecha_ingreso y puesto.
    """
    __tablename__ = 'Empresas_empleados'

    # Claves primarias compuestas
    id_empresas = Column(Integer, ForeignKey('Empresas.id_empresas'), primary_key=True, nullable=False)
    id_empleados = Column(Integer, ForeignKey('Empleados.id_empleados'), primary_key=True, nullable=False)

    # Atributos adicionales
    fecha_ingreso = Column(Date, nullable=False)
    puesto = Column(String(100), nullable=False)

    # Relaciones
    empresa = relationship('Empresas', back_populates='empleados_relacion')
    empleado = relationship('Empleados', back_populates='empresas_relacion')

    # Validación de fecha_ingreso
    @validates('fecha_ingreso')
    def validar_fecha_ingreso(self, key, value: str | date):
        """Valida que la fecha de ingreso tenga formato YYYY-MM-DD."""
        if isinstance(value, date):
            return value
        try:
            return datetime.strptime(value, '%Y-%m-%d').date()
        except ValueError:
            raise ValueError("La fecha de ingreso no tiene un formato válido (usa YYYY-MM-DD).")

    # Validación del puesto
    @validates('puesto')
    def validar_puesto(self, key, value: str):
        """Valida que el puesto no esté vacío y no supere 100 caracteres."""
        if not value:
            raise ValueError("El puesto de trabajo no puede estar vacío.")
        if len(value) > 100:
            raise ValueError("El puesto de trabajo no puede exceder los 100 caracteres.")
        return value
    
    @classmethod
    def empresa_empleado_relacion(cls, id_empresa: int, id_empleado: int, fecha_ingreso: Date, puesto: str):
        with SessionLocal() as session:
            empresa = session.query(Empresas).filter_by(id_empresas=id_empresa).first()
            empleado = session.query(Empleados).filter_by(id_empleados=id_empleado).first()
        
        if not empresa:
            print(f'La empresa con id {id_empresa} no se encuentra cargada en la base de datos.')
        elif not empleado:
            print(f'El empleado con id {id_empleado} no se encuentra cargado en la base de datos.')
        else: 
            print('Error inesperado.')
        
        relacion = cls(
            id_empresas = id_empresa,
            id_empleados = id_empleado, 
            fecha_ingreso=fecha_ingreso,
            puesto=puesto
        )    
        
        session.add(relacion)
        session.commit()
        session.refresh(relacion)
        print(f'Relación creada correctamente con Id Empleado: {id_empleado} y Id Empresa: {id_empresa}.')
        return relacion
        































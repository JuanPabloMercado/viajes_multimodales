from imports import *

class Empresas_empleados(Base):
    """
    Clase intermedia que representa la relación N:M entre Empresas y Empleados.
    Incluye atributos adicionales: fecha_ingreso y puesto.
    """
    __tablename__ = 'empresas_empleados'

    # Claves primarias compuestas
    id_empresas = Column(Integer, ForeignKey('empresas.id_empresas'), primary_key=True, nullable=False)
    id_empleados = Column(Integer, ForeignKey('empleados.id_empleados'), primary_key=True, nullable=False)

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































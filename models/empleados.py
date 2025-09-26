from imports import *

class Empleados(Base):
    """
    Representa la entidad Empleados en el sistema de viajes multimodales.
    Incluye validación de DNI, email y fecha de nacimiento.
    """
    __tablename__ = 'empleados'

    id_empleados = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(50), nullable=False)
    apellido = Column(String(50), nullable=False)
    dni = Column(String(8), nullable=False, unique=True)
    fecha_nacimiento = Column(Date, nullable=False)
    email = Column(String(100), nullable=False, unique=True)

    # Relación hacia Empresas_empleados
    empresas_relacion = relationship('Empresas_empleados', back_populates='empleado')

    def __repr__(self) -> str:
        return (f"Empleados(Id del empleado: {self.id_empleados}, "
                f"Nombre: {self.nombre}, Apellido: {self.apellido}, "
                f"DNI: {self.dni}, Fecha de Nacimiento: {self.fecha_nacimiento}, "
                f"Email: {self.email})")

    # Validaciones
    @validates('dni')
    def validar_dni(self, key, dni: str) -> str:
        """Valida que el DNI tenga exactamente 8 dígitos numéricos."""
        if not re.match(r'^\d{8}$', dni):
            raise ValueError("El DNI debe tener 8 dígitos. Intenta nuevamente.")
        return dni

    @validates('email')
    def validar_email(self, key, email: str) -> str:
        """Valida el formato del email."""
        if not re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', email):
            raise ValueError("El email no tiene un formato válido. Intenta nuevamente.")
        return email

    @validates('fecha_nacimiento')
    def validar_fecha_nacimiento(self, key, fecha_nacimiento: str | date) -> date:
        """Valida que la fecha de nacimiento tenga formato YYYY-MM-DD o sea un objeto date."""
        if isinstance(fecha_nacimiento, date):
            return fecha_nacimiento
        try:
            return datetime.strptime(fecha_nacimiento, '%Y-%m-%d').date()
        except ValueError:
            raise ValueError("La fecha de nacimiento no tiene un formato válido (usa YYYY-MM-DD).")

    # Propiedad auxiliar: empresas directas del empleado
    @property
    def empresas(self):
        return [rel.empresa for rel in self.empresas_relacion]







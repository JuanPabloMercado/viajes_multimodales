from .imports import * 
from .base import Base 
from models.conexion_db import SessionLocal
session = SessionLocal()

class Empleados(Base):
    """
    Representa la entidad Empleados en el sistema de viajes multimodales.
    Incluye validación de DNI, email y fecha de nacimiento.
    """
    __tablename__ = 'Empleados'

    id_empleados = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(50), nullable=False)
    apellido = Column(String(50), nullable=False)
    dni = Column(String(8), nullable=False, unique=True)
    fecha_nacimiento = Column(Date, nullable=False)
    email = Column(String(100), nullable=False, unique=True)
    estado = Column(String(10), nullable = False)

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

    #Métodos CRUD
    @classmethod
    def crear_empleado(cls, nombre: str, apellido: str, dni: str, fecha_nacimiento: Date, email: str, estado: str):
        """Crea un nuevo empleado"""
        with SessionLocal() as session:
            empleado = cls(nombre=nombre, apellido=apellido, dni=dni, fecha_nacimiento=fecha_nacimiento, email=email, estado=estado)
            session.add(empleado)
            session.commit()
            session.refresh(empleado)
            return empleado
        
    @classmethod
    def actualizar_empleado(cls, identificador: int | str, **kwargs):
        """
        Actualiza un empleado existente según su id_empleados, dni o email.
        Ejemplo:
            Empleados.actualizar_empleado(1, nombre="Pedro")
            Empleados.actualizar_empleado("37495048", estado="Inactivo")
        """
        with SessionLocal() as session:
            # Intentamos encontrar el empleado por ID, DNI o email
            empleado = None
            if isinstance(identificador, int):
                empleado = session.query(cls).filter_by(id_empleados=identificador).first()
            elif isinstance(identificador, str):
                # Buscamos por DNI o por email
                empleado = session.query(cls).filter(
                    (cls.dni == identificador) | (cls.email == identificador)
                ).first()

            if not empleado:
                raise ValueError(f"No se encontró ningún empleado con identificador '{identificador}'")

            # Actualizamos los campos recibidos
            for key, value in kwargs.items():
                if hasattr(empleado, key):
                    setattr(empleado, key, value)

            session.commit()
            session.refresh(empleado)
            return empleado
    @classmethod
    def cambiar_estado(cls, identificardor: int | str):
        """Cambia el estado de un empleado a Inactivo."""
        with SessionLocal() as session:
            if isinstance(identificardor, int):
                empleado = session.query(cls).filter_by(id_empleados=identificardor).first()
            elif isinstance(identificardor, str):
                empleado = session.query(cls).filter(
                    (cls.dni==identificardor) | (cls.email==identificardor)
                ).first()
            else:
                print('El identificador debe ser un número o una cadena.')
                
            if not empleado:
                print(f'No existe el empleado activo con identificador {identificardor}.')
            
            empleado.estado = 'Inactivo'
            session.commit()
            session.refresh(empleado)
            print(f"El empleado '{empleado.nombre} {empleado.apellido}' fue marcado como Inactivo.")
            return empleado

        





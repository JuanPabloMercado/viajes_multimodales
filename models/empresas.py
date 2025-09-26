from imports import *

class Empresas(Base):
    """
    Representa la entidad Empresas en el sistema de viajes multimodales.
    Incluye validación de CUIT y definición ORM con SQLAlchemy.
    """
    __tablename__ = 'empresas'

    id_empresas = Column(Integer, primary_key=True, autoincrement=True)
    cuit = Column(String(13), nullable=False, unique=True)
    razon_social = Column(String(100), nullable=False)
    domicilio = Column(String(200), nullable=False)

    # Relación hacia Empresas_empleados
    empleados_relacion = relationship('Empresas_empleados', back_populates='empresa')

    # Relación N:M con Viajes
    viajes = relationship('Viajes', secondary='Empresas_viajes', back_populates='empresas')

    def __repr__(self) -> str:
        return (f"Empresas(Id de la empresa: {self.id_empresas}, "
                f"CUIT: {self.cuit}, Razón Social: {self.razon_social}, "
                f"Domicilio: {self.domicilio})")

    # Validación con decorador @validates
    @validates('cuit')
    def validar_cuit(self, key, cuit: str) -> str:
        """Valida el formato del CUIT Argentino: XX-XXXXXXXX-X"""
        if not re.match(r'^\d{2}-\d{8}-\d$', cuit):
            raise ValueError("El CUIT debe tener el formato XX-XXXXXXXX-X. Intenta nuevamente.")
        return cuit

    # Propiedad auxiliar: empleados directos de la empresa
    @property
    def empleados(self):
        return [rel.empleado for rel in self.empleados_relacion]
































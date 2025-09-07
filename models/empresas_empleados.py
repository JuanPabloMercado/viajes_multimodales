from imports import *

class Empresas_empleados(Base):
    __tablename__ = 'empresas_empleados'
    
    """
    Clase intermedia que representa la relación N:M entre Empresas y Empleados. 
    Contiene FK hacia Empresas y Empleados, además de atributos adicionales de la 
    relación como fecha de ingreso y puesto. 
    """

    __tablename__ = 'empresas_empleados'
    
    id_empresas_empleados = Column(Integer, primary_key=True, autoincrement=True)
    
    #Claves foráneas. 
    id_empresas = Column(Integer, ForeignKey('empresas.id_empresas'), nullable=False)
    id_empleados = Column(Integer, ForeignKey('empleados.id_empleados'), nullable=False)
    
    #Atributos de relación
    fecha_ingreso = Column(Date, nullable=False)
    puesto = Column(String(100), nullable=False)
    
    #Relaciones hacia las tablas principales
    empresas = relationship("Empresas", back_populates="empleados_relacion")
    empleados = relationship("Empleados", back_populates="empresas_relacion")


    #Validación de la fecha de ingreso
    @validates('fecha_ingreso')
    def validar_fecha_ingreso(self, key, value: str | date):
        """
        Valida que la fecha de ingreso tenga el formato YYYY-MM-DD.
        Acepta string u objeto date.
        """

        if isinstance(value, date): 
            return value
        try:
            return datetime.strptime(value, '%Y-%m-%d').date()
        except ValueError:
            raise ValueError("La fecha de ingreso no tiene un formato válido (usa YYYY-MM-DD).")
        
    #Validación del puesto de trabajo.
    @validates('puesto')
    def validar_puesto(self, key, value: str):
        """
        Valida que el puesto de trabajo no esté vacío y tenga una longitud máxima.
        """

        if not value:
            raise ValueError("El puesto de trabajo no puede estar vacío.")
        if len(value) > 100:
            raise ValueError("El puesto de trabajo no puede exceder los 100 caracteres.")
        return value
    
    































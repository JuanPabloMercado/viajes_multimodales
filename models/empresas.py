from .imports import * 
from .base import Base 
from .empresas_viajes import Empresas_viajes
from models.conexion_db import SessionLocal
session = SessionLocal()

class Empresas(Base):
    """
    Representa la entidad Empresas en el sistema de viajes multimodales.
    Incluye validación de CUIT y definición ORM con SQLAlchemy.
    """
    __tablename__ = 'Empresas'

    id_empresas = Column(Integer, primary_key=True, autoincrement=True)
    cuit = Column(String(13), nullable=False, unique=True)
    razon_social = Column(String(100), nullable=False)
    domicilio = Column(String(200), nullable=False)
    estado = Column(String(10), default='Activo', nullable = False)

    # Relación hacia Empresas_empleados
    empleados_relacion = relationship('Empresas_empleados', back_populates='empresa')

    # Relación N:M con Viajes
    viajes_relacion = relationship('Viajes', secondary='Empresas_viajes', back_populates='empresas_relacion')

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


    #Métodos internos CRUD
    @classmethod
    def crear_empresa(cls, cuit: str, razon_social: str, domicilio: str):
        """ Crea una nueva empresa."""
        empresa = cls(cuit=cuit, razon_social=razon_social, domicilio=domicilio)
        session.add(empresa)
        session.commit()
        session.refresh(empresa)
        print(f'Empresa {empresa.razon_social} creada correctamente.')
        return empresa
    
    @classmethod
    def actualizar_empresa(cls, identificador: int | str, **kwargs):
        with SessionLocal() as session:
            if isinstance(identificador, int):
                empresa = session.query(cls).filter_by(id_empresas=identificador).first()
            elif isinstance(identificador, str):
                empresa = session.query(cls).filter(
                    (cls.razon_social==identificador) | (cls.domicilio==identificador)
                ).first()
            else:
                print(f'El identificador debe ser un número o una cadena.')
                return None
                
            if not empresa:
                print(f'No existe empresa con el identificado {identificador}.')
                return None
            
            for key, value in kwargs.items():
                if hasattr(empresa, key):
                    setattr(empresa, key, value)
                """
                    **kwargs: Un diccionario de 
                    argumentos de palabra clave. Esto permite que el usuario pase 
                    cualquier número de atributos a actualizar 
                    (Ej: razon_social='Nuevo nombre', domicilio='Nueva dirección').
                    if hasattr(self, key):: Esta es una verificación de seguridad crucial. Asegura que solo se 
                    intenten actualizar atributos que realmente existen en el objeto self 
                    (la instancia Empresas). Esto evita errores si un usuario pasa un argumento incorrecto 
                    (Ej: empresa.actualizar(..., pais='Chile') si pais no es una columna).

                    setattr(self, key, value): Esta es la función mágica de Python que actualiza 
                    dinámicamente el atributo del objeto. Es equivalente a escribir: 
                    self.razon_social = 'Nuevo nombre'. Al realizar esto, la sesión de SQLAlchemy
                    automáticamente marca la instancia como "sucia" (dirty).
                """

            session.commit()
            session.refresh(empresa)
            return empresa
    
    @classmethod
    def cambiar_estado(cls, identificador: int | str):
        """Cambia el estado de una empresa a 'Inactivo'."""
        with SessionLocal() as session:
            # Buscar la empresa
            if isinstance(identificador, int):
                empresa = session.query(cls).filter_by(id_empresas=identificador).first()
            elif isinstance(identificador, str):
                empresa = session.query(cls).filter(
                    (cls.razon_social == identificador) | (cls.domicilio == identificador)
                ).first()
            else:
                print("El identificador debe ser un número o una cadena.")
                return None

            if not empresa:
                print(f"No existe una empresa con identificador '{identificador}'.")
                return None

            # Cambiar el estado
            empresa.estado = 'Inactivo'
            session.commit()
            session.refresh(empresa)
            print(f"Empresa '{empresa.razon_social}' marcada como Inactiva.")
            return empresa
    
    @classmethod
    def obtener_conteo_viajes(cls):
        """
        Calcula y retorna la cantidad total de viajes por cada empresa
        utilizando una JOIN con la tabla intermedia Empresas_viajes.
        """
        # Necesitamos importar las dependencias funcionales dentro del método o globalmente
        from sqlalchemy import func 

        try:
            with SessionLocal() as session:
                # La clave es usar func.count() con GROUP BY
                consulta = session.query(
                    cls.id_empresas, 
                    cls.razon_social,
                    func.count(Empresas_viajes.id_viajes).label('total_viajes')
                ).select_from(cls) \
                .join(Empresas_viajes, cls.id_empresas == Empresas_viajes.id_empresas) \
                .group_by(cls.id_empresas, cls.razon_social) \
                .all()

                # Formatear la salida
                resultados = [
                    {
                        'id_empresa': id_empresa,
                        'razon_social': razon_social,
                        'total_viajes': total_viajes
                    } 
                    for id_empresa, razon_social, total_viajes in consulta
                ]
                
                return resultados

        except Exception as e:
            # Manejo de errores
            print(f"Error al obtener el conteo de viajes por empresa: {e}")
            return []

                
            


        
        





























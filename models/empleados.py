import re #coding: utf-8
from datetime import datetime, date


class Empleados():
    
    """
    Representa la entidad Empleado en el sistema de viajes multimodales.
    Valida atributos como DNI, email y fecha de nacimiento.
    """

    #Definición de los atributos de instancia
    def __init__(self, id_empleados: int, nombre: str, apellido: str, dni: str, fecha_nacimiento: str, email: str):
        self.id_empleados = id_empleados
        self.nombre = nombre.strip().title()
        self.apellido = apellido.strip().title()
        self.dni = self.validar_dni(dni) 
        self.fecha_nacimiento = self.validar_fecha_nacimiento(fecha_nacimiento) 
        self.email = self.validar_email(email) 


    #Definición de los métodos de la clase
    #Mediante los siguientes métodos se procede a validar los datos de entrada de los atributos de instancia, 
    #Teniendo en cuenta el dominio de los datos declarados en el diagrama E-R de la base de datos. 
    
    def __repr__(self) -> str:
        return f"Empleados(Id del empleado: {self.id_empleados}, Nombre: {self.nombre}, Apellido: {self.apellido}, DNI: {self.dni}, Fecha de Nacimiento: {self.fecha_nacimiento}, Email: {self.email})"
    

    def validar_dni(self, dni:str) -> str:
        """Valida el formato del DNI Argentino."""
        if not re.match(r'^\d{8}$', dni):
            raise ValueError("El DNI debe tener 8 dígitos. Intenta nuevamente.")
        else:
            return dni
                

    def validar_email(self, email: str) -> str:
        """Valida el formato del email."""
        if not re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', email):
            raise ValueError("El email no tiene un formato válido. Intenta nuevamente.")
        else:
            return email
         
    
    def validar_fecha_nacimiento(self, fecha_nacimiento: str) -> date:
        """Valida el formato de la fecha de nacimiento: YYYY/MM/DD"""
        try:
            return datetime.strptime(fecha_nacimiento, '%Y-%m-%d').date() #convierte un string a un objeto date
        except ValueError:
            raise ValueError("La fecha de nacimiento no tiene un formato válido. Intenta nuevamente.")
















import re #coding: utf-8


class Empresas():
    
    """
    Representa la entidad Empresas en el sistema de viajes multimodales 
    Valida atributos como CUIT. 
    """
    
    #Definición de los atributos de instancia. 
    #Los argumentos son posicionales. 
    def __init__(self, id_empresas: int, cuit: str, razon_social: str, domicilio: str):
        self.id_empresas = id_empresas
        self.cuit = self.validar_cuit(cuit)
        self.razon_social = razon_social
        self.domicilio = domicilio
        
        
        #Definición de los métodos de la clase. 
        
    def __repr__(self) -> str:
        return f"Empresas(Id de la empresa: {self.id_empresas}, CUIT: {self.cuit}, Razón Social: {self.razon_social}, Domicilio: {self.domicilio})"


    def validar_cuit(self, cuit: str) -> str:
        """Valida el formato del CUIT Argentino """
        if not re.match(r'^\d{2}-\d{8}-\d$', cuit):
            raise ValueError("El CUIT debe tener el formato XX-XXXXXXXX-X. Intenta nuevamente.")
        else:
            return cuit




































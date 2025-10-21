# create_db.py
from models.imports import Base
from models.conexion_db import engine


# Importar todos los modelos para que SQLAlchemy los registre
from models import (

    Paises, 
    Provincias,
    Ciudades,
    Tipo_transporte,
    tipo_cancelacion,
    Tablas_sistema,
    Tipo_cambio,
    
    empresas,
    empleados,
    Destinos_generales,
    Destinos_especificos,
    Medios_transporte,
    viajes,
    
    empresas_empleados,
    empresas_viajes,
    Itinerarios,
    Itinerarios_transporte,
    Itinerario_destinos,
    
    Costos_destinos_generales,
    Costos_destinos_especificos,
    Costos_transporte,
    costos_viajes,
    viajes_costos,
    
    Historial_cambios,
    Historial_detalle,
    cancelaciones, 

)

if __name__ == "__main__":
    print("Creando base de datos y tablas...")
    Base.metadata.create_all(engine)
    print("Base de datos creada con éxito.")

from .base import Base

from .Paises import Paises
from .Provincias import Provincias
from .Ciudades import Ciudades
from .Tipo_transporte import Tipo_transporte
from .tipo_cancelacion import Tipo_cancelacion
from .Tablas_sistema import Tablas_sistema
from .Tipo_cambio import Tipo_cambio

from .empresas import Empresas
from .empleados import Empleados
from .Destinos_generales import Destinos_generales
from .Destinos_especificos import Destinos_especificos
from .Medios_transporte import Medios_transporte
from .viajes import Viajes

from .empresas_empleados import Empresas_empleados
from .empresas_viajes import Empresas_viajes
from .Itinerarios import Itinerarios
from .Itinerarios_transporte import Itinerarios_transporte
from .Itinerario_destinos import Itinerario_destinos

from .Costos_destinos_generales import Costos_destinos_generales 
from .Costos_destinos_especificos import Costos_destinos_especificos
from .Costos_transporte import Costos_transporte
from .costos_viajes import Costos_viajes
from .viajes_costos import Viajes_costos

from .Historial_cambios import Historial_cambios
from .Historial_detalle import Historial_detalle
from .cancelaciones import Cancelaciones


# Lista para importar todo de golpe si se usa *
__all__ = [ "Base",
    "Paises", "Provincias", "Ciudades", "Tipo_transporte", "Tipo_cancelacion", "Tablas_sistema", "Tipo_cambio",
    "Empresas", "Empleados", "Destinos_generales", "Destinos_especificos", "Medios_transporte", "Viajes",
    "Empresas_empleados", "Empresas_viajes", "Itinerarios", "Itinerarios_transporte", "Itinerario_destinos",
    "Costos_destinos_generales", "Costos_destinos_especificos", "Costos_transporte", "Costos_viajes", "Viajes_costos",
    "Historial_cambios", "Historial_detalle", "Cancelaciones"
]


"""from imports import *
#from .conexion_db import Base, session


from .Paises import Paises
from .Provincias import Provincias
from .Ciudades import Ciudades
from .Tipo_transporte import Tipo_transporte
from .tipo_cancelacion import Tipo_cancelacion
from .Tablas_sistema import Tablas_sistema
from .Tipo_cambio import Tipo_cambio

from .empresas import Empresas
from .empleados import Empleados
from .Destinos_generales import Destinos_generales
from .Destinos_especificos import Destinos_especificos   
from .Medios_transporte import Medios_transporte
from .viajes import Viajes

from .empresas_empleados import Empresas_empleados
from .empresas_viajes import Empresas_viajes
from .Itinerarios import Itinerarios
from .Itinerarios_transporte import Itinerarios_transporte
from .Itinerario_destinos import Itinerario_destinos

from .Costos_destinos_generales import Costos_destinos_generales 
from .Costos_destinos_especificos  import Costos_destinos_especificos
from .Costos_transporte  import Costos_transporte
from .costos_viajes import Costos_viajes
from .viajes_costos import Viajes_costos


from . import Historial_cambios, Historial_detalle, cancelaciones


# Lista para importar todo de golpe si se usa *
__all__ = [
    "Paises", "Provincias", "Ciudades", "Tipo_transporte", "Tipo_cancelacion", "Tablas_sistema", "Tipo_cambio",
    "Empresas", "Empleados", "Destinos_generales", "Destinos_especificos", "Medios_transporte", "Viajes",
    "Empresas_empleados", "Empresas_viajes", "Itinerarios", "Itinerarios_transporte", "Itinerario_destinos",
    "Costos_destinos_generales", "Costos_destinos_especificos", "Costos_transporte", "costos_viajes", "viajes_costos",
    "Historial_cambios", "Historial_detalle", "cancelaciones"
]
"""
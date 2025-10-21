"""
demo.py

Propósito:
---------
Demostrar la arquitectura, ingeniería de la base de datos y flujo de trabajo del proyecto de gestión de viajes multimodales.
Este script permite:
    - Crear la base de datos y sus tablas (si no existen).
    - Cargar datos de ejemplo en las tablas principales.
    - Ejecutar los métodos definidos en las clases para gestionar viajes, itinerarios, destinos y medios de transporte.
    - Consultar y mostrar datos en consola para verificar integridad y relaciones.

Justificación de su existencia:
-------------------------------
Este archivo no tiene interfaz gráfica ni interacción con el usuario, ya que su objetivo es:
    - Verificar la correcta creación de las tablas y relaciones.
    - Demostrar el funcionamiento de los métodos de las clases.
    - Mostrar la integridad referencial y el flujo de datos en SQLAlchemy.
    - Servir como ejemplo reproducible para pruebas unitarias o demostraciones.

Estructura y secciones:
-----------------------
1. crear_base(): 
    - Crea todas las tablas de la base de datos usando SQLAlchemy.
    - Equivalente al script create_db.py pero integrado.

2. cargar_datos_ejemplo():
    - Inserta datos de prueba en las tablas:
        - Paises, Provincias, Ciudades
        - Empresas, Empleados
        - Costos de destinos generales y específicos
        - Destinos generales y específicos
        - Medios de transporte
        - Viajes completos con itinerarios y destinos
    - Llama al método 'crear_viaje_completo' para demostrar el flujo de datos completo.

3. mostrar_datos():
    - Realiza consultas simples sobre los viajes y sus itinerarios.
    - Muestra en consola información básica de viajes, itinerarios y destinos, reflejando las relaciones.

Notas importantes:
-----------------
- El script puede ejecutarse múltiples veces sin problemas si se desea recrear la base.
- Los IDs y datos de ejemplo se pueden modificar según necesidad.
- Sirve como demostración de los triggers de auditoría, relaciones N:M y lógica de negocio implementada en las clases.
- Ideal para mostrar la arquitectura y flujo de trabajo de SQLAlchemy a terceros, sin necesidad de interfaces adicionales.

"""
# demo.py
from datetime import date, datetime
from models.conexion_db import SessionLocal, engine
from models.imports import Base
from models import (
    Paises, Provincias, Ciudades,
    Empresas, Empleados,
    Destinos_generales, Destinos_especificos,
    Costos_destinos_generales, Costos_destinos_especificos,
    Viajes, Itinerarios, Itinerario_destinos,
    Medios_transporte
)

def crear_base():
    """Crea todas las tablas en la base de datos."""
    print("Creando base de datos y tablas...")
    Base.metadata.create_all(engine)
    print("Base de datos creada con éxito.")

def cargar_datos_ejemplo():
    """Carga datos de prueba en la base de datos para demostrar el flujo de trabajo."""
    with SessionLocal() as session:
        # Crear país, provincia y ciudad
        pais = Paises.crear_pais("Argentina")
        provincia = Provincias.crear_provincia("Buenos Aires", 1)
        ciudad = Ciudades.crear_ciudad("La Plata", 1)

        # Crear empresa y empleado
        empresa = Empresas.crear_empresa("Empresa Demo", "20304050607", "Calle Falsa 123")
        empleado = Empleados.crear_empleado("Juan Pablo", "Mercado", '29475938', '2023-12-23', 'jpm@gmail.com', 'Activo')

        # Crear costos de destinos
        costo_dest_gen = Costos_destinos_generales.crear_costo_destino_general(1000.00)
        costo_dest_esp = Costos_destinos_especificos.crear_costo_destino_especifico(500.00)

        # Crear destinos generales y específicos
        destino_gen = Destinos_generales.crear_destino_general("Buenos Aires Centro", 1, 1)
        destino_esp = Destinos_especificos.crear_destino_especifico(
            datetime(2025, 11, 18, 9, 0),
            datetime(2025, 11, 18, 12, 0),
            "Visita guiada al museo",
            1,
            1
        )

        # Crear medio de transporte
        transporte = Medios_transporte.crear_medio("Autobus", "Bus interurbano")

        # Crear viaje completo con itinerarios y destinos
        datos_viaje = {
            "fecha_inicio": date(2025, 11, 18),
            "fecha_fin": date(2025, 11, 30),
            "estado": "Activo",
            "empresas_participantes": [1],
            "itinerarios": [
                {
                    "fecha_inicio": date(2025, 11, 18),
                    "fecha_fin": date(2025, 11, 20),
                    "detalle": "Primer itinerario demo",
                    "estado": "Activo",
                    "destinos_generales": [
                        {"id_destinos_generales": 1, "orden_parada": 1, "destinos_especificos": [1]}
                    ],
                    "medios_transporte": [1]
                }
            ]
        }

        viaje = Viajes.crear_viaje_completo(datos_viaje)

        print("Datos de prueba cargados con éxito.")

def mostrar_datos():
    """Muestra algunos datos de ejemplo para verificar que se cargaron correctamente."""
    with SessionLocal() as session:
        viajes = session.query(Viajes).all()
        for v in viajes:
            print(f"Viaje {v.id_viajes} desde {v.fecha_inicio} hasta {v.fecha_fin}, estado: {v.estado}")
            for it in v.itinerarios_relacion:
                print(f"  Itinerario {it.id_itinerarios} del {it.fecha_inicio} al {it.fecha_fin}")
                for idest in it.itinerario_destinos_relacion:
                    print(f"    Destino general ID: {idest.id_destinos_generales}, orden parada: {idest.orden_parada}")
                    if idest.id_destinos_especificos:
                        print(f"      Destino específico ID: {idest.id_destinos_especificos}")

if __name__ == "__main__":
    crear_base()
    cargar_datos_ejemplo()
    mostrar_datos()


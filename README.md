# Proyecto Gestión de Viajes Multimodales

## Descripción
Este proyecto implementa un sistema de **gestión de viajes corporativos multimodales**, diseñado para demostrar la arquitectura y la ingeniería de bases de datos relacionales utilizando **SQLAlchemy** en Python.  
El objetivo principal es mostrar la estructura de la base de datos, las relaciones entre entidades, los flujos de trabajo de creación y actualización de registros, y el registro de auditorías mediante triggers.

## Arquitectura del Proyecto
- **Python 3.x** como lenguaje principal.
- **SQLAlchemy ORM** para modelar y manipular la base de datos.
- **SQLite** como motor de base de datos (puede adaptarse a PostgreSQL, MySQL u otros).
- **Estructura modular**:
  - `models/` → Contiene todas las clases y la conexión a la base de datos.
  - `consultas_practica/` → Contiene scripts de prueba y consultas de ejemplo.
  - `create_db.py` → Script para crear la base de datos y todas las tablas.
  - `triggers.sql` → Contiene todos los triggers de auditoría y validaciones.

## Base de Datos
La base de datos incluye módulos para:
- Gestión de **empresas** y **empleados**.
- Gestión de **viajes** e **itinerarios**, incluyendo destinos generales y específicos.
- Gestión de **medios de transporte** y costos asociados.
- **Auditoría** de cambios en tablas críticas mediante:
  - `Historial_cambios`
  - `Historial_detalle`
  - `Tipo_cambio`
  - `Tablas_sistema`

Se registran automáticamente cambios de INSERT, UPDATE y DELETE, así como bajas lógicas de registros.

## Clases Principales
Algunas de las clases representadas:
- `Viajes`, `Itinerarios`, `Empresas`, `Empleados`
- `Destinos_generales`, `Destinos_especificos`, `Medios_transporte`
- Tablas intermedias para relaciones N:M: `Empresas_empleados`, `Empresas_viajes`, `Itinerarios_transporte`, `Itinerario_destinos`
- Clases de auditoría: `Historial_cambios`, `Historial_detalle`, `Tipo_cambio`, `Tablas_sistema`

## Flujo de Trabajo
1. Se inicializa la base de datos ejecutando `create_db.py`.
2. Se crean y modifican registros mediante métodos de clase (`crear_`, `actualizar_`, `cambiar_estado`) definidos en cada modelo.
3. Los triggers almacenan automáticamente las operaciones relevantes en las tablas de auditoría.
4. Las relaciones N:M se manejan mediante tablas intermedias y métodos específicos.


## Uso
- Clonar el repositorio:
```bash
git clone https://github.com/JuanPabloMercado/viajes_multimodales.git


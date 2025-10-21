# db.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base


# 1. Definimos la base de la que heredarán todos los modelos
Base = declarative_base()


# 2. Definimos el motor de conexión (engine)
#    - "sqlite:///viajes.db" crea un archivo viajes.db en el directorio actual
#    - echo=True muestra todas las consultas SQL ejecutadas (útil para depuración)
engine = create_engine("sqlite:///viajes.db", echo=True)

# 3. Definimos el "sessionmaker", que es una fábrica de sesiones
#    Cada sesión representa una conexión a la BD con la que trabajamos
SessionLocal = sessionmaker(bind=engine)

# 4. Función auxiliar para obtener una sesión
def get_session():
    """
    Devuelve una nueva sesión de base de datos.
    Usar esta función siempre que queramos interactuar con la BD.
    """
    return SessionLocal()

# 5. Crear todas las tablas a partir de los modelos definidos en models.py
#    NOTA: debemos importar los modelos antes de ejecutar esta línea,
#    de lo contrario, SQLAlchemy no sabrá qué tablas generar.
import models
Base.metadata.create_all(bind=engine)














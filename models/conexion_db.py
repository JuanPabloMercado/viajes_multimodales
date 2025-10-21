# conexion_db.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.base import Base  # Evita ciclos
import os

# 📍 Ruta de la base de datos
db_path = "C:/Users/Juan Pablo/Desktop/ENOVA/Proyectos de desarrollo/gestion_de_viajes_corporativos/viajes_multimodales/data/database.db"
DATABASE_URL = f"sqlite:///{db_path}"

# 1. Crear el motor de conexión
engine = create_engine(DATABASE_URL, echo=True)
print("Conexión exitosa a la base de datos.")

# 2. Crear todas las tablas
Base.metadata.create_all(engine)

# 3. Crear el factory de sesiones
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

# 4. Función de utilidad para obtener sesión
def get_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

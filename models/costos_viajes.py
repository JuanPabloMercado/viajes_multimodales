from .imports import * 
from .base import Base 
from models.conexion_db import SessionLocal
from models import *
session = SessionLocal()



class Costos_viajes(Base):
    __tablename__ = 'Costos_viajes'
    
    id_costos_viajes = Column(Integer, primary_key = True, autoincrement=True)
    costo_base = Column(Numeric(10, 2), nullable=False)

    #Relación con la tabla Viajes a través de la tabla intermedia viajes_costos
    viajes_relacion = relationship('Viajes', secondary='Viajes_costos', back_populates='costos_viajes_relacion')
    
    #Métodos CRUD
    @classmethod
    def ingresar_costo(cls, costo_base: Numeric):
        with SessionLocal() as session:
            nuevo_costo = session.query(Costos_viajes).filter_by(costo_base=costo_base).first()
            
            if nuevo_costo:
                print(f"El costo {costo_base} ya existe con id {nuevo_costo.id_costos_viajes}")
                return nuevo_costo

            
            insercion = Costos_viajes(
                costo_base = costo_base
            )
            
            session.add(insercion)
            session.commit()
            session.refresh(insercion)
            print(f'Nuevo costo agregado: Id: {insercion.id_costos_viajes}.')
            return insercion











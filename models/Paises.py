from imports import *

class Paises(Base):
    __tablename__ = 'Paises'
    
    id_paises = Column(Integer, primary_key=True, autoincrement=True)
    nombre_pais = Column(String(100), nullable=False, unique=True)
    
    #Relación a la tabla Provincias
    provincias_relacion = relationship('Provincias', back_populates='paises_relacion')















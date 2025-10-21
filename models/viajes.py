from .imports import * 
from .base import Base 
from models.conexion_db import SessionLocal
from models import *
import logging
from .costos_viajes import Costos_viajes
from .Itinerarios import Itinerarios
from .cancelaciones import Cancelaciones
from .Itinerario_destinos import Itinerario_destinos
import logging
from sqlalchemy.orm import selectinload, joinedload, relationship # Añadido para Eager Loading
from decimal import Decimal

session = SessionLocal()


class Viajes(Base):
    """
    Representa la entidad Viajes, gestionando la creación, recuperación y
    presentación de un viaje multimodal completo, incluyendo itinerarios, costos,
    empresas, transportes y destinos anidados.
    """
    
    __tablename__ = 'Viajes'

    id_viajes = Column(Integer, primary_key = True, autoincrement=True)
    fecha_inicio = Column(DateTime)
    fecha_fin = Column(DateTime)
    estado = Column(
        Enum('Activo', 'Cancelado', 'Finalizado', name='estado_enum'),
        default='Activo',
        nullable=False
    )

    # Relaciones ORM
    cancelaciones_relacion = relationship('Cancelaciones', back_populates='viajes_relacion')
    costos_viajes_relacion = relationship('Costos_viajes', secondary='Viajes_costos', back_populates='viajes_relacion')
    empresas_relacion = relationship('Empresas', secondary='Empresas_viajes', back_populates='viajes_relacion')
    
    # RELACIÓN AGREGADA: Relación 1:N con Itinerarios. 
    # Es esencial para la consulta de carga ansiosa (Eager Loading) del viaje completo.
    itinerarios_relacion = relationship('Itinerarios', backref='viaje_parent') 

 
    # 1. MÉTODO DE CREACIÓN (Implementación completa del usuario)

    @classmethod
    def crear_viaje_completo(cls, datos_viaje: dict):
        """
        Crea un registro de Viajes junto con todas sus entidades anidadas
        (Empresas, Itinerarios, Destinos, Transporte) dentro de una única
        transacción de base de datos.
        
        Calcula el costo total del viaje sumando los costos de itinerarios,
        destinos y transportes asociados.

        :param datos_viaje: Diccionario con la estructura completa del viaje a crear.
        :type datos_viaje: dict
        :raises ValueError: Si no se encuentra alguna clave foránea (Empresa, DG, DE, Transporte).
        :raises Exception: Si la transacción falla, se ejecuta un rollback.
        :return: El objeto Viajes recién creado y registrado en la base de datos.
        :rtype: Viajes
        """
        # Configuración de logging (nivel INFO)
        logging.basicConfig(level=logging.INFO)
        logger = logging.getLogger("Viajes")

        try:
            with SessionLocal() as session:
                # 1. Crear el viaje principal
                viaje = cls(
                    fecha_inicio=datos_viaje['fecha_inicio'],
                    fecha_fin=datos_viaje['fecha_fin'],
                    estado=datos_viaje.get('estado', 'Activo')
                )
                session.add(viaje)
                session.commit()
                session.refresh(viaje)
                logger.info(f"Paso 1 Completo: Viaje ID {viaje.id_viajes} creado.")

                costo_total_viaje = Decimal(0)

                # 2. Asociar empresas
                num_empresas = len(datos_viaje.get('empresas_participantes', []))
                for id_empresa in datos_viaje.get('empresas_participantes', []):
                    empresa = session.query(Empresas).get(id_empresa)
                    if not empresa:
                        logger.error(f"Error FK: No se encontró la empresa con ID {id_empresa}.")
                        raise ValueError(f"Empresa con ID {id_empresa} no existe.")

                    viaje.empresas_relacion.append(empresa)

                session.commit()
                logger.info(f"Paso 2 Completo: {num_empresas} empresas asociadas al viaje {viaje.id_viajes}.")

                # 3. Crear itinerarios
                itinerarios_data_list = datos_viaje.get('itinerarios') or datos_viaje.get('Itinerarios', [])

                for i, itinerario_data in enumerate(itinerarios_data_list):
                    itinerario = Itinerarios(
                        fecha_inicio=itinerario_data['fecha_inicio'],
                        fecha_fin=itinerario_data['fecha_fin'],
                        detalle=itinerario_data.get('detalle'),
                        estado=itinerario_data.get('estado', 'Activo'),
                        id_viajes=viaje.id_viajes
                    )
                    session.add(itinerario)
                    session.commit()
                    session.refresh(itinerario)
                    logger.info(f"Creando Itinerario {i+1} (ID {itinerario.id_itinerarios}).")

                    costo_total_itinerario = Decimal(0)

                    # 3a. Destinos generales y específicos
                    num_destinos_registrados = 0
                    for dg in itinerario_data.get('destinos_generales', []):
                        id_dg = dg['id_destinos_generales']
                        orden = dg.get('orden_parada', 0)
                        destino_general = session.query(Destinos_generales).get(id_dg)
                        
                        if not destino_general:
                            logger.error(f"Error FK: No se encontró el Destino General con ID {id_dg}.")
                            raise ValueError(f"Destino General con ID {id_dg} no existe.")

                        destinos_especificos_list = dg.get('destinos_especificos', [])
                        
                        if destinos_especificos_list:
                            # CASO 1: DG CON Destinos Específicos (DE)
                            costo_base_dg = destino_general.costos_destinos_generales_relacion.costo_base if destino_general.costos_destinos_generales_relacion else 0
                            costo_total_itinerario += Decimal(costo_base_dg or 0)
                            
                            for id_de in destinos_especificos_list:
                                destino_especifico = session.query(Destinos_especificos).get(id_de)
                                
                                if not destino_especifico:
                                    logger.error(f"Error FK: No se encontró el Destino Específico con ID {id_de}.")
                                    raise ValueError(f"Destino Específico con ID {id_de} no existe.")
                                
                                costo_base_de = destino_especifico.costos_destinos_especificos_relacion.costo_base if destino_especifico.costos_destinos_especificos_relacion else 0
                                costo_total_itinerario += Decimal(costo_base_de or 0)
                                
                                registro_destino = Itinerario_destinos(
                                    id_itinerarios=itinerario.id_itinerarios,
                                    id_destinos_generales=id_dg,
                                    id_destinos_especificos=id_de,
                                    orden_parada=orden
                                )
                                session.add(registro_destino)
                                num_destinos_registrados += 1
                        else:
                            # CASO 2: DG SIN Destinos Específicos
                            costo_base_dg = destino_general.costos_destinos_generales_relacion.costo_base if destino_general.costos_destinos_generales_relacion else 0
                            costo_total_itinerario += Decimal(costo_base_dg or 0)
                            
                            registro_destino = Itinerario_destinos(
                                id_itinerarios=itinerario.id_itinerarios,
                                id_destinos_generales=id_dg,
                                id_destinos_especificos=None,
                                orden_parada=orden
                            )
                            session.add(registro_destino)
                            num_destinos_registrados += 1
                    
                    logger.info(f"Intentando guardar {num_destinos_registrados} registros de destinos...")
                    session.commit()
                    logger.info(f"Destinos guardados para Itinerario {itinerario.id_itinerarios}.")


                    # 3b. Medios de transporte
                    num_transportes_registrados = 0
                    for id_transporte in itinerario_data.get('medios_transporte', []):
                        transporte = session.query(Medios_transporte).get(id_transporte)
                        
                        if not transporte:
                            logger.error(f"Error FK: No se encontró el Medio de Transporte con ID {id_transporte}.")
                            raise ValueError(f"Medio de Transporte con ID {id_transporte} no existe.")
                        
                        itinerario.medios_transporte.append(transporte)
                        costo_base_transporte = transporte.costos_transporte_relacion.costo_base if transporte.costos_transporte_relacion else 0
                        costo_total_itinerario += Decimal(costo_base_transporte or 0)
                        num_transportes_registrados += 1
                        
                    logger.info(f"Intentando guardar {num_transportes_registrados} registros de transporte...")
                    session.commit()
                    logger.info(f"Transporte guardado para Itinerario {itinerario.id_itinerarios}.")

                    costo_total_viaje += costo_total_itinerario

                # 4. Registrar costo total del viaje
                registro_costo_total = Costos_viajes(costo_base=costo_total_viaje)
                session.add(registro_costo_total)
                
                # Asociamos el objeto y realizamos el commit final para costos.
                viaje.costos_viajes_relacion.append(registro_costo_total)
                
                logger.info(f"Intentando guardar costo total {costo_total_viaje} para viaje {viaje.id_viajes}...")
                session.commit()
                logger.info(f"Paso 4 Completo: Costo total asociado y guardado.")
                
                return viaje

        except Exception as e:
            logger.error(f"Transacción Fallida: {e}. Se ejecutó ROLLBACK.")
            raise 

    # 2. MÉTODO DE RECUPERACIÓN (Eager Loading)

    @classmethod
    def obtener_viaje_completo(cls, identificador: int):
        """
        Recupera una instancia de Viajes de la base de datos realizando una
        carga ansiosa (Eager Loading) de todas sus relaciones anidadas
        (Itinerarios, Transportes, Destinos, Costos).
        
        Este método es fundamental para evitar el problema N+1 y garantizar 
        que todos los datos estén accesibles al usar el objeto retornado.

        :param identificador: El ID único del viaje (id_viajes) a recuperar.
        :type identificador: int
        :raises ValueError: Si no se encuentra un viaje con el ID especificado.
        :return: El objeto Viajes con todas las relaciones cargadas.
        :rtype: Viajes
        """
        try:
            with SessionLocal() as session:
                
                # Consulta principal con Carga Ansiosa (Eager Loading)
                viaje = session.query(cls).filter(cls.id_viajes == identificador).options(
                    
                    # Nivel 1: Carga de relaciones de Viajes
                    selectinload(cls.costos_viajes_relacion),
                    selectinload(cls.empresas_relacion),
                    
                    # Nivel 2: Carga de Itinerarios (Relación 1:N)
                    selectinload(cls.itinerarios_relacion).options( 
                        
                        # Nivel 3: Carga de Medios_transporte (Relación N:M) y sus sub-relaciones 1:1 (joinedload)
                        selectinload(Itinerarios.medios_transporte).options(
                            joinedload(Medios_transporte.tipo_transporte_relacion),
                            joinedload(Medios_transporte.costos_transporte_relacion)
                        ),
                        
                        # Nivel 3: Carga de Itinerario_destinos (Relación 1:N) y sus sub-relaciones 1:1
                        selectinload(Itinerarios.itinerario_destinos_relacion).options( 
                            
                            # Nivel 4: Carga de Destino General y sus Costos
                            joinedload(Itinerario_destinos.destinos_generales_relacion).options(
                                joinedload(Destinos_generales.costos_destinos_generales_relacion)
                            ),
                            
                            # Nivel 4: Carga de Destino Específico y sus Costos
                            joinedload(Itinerario_destinos.destinos_especificos_relacion).options(
                                joinedload(Destinos_especificos.costos_destinos_especificos_relacion)
                            )
                        )
                    )
                ).first()

                if not viaje:
                    raise ValueError(f"No se encontró ningún viaje con ID {identificador}")

                return viaje
        
        except Exception as e:
            # Propaga la excepción para manejo superior
            raise e
            

    # 3. MÉTODO DE IMPRESIÓN/PRESENTACIÓN

    @classmethod
    def imprimir_viaje_completo(cls, id_viajes: int):
        """
        Recupera el objeto Viajes completo utilizando obtener_viaje_completo()
        e imprime su información detallada de manera estructurada en consola.
        
        Este método separa la lógica de presentación de la lógica de recuperación
        de datos.

        :param id_viajes: El ID único del viaje a imprimir.
        :type id_viajes: int
        :raises ValueError: Si el viaje no es encontrado por el método de recuperación.
        :raises Exception: Para cualquier otro error durante el proceso.
        :return: None (Imprime directamente en la salida estándar).
        """
        try:
            # 1. Recupera el objeto completamente cargado
            viaje = cls.obtener_viaje_completo(id_viajes)

            print("\n" + "="*70)
            print(f"RESUMEN DE VIAJE ID: {viaje.id_viajes} | ESTADO: {viaje.estado}")
            print("="*70)
            
            # Formateo de fechas para impresión
            fecha_inicio_str = viaje.fecha_inicio.strftime('%Y-%m-%d') if isinstance(viaje.fecha_inicio, (datetime, date)) else str(viaje.fecha_inicio)
            fecha_fin_str = viaje.fecha_fin.strftime('%Y-%m-%d') if isinstance(viaje.fecha_fin, (datetime, date)) else str(viaje.fecha_fin)
            print(f"Fechas: {fecha_inicio_str} a {fecha_fin_str}")

            # Costo Total
            costo_total = viaje.costos_viajes_relacion[0].costo_base if viaje.costos_viajes_relacion else Decimal(0)
            print(f"Costo Base Total del Viaje: ${costo_total:,.2f}")
            
            # Empresas
            # Se extrae la razón social de la relación y se unen en una cadena.
            empresas = [e.razon_social for e in viaje.empresas_relacion]
            print(f"Empresas Participantes: {', '.join(empresas) if empresas else 'Ninguna'}")
            print("-" * 70)

            # Itinerarios
            # Recorre la lista de itinerarios cargados ansiosamente
            for i, itinerario in enumerate(viaje.itinerarios_relacion, 1):
                print(f"ITINERARIO {i}: ID {itinerario.id_itinerarios} - {itinerario.detalle or 'Sin Detalle'}")
                # El resto del código de impresión de itinerario, transporte y destinos iría aquí.

            print("-" * 70)

        except ValueError as ve:
            print(f"ERROR: {ve}")
        except Exception as e:
            print(f"Ocurrió un error al procesar el viaje: {e}")
            
            
            
    @classmethod
    def cancelar_viaje(cls, id_viajes: int):
        """
        Cancela un viaje estableciendo su estado a 'Cancelado'.
        
        :param id_viajes: El ID único del viaje a cancelar.
        :type id_viajes: int
        :raises ValueError: Si no se encuentra un viaje con el ID especificado.
        :return: El objeto Viajes actualizado.
        :rtype: Viajes
        """
        try:
            with SessionLocal() as session:
                viaje = session.query(cls).filter(cls.id_viajes == id_viajes).first()
                
                if not viaje:
                    raise ValueError(f"No se encontró ningún viaje con ID {id_viajes}")
                
                viaje.estado = 'Cancelado'
                session.commit()
                session.refresh(viaje)
                print(f'El viaje con ID {id_viajes} ha sido cancelado exitosamente.')
                
                detalle_cancelacion = Cancelaciones(
                    observaciones='Cancelación automática mediante el método cancelar_viaje.',
                    fecha_cancelacion=datetime.now(),
                    id_viajes=id_viajes,
                    id_tipo_cancelacion= 2
                )
                
                session.add(detalle_cancelacion)
                session.commit()
                session.refresh(detalle_cancelacion)
                print(f'Detalle de cancelación registrado: {detalle_cancelacion.id_cancelaciones}')
                
                return viaje
        
        except Exception as e:
            raise e

    @classmethod
    def gastos_totales_viaje(cls, id_viajes: int) -> Decimal:
        """
        Calcula y retorna el gasto total asociado a un viaje específico.
        
        :param id_viajes: El ID único del viaje.
        :type id_viajes: int
        :raises ValueError: Si no se encuentra un viaje con el ID especificado.
        :return: El gasto total del viaje.
        :rtype: Decimal
        """
        try:
            with SessionLocal() as session:
                viaje = session.query(cls).filter(cls.id_viajes == id_viajes).first()
                
                if not viaje:
                    raise ValueError(f"No se encontró ningún viaje con ID {id_viajes}")
                
                costo_total = Decimal(0)
                
                for costo in viaje.costos_viajes_relacion:
                    costo_total += costo.costo_base or Decimal(0)
                
                return costo_total
        
        except Exception as e:
            raise e









"""
class Viajes(Base):
    
    __tablename__ = 'Viajes'

    id_viajes = Column(Integer, primary_key = True, autoincrement=True)
    fecha_inicio = Column(DateTime)
    fecha_fin = Column(DateTime)
    estado = Column(
        Enum('Activo', 'Cancelado', 'Finalizado', name='estado_enum'),
        default='Activo',
        nullable=False
    )

    #Relación con la tabla cancelaciones
    cancelaciones_relacion = relationship('Cancelaciones', back_populates='viajes_relacion')
    #Relación con la tabla costos_viajes a través de la tabla intermedia viajes_costos
    costos_viajes_relacion = relationship('Costos_viajes', secondary='Viajes_costos', back_populates='viajes_relacion')
    #Relación N:M com la tabla Empresas utilizando la relación intermedia Empresas_viajes
    empresas_relacion = relationship('Empresas', secondary='Empresas_viajes', back_populates='viajes_relacion')
    
    #Creación general para la adquisición de un viaje, incluye itinerarios, gestión de destinos, transporte, costos, etc. 
    @classmethod
    def crear_viaje_completo(cls, datos_viaje: dict):
        # Configuración de logging (nivel INFO)
        logging.basicConfig(level=logging.INFO)
        logger = logging.getLogger("Viajes")

        try:
            with SessionLocal() as session:
                # 1️⃣ Crear el viaje principal
                viaje = cls(
                    fecha_inicio=datos_viaje['fecha_inicio'],
                    fecha_fin=datos_viaje['fecha_fin'],
                    estado=datos_viaje.get('estado', 'Activo')
                )
                session.add(viaje)
                session.commit()
                session.refresh(viaje)
                logger.info(f"✅ PASO 1 COMPLETO: Viaje ID {viaje.id_viajes} creado.")

                costo_total_viaje = Decimal(0)

                # 2️⃣ Asociar empresas
                num_empresas = len(datos_viaje.get('empresas_participantes', []))
                for id_empresa in datos_viaje.get('empresas_participantes', []):
                    empresa = session.query(Empresas).get(id_empresa)
                    if not empresa:
                        logger.error(f"❌ ERROR FK: No se encontró la empresa con ID {id_empresa}.")
                        raise ValueError(f"Empresa con ID {id_empresa} no existe.")

                    viaje.empresas_relacion.append(empresa)

                session.commit()
                logger.info(f"✅ PASO 2 COMPLETO: {num_empresas} empresas asociadas al viaje {viaje.id_viajes}.")

                # 3️⃣ Crear itinerarios
                itinerarios_data_list = datos_viaje.get('itinerarios') or datos_viaje.get('Itinerarios', [])

                for i, itinerario_data in enumerate(itinerarios_data_list):
                    itinerario = Itinerarios(
                        fecha_inicio=itinerario_data['fecha_inicio'],
                        fecha_fin=itinerario_data['fecha_fin'],
                        detalle=itinerario_data.get('detalle'),
                        estado=itinerario_data.get('estado', 'Activo'),
                        id_viajes=viaje.id_viajes
                    )
                    session.add(itinerario)
                    session.commit()
                    session.refresh(itinerario)
                    logger.info(f"👉 Creando Itinerario {i+1} (ID {itinerario.id_itinerarios}).")

                    costo_total_itinerario = Decimal(0)

                    # 3a️⃣ Destinos generales y específicos
                    num_destinos_registrados = 0
                    for dg in itinerario_data.get('destinos_generales', []):
                        id_dg = dg['id_destinos_generales']
                        orden = dg.get('orden_parada', 0)
                        destino_general = session.query(Destinos_generales).get(id_dg)
                        
                        if not destino_general:
                            logger.error(f"❌ ERROR FK: No se encontró el Destino General con ID {id_dg}.")
                            raise ValueError(f"Destino General con ID {id_dg} no existe.")

                        destinos_especificos_list = dg.get('destinos_especificos', [])
                        
                        if destinos_especificos_list:
                            # CASO 1: DG CON Destinos Específicos (DE)
                            costo_base_dg = destino_general.costos_destinos_generales_relacion.costo_base if destino_general.costos_destinos_generales_relacion else 0
                            costo_total_itinerario += Decimal(costo_base_dg or 0)
                            
                            for id_de in destinos_especificos_list:
                                destino_especifico = session.query(Destinos_especificos).get(id_de)
                                
                                if not destino_especifico:
                                    logger.error(f"❌ ERROR FK: No se encontró el Destino Específico con ID {id_de}.")
                                    raise ValueError(f"Destino Específico con ID {id_de} no existe.")
                                
                                costo_base_de = destino_especifico.costos_destinos_especificos_relacion.costo_base if destino_especifico.costos_destinos_especificos_relacion else 0
                                costo_total_itinerario += Decimal(costo_base_de or 0)
                                
                                registro_destino = Itinerario_destinos(
                                    id_itinerarios=itinerario.id_itinerarios,
                                    id_destinos_generales=id_dg,
                                    id_destinos_especificos=id_de,
                                    orden_parada=orden
                                )
                                session.add(registro_destino)
                                num_destinos_registrados += 1
                        else:
                            # CASO 2: DG SIN Destinos Específicos
                            costo_base_dg = destino_general.costos_destinos_generales_relacion.costo_base if destino_general.costos_destinos_generales_relacion else 0
                            costo_total_itinerario += Decimal(costo_base_dg or 0)
                            
                            registro_destino = Itinerario_destinos(
                                id_itinerarios=itinerario.id_itinerarios,
                                id_destinos_generales=id_dg,
                                id_destinos_especificos=None,
                                orden_parada=orden
                            )
                            session.add(registro_destino)
                            num_destinos_registrados += 1
                    
                    logger.info(f"✨ Intentando guardar {num_destinos_registrados} registros de destinos...")
                    session.commit()
                    logger.info(f"✅ Destinos guardados para Itinerario {itinerario.id_itinerarios}.")


                    # 3b️⃣ Medios de transporte
                    num_transportes_registrados = 0
                    for id_transporte in itinerario_data.get('medios_transporte', []):
                        transporte = session.query(Medios_transporte).get(id_transporte)
                        
                        if not transporte:
                            logger.error(f"❌ ERROR FK: No se encontró el Medio de Transporte con ID {id_transporte}.")
                            raise ValueError(f"Medio de Transporte con ID {id_transporte} no existe.")
                        
                        itinerario.medios_transporte.append(transporte)
                        costo_base_transporte = transporte.costos_transporte_relacion.costo_base if transporte.costos_transporte_relacion else 0
                        costo_total_itinerario += Decimal(costo_base_transporte or 0)
                        num_transportes_registrados += 1
                        
                    logger.info(f"✨ Intentando guardar {num_transportes_registrados} registros de transporte...")
                    session.commit()
                    logger.info(f"✅ Transporte guardado para Itinerario {itinerario.id_itinerarios}.")

                    costo_total_viaje += costo_total_itinerario

                # 4️⃣ Registrar costo total del viaje
                registro_costo_total = Costos_viajes(costo_base=costo_total_viaje)
                session.add(registro_costo_total)
                
                # Asociamos el objeto y realizamos el commit final para costos.
                viaje.costos_viajes_relacion.append(registro_costo_total)
                
                logger.info(f"✨ Intentando guardar costo total {costo_total_viaje} para viaje {viaje.id_viajes}...")
                session.commit()
                logger.info(f"✅ PASO 4 COMPLETO: Costo total asociado y guardado.")
                
                # ❌ session.refresh(viaje) ELIMINADO para evitar el ROLLBACK transaccional innecesario.

                return viaje

        except Exception as e:
            logger.error(f"🛑 TRANSACCIÓN FALLIDA: {e}. Se ejecutó ROLLBACK.")
            raise # Propaga el error para que la aplicación lo maneje.
    
    

"""
    
    
    
    
    
    
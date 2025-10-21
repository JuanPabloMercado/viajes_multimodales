
-- TRIGGERS: Destinos_especificos


CREATE TRIGGER trg_destinos_especificos_insert
AFTER INSERT ON "Destinos_especificos"
FOR EACH ROW
BEGIN
    INSERT INTO "Historial_cambios" (
        registro_afectado,
        razon_cambio,
        fecha_cambio,
        id_tablas_sistema,
        id_tipo_cambio
    )
    VALUES (
        NEW.id_destinos_especificos,
        'Trigger automático: INSERT en Destinos_especificos',
        CURRENT_TIMESTAMP,
        (SELECT id_tabla_sistema FROM "Tablas_sistema" WHERE nombre_tabla = 'Destinos_especificos'),
        (SELECT id_tipo_cambio FROM "Tipo_cambio" WHERE nombre_tipo = 'INSERT')
    );
END;

CREATE TRIGGER trg_destinos_especificos_update
AFTER UPDATE ON "Destinos_especificos"
FOR EACH ROW
BEGIN
    INSERT INTO "Historial_cambios" (
        registro_afectado,
        razon_cambio,
        fecha_cambio,
        id_tablas_sistema,
        id_tipo_cambio
    )
    VALUES (
        OLD.id_destinos_especificos,
        'Trigger automático: UPDATE en Destinos_especificos',
        CURRENT_TIMESTAMP,
        (SELECT id_tabla_sistema FROM "Tablas_sistema" WHERE nombre_tabla = 'Destinos_especificos'),
        (SELECT id_tipo_cambio FROM "Tipo_cambio" WHERE nombre_tipo = 'UPDATE')
    );

    INSERT INTO "Historial_detalle" (campo_modificado, valor_anterior, valor_nuevo, id_historial_cambios)
    SELECT 'hora_inicio', OLD.hora_inicio, NEW.hora_inicio, last_insert_rowid()
    WHERE OLD.hora_inicio IS NOT NEW.hora_inicio;

    INSERT INTO "Historial_detalle" (campo_modificado, valor_anterior, valor_nuevo, id_historial_cambios)
    SELECT 'hora_fin', OLD.hora_fin, NEW.hora_fin, last_insert_rowid()
    WHERE OLD.hora_fin IS NOT NEW.hora_fin;

    INSERT INTO "Historial_detalle" (campo_modificado, valor_anterior, valor_nuevo, id_historial_cambios)
    SELECT 'detalles', OLD.detalles, NEW.detalles, last_insert_rowid()
    WHERE OLD.detalles IS NOT NEW.detalles;

    INSERT INTO "Historial_detalle" (campo_modificado, valor_anterior, valor_nuevo, id_historial_cambios)
    SELECT 'id_costos_destinos_especificos', OLD.id_costos_destinos_especificos, NEW.id_costos_destinos_especificos, last_insert_rowid()
    WHERE OLD.id_costos_destinos_especificos IS NOT NEW.id_costos_destinos_especificos;

    INSERT INTO "Historial_detalle" (campo_modificado, valor_anterior, valor_nuevo, id_historial_cambios)
    SELECT 'id_destinos_generales', OLD.id_destinos_generales, NEW.id_destinos_generales, last_insert_rowid()
    WHERE OLD.id_destinos_generales IS NOT NEW.id_destinos_generales;
END;



-- TRIGGERS: Empresas


CREATE TRIGGER trg_empresas_update
AFTER UPDATE ON "Empresas"
FOR EACH ROW
BEGIN
    INSERT INTO "Historial_cambios" (
        registro_afectado,
        razon_cambio,
        fecha_cambio,
        id_tablas_sistema,
        id_tipo_cambio
    )
    VALUES (
        OLD.id_empresas,
        'Trigger automático: UPDATE en Empresas',
        CURRENT_TIMESTAMP,
        (SELECT id_tabla_sistema FROM "Tablas_sistema" WHERE nombre_tabla = 'Empresas'),
        (SELECT id_tipo_cambio FROM "Tipo_cambio" WHERE nombre_tipo = 'UPDATE')
    );

    INSERT INTO "Historial_detalle" (campo_modificado, valor_anterior, valor_nuevo, id_historial_cambios)
    SELECT 'cuit', OLD.cuit, NEW.cuit, last_insert_rowid() WHERE OLD.cuit IS NOT NEW.cuit;

    INSERT INTO "Historial_detalle" (campo_modificado, valor_anterior, valor_nuevo, id_historial_cambios)
    SELECT 'razon_social', OLD.razon_social, NEW.razon_social, last_insert_rowid() WHERE OLD.razon_social IS NOT NEW.razon_social;

    INSERT INTO "Historial_detalle" (campo_modificado, valor_anterior, valor_nuevo, id_historial_cambios)
    SELECT 'domicilio', OLD.domicilio, NEW.domicilio, last_insert_rowid() WHERE OLD.domicilio IS NOT NEW.domicilio;

    INSERT INTO "Historial_detalle" (campo_modificado, valor_anterior, valor_nuevo, id_historial_cambios)
    SELECT 'estado', OLD.estado, NEW.estado, last_insert_rowid() WHERE OLD.estado IS NOT NEW.estado;
END;

CREATE TRIGGER tgr_empresas_bfr_update
BEFORE UPDATE ON "Empresas"
FOR EACH ROW
BEGIN
    SELECT RAISE(ABORT, 'No se puede modificar la empresa. El estado debe ser Activo.')
    WHERE OLD.estado IS NOT 'Activo';

    SELECT RAISE(ABORT, 'No se puede cambiar el cuit. La empresa tiene viajes activos asociados.')
    WHERE OLD.cuit IS NOT NEW.cuit
      AND EXISTS (
          SELECT 1
          FROM "Empresas_viajes" AS ev
          JOIN "Viajes" AS v
          ON ev.id_viajes = v.id_viajes
          WHERE ev.id_empresas = OLD.id_empresas
            AND v.estado = 'Activo'
      );
END;

CREATE TRIGGER tge_empresas_soft_delete
BEFORE DELETE ON "Empresas"
FOR EACH ROW
BEGIN
    SELECT RAISE(ABORT, 'No se puede dar de baja la empresa. Tiene viajes activos asociados.')
    WHERE EXISTS (
        SELECT 1
        FROM "Empresas_viajes" ev
        JOIN "Viajes" v
        ON ev.id_viajes = v.id_viajes
        WHERE ev.id_empresas = OLD.id_empresas
          AND v.estado = 'Activo'
    );

    UPDATE "Empresas"
    SET estado = 'Inactivo'
    WHERE id_empresas = OLD.id_empresas;

    INSERT INTO "Historial_cambios" (
        registro_afectado,
        razon_cambio,
        fecha_cambio,
        id_tablas_sistema,
        id_tipo_cambio
    )
    VALUES (
        OLD.id_empresas,
        'Trigger automático: Baja lógica (DELETE) en Empresas.',
        CURRENT_TIMESTAMP,
        (SELECT id_tabla_sistema FROM "Tablas_sistema" WHERE nombre_tabla = 'Empresas'),
        (SELECT id_tipo_cambio FROM "Tipo_cambio" WHERE nombre_tipo = 'DELETE')
    );

    INSERT INTO "Historial_detalle" (campo_modificado, valor_anterior, valor_nuevo, id_historial_cambios)
    SELECT 'estado', OLD.estado, 'Inactivo', last_insert_rowid();
END;



-- TRIGGERS: Empleados


CREATE TRIGGER tgr_empleados_bfr_update
BEFORE UPDATE ON "Empleados"
FOR EACH ROW
BEGIN
    SELECT RAISE(ABORT, 'No se puede modificar el empleado. El estado debe ser Activo.')
    WHERE OLD.estado IS NOT 'Activo';
END;

CREATE TRIGGER tgr_empleados_soft_delete
BEFORE DELETE ON "Empleados"
FOR EACH ROW
BEGIN
    UPDATE "Empleados"
    SET estado = 'Inactivo'
    WHERE id_empleados = OLD.id_empleados;

    INSERT INTO "Historial_cambios" (
        registro_afectado,
        razon_cambio,
        fecha_cambio,
        id_tablas_sistema,
        id_tipo_cambio
    )
    VALUES (
        OLD.id_empleados,
        'Trigger automático: Baja lógica (DELETE) en Empleados.',
        CURRENT_TIMESTAMP,
        (SELECT id_tabla_sistema FROM "Tablas_sistema" WHERE nombre_tabla = 'Empleados'),
        (SELECT id_tipo_cambio FROM "Tipo_cambio" WHERE nombre_tipo = 'DELETE')
    );

    INSERT INTO "Historial_detalle" (
        campo_modificado,
        valor_anterior,
        valor_nuevo,
        id_historial_cambios
    )
    SELECT 'estado', OLD.estado, 'Inactivo', last_insert_rowid();

    SELECT RAISE(ABORT, 'Baja lógica ejecutada correctamente. La eliminación física fue prevenida.');
END;


-- TRIGGERS: Itinerarios


CREATE TRIGGER tgr_itinerarios_aft_insert
AFTER INSERT ON "Itinerarios"
FOR EACH ROW
BEGIN
    INSERT INTO "Historial_cambios" (
        registro_afectado,
        razon_cambio,
        fecha_cambio,
        id_tablas_sistema,
        id_tipo_cambio
    )
    VALUES (
        NEW.id_itinerarios,
        'Trigger automático: INSERT en Itinerarios',
        CURRENT_TIMESTAMP,
        (SELECT id_tabla_sistema FROM "Tablas_sistema" WHERE nombre_tabla = 'Itinerarios'),
        (SELECT id_tipo_cambio FROM "Tipo_cambio" WHERE nombre_tipo = 'INSERT')
    );
END;

CREATE TRIGGER tgr_itinerarios_aft_update
AFTER UPDATE ON "Itinerarios"
FOR EACH ROW
BEGIN
    INSERT INTO "Historial_cambios" (
        registro_afectado,
        razon_cambio,
        fecha_cambio,
        id_tablas_sistema,
        id_tipo_cambio
    )
    VALUES (
        OLD.id_itinerarios,
        'Trigger automático: UPDATE en Itinerarios',
        CURRENT_TIMESTAMP,
        (SELECT id_tabla_sistema FROM "Tablas_sistema" WHERE nombre_tabla = 'Itinerarios'),
        (SELECT id_tipo_cambio FROM "Tipo_cambio" WHERE nombre_tipo = 'UPDATE')
    );

    INSERT INTO "Historial_detalle" (campo_modificado, valor_anterior, valor_nuevo, id_historial_cambios)
    SELECT 'fecha_inicio', OLD.fecha_inicio, NEW.fecha_inicio, last_insert_rowid()
    WHERE OLD.fecha_inicio IS NOT NEW.fecha_inicio;

    INSERT INTO "Historial_detalle" (campo_modificado, valor_anterior, valor_nuevo, id_historial_cambios)
    SELECT 'fecha_fin', OLD.fecha_fin, NEW.fecha_fin, last_insert_rowid()
    WHERE OLD.fecha_fin IS NOT NEW.fecha_fin;

    INSERT INTO "Historial_detalle" (campo_modificado, valor_anterior, valor_nuevo, id_historial_cambios)
    SELECT 'detalle', OLD.detalle, NEW.detalle, last_insert_rowid()
    WHERE OLD.detalle IS NOT NEW.detalle;

    INSERT INTO "Historial_detalle" (campo_modificado, valor_anterior, valor_nuevo, id_historial_cambios)
    SELECT 'id_viajes', OLD.id_viajes, NEW.id_viajes, last_insert_rowid()
    WHERE OLD.id_viajes IS NOT NEW.id_viajes;
END;

CREATE TRIGGER tgr_itinerarios_soft_delete
BEFORE DELETE ON "Itinerarios"
FOR EACH ROW
BEGIN
    SELECT RAISE(ABORT, 'No se puede dar de baja el itinerario. El viaje asociado se encuentra en estado "Activo".')
    WHERE EXISTS (
        SELECT 1
        FROM "Viajes" v
        WHERE v.id_viajes = OLD.id

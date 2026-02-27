/* Totales por sede:
    ¿Cuántos alumnos hay en cada plantel?
*/

SELECT
    PLANTEL.plantel AS SEDE, 
    COUNT(ASIGNACION.folio) AS NUM_ALUMNOS
FROM planteles PLANTEL
INNER JOIN oferta_academica OFERTA
ON PLANTEL.id = OFERTA.id_plantel
    LEFT JOIN asignaciones ASIGNACION
    ON OFERTA.id = ASIGNACION.id_oferta_asignada
GROUP BY PLANTEL.plantel
ORDER BY PLANTEL.plantel asc;

/* Popularidad de carreras:
    ¿Cuál es la carrera con más asignados en total?
*/

SELECT
    CARRERAS.carrera AS CARRERA,
    COUNT(ASIGNACION.folio) AS NUM_ALUMNOS
FROM carreras CARRERAS
INNER JOIN oferta_academica OFERTA
ON CARRERAS.id = OFERTA.id_carrera
    INNER JOIN asignaciones ASIGNACION
    ON OFERTA.id = ASIGNACION.id_oferta_asignada
GROUP BY CARRERAS.carrera
ORDER BY ALUMNOS desc
LIMIT 1;

/* Diversidad académica:
    ¿Cuántas carreras distintas se ofrecen en cada plantel?
*/

SELECT
    PLANTEL.plantel AS SEDE,
    COUNT(OFERTA.id_carrera) AS NUM_CARRERAS
FROM planteles PLANTEL
INNER JOIN oferta_academica OFERTA
ON PLANTEL.id = OFERTA.id_plantel
GROUP BY PLANTEL.plantel;

/* Conteo de folios:
    ¿Cuántos registros totales hay en la base de datos?
*/

-- Total de registros en la base de datos
SELECT
    SUM(REGISTROS_TABLA) AS NUM_REGISTROS_DB
FROM (
    SELECT 
        COUNT(*) AS REGISTROS_TABLA
    FROM carreras
    
    UNION ALL

    SELECT
        COUNT(*)
    FROM planteles

    UNION ALL

    SELECT
        COUNT(*)
    FROM oferta_academica

    UNION ALL

    SELECT
        COUNT(*)
    FROM aspirantes

    UNION ALL
    
    SELECT
        COUNT(*)
    FROM asignaciones
);

-- Registros de aspirantes

SELECT
    COUNT(*) AS NUM_ASPIRANTES
FROM aspirantes;

/* Análisis de Género:
    ¿Cuál es el porcentaje de hombres y mujeres asignados?
*/

/* Filtros complejos:
    ¿Cuántos alumnos con el apellido más numeroso fueron asignados a carreras técnicas?
*/

/* Filtros complejos:
    ¿Cuántos alumnos hay por cada letra inicial del apellido?
*/

/* Detección de errores:
    ¿Hay alguna CURP que no tenga los 18 caracteres reglamentarios?
*/

/* Cruce de datos:
    ¿Cuál es la carrera más saturada del plantel con menos alumnos totales?
*/

/* Distribución por Estado:
    ¿Cuántos alumnos vienen de un estado diferente al de la sede del plantel?
*/

/* Ranking:
    "Top 3" de las carreras por cada plantel.
*/
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
ORDER BY NUM_ALUMNOS desc
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

SELECT
    SUBSTR(curp, 11, 1) AS SEXO,
    COUNT(*) AS NUM_ALUMNOS
FROM aspirantes
GROUP BY SEXO;

/* Filtros complejos:
    ¿Cuántos alumnos hay por cada letra inicial del apellido?
*/

SELECT 
    SUBSTR(curp, 1, 1) AS LETRA_INICIAL,
    COUNT(*) AS NUM_ALUMNOS
FROM aspirantes
GROUP BY LETRA_INICIAL;

/* Detección de errores:
    ¿Hay alguna CURP que no tenga los 18 caracteres reglamentarios?
*/

-- Verificar existencia de CURPs con tamaño distinto al oficial

SELECT
    LENGTH(curp) AS TAMANO_CURP
FROM aspirantes
WHERE TAMANO_CURP != 18;

-- Contar existencias de CURPs por tamaños

SELECT
    LENGTH(curp) AS TAMANO_CURP,
    COUNT(*) AS NUM_CURP,
FROM aspirantes
GROUP BY TAMANO_CURP;

-- Visualizar dichas CURPS con tamaño no oficial: Query 1

SELECT 
    curp AS CURP_INVALIDA
FROM aspirantes
WHERE LENGTH(curp) != 18;

-- Visualizar dichas CURPs con tamaño no oficial: Query 2

SELECT
    curp AS CURP_INVALIDA,
    LENGTH(curp) AS CURP_TAMANO
FROM aspirantes
WHERE CURP_TAMANO != 18;

/* Cruce de datos:
    ¿Cuál es la carrera más saturada del plantel con menos alumnos totales?
*/

-- Obtenemos el plantel con menos alumnos

SELECT
    PLANTEL.plantel AS SEDE,
    COUNT(ASIGNACION.folio) AS NUM_ALUMNOS
FROM planteles PLANTEL
INNER JOIN oferta_academica OFERTA
ON PLANTEL.id = OFERTA.id_plantel
    LEFT JOIN asignaciones ASIGNACION
    ON OFERTA.id = ASIGNACION.id_oferta_asignada
GROUP BY PLANTEL.plantel
ORDER BY NUM_ALUMNOS asc
LIMIT 1;

-- Con la query anterior buscamos la cantidad de alumnos por carrera y por plantel y filtramos con el dato obtenido anteriormente

SELECT
    PLANTEL.plantel AS SEDE,
    CARRERA.carrera AS ESTUDIO,
    COUNT(ASIGNACION.folio) AS NUM_ALUMNOS
FROM planteles PLANTEL
INNER JOIN oferta_academica OFERTA
ON PLANTEL.id = OFERTA.id_plantel
    LEFT JOIN asignaciones ASIGNACION
    ON OFERTA.id = ASIGNACION.id_oferta_asignada
        LEFT JOIN carreras CARRERA
        ON CARRERA.id = OFERTA.id_carrera
WHERE PLANTEL.plantel = 'LEONA VICARIO'
GROUP BY SEDE, ESTUDIO
ORDER BY NUM_ALUMNOS DESC
LIMIT 1;


/* Distribución por Estado:
    ¿Cuántos alumnos vienen de un estado diferente al de la sede del plantel?
*/

SELECT
    COUNT(curp) AS ESTUDIANTES_OTROS_ESTADOS
FROM aspirantes
WHERE SUBSTR(curp, 12, 2) != 'QR';
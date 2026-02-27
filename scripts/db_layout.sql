-- Maquetación de la base de datos en SQLite
-- Crear y usar la base de datos para los aspirantes

CREATE DATABASE ADMISIONES_COLEGIO_QROO_2020;

USE ADMISIONES_COLEGIO_QROO_2020;

-- Para que funcionen las FOREIGN KEYS

PRAGMA foreign_keys = ON;

-- Crear las tablas principales

CREATE TABLE IF NOT EXISTS carreras (
    id INTEGER NOT NULL,
    carrera TEXT UNIQUE NOT NULL,
    
    PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS planteles (
    id INTEGER NOT NULL,
    plantel TEXT UNIQUE NOT NULL,

    PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS oferta_academica (
    id INTEGER NOT NULL,
    id_plantel INTEGER NOT NULL,
    id_carrera INTEGER NOT NULL, 

    PRIMARY KEY (id),

    FOREIGN KEY (id_plantel) REFERENCES planteles(id),
    FOREIGN KEY (id_carrera) REFERENCES carreras(id)
);

CREATE TABLE IF NOT EXISTS aspirantes (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    curp TEXT UNIQUE NOT NULL,
    aspirante TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS asignaciones (
    folio INTEGER UNIQUE NOT NULL,
    id_aspirante INTEGER UNIQUE NOT NULL,
    id_oferta_asignada INTEGER NOT NULL,
    
    PRIMARY KEY (folio),

    FOREIGN KEY (id_aspirante) REFERENCES aspirantes(id),
    FOREIGN KEY (id_oferta_asignada) REFERENCES oferta_academica(id)
);

-- Inserción de datos

INSERT INTO carreras(id, carrera) -- el id por índice del método
VALUES (?, ?);

INSERT INTO planteles(id, plantel)
VALUES (?, ?);

INSERT INTO oferta_academica(id, id_plantel, id_carrera)
VALUES (?, ?, ?);

INSERT INTO aspirantes(curp, aspirante)
VALUES (?, ?);

INSERT INTO asignaciones(folio, id_aspirante, id_oferta_asignada)
VALUES (?, ?, ?);

-- Eliminar base de datos

DROP TABLE IF EXISTS;
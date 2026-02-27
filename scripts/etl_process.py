import sqlite3, os

def open_file(path: str, function, *args):
    with open(path) as file:
        var = function(file, *args)

        return var

def get_fields(file) -> list[str]:
    fields_ln: list = file.readline().rstrip().split(';')
    fields: list[str] = [field.strip().upper() for field in fields_ln]

    return fields

def get_careers(file) -> list[str]:
    unordered_careers: set = set()

    next(file)
    for ln in file:
        career: str = ln.split(';')[-2].strip().upper()

        if career not in unordered_careers:
            unordered_careers.add(career)

    careers: list[str] = sorted(list(unordered_careers))

    return careers

def get_campus(file) -> list[str]:
    unordered_campus: set = set()

    next(file)
    for ln in file:
        plantel: str = ln.split(';')[-1].strip().upper()

        if plantel not in unordered_campus:
            unordered_campus.add(plantel)

    campus: list[str] = sorted(list(unordered_campus)) 

    return campus

def get_academic_offer(file) -> dict[str, list[str]]:
    academic_offer: dict[str, list[str]] = dict()

    next(file)
    for ln in file:
        campus: str = ln.split(';')[-1].strip().upper()
        career: str = ln.split(';')[-2].strip().upper()

        if campus not in academic_offer:
            academic_offer[campus] = list()

        if career not in academic_offer[campus]:
            academic_offer[campus].append(career)
            
    sorted(academic_offer)

    return academic_offer

def connect_db(path: str, function, *args) -> bool:
    try:
        try:
            connection = sqlite3.connect(path)
            with connection as db:
                print(f'Se ha aperturado la base de datos en SQLite con versión {sqlite3.sqlite_version} con éxito.')
                
                return function(db, *args)
       
        except sqlite3.OperationalError as sqlite_error:
            print(f'Ha fallado la apertura de la base de datos: {sqlite_error}.')
            return False
    except ModuleNotFoundError as module_error:
        print(f'Error. Ha fallado la importación del módulo "sqlite3": {module_error}.')
        return False

def create_tables(database) -> bool:
    sql_statements: list[str] = [
        '''PRAGMA foreign_keys = ON;''',

        '''CREATE TABLE IF NOT EXISTS planteles (
            id INTEGER NOT NULL,
            plantel TEXT UNIQUE NOT NULL,

            PRIMARY KEY (id)
        );''',

        '''CREATE TABLE IF NOT EXISTS carreras (
            id INTEGER NOT NULL,
            carrera TEXT UNIQUE NOT NULL,

            PRIMARY KEY (id)
        );''',

        '''CREATE TABLE IF NOT EXISTS oferta_academica (
            id INTEGER NOT NULL,
            id_plantel INTEGER NOT NULL,
            id_carrera INTEGER NOT NULL, 

            PRIMARY KEY (id),

            FOREIGN KEY (id_plantel) REFERENCES planteles(id),
            FOREIGN KEY (id_carrera) REFERENCES carreras(id)
        );''',

        '''CREATE TABLE IF NOT EXISTS aspirantes (
            id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
            curp TEXT UNIQUE NOT NULL,
            aspirante TEXT NOT NULL
        );''',

        '''CREATE TABLE IF NOT EXISTS asignaciones (
            folio INTEGER UNIQUE NOT NULL,
            id_aspirante INTEGER UNIQUE NOT NULL,
            id_oferta_asignada INTEGER NOT NULL,

            PRIMARY KEY (folio),

            FOREIGN KEY (id_aspirante) REFERENCES aspirantes(id),
            FOREIGN KEY (id_oferta_asignada) REFERENCES oferta_academica(id)
        );'''  
    ]

    try:
        for statement in sql_statements:
            database.cursor().execute(statement)
    except sqlite3.Error as sqlite_error:
        print(f'Se ha producido un error al crear una tabla. {sqlite_error}')
        return False
    else:
        database.commit()
        print('Se ha creado todas las tablas con éxito.')
        return True

# def create_tables(db, name_table, fields_type_table):
#     try:
#         field_type: list = [f'{key} {value}' for key, value in fields_type_table]
#         statement: str = f'CREATE TABLE IF NOT EXISTS {name_table} ( {','.join  (field_type)} );'
#         db.cursor().execute(statement)          
#     except:
#         print(f'Se ha producido un error al crear la tabla {name_table}')
#     else:
#         db.commit()
#         print(f'Se ha creado la tabla {name_table} con éxito.')

def insert_careers(database, table_name: str, careers: list[str]) -> bool:
    try:
        data_careers: list[tuple[int, str]] = [(id + 1, career) for id, career in enumerate(careers)]

        sql_statement: str = f'INSERT INTO {table_name} (id, carrera) VALUES (?, ?);'
        database.cursor().executemany(sql_statement, data_careers)
    except Exception as generic_error:
        print(f'Ha fallado la inserción de datos en "{table_name}": {generic_error}.')
        return False
    else:
        database.commit()
        print(f'Se han insertado {len(data_careers)} registros en "{table_name}".')
        return True

def insert_campus(database, table_name: str, campus: list[str]) -> bool:
    try:
        data_campus: list[tuple[int, str]] = [(id + 1, plantel) for id, plantel, in enumerate(campus)]

        sql_statement: str = f'INSERT INTO {table_name} (id, plantel) VALUES (?, ?)'
        database.cursor().executemany(sql_statement, data_campus)
    except Exception as generic_error:
        print(f'Ha fallado la inserción de datos en "{table_name}": {generic_error}.')
        return False
    else:
        database.commit()
        print(f'Se han insertado {len(data_campus)} registros en "{table_name}".')
        return True

def insert_academic_offers(database, table_name: str, academic_offers: dict[str, list[str]], careers: list[str], campus: list[str]) -> bool:
    try:
        careers_map: dict = {career: id + 1 for id, career in enumerate(careers)}
        campus_map: dict = {plantel: id + 1 for id, plantel in enumerate(campus)}

        data_academic_offers: list[tuple[int, int, int]] = []

        id_academic_offer: int = 1
        for plantel, careers_for_plantel in academic_offers.items():
            id_plantel: int = campus_map[plantel]
            for career in careers_for_plantel:
                id_career: int = careers_map[career]
                data_academic_offers.append((id_academic_offer, id_plantel, id_career))
                id_academic_offer += 1

        sql_statement: str = f'INSERT INTO {table_name} (id, id_plantel, id_carrera) VALUES (?, ?, ?)'
        database.cursor().executemany(sql_statement, data_academic_offers)
    except Exception as generic_error:
        print(f'Ha fallado la inserción de datos en "{table_name}": {generic_error}.')
        return False
    else:
        print(f'Se han insertado {len(data_academic_offers)} registros en "{table_name}".')
        database.commit()
        return True

def insert_applicants(database, table_name: str, path: str) -> bool:
    def extract_data(file) -> list[tuple[str]]:
            extracted_data: list[tuple] = []
            next(file)
            for ln in file:
                record: list[str] = ln.split(';')
                curp: str = record[1].strip().upper()
                name: str = record[2].strip().upper()
                
                if curp == '-':
                    RUTE_LOG: str = '../data/db/logs/'
                    NAME_LOG: str = 'insertApplicants.log'
                    PATH_LOG: str = f'{RUTE_LOG}{NAME_LOG}'

                    os.makedirs(RUTE_LOG, exist_ok=True)

                    with open(PATH_LOG, 'a') as log:
                        log.write(f'(CURP: "{curp}"; NOMBRE COMPLETO: "{name}")\n')
                else:
                    extracted_data.append((curp, name))
            
            return extracted_data 
    try:    
        data_applicants: list[tuple[str]] = open_file(path, extract_data)

        sql_statement: str = f'INSERT INTO {table_name} (curp, aspirante) VALUES (?, ?);'
        database.cursor().executemany(sql_statement, data_applicants)
    except Exception as generic_error:
        print(f'Ha fallado la inserción de datos en "{table_name}": {generic_error}.')
        return False
    else:
        database.commit()
        print(f'Se han insertado {len(data_applicants)} registros en "{table_name}".')
        return True

def insert_assignments(database, table_name: str, path: str, academic_offers: dict[str, list[str]], careers: list[str], campus: list[str]) -> bool:
    def extract_data(file, academic_offers: dict[str, list[str]], careers: list[str], campus: list[str]) -> list[tuple[int, int, int]]:
        extracted_data: list[tuple[int, int, int]] = []
        id_aspirante: int = 1

        next(file)
        for ln in file:
            record: list[str] = ln.split(';')
            folio: int = int(record[0].strip().upper())
            tmp_career: str = record[-2].strip().upper()
            tmp_plantel: str = record[-1].strip().upper()

            careers_map: dict[str, int] = {career: id + 1 for id, career in enumerate(careers)}
            campus_map: dict[str, int] = {plantel: id + 1 for id, plantel in enumerate(campus)}


            id_academic_offer: int = 1
            for plantel, careers_for_plantel in academic_offers.items():
                id_plantel: int = campus_map[plantel]
                for career in careers_for_plantel:
                    id_career: int = careers_map[career]

                    condition = tmp_career == career and tmp_plantel == plantel
                    if condition:

                        curp: str = record[1].strip().upper()
                        if curp == '-':
                            RUTE_LOG: str = '../data/db/logs/'
                            NAME_LOG: str = 'insertAssignments.log'
                            PATH_LOG: str = f'{RUTE_LOG}{NAME_LOG}'

                            os.makedirs(RUTE_LOG, exist_ok = True)

                            with open(PATH_LOG, 'a') as log:
                                log.write(f'ID ASPIRANTE: "{id_aspirante}"; FOLIO: "{folio}"; CURP: "{curp}"; ID OFERTA: "{id_academic_offer}"\n')
                        else:
                            extracted_data.append((folio, id_aspirante, id_academic_offer))
                            id_aspirante += 1    
                    
                    id_academic_offer += 1    
                    
        return extracted_data
    
    try:
        data_assignments: list[tuple] = open_file(path, extract_data, academic_offers, careers, campus)

        sql_statement: str = f'INSERT INTO {table_name} (folio, id_aspirante, id_oferta_asignada) VALUES (?, ?, ?);'
        database.cursor().executemany(sql_statement, data_assignments)
    except Exception as generic_error:
        print(f'Ha fallado la inserción de datos en "{table_name}": {generic_error}.')
        return False
    else:
        database.commit()
        print(f'Se han insertado {len(data_assignments)} registros en "{table_name}".')
        return True

def delete_db(path: str) -> bool:
    try:
        try:
            os.remove(path)
        except OSError as os_error:
            print(f'Ha fallado la eliminación de emergencia de la base de datos: {os_error}.')
            return False
        else:
            return True
    except ModuleNotFoundError as module_error:
        print(f'Error. Ha fallado la importación del módulo "os": {module_error}.')
        return False
    else:
        return True

def main() -> bool:
    RUTE_FILE: str = '../data/raw/csv/'
    NAME_FILE: str = 'ASIGNACIONES_2020.csv'
    PATH_FILE: str = f'{RUTE_FILE}{NAME_FILE}'

    os.makedirs(RUTE_FILE, exist_ok = True)

    RUTE_DB: str = '../data/db/'
    NAME_DB: str = 'ADMISIONES_COLEGIO_QROO_2020.db'
    PATH_DB: str = f'{RUTE_DB}{NAME_DB}'

    os.makedirs(RUTE_DB, exist_ok = True)

    tables: list[str] = ['carreras', 'planteles', 'oferta_academica', 'aspirantes', 'asignaciones']

    fields: list = open_file(PATH_FILE, get_fields)
    campus: list = open_file(PATH_FILE, get_campus)
    careers: list = open_file(PATH_FILE, get_careers)
    academic_offers: dict[str, list[str]] = open_file(PATH_FILE, get_academic_offer)

    if connect_db(PATH_DB, create_tables):
        if connect_db(PATH_DB, insert_careers, tables[0], careers):
            if connect_db(PATH_DB, insert_campus, tables[1], campus):
                if connect_db(PATH_DB, insert_academic_offers, tables[2], academic_offers, careers, campus):
                    if connect_db(PATH_DB, insert_applicants, tables[3], PATH_FILE):
                        if connect_db(PATH_DB, insert_assignments, tables[4], PATH_FILE, academic_offers, careers, campus):
                            print('La base de datos ha finalizado con éxito.')
                            print('Nota: Verifique en los logs por si requiere inserción manual de registros.')
                            return True
          
    if delete_db(PATH_DB):
        print('Se ha eliminado la base de datos por precaución.')
        return False
    else:
        return True

if __name__ == '__main__':
    main()

"""
with open('../data/raw/csv/ASIGNACIONES_2020.csv', 'r') as dataset:
    carreras: set = set()
    planteles: set = set()
    oferta: dict = dict()
    fields: list = list()
    for line in dataset:
        println = line.split(';')
        for ln in println:
            fields.append(ln.strip().upper())
        break
    for line in dataset:
        println:list = line.split(';')
        carrera: str = println[-2].strip().upper()
        plantel: str = println[-1].strip().upper()
        #Identificar oferta académica
        if plantel not in planteles:
            oferta[plantel]:list = list()
        else:
            if carrera not in oferta[plantel]:
                oferta[plantel].append(carrera)
        # Identificar las carreras
        carreras.add(carrera)
        # Identificar los planteles
        planteles.add(plantel)
"""
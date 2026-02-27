"""
Código asistido por Inteligencia Artificial
Ha sido generado parcialmente con asistencia del modelo Gemini 3
El código ha sido modificado y adaptado
"""

import csv
import random
import string

def generar_curp_ficticio():
    letras = ''.join(random.choices(string.ascii_uppercase, k=4))
    fecha = "".join(random.choices(string.digits, k=6))
    sexo = random.choice(['H', 'M'])
    estado = random.choice([
    "AS", "BC", "BS", "CC", "CL", "CM", "CS", "CH", "DF", "DG", 
    "GT", "GR", "HG", "JC", "MC", "MN", "MS", "NT", "NL", "OC", 
    "PL", "QT", "QR", "SP", "SL", "SR", "TC", "TS", "TL", "VZ", 
    "YN", "ZS"
    ])
    consonantes = ''.join(random.choices(string.ascii_uppercase, k=3))
    control = ''.join(random.choices(string.ascii_uppercase + string.digits, k=2))
    return f"{letras}{fecha}{sexo}{estado}{consonantes}{control}"

def generar_datos_csv(nombre_archivo, n_registros):
    nombres = ["MIGUEL", "EMANUEL", "CHRISTOPHER", "BRIANA", "MARIA", "JUAN", "ELENA", "ROBERTO"]
    segundos_nombres = ["ANGEL", "FELIPE", "ALEJANDRO", "SHERLIN", "ISABEL", "ANTONIO", "PAOLA"]
    apellidos = ["ALMEIDA", "AKE", "YAM", "ARRIAGA", "PEREZ", "NIC", "AREVALO", "CERVERA", "PANTI"]
    
    carreras = ["TÉC. EN ELECTRICIDAD", "TÉC. EN TURISMO", "TÉC. EN ENFERMERÍA", "TÉC. EN INFORMÁTICA"]
    planteles = [
        "BENITO JUÁREZ", "SOLIDARIDAD", "OTHÓN P. BLANCO", "COZUMEL", 
        "FELIPE CARRILLO PUERTO", "TULUM", "BACALAR", "ISLA MUJERES", 
        "PUERTO MORELOS", "JOSÉ MARÍA MORELOS", "LÁZARO CÁRDENAS"
    ]

    folios_usados = set()

    with open(nombre_archivo, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file, delimiter=';')
        # Encabezados
        writer.writerow(["FOLIO", "CURP", "NOMBRE COMPLETO", "CARRERA ASIGNADA", "PLANTEL"])
        
        for _ in range(n_registros):
            # Generar folio único de 9 dígitos
            while True:
                folio = random.randint(210000000, 219000000)
                if folio not in folios_usados:
                    folios_usados.add(folio)
                    break
            
            nombre_completo = f"{random.choice(nombres)} {random.choice(segundos_nombres)} {random.choice(apellidos)} {random.choice(apellidos)}"
            curp = generar_curp_ficticio()
            carrera = random.choice(carreras)
            plantel = random.choice(planteles)
            
            writer.writerow([folio, curp, nombre_completo, carrera, plantel])

# Generar 100 registros
generar_datos_csv('data/samples/ASIGNACIONES_QROO_2020.csv', 100)
print("Archivo CSV generado con éxito.")
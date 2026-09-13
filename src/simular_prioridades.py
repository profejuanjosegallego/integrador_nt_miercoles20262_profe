import os
import random
from faker import Faker
import pandas as pd

# -----------------------------------------------------------------------------
# CONFIGURACIÓN DE SEMILLAS Y LOCALIZACIÓN (REPRODUCIBILIDAD)
# -----------------------------------------------------------------------------
# Se fijan las semillas en 42 para garantizar que la simulación sea exactamente
# la misma en cualquier equipo de los compañeros o del docente.
SEED_VALUE = 42
random.seed(SEED_VALUE)
Faker.seed(SEED_VALUE)

# Configurar Faker con localización de Colombia
fake = Faker('es_CO')

def generar_y_ensuciar_prioridades(cantidad=200):
    """
    Genera datos sintéticos para la tabla 'prioridades' con las columnas del
    Backend II más una columna extra para análisis de datos, ensuciando la 
    información a propósito para la etapa de limpieza.
    """
    niveles = ['Baja', 'Media', 'Alta', 'Crítica']
    estados = ['Activo', 'Inactivo', 'En Espera']
    
    lista_prioridades = []
    
    for i in range(1, cantidad + 1):
        nivel = random.choice(niveles)
        
        # ---------------------------------------------------------------------
        # ENSUCIAR DATOS A PROPÓSITO:
        # ---------------------------------------------------------------------
        
        # 1. Espacios sobrantes y mayúsculas/minúsculas mezcladas en 'nivel_urgencia'
        if i % 7 == 0:
            nivel = f"  {nivel.lower()}  "
        elif i % 11 == 0:
            nivel = nivel.upper()
            
        # 2. Formatos distintos y espacios en 'nombre_prioridad'
        nombre_prioridad = f"PRIORIDAD_{fake.word().upper()}"
        if i % 5 == 0:
            nombre_prioridad = f"  pri_{fake.word()}  "

        # 3. Valores Nulos (None) asignados periódicamente
        if i % 12 == 0:
            estado_val = None
        else:
            estado_val = random.choice(estados)

        tiempo_respuesta = random.choice([2, 4, 8, 12, 24, 48, None])

        # NOTA SOBRE COLUMNA EXTRA:
        # 'dias_max_respuesta' NO está en el modelo de Backend II; es una
        # columna EXTRA agregada únicamente para este ejercicio de analítica.
        dias_max_respuesta = random.choice([1, 2, 3, 5, 7, None])

        # Diccionario representando las columnas del modelo Backend II + Extra
        registro = {
            "id_prioridad": i,
            "nombre_prioridad": nombre_prioridad,
            "nivel_urgencia": nivel,
            "tiempo_respuesta_horas": tiempo_respuesta,
            "descripcion": fake.sentence(nb_words=6),
            "estado": estado_val,
            "dias_max_respuesta": dias_max_respuesta  # <-- COLUMNA EXTRA PARA ANÁLISIS
        }
        lista_prioridades.append(registro)

    # Convertir a DataFrame de Pandas
    df = pd.DataFrame(lista_prioridades)
    
    # 4. Generar DUPLICADOS a propósito (duplicar filas específicas al final)
    filas_duplicadas = df.iloc[[5, 15, 25, 35, 45]].copy()
    df = pd.concat([df, filas_duplicadas], ignore_index=True)
    
    return df

if __name__ == "__main__":
    print("🚀 Generando 200 filas simuladas de 'prioridades' con Faker (es_CO)...")
    
    # Generar DataFrame con datos sucios
    df_prioridades_sucias = generar_y_ensuciar_prioridades(200)
    
    # Crear carpeta 'data' si no existe
    os.makedirs('data', exist_ok=True)
    
    # Exportar los datos crudos a CSV
    ruta_salida = 'data/prioridades_raw.csv'
    df_prioridades_sucias.to_csv(ruta_salida, index=False, encoding='utf-8')
    
    print(f"✅ Archivo generado exitosamente en: '{ruta_salida}'")
    print(f"📊 Registros totales exportados (incluyendo duplicados): {len(df_prioridades_sucias)}")
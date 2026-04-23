import os
import sys
import pandas as pd
import yaml
import logging
from pathlib import Path

# Cambiar al directorio raíz del proyecto
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(script_dir)
os.chdir(project_root)

from validators import validate_structure, check_duplicates
from rules_engine import load_rules, apply_rules
from exceptions_handler import mark_exceptions
from file_generator import generate_outputs

# Configuración de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('execution.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)

def load_config():
    with open('config/config.yaml', 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

def get_input_file():
    """Obtiene el nombre del archivo de entrada"""
    # Si se pasó como argumento al ejecutar: python main.py mi_archivo.csv
    if len(sys.argv) > 1:
        input_file = sys.argv[1]
        if not input_file.endswith('.csv'):
            input_file += '.csv'
        return input_file
    
    # Si no, preguntar al usuario
    print("\n📁 Archivos disponibles en data/input/:")
    input_dir = Path('data/input')
    if input_dir.exists():
        archivos = [f.name for f in input_dir.glob('*.csv')]
        for i, archivo in enumerate(archivos, 1):
            print(f"  {i}. {archivo}")
        print(f"  {len(archivos)+1}. Escribir otro nombre")
        
        try:
            opcion = int(input("\nSelecciona una opción: "))
            if 1 <= opcion <= len(archivos):
                return archivos[opcion-1]
            elif opcion == len(archivos)+1:
                return input("Nombre del archivo (ej: facturas.csv): ")
        except:
            pass
    
    # Por defecto, usar transacciones.csv
    return 'transacciones.csv'

def main():
    logging.info("=== Iniciando proceso de cierre contable ===")
    
    # 1. Obtener archivo de entrada
    input_filename = get_input_file()
    input_file_path = f'data/input/{input_filename}'
    
    if not os.path.exists(input_file_path):
        logging.error(f"No se encuentra el archivo: {input_file_path}")
        print(f"\n❌ Error: No se encuentra '{input_filename}' en data/input/")
        return
    
    # 2. Cargar configuración
    config = load_config()
    
    # 3. Cargar archivo original
    df_original = pd.read_csv(input_file_path)
    logging.info(f"Archivo cargado: {input_filename} - {len(df_original)} filas")
    
    # 4. Validar estructura
    required_columns = config['required_columns']
    is_valid, df = validate_structure(df_original, required_columns)
    if not is_valid:
        logging.error("Estructura inválida. Ejecución detenida.")
        return
    
    # 5. Verificar duplicados
    tiene_duplicados, df_duplicados = check_duplicates(df)
    
    if tiene_duplicados:
        print(f"\n⚠️ Se encontraron {len(df_duplicados)} filas duplicadas")
        os.makedirs('data/output', exist_ok=True)
        df_duplicados.to_csv('data/output/duplicados.csv', index=False)
        print(f"   Las filas duplicadas se guardaron en 'data/output/duplicados.csv'")
        
        respuesta = input("\n¿Deseas eliminar los duplicados? (s/n): ")
        if respuesta.lower() == 's':
            df = df.drop_duplicates()
            logging.info(f"Duplicados eliminados. Quedan {len(df)} filas")
        else:
            logging.info("Se mantuvieron los duplicados")
    
    # 6. Cargar reglas
    proveedores_df = load_rules('data/rules/proveedores.csv')
    cuentas_df = load_rules('data/rules/cuentas.csv')
    categorias_df = load_rules('data/rules/categorias.csv')
    
    # 7. Aplicar reglas
    df_processed, log_cambios = apply_rules(df, proveedores_df, categorias_df)
    
    # 8. Identificar excepciones
    df_processed, df_excepciones = mark_exceptions(df_processed, log_cambios)
    
    # 9. Generar outputs (usando el nombre base del archivo)
    base_name = Path(input_filename).stem
    generate_outputs(df_processed, df_excepciones, log_cambios, base_name)
    
    logging.info("=== Proceso completado exitosamente ===")
    print(f"\n✅ Resultados guardados en data/output/ con prefijo '{base_name}'")

if __name__ == "__main__":
    main()
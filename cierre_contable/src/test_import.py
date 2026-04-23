import os
import sys
import pandas as pd
import yaml
from pathlib import Path

# Cambiar al directorio raíz del proyecto
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(script_dir)
os.chdir(project_root)
print(f"📁 Directorio de trabajo: {os.getcwd()}")

# Añadir src al path
sys.path.append(os.path.join(project_root, 'src'))

try:
    from validators import validate_structure
    from rules_engine import load_rules, clasificar_por_proveedor, clasificar_por_descripcion
    print("✅ Módulos importados correctamente")
except ImportError as e:
    print(f"❌ Error importando módulos: {e}")

# Cargar config
try:
    with open('config/config.yaml', 'r', encoding='utf-8') as f:
        config = yaml.safe_load(f)
    print(f"✅ Configuración cargada")
except Exception as e:
    print(f"❌ Error cargando config: {e}")

# Cargar CSV de ejemplo
try:
    df = pd.read_csv('data/input/transacciones.csv')
    print(f"✅ CSV cargado: {len(df)} filas")
    print(df.head())
except Exception as e:
    print(f"❌ Error cargando CSV: {e}")

# Probar validación
try:
    required = config.get('required_columns', [])
    is_valid, df_clean = validate_structure(df, required)
    print(f"✅ Validación: {'Válido' if is_valid else 'Inválido'}")
except Exception as e:
    print(f"❌ Error en validación: {e}")

# Probar reglas de proveedores
try:
    proveedores_df = load_rules('data/rules/proveedores.csv')
    cat, cc, motivo = clasificar_por_proveedor('Iberdrola Madrid', proveedores_df)
    print(f"✅ Clasificación por proveedor: {cat} / {cc} / {motivo}")
except Exception as e:
    print(f"❌ Error en reglas proveedores: {e}")

print("\n✅ Prueba completada")
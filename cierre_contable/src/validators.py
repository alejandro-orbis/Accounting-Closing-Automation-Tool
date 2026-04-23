import pandas as pd
import logging

def validate_structure(df, required_columns):
    """
    Valida que el CSV tenga las columnas obligatorias
    Retorna: (is_valid, df_limpio)
    """
    logging.info("Validando estructura del archivo...")
    
    # Limpiar espacios en nombres de columnas
    df.columns = df.columns.str.strip().str.lower()
    
    columnas_faltantes = [col for col in required_columns if col not in df.columns]
    
    if columnas_faltantes:
        logging.error(f"Columnas obligatorias faltantes: {columnas_faltantes}")
        return False, None
    
    # Eliminar filas completamente vacías
    df_clean = df.dropna(how='all')
    
    logging.info(f"Estructura válida. {len(df_clean)} filas procesables")
    return True, df_clean

def check_duplicates(df, columnas=None):
    """
    Detecta filas duplicadas en el DataFrame
    columnas: lista de columnas a considerar para detectar duplicados
              Si es None, considera todas las columnas
    """
    if columnas is None:
        duplicados = df[df.duplicated(keep=False)]
    else:
        duplicados = df[df.duplicated(subset=columnas, keep=False)]
    
    if not duplicados.empty:
        logging.warning(f"Se encontraron {len(duplicados)} filas duplicadas")
        return True, duplicados
    else:
        logging.info("No se encontraron duplicados")
        return False, pd.DataFrame()
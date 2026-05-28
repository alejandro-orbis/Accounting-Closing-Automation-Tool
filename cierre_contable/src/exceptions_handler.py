import pandas as pd
import logging

def mark_exceptions(df, log_cambios_df):
    """
    Identifica filas que requieren revisión manual
    """
    logging.info("Identificando excepciones...")
    
    df_resultado = df.copy()
    
    # Filas que no tienen categoría asignada
    df_excepciones = df_resultado[df_resultado['estado'] == 'excepcion'].copy()
    
    # Añadir motivo adicional si es necesario
    if not df_excepciones.empty:
        logging.warning(f"Se encontraron {len(df_excepciones)} excepciones para revisión manual")
    
    return df_resultado, df_excepciones
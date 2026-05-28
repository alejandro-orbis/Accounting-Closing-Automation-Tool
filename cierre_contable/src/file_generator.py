import pandas as pd
import logging
from datetime import datetime
import os

def generate_outputs(df_processed, df_excepciones, log_cambios, base_name="transacciones"):
    """
    Genera los archivos de salida
    """
    logging.info("Generando archivos de salida...")
    
    # Crear carpeta output si no existe
    os.makedirs('data/output', exist_ok=True)
    
    # 1. Guardar cierre ajustado
    df_processed.to_csv(f'data/output/{base_name}_ajustado.csv', index=False)
    logging.info(f"[OK] {base_name}_ajustado.csv - {len(df_processed)} filas")
    
    # 2. Guardar excepciones
    if not df_excepciones.empty:
        df_excepciones.to_csv(f'data/output/{base_name}_excepciones.csv', index=False)
        logging.info(f"[OK] {base_name}_excepciones.csv - {len(df_excepciones)} filas")
    
    # 3. Guardar log de cambios
    if not log_cambios.empty:
        log_cambios.to_csv(f'data/output/{base_name}_log_cambios.csv', index=False)
        logging.info(f"[OK] {base_name}_log_cambios.csv - {len(log_cambios)} cambios")
    
    # 4. Generar Excel consolidado
    try:
        with pd.ExcelWriter(f'data/output/{base_name}_informe.xlsx', engine='openpyxl') as writer:
            df_processed.to_excel(writer, sheet_name='datos_ajustados', index=False)
            if not df_excepciones.empty:
                df_excepciones.to_excel(writer, sheet_name='excepciones', index=False)
            if not log_cambios.empty:
                log_cambios.to_excel(writer, sheet_name='log_cambios', index=False)
            
            # Resumen de métricas
            resumen = pd.DataFrame({
                'Metrica': ['Total filas', 'Clasificadas', 'Excepciones', 'Cambios aplicados'],
                'Valor': [
                    len(df_processed),
                    len(df_processed[df_processed['estado'] == 'clasificado']) if 'estado' in df_processed.columns else 0,
                    len(df_excepciones),
                    len(log_cambios)
                ]
            })
            resumen.to_excel(writer, sheet_name='resumen', index=False)
        
        logging.info(f"[OK] {base_name}_informe.xlsx generado")
    except Exception as e:
        logging.warning(f"No se pudo generar Excel: {e}")
        logging.info("Los archivos CSV se generaron correctamente")
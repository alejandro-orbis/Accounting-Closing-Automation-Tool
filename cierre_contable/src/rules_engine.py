import pandas as pd
import logging

def load_rules(file_path):
    """Carga reglas desde CSV editable"""
    try:
        df = pd.read_csv(file_path)
        logging.info(f"Reglas cargadas: {file_path} - {len(df)} reglas")
        return df
    except Exception as e:
        logging.warning(f"No se pudo cargar {file_path}: {e}")
        return pd.DataFrame()

def clasificar_por_proveedor(proveedor, rules_df):
    """Busca coincidencia parcial en proveedores"""
    if rules_df.empty:
        return None, None, None
    
    for _, rule in rules_df.iterrows():
        if pd.isna(rule['proveedor_buscar']):
            continue
        if rule['proveedor_buscar'].lower() in str(proveedor).lower():
            return rule['categoria'], rule['centro_costo'], f"Proveedor: {rule['proveedor_buscar']}"
    return None, None, None

def clasificar_por_descripcion(descripcion, rules_df):
    """Busca palabras clave en la descripción"""
    if rules_df.empty:
        return None, None, None
    
    for _, rule in rules_df.iterrows():
        if pd.isna(rule['palabra_clave']):
            continue
        if rule['palabra_clave'].lower() in str(descripcion).lower():
            return rule['categoria'], rule['centro_costo'], f"Palabra clave: {rule['palabra_clave']}"
    return None, None, None

def apply_rules(df, proveedores_df, categorias_df):
    """
    Aplica todas las reglas y registra cambios
    """
    logging.info("Aplicando reglas de clasificación...")
    
    df_resultado = df.copy()
    log_cambios = []
    
    # Añadir columnas nuevas si no existen
    for col in ['categoria_asignada', 'centro_costo', 'estado']:
        if col not in df_resultado.columns:
            df_resultado[col] = ''
    
    for idx, row in df_resultado.iterrows():
        categoria = None
        centro_costo = None
        motivo = []
        
        # Intento 1: Clasificar por proveedor
        cat, cc, motivo1 = clasificar_por_proveedor(row.get('proveedor', ''), proveedores_df)
        if cat:
            categoria = cat
            centro_costo = cc
            motivo.append(motivo1)
        
        # Intento 2: Si no, clasificar por descripción
        if not categoria:
            cat, cc, motivo2 = clasificar_por_descripcion(row.get('descripcion', ''), categorias_df)
            if cat:
                categoria = cat
                centro_costo = cc
                motivo.append(motivo2)
        
        # Registrar resultado
        if categoria:
            df_resultado.at[idx, 'categoria_asignada'] = categoria
            df_resultado.at[idx, 'centro_costo'] = centro_costo
            df_resultado.at[idx, 'estado'] = 'clasificado'
            
            log_cambios.append({
                'fila': idx,
                'campo': 'categoria_asignada',
                'valor_original': row.get('categoria_asignada', ''),
                'valor_nuevo': categoria,
                'motivo': ' - '.join(motivo) if motivo else 'Clasificación automática'
            })
        else:
            df_resultado.at[idx, 'estado'] = 'excepcion'
            log_cambios.append({
                'fila': idx,
                'campo': 'estado',
                'valor_original': 'pendiente',
                'valor_nuevo': 'excepcion',
                'motivo': 'No se pudo clasificar automáticamente'
            })
    
    logging.info(f"Clasificación completada. {len(log_cambios)} cambios registrados")
    return df_resultado, pd.DataFrame(log_cambios)
"""
Escriba el codigo que ejecute la accion solicitada en la pregunta.
"""
def parse_fecha(fecha):
    if '/' in fecha:
        partes = fecha.split('/')
        if len(partes[0]) == 4:  # Formato YYYY/MM/DD
            return f"{partes[0]}-{partes[1].zfill(2)}-{partes[2].zfill(2)}"
        else:  # Formato DD/MM/YYYY
            return f"{partes[2]}-{partes[1].zfill(2)}-{partes[0].zfill(2)}"
    return fecha

def pregunta_01():
    """
    Realice la limpieza del archivo "files/input/solicitudes_de_credito.csv".
    El archivo tiene problemas como registros duplicados y datos faltantes.
    Tenga en cuenta todas las verificaciones discutidas en clase para
    realizar la limpieza de los datos.

    El archivo limpio debe escribirse en "files/output/solicitudes_de_credito.csv"

    """
    import pandas as pd
    from pathlib import Path

    base_path = Path(__file__).resolve().parents[1]
    input_path = base_path / "files" / "input" / "solicitudes_de_credito.csv"

    df_cleaned = pd.read_csv(input_path, sep=";", index_col=0)

    # Corregir nombres de valores inconsistentes en las columnas
    for column in df_cleaned.select_dtypes(include=['object']).columns:
        df_cleaned[column] = (
            df_cleaned[column]
            .str.lower()
            .str.replace("_", " ", regex=False)
            .str.replace("-", " ", regex=False)
            .str.replace(",", "", regex=False)
            .str.replace("$", "", regex=False)
            .str.replace(".00", "", regex=False)
        )

    # Asegurar tipos de datos correctos
    df_cleaned["monto_del_credito"] = df_cleaned["monto_del_credito"].astype(float)
    df_cleaned["comuna_ciudadano"] = df_cleaned["comuna_ciudadano"].astype(int)

    # Ajustar formato de fechas - manejar formatos mixtos
    df_cleaned['fecha_de_beneficio'] = df_cleaned['fecha_de_beneficio'].apply(parse_fecha)

    # Eliminar registros duplicados
    df_cleaned = df_cleaned.drop_duplicates()

    # Eliminar filas con datos faltantes
    df_cleaned = df_cleaned.dropna()
    
    # Guardar el archivo limpio
    output_path = base_path / "files" / "output" / "solicitudes_de_credito.csv"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    df_cleaned.to_csv(output_path, sep=";", index=False)


pregunta_01()
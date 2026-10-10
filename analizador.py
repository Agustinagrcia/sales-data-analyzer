import pandas as pd
import os

def limpiar_monto_serie(serie):
    """Limpia una columna entera de texto de dinero y la convierte a números (float)."""
    return (
        serie.astype(str)
        .str.replace("$", "", regex=False)
        .str.replace(",", "", regex=False)
        .astype(float)
    )

def analizar_con_pandas(ruta_archivo):
    if not os.path.exists(ruta_archivo):
        print(f" Error: No se encontró el archivo '{ruta_archivo}'.")
        return

    print("Procesando datos")
    df = pd.read_csv(ruta_archivo, skiprows=2)
    df.columns = df.columns.str.strip()

    df = df.dropna(subset=['articulo vendido'])
    df = df[df['articulo vendido'].str.strip() != '']

    df['prendas_num'] = pd.to_numeric(df['prendas'], errors='coerce').fillna(0).astype(int)
    df['monto_limpio'] = limpiar_monto_serie(df['monto cobrado'])
    df['ganancia_limpia'] = limpiar_monto_serie(df['ganancia'])

    total_transacciones = len(df)
    total_prendas = df['prendas_num'].sum()
    facturacion_total = df['monto_limpio'].sum()
    ganancia_total = df['ganancia_limpia'].sum()
    
    margen_promedio = (ganancia_total / facturacion_total * 100) if facturacion_total > 0 else 0.0

    print("\n" + "="*45)
    print("📊 RESUMEN MENSUAL DE MOTIVA (CON PANDAS)")
    print("="*45)
    print(f"Total de transacciones: {total_transacciones}")
    print(f"Prendas vendidas: {total_prendas}")
    print(f"Facturación total: ${facturacion_total:,.2f}")
    print(f"Ganancia estimada total: ${ganancia_total:,.2f}")
    print(f"Margen de ganancia promedio: {margen_promedio:.2f}%")
    print("="*45)

    print("\n🔍 Vista previa de los datos en el DataFrame:")
    print(df[['fecha', 'articulo vendido', 'prendas_num', 'monto_limpio']].head())

if __name__ == "__main__":
    analizar_con_pandas("ventas_septiembre.csv")
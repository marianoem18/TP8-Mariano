import streamlit as st
import pandas as pd

# Título de la aplicación
st.title("Análisis de Ventas por Producto")

# Cargar archivo CSV
st.sidebar.header("Cargar archivo de datos")
uploaded_file = st.sidebar.file_uploader("Sube tu archivo CSV", type=["csv"])

# Mostrar mensaje inicial si no hay archivo cargado
if not uploaded_file:
    st.info("Por favor, sube un archivo CSV para comenzar.")
    st.stop()

# Leer los datos del archivo CSV
data = pd.read_csv(uploaded_file)

# Verificar que las columnas necesarias existan
columnas_esperadas = ["Sucursal", "Producto", "Año", "Mes", "Unidades_vendidas", "Ingreso_total", "Costo_total"]
if not all(col in data.columns for col in columnas_esperadas):
    st.error("El archivo CSV debe contener las columnas: " + ", ".join(columnas_esperadas))
    st.stop()

# Filtrar sucursales
sucursales = ["Todas"] + data["Sucursal"].unique().tolist()
selected_branch = st.sidebar.selectbox("Seleccionar Sucursal", sucursales)

# Filtrar datos según la sucursal seleccionada
if selected_branch != "Todas":
    data = data[data["Sucursal"] == selected_branch]

# Convertir columnas Año y Mes a formato de fecha
try:
    # Construir columna de fecha combinando Año y Mes
    data["Fecha"] = pd.to_datetime(
        data["Año"].astype(str) + "-" + data["Mes"].astype(str) + "-01",
        errors="coerce"
    )
    # Eliminar filas con fechas inválidas
    data = data.dropna(subset=["Fecha"])
except Exception as e:
    st.error(f"Error al crear las fechas: {e}")
    st.stop()

# Calcular métricas para cada producto
st.header(f"Datos de la sucursal: {selected_branch}")

productos = data["Producto"].unique()
for producto in productos:
    prod_data = data[data["Producto"] == producto]
    
    # Cálculos
    unidades_vendidas = prod_data["Unidades_vendidas"].sum()
    ingreso_total = prod_data["Ingreso_total"].sum()
    costo_total = prod_data["Costo_total"].sum()
    precio_promedio = ingreso_total / unidades_vendidas if unidades_vendidas > 0 else 0
    margen_promedio = ((ingreso_total - costo_total) / ingreso_total) if ingreso_total > 0 else 0
    
    # Mostrar resultados
    st.subheader(producto)
    st.write(f"**Precio Promedio:** ${precio_promedio:.2f}")
    st.write(f"**Margen Promedio:** {margen_promedio:.2%}")
    st.write(f"**Unidades Vendidas:** {int(unidades_vendidas)}")

    # Evolución de ventas
    ventas_mensuales = prod_data.groupby("Fecha").sum(numeric_only=True).reset_index()

    # Graficar
    st.line_chart(
        ventas_mensuales.set_index("Fecha")["Unidades_vendidas"],
        use_container_width=True,
    )

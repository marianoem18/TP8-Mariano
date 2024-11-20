import streamlit as st
import pandas as pd
import numpy as np

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

    # Simular deltas de ejemplo (puedes reemplazar estos valores por cálculos reales)
    delta_precio = 10.5  # Ejemplo: aumento del precio promedio en 10.5%
    delta_margen = -2.3  # Ejemplo: disminución del margen en 2.3%
    delta_unidades = 5.7  # Ejemplo: aumento de unidades vendidas en 5.7%

    # Crear columna 'Fecha' para el gráfico
    prod_data["Fecha"] = pd.to_datetime(prod_data["Año"].astype(str) + '-' + prod_data["Mes"].astype(str) + '-01', errors="coerce")
    ventas_mensuales = prod_data.groupby("Fecha").sum(numeric_only=True).reset_index()

    # Crear columnas para organizar el diseño
    col1, col2 = st.columns([1, 2])  # Col1: Métricas, Col2: Gráfico

    with col1:
        # Mostrar las métricas con porcentaje (delta)
        st.subheader(producto)
        st.metric("Precio Promedio", f"${precio_promedio:,.2f}", f"{delta_precio:.2f}%", delta_color="normal")
        st.metric("Margen Promedio", f"{margen_promedio:.2%}", f"{delta_margen:.2f}%", delta_color="normal")
        st.metric("Unidades Vendidas", f"{int(unidades_vendidas):,}", f"{delta_unidades:.2f}%", delta_color="normal")

    with col2:
        # Gráfico de la evolución de ventas
        if not ventas_mensuales.empty:
            st.line_chart(
                ventas_mensuales.set_index("Fecha")["Unidades_vendidas"],
                use_container_width=True,
            )
        else:
            st.warning(f"No hay datos suficientes para generar un gráfico de ventas para {producto}.")

    st.divider()

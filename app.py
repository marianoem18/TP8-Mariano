import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
import matplotlib.dates as mdates

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
    prod_data["Fecha"] = pd.to_datetime(prod_data["Año"].astype(str) + '-' + prod_data["Mes"].astype(str) + '-01', errors="coerce")
    ventas_mensuales = prod_data.groupby("Fecha").sum(numeric_only=True).reset_index()
    
    # Calcular métricas
    precio_promedio = round(prod_data["Ingreso_total"].sum() / prod_data["Unidades_vendidas"].sum(), 2)
    margen_promedio = round((prod_data["Ingreso_total"].sum() - prod_data["Costo_total"].sum()) / prod_data["Ingreso_total"].sum() * 100, 2)
    unidades_totales = prod_data["Unidades_vendidas"].sum()
    
    # Variaciones (ejemplo con valores simulados, adaptar según lógica real)
    variacion_precio = 29.57  # % ficticio
    variacion_margen = -0.27  # % ficticio
    variacion_unidades = 9.98  # % ficticio

    # Layout en dos columnas
    col1, col2 = st.columns([1, 2])  # Más ancho para el gráfico

    with col1:
        st.subheader(producto)
        st.metric("Precio Promedio", f"${precio_promedio}", f"{variacion_precio}%")
        st.metric("Margen Promedio", f"{margen_promedio}%", f"{variacion_margen}%", delta_color="normal")
        st.metric("Unidades Vendidas", f"{unidades_totales:,.0f}", f"{variacion_unidades}%")

    with col2:
        # Gráfico personalizado con matplotlib
        if not ventas_mensuales.empty:
            fig, ax = plt.subplots(figsize=(10, 6))
            # Graficar datos de ventas
            ax.plot(ventas_mensuales["Fecha"], ventas_mensuales["Unidades_vendidas"], label=producto, color="blue")

            # Configurar cuadrícula y divisiones
            ax.grid(True, which="both", linestyle="--", linewidth=0.5, alpha=0.7)

            # Líneas divisorias mensuales
            ax.xaxis.set_major_locator(mdates.MonthLocator())  # Divisiones mensuales (líneas)
            ax.xaxis.set_minor_locator(mdates.MonthLocator())  # Opcional: sublíneas
            ax.xaxis.set_major_formatter(mdates.DateFormatter(""))  # No texto en las divisiones mensuales

            # Etiquetas de texto anuales
            ax.xaxis.set_major_locator(mdates.YearLocator())  # Etiquetas en cada año
            ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))  # Mostrar solo el año en texto
            plt.xticks(rotation=0)  # No rotar etiquetas

            # Calcular y añadir línea de tendencia
            x = np.arange(len(ventas_mensuales)).reshape(-1, 1)  # Meses como variable independiente
            y = ventas_mensuales["Unidades_vendidas"].values.reshape(-1, 1)  # Ventas como dependiente
            modelo = LinearRegression()
            modelo.fit(x, y)
            tendencia = modelo.predict(x)
            ax.plot(ventas_mensuales["Fecha"], tendencia, color="red", linestyle="--", label="Tendencia")

            # Etiquetas y título
            ax.set_title("Evolución de Ventas Mensual", fontsize=14)
            ax.set_xlabel("Año", fontsize=12)
            ax.set_ylabel("Unidades Vendidas", fontsize=12)
            ax.legend()

            # Mostrar gráfico en Streamlit
            st.pyplot(fig)
        else:
            st.warning(f"No hay datos suficientes para generar un gráfico de ventas para {producto}.")
    
    st.divider()

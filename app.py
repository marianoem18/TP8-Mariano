import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
import matplotlib.dates as mdates

# ======== Funciones auxiliares ========

def cargar_datos(uploaded_file):
    """Carga el archivo CSV y valida que tenga las columnas necesarias."""
    columnas_requeridas = ["Sucursal", "Producto", "Año", "Mes", "Unidades_vendidas", "Ingreso_total", "Costo_total"]
    try:
        datos = pd.read_csv(uploaded_file)
        if not all(col in datos.columns for col in columnas_requeridas):
            st.error(f"El archivo debe contener las columnas: {', '.join(columnas_requeridas)}")
            return None
        return datos
    except Exception as e:
        st.error(f"Error al leer el archivo: {e}")
        return None


def calcular_variaciones(df, producto):
    """Calcula las variaciones de precio, margen y unidades para un producto."""
    df_producto = df[df["Producto"] == producto]
    df_producto["Fecha"] = pd.to_datetime(df_producto["Año"].astype(str) + '-' + df_producto["Mes"].astype(str) + '-01', errors="coerce")
    df_producto.sort_values("Fecha", inplace=True)
    
    # Calcular variaciones mes a mes
    df_producto["Var_precio"] = df_producto["Ingreso_total"].pct_change() * 100
    df_producto["Var_margen"] = ((df_producto["Ingreso_total"] - df_producto["Costo_total"]).pct_change()) * 100
    df_producto["Var_unidades"] = df_producto["Unidades_vendidas"].pct_change() * 100

    # Retornar las últimas variaciones como resumen
    return {
        "precio": df_producto["Var_precio"].iloc[-1] if len(df_producto) > 1 else 0,
        "margen": df_producto["Var_margen"].iloc[-1] if len(df_producto) > 1 else 0,
        "unidades": df_producto["Var_unidades"].iloc[-1] if len(df_producto) > 1 else 0,
    }


def generar_grafico(ventas_mensuales, producto):
    """Genera un gráfico con la evolución de ventas y la tendencia."""
    fig, ax = plt.subplots(figsize=(10, 6))

    # Gráfico de unidades vendidas
    ax.plot(ventas_mensuales["Fecha"], ventas_mensuales["Unidades_vendidas"], label="Unidades Vendidas", color="blue")

    # Línea de tendencia
    if len(ventas_mensuales) > 1:
        x = np.arange(len(ventas_mensuales)).reshape(-1, 1)
        y = ventas_mensuales["Unidades_vendidas"].values.reshape(-1, 1)
        modelo = LinearRegression()
        modelo.fit(x, y)
        tendencia = modelo.predict(x)
        ax.plot(ventas_mensuales["Fecha"], tendencia, color="red", linestyle="--", label="Tendencia")

<<<<<<< HEAD
<<<<<<< HEAD
        # Eliminar producto del stock
        st.subheader("Eliminar Producto del Stock")
        id_stock_to_delete = st.number_input("ID Stock a Eliminar", min_value=0, step=1)
        if st.button("Eliminar del Stock"):
            stock_df = stock_df[stock_df["id_stock"] != id_stock_to_delete]
            save_csv(stock_df, "stock.csv")
            st.success("Producto eliminado del stock.")
=======
    # Configuraciones del gráfico
    ax.set_title(f"Evolución de Ventas Mensuales - {producto}", fontsize=14)
    ax.set_xlabel("Fecha", fontsize=12)
    ax.set_ylabel("Unidades Vendidas", fontsize=12)
    ax.grid(True, linestyle="--", linewidth=0.5, alpha=0.7)
>>>>>>> parent of 3dae5eb (metodologia)

    # Formatear eje X
    ax.xaxis.set_minor_locator(mdates.MonthLocator())  # Líneas divisorias mensuales
    ax.xaxis.set_major_locator(mdates.YearLocator())  # Líneas divisorias anuales
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))  # Mostrar solo años en las etiquetas principales
    ax.tick_params(axis="x", rotation=45)  # Rotar las etiquetas para mejor legibilidad

    # Mostrar líneas verticales menores para cada mes
    ax.grid(which="minor", color="gray", linestyle="--", linewidth=0.5, alpha=0.5)

<<<<<<< HEAD
    elif choice == "Gestión de Proveedores":
        st.header("Gestión de Proveedores")
        proveedores_df = load_csv("proveedores.csv")
=======
    # Configuraciones del gráfico
    ax.set_title(f"Evolución de Ventas Mensuales - {producto}", fontsize=14)
    ax.set_xlabel("Fecha", fontsize=12)
    ax.set_ylabel("Unidades Vendidas", fontsize=12)
    ax.grid(True, linestyle="--", linewidth=0.5, alpha=0.7)
    ax.legend()
    return fig
>>>>>>> parent of 70ad468 (Ultimo corregido)
=======
    # Leyenda
    ax.legend()
    return fig
>>>>>>> parent of 3dae5eb (metodologia)


<<<<<<< HEAD
<<<<<<< HEAD
        # Agregar nuevo proveedor
        st.subheader("Agregar Nuevo Proveedor")
        id_proveedor = st.text_input("ID Proveedor")
        nombre = st.text_input("Nombre del Proveedor")
        direccion = st.text_input("Dirección")
        telefono = st.text_input("Teléfono")
        email = st.text_input("Email")
=======



st.title("Análisis de Ventas por producto")
>>>>>>> parent of 70ad468 (Ultimo corregido)
=======
st.title("Análisis de Ventas por producto")
>>>>>>> parent of 3dae5eb (metodologia)

# Carga del archivo CSV
st.sidebar.header("Carga de archivo")
archivo_cargado = st.sidebar.file_uploader("Subir archivo CSV", type=["csv"])

if archivo_cargado:
    datos = cargar_datos(archivo_cargado)
    if datos is not None:
        sucursales = ["Todas"] + datos["Sucursal"].unique().tolist()
        sucursal_seleccionada = st.sidebar.selectbox("Seleccionar Sucursal", sucursales)

        if sucursal_seleccionada != "Todas":
            datos = datos[datos["Sucursal"] == sucursal_seleccionada]

        st.header(f"Análisis de Sucursal: {sucursal_seleccionada}")
        
        # Iterar por cada producto
        productos = datos["Producto"].unique()
        for producto in productos:
            prod_datos = datos[datos["Producto"] == producto]

            # Cálculos principales
            prod_datos["Fecha"] = pd.to_datetime(prod_datos["Año"].astype(str) + '-' + prod_datos["Mes"].astype(str) + '-01', errors="coerce")
            ventas_mensuales = prod_datos.groupby("Fecha").sum(numeric_only=True).reset_index()
            precio_promedio = round(prod_datos["Ingreso_total"].sum() / prod_datos["Unidades_vendidas"].sum(), 2)
            margen_promedio = round((prod_datos["Ingreso_total"].sum() - prod_datos["Costo_total"].sum()) / prod_datos["Ingreso_total"].sum() * 100, 2)
            unidades_totales = prod_datos["Unidades_vendidas"].sum()

            # Calcular variaciones reales
            variaciones = calcular_variaciones(prod_datos, producto)

<<<<<<< HEAD
<<<<<<< HEAD
        productos_seleccionados = st.multiselect(
            "Seleccionar Productos",
            stock_df["id_producto"].tolist(),
            format_func=lambda x: f"{x} - {stock_df[stock_df['id_producto'] == x]['descripcion'].values[0]}"
        )
        cantidades = {prod: st.number_input(f"Cantidad para {prod}", min_value=0, step=1) for prod in productos_seleccionados}

        if st.button("Registrar Venta"):
            total = sum(
                cantidades[prod] * stock_df[stock_df["id_producto"] == prod]["precio"].values[0]
                for prod in productos_seleccionados
            )
            new_id_venta = ventas_df["id_venta"].max() + 1 if not ventas_df.empty else 1
            new_row = {
                "id_venta": new_id_venta,
                "fecha": pd.Timestamp.now().strftime("%Y-%m-%d"),
                "productos": str(productos_seleccionados),
                "total": total,
                "metodo_pago": "Efectivo",  # Se puede agregar selección.
            }
            ventas_df = pd.concat([ventas_df, pd.DataFrame([new_row])], ignore_index=True)
            save_csv(ventas_df, "ventas.csv")
            st.success(f"Venta registrada. Total: {total:.2f}")

    elif choice == "Ventas":
        st.header("Ventas")
        ventas_df = load_csv("ventas.csv")

        st.subheader("Lista de Ventas Registradas")
        if ventas_df.empty:
            st.info("No hay ventas registradas.")
        else:
            st.dataframe(ventas_df)

if __name__ == "__main__":
    main()
=======
            # Mostrar métricas
=======
            # Mostrar métricas
            st.divider()  # Separar productos con una línea
>>>>>>> parent of 3dae5eb (metodologia)
            col1, col2 = st.columns([1, 2])
            with col1:
                st.subheader(producto)
                st.metric("Precio Promedio", f"${precio_promedio}", f"{variaciones['precio']:.2f}%")
                st.metric("Margen Promedio", f"{margen_promedio}%", f"{variaciones['margen']:.2f}%", delta_color="normal")
                st.metric("Unidades Vendidas", f"{unidades_totales:,.0f}", f"{variaciones['unidades']:.2f}%")
            with col2:
                if not ventas_mensuales.empty:
                    fig = generar_grafico(ventas_mensuales, producto)
                    st.pyplot(fig)
                else:
                    st.warning(f"No hay suficientes datos para generar un gráfico de ventas para {producto}.")
else:
    st.info("Por favor, sube un archivo CSV para comenzar.")
<<<<<<< HEAD
>>>>>>> parent of 70ad468 (Ultimo corregido)
=======
>>>>>>> parent of 3dae5eb (metodologia)

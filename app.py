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
        st.error(f"Error al cargar {file_name}: {e}")
        return pd.DataFrame()

# Función para guardar datos en un archivo CSV
def save_csv(df, file_name):
    try:
        df.to_csv(file_name, index=False)
    except Exception as e:
        st.error(f"Error al guardar {file_name}: {e}")

# Interfaz principal
def main():
    st.title("Sistema de Ventas de Repuestos Sanitarios")

    menu = ["Gestión de Stock", "Gestión de Proveedores", "Compras a Proveedores", "Nueva Venta", "Ventas"]
    choice = st.sidebar.selectbox("Navegación", menu)

    if choice == "Gestión de Stock":
        st.header("Gestión de Stock")
        stock_df = load_csv("stock.csv")

        st.subheader("Lista de Stock")
        st.dataframe(stock_df)

        # Agregar nuevo producto
        st.subheader("Agregar Nuevo Producto al Stock")
        id_producto = st.text_input("ID Producto")
        descripcion = st.text_input("Descripción")
        precio = st.number_input("Precio", min_value=0.0, step=0.01)
        cantidad = st.number_input("Cantidad", min_value=0, step=1)

        if st.button("Agregar al Stock"):
            if not id_producto or not descripcion or precio <= 0 or cantidad <= 0:
                st.error("Por favor, completa todos los campos correctamente.")
            else:
                new_id_stock = stock_df["id_stock"].max() + 1 if not stock_df.empty else 1
                new_row = {
                    "id_stock": new_id_stock,
                    "id_producto": id_producto,
                    "cantidad": cantidad,
                    "descripcion": descripcion,
                    "precio": precio,
                }
                stock_df = pd.concat([stock_df, pd.DataFrame([new_row])], ignore_index=True)
                save_csv(stock_df, "stock.csv")
                st.success("Producto agregado al stock.")

        # Eliminar producto del stock
        st.subheader("Eliminar Producto del Stock")
        id_stock_to_delete = st.number_input("ID Stock a Eliminar", min_value=0, step=1)
        if st.button("Eliminar del Stock"):
            stock_df = stock_df[stock_df["id_stock"] != id_stock_to_delete]
            save_csv(stock_df, "stock.csv")
            st.success("Producto eliminado del stock.")

        # Modificar producto del stock
        st.subheader("Modificar Producto del Stock")
        id_stock_to_modify = st.number_input("ID Stock a Modificar", min_value=0, step=1)
        nueva_cantidad = st.number_input("Nueva Cantidad", min_value=0, step=1)
        nuevo_precio = st.number_input("Nuevo Precio", min_value=0.0, step=0.01)

        if st.button("Modificar Producto"):
            if id_stock_to_modify in stock_df["id_stock"].values:
                stock_df.loc[stock_df["id_stock"] == id_stock_to_modify, "cantidad"] = nueva_cantidad
                stock_df.loc[stock_df["id_stock"] == id_stock_to_modify, "precio"] = nuevo_precio
                save_csv(stock_df, "stock.csv")
                st.success("Producto modificado correctamente.")
            else:
                st.error("ID Stock no encontrado.")

    elif choice == "Gestión de Proveedores":
        st.header("Gestión de Proveedores")
        proveedores_df = load_csv("proveedores.csv")

        st.subheader("Lista de Proveedores")
        st.dataframe(proveedores_df)

        # Agregar nuevo proveedor
        st.subheader("Agregar Nuevo Proveedor")
        id_proveedor = st.text_input("ID Proveedor")
        nombre = st.text_input("Nombre del Proveedor")
        direccion = st.text_input("Dirección")
        telefono = st.text_input("Teléfono")
        email = st.text_input("Email")

        if st.button("Agregar Proveedor"):
            if not id_proveedor or not nombre:
                st.error("Por favor, completa todos los campos obligatorios.")
            else:
                new_row = {
                    "id_proveedor": id_proveedor,
                    "nombre": nombre,
                    "direccion": direccion,
                    "telefono": telefono,
                    "email": email,
                }
                proveedores_df = pd.concat([proveedores_df, pd.DataFrame([new_row])], ignore_index=True)
                save_csv(proveedores_df, "proveedores.csv")
                st.success("Proveedor agregado correctamente.")

    elif choice == "Compras a Proveedores":
        st.header("Compras a Proveedores")
        compras_df = load_csv("compras.csv")

        st.subheader("Lista de Compras")
        st.dataframe(compras_df)

        st.subheader("Agregar Nueva Compra")
        id_proveedor = st.text_input("ID Proveedor")
        fecha = st.date_input("Fecha")
        total = st.number_input("Total", min_value=0.0, step=0.01)

        if st.button("Registrar Compra"):
            if not id_proveedor or total <= 0:
                st.error("Por favor, completa todos los campos obligatorios.")
            else:
                new_id_compra = compras_df["id_compra"].max() + 1 if not compras_df.empty else 1
                new_row = {
                    "id_compra": new_id_compra,
                    "id_proveedor": id_proveedor,
                    "fecha": fecha,
                    "total": total,
                }
                compras_df = pd.concat([compras_df, pd.DataFrame([new_row])], ignore_index=True)
                save_csv(compras_df, "compras.csv")
                st.success("Compra registrada correctamente.")

    elif choice == "Nueva Venta":
        st.header("Nueva Venta")
        stock_df = load_csv("stock.csv")
        ventas_df = load_csv("ventas.csv")

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

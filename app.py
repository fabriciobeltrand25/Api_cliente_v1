import streamlit as st
import pandas as pd
import sqlite3
from api_client import obtener_usuarios_api
from database import crear_tabla,consultar_usuarios, eliminar_usuarios,guardar_usuarios 


st.set_page_config(page_title="Proyecto Cloud", layout="wide")

crear_tabla() 
st.title("Api-SQLITE-STREAMLITE")  
st.write("Esta aplicación obtiene datos de una API, los guarda en una base de datos SQLite y permite consultarlos.")  

menu=st.sidebar.selectbox (
    "Selecccione una opción",
    [
        "Inicio",
        "Consumir API",
        "Ver la base de datos",
        "Buscar los usuarios",
        "Eliminar los datos"
            
    ]
       
)
if menu=="Inicio":
    st.subheader("inicio")
    st.write("Bienvenido a la aplicación. Utiliza el menú lateral para navegar entre las diferentes opciones.") 
    
    st.info("Esta aplicación permite consumir datos de una API, almacenarlos en una base de datos SQLite y consultarlos de manera sencilla.")
    
elif menu=="Consumir API":
    st.header("Consumir API")
    st.write("API USTILIZADA")
    st.code("https://jsonplaceholder.typicode.com/users")
    
    if st.button("Obtener y guardar usuarios"):
        usuarios=obtener_usuarios_api()
        if usuarios:
            guardar_usuarios(usuarios)
            st.success("Usuarios obtenidos y guardados en la base de datos.")
            st.json(usuarios[0])
        else:
            st.error("Error al obtener los usuarios de la API.")

#nuevo pegado

elif menu == "Ver la base de datos":
    st.header("Tabla almacenada en SQLite")
    df = consultar_usuarios()
    if df.empty:
        st.warning("La base de datos está vacía. Primero consuma la API.")
    else:
        st.dataframe(df, use_container_width=True)
        col1, col2, col3 = st.columns(3)
        col1.metric("Total usuarios", len(df))
        col2.metric("Total ciudades", df["ciudad"].nunique())
        col3.metric("Total correos", df["email"].nunique())
        

elif menu == "Buscar los usuarios":
    st.header("Buscar usuario en SQLite")
    df = consultar_usuarios()
    if df.empty:
        st.warning("No hay datos guardados.")
    else:
        nombre = st.text_input("Ingrese nombre o usuario a buscar")
        if nombre:
            resultado = df[
                df["nombre"].str.contains(nombre, case=False, na=False) |
                df["usuario"].str.contains(nombre, case=False, na=False)
            ]
            if resultado.empty:
                st.error("No se encontraron coincidencias.")
            else:
                st.success("Resultado encontrado.")
                st.dataframe(resultado, use_container_width=True)
                
elif menu == "Eliminar los datos":
    st.header("Eliminar registros de SQLite")
    st.warning("Esta acción eliminará todos los datos almacenados.")
    if st.button("Eliminar todos los datos"):
        eliminar_datos()
        st.success("Datos eliminados correctamente.")
        
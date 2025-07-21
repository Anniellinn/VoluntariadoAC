# pip install st-star-rating

import streamlit as st
import pandas as pd
from datetime import datetime
import plotly.express as px
import plotly.graph_objects as go
from PIL import Image
import io
from streamlit_star_rating import st_star_rating
import os

# data

data = pd.read_excel('niños_prep.xlsx',na_values=[])
data = data.fillna("N/A")


nombres=set(data['Nombre'])



def load_data():
    data_path = 'niños_prep.xlsx'
    data = pd.read_excel(data_path, na_values=[])
    data = data.fillna("N/A")
    return data

# Inicialización de la variable de estado si no existe
if 'data' not in st.session_state:
    st.session_state.data = load_data()

# Mostrar botones y manejar la recarga de datos
def show_buttons_and_load_data():
    if st.button("Recargar datos"):
        st.session_state.data = load_data()  # Recarga los datos
        st.success("Datos recargados con éxito!")

# Mostrar los datos en Streamlit
def display_data():
    st.write(st.session_state.data)

def main():
    #st.sidebar.title("Menú de Navegación")
    show_buttons_and_load_data()
    # display_data()

if __name__ == "__main__":
    main()

col1, col2 = st.columns([1, 3])  # Ajusta los valores para cambiar el tamaño relativo de las columnas

#st.sidebar.image('logo.jpg', width=200)
st.sidebar.title("Menú de Navegación")

menu_opciones = {
    "explorar": "🔍 Explorar niño/a",
    "registrar": "📝 Registrar datos",
    "foto": "📸 Añadir foto"
}

# Mostrar opciones con emojis en el sidebar
menu_opcion = st.sidebar.radio(
    "Selecciona función: ",#👉
    options=list(menu_opciones.keys()),  # Opciones internas
    format_func=lambda x: menu_opciones[x],  # Mostrar con emojis
    key="menu"
)

if menu_opcion == "foto":

    with col1:
        st.image('logo.jpg')  # Añadiremos la imagen de los niños 

    # Colocar el título en la segunda columna
    with col2:
        st.write(f"""
        #  Fotografías
        """)
        
    uploaded_file = st.file_uploader("Sube una foto:", type=["jpg", "jpeg", "png"])
    st.caption("⚠️ El nombre de la foto debe de corresponder con el nombre del niño/a.")


    if uploaded_file is not None:
        image = Image.open(uploaded_file)
                
        st.image(image, caption="Foto subida", width=150)

        # with open("foto_subida.jpg", "wb") as f:
        #     f.write(uploaded_file.getbuffer())
            
    st.text(' ')

    if st.button("Guardar registro"):
            
        try: 
                    # foto
            save_path = "fotos"  
            if not os.path.exists(save_path):
                os.makedirs(save_path)  # Crear la ruta si no existe
                    
                    # Guardar la imagen con su nombre original
            image.save(os.path.join(save_path, uploaded_file.name))
            st.success("La foto se ha guardado correctamente.")

                    # datos
        except: 
            st.warning('No se pudieron guardar los cambios, añada la foto correctamente.', icon="⚠️")
            

elif menu_opcion == "explorar":
    opcion = st.sidebar.selectbox(
        "Elige un/a Niñ@: ", # refinar esto con Misael
        nombres
    )
    
    niñx = data[(data['Nombre'] == opcion)]# & (data['Año'] == 2025)


    # Colocar la imagen en la primera columna
    with col1:
        st.image('logo.jpg')  # Añadiremos la imagen de los niños 

    # Colocar el título en la segunda columna
    
    with col2:

        st.write(f"""
        #  {opcion}
        """)
        try:
            st.write(f"""
            {niñx['Sexo'].values[0]}, {int(niñx['Edad'].values[0]+1)} años, nacid@ en {int(niñx['Fecha de nacimiento'].values[0])}
            """)
        except:
            st.write(f"""
            {niñx['Sexo'].values[0]}
            """)

    if 'selected' not in st.session_state:
        st.session_state.selected = None
        
 
    col1, col2, col3,col4= st.columns([3, 3, 3,3])  # Ajusta los valores para cambiar el tamaño relativo de las columnas

    with col1:
        if st.button("🏠 Historia clínica y antecedentes"):
            st.session_state.selected = "familiares"  # Cambia el estado a "familiares"
    with col2:
        if st.button("📏 Antropometría y crecimiento"):
            st.session_state.selected = "creci"  # Cambia el estado a "varianza"
    with col3:
        if st.button("💉 Vacunas"):
            st.session_state.selected = "vacunas"  # Cambia el estado a "faltantes"
    with col4:
        if st.button("🧠 Psicología y Comportamiento"):
            st.session_state.selected = "psico"  # Cambia el estado a "faltantes"

    
    col1, col2, col3,col4 = st.columns([3, 3, 3, 3])  # Ajusta los valores para cambiar el tamaño relativo de las columnas

    with col1:

        if st.button("👁️ Oftalmología"):
            st.session_state.selected = "oftalmo"  # Cambia el estado a "familiares"
    with col2:
        if st.button("👂 Otorrino"):
            st.session_state.selected = "oto"  # Cambia el estado a "varianza"
    with col3:
        if st.button("🦷 Bucal"):
            st.session_state.selected = "bucal"  # Cambia el estado a "faltantes"
    with col4:
        if st.button("🫀 Auscultación"):
            st.session_state.selected = "auscu"  # Cambia el estado a "faltantes"

    col1, col2, col3,col4 = st.columns([3, 3, 3, 3])
    with col1:
        if st.button("🖐️ Dermatología"):
            st.session_state.selected = "derma"  # Cambia el estado a "faltantes"
    with col2:
        if st.button("📋 Valoración final"):
            st.session_state.selected = "val"  # Cambia el estado a "familiares"
    

    # Muestra contenido basado en el estado seleccionado
    if st.session_state.selected == "familiares":
        
        niñx_familiares = niñx[['Año','Hogar', 'Unidad Familiar', 'Antecedentes Médicos', 'Antecedentes Familiares']]
        niñx_familiares = niñx_familiares.reset_index(drop=True)

        tabla1 = go.Figure(data=[go.Table(
            header=dict(
                values=list(niñx_familiares.columns),  # Usar los nombres de las columnas del DataFrame
                fill_color='#1a75ce',  # Color del fondo de los encabezados
                align='center',  # Alineación de los textos
                font=dict(size=14, color='white'),  # Estilo de fuente para el encabezado
                height=50
            ),
            cells=dict(
                values=[niñx_familiares[col] for col in niñx_familiares.columns],  # Usar los valores de las columnas del DataFrame
                fill_color='white',  # Color del fondo de las celdas
                align='center',  # Alineación de los textos
                font=dict(size=13, color='black'),  # Tamaño y color del texto para las celdas
                height=50
            )
        )])
        tabla1.update_layout(
            height=250,  # Ajusta la altura de la tabla
            margin=dict(t=30, b=0)
        )
        # Mostrar la tabla en Streamlit
        st.plotly_chart(tabla1, use_container_width=True)
        

        niñx_familiares = niñx[['Año','Medicación', 'Alergias', 'Comentarios Alergias',
       'Comentarios Medicación']]
        niñx_familiares = niñx_familiares.reset_index(drop=True)

        tabla2 = go.Figure(data=[go.Table(
            header=dict(
                values=list(niñx_familiares.columns),  # Usar los nombres de las columnas del DataFrame
                fill_color='#1a75ce',  # Color del fondo de los encabezados
                align='center',  # Alineación de los textos
                font=dict(size=14, color='white'),  # Estilo de fuente para el encabezado
                height=30
            ),
            cells=dict(
                values=[niñx_familiares[col] for col in niñx_familiares.columns],  # Usar los valores de las columnas del DataFrame
                fill_color='white',  # Color del fondo de las celdas
                align='center',  # Alineación de los textos
                font=dict(size=13, color='black'),  # Tamaño y color del texto para las celdas
                height=30
            )
        )])

        tabla2.update_layout(
            height=250,  # Ajusta la altura de la tabla
            margin=dict(t=0, b=0)
        )
        # Mostrar la tabla en Streamlit
        st.plotly_chart(tabla2, use_container_width=True)

        if niñx['Sexo'].values[0]=='Femenino':

            niñx_familiares = niñx[['Año','Menarquia', 'Comentarios Menarquía']]
            niñx_familiares = niñx_familiares.reset_index(drop=True)

            tabla3 = go.Figure(data=[go.Table(
                header=dict(
                    values=list(niñx_familiares.columns),  # Usar los nombres de las columnas del DataFrame
                    fill_color='#1a75ce',  # Color del fondo de los encabezados
                    align='center',  # Alineación de los textos
                    font=dict(size=14, color='white'),  # Estilo de fuente para el encabezado
                    height=30
                ),
                cells=dict(
                    values=[niñx_familiares[col] for col in niñx_familiares.columns],  # Usar los valores de las columnas del DataFrame
                    fill_color='white',  # Color del fondo de las celdas
                    align='center',  # Alineación de los textos
                    font=dict(size=13, color='black'),  # Tamaño y color del texto para las celdas
                    height=30
                )
            )])

            tabla3.update_layout(
                height=250,  # Ajusta la altura de la tabla
                margin=dict(t=0, b=0)
            )
            # Mostrar la tabla en Streamlit
            st.plotly_chart(tabla3, use_container_width=True)



    elif st.session_state.selected == "psico":
        niñx5 = niñx[(data['Año'] == 2025)]# & 
        try:
            caritas = ["😠", "😟", "😐", "😊", "😁"]
            categorias = [niñx5['Autoestima/autoimagen'].values[0], niñx5['Relacional'].values[0], niñx5['Organización'].values[0], niñx5['Transtorno del sueño'].values[0], niñx5['Ansiedad'].values[0],   niñx5['Alimentación'].values[0], niñx5['Estado Anímico'].values[0], niñx5['Ideación Automítica'].values[0]]  # Ejemplo de valores
            categorias_labels = ['Autoestima','Relacional','Organización','Transtorno del sueño','Ansiedad','Alimentación', 'Estado Anímico', 'Ideación Automítica' ]  # Ejemplo de valores
            
            # Mapear valores a caritas y colores
            def asignar_carita_y_color(valor):
                if valor == 1:
                    return "😠", "#FF6F61"
                elif valor == 2:
                    return "😟", "#FFB347"
                elif valor == 3:
                    return "😐", "#FFF176"
                elif valor == 4:
                    return "😊", "#AED581"
                elif valor == 5:
                    return "😁", "#81C784"
                else:
                    return "❓", "#D3D3D3"  # Default para valores fuera de rango

    # Aplicar la función a los valores de las categorías
            caritas = []
            colores = []
            for valor in categorias:
                carita, color = asignar_carita_y_color(int(valor))
                caritas.append(carita)
                colores.append(color)

            # Crear el gráfico de barras
            fig = go.Figure()

            fig.add_trace(go.Bar(
                x=categorias_labels,  # Etiquetas del eje X
                y=categorias,  # Valores numéricos para las barras
                text=caritas,  # Caritas dinámicas basadas en los valores
                textposition='outside',
                marker=dict(color=colores)  # Colores dinámicos basados en los valores
            ))

            # Configurar diseño del gráfico
            fig.update_layout(
                xaxis=dict(title="Categorías"),  # Título del eje X
                yaxis=dict(title="Valores"),  # Título del eje Y
                height=500  # Altura del gráfico
            )

            st.plotly_chart(fig)
        except:
            pass


        niñx_familiares = niñx[['Año','Comentarios Psicología']]
        niñx_familiares = niñx_familiares.reset_index(drop=True)


        tabla4 = go.Figure(data=[go.Table(
            header=dict(
                values=list(niñx_familiares.columns),  # Usar los nombres de las columnas del DataFrame
                fill_color='#1a75ce',  # Color del fondo de los encabezados
                align='center',  # Alineación de los textos
                font=dict(size=14, color='white'),  # Estilo de fuente para el encabezado
                height=30
            ),
            cells=dict(
                values=[niñx_familiares[col] for col in niñx_familiares.columns],  # Usar los valores de las columnas del DataFrame
                fill_color='white',  # Color del fondo de las celdas
                align='center',  # Alineación de los textos
                font=dict(size=13, color='black'),  # Tamaño y color del texto para las celdas
                height=30
            )
        )])
        tabla4.update_layout(
            height=250,  # Ajusta la altura de la tabla
            margin=dict(t=30, b=0)
        )
        # Mostrar la tabla en Streamlit
        st.plotly_chart(tabla4, use_container_width=True)

    elif st.session_state.selected == "bucal":
        niñx_familiares = niñx[['Año', 'Caries', 'Comentarios Higiene Bucal', 'Urgente']]
        niñx_familiares = niñx_familiares.reset_index(drop=True)

        tabla1 = go.Figure(data=[go.Table(
            header=dict(
                values=list(niñx_familiares.columns),  # Usar los nombres de las columnas del DataFrame
                fill_color='#1a75ce',  # Color del fondo de los encabezados
                align='center',  # Alineación de los textos
                font=dict(size=14, color='white'),  # Estilo de fuente para el encabezado
                height=30
            ),
            cells=dict(
                values=[niñx_familiares[col] for col in niñx_familiares.columns],  # Usar los valores de las columnas del DataFrame
                fill_color='white',  # Color del fondo de las celdas
                align='center',  # Alineación de los textos
                font=dict(size=13, color='black'),  # Tamaño y color del texto para las celdas
                height=30
            )
        )])
        tabla1.update_layout(
            height=250,  # Ajusta la altura de la tabla
            margin=dict(t=30, b=0)
        )
        # Mostrar la tabla en Streamlit
        st.plotly_chart(tabla1, use_container_width=True)

    elif st.session_state.selected == "derma":

        niñx_familiares = niñx[['Año','Abdomen', 'Comentarios Abdomen' ]]
        niñx_familiares = niñx_familiares.reset_index(drop=True)

        tabla1 = go.Figure(data=[go.Table(
            header=dict(
                values=list(niñx_familiares.columns),  # Usar los nombres de las columnas del DataFrame
                fill_color='#1a75ce',  # Color del fondo de los encabezados
                align='center',  # Alineación de los textos
                font=dict(size=14, color='white'),  # Estilo de fuente para el encabezado
                height=30
            ),
            cells=dict(
                values=[niñx_familiares[col] for col in niñx_familiares.columns],  # Usar los valores de las columnas del DataFrame
                fill_color='white',  # Color del fondo de las celdas
                align='center',  # Alineación de los textos
                font=dict(size=13, color='black'),  # Tamaño y color del texto para las celdas
                height=30
            )
        )])
        tabla1.update_layout(
            height=250,  # Ajusta la altura de la tabla
            margin=dict(t=30, b=0)
        )
        # Mostrar la tabla en Streamlit
        st.plotly_chart(tabla1, use_container_width=True)

        niñx_familiares3 = niñx[['Año', 'Piojos', 'Piel', 'Lesiones', 'Tatuajes']]
        niñx_familiares3 = niñx_familiares3.reset_index(drop=True)

        tabla3 = go.Figure(data=[go.Table(
            header=dict(
                values=list(niñx_familiares3.columns),  # Usar los nombres de las columnas del DataFrame
                fill_color='#1a75ce',  # Color del fondo de los encabezados
                align='center',  # Alineación de los textos
                font=dict(size=14, color='white'),  # Estilo de fuente para el encabezado
                height=30
            ),
            cells=dict(
                values=[niñx_familiares3[col] for col in niñx_familiares3.columns],  # Usar los valores de las columnas del DataFrame
                fill_color='white',  # Color del fondo de las celdas
                align='center',  # Alineación de los textos
                font=dict(size=13, color='black'),  # Tamaño y color del texto para las celdas
                height=30
            )
        )])

        tabla3.update_layout(
            height=250,  # Ajusta la altura de la tabla
            margin=dict(t=0, b=0)
        )
        # Mostrar la tabla en Streamlit
        st.plotly_chart(tabla3, use_container_width=True)

    elif st.session_state.selected == "auscu":
        niñx_familiares = niñx[['Año','Corazón', 'Comentarios Cardiaca' ]]
        niñx_familiares = niñx_familiares.reset_index(drop=True)

        tabla1 = go.Figure(data=[go.Table(
            header=dict(
                values=list(niñx_familiares.columns),  # Usar los nombres de las columnas del DataFrame
                fill_color='#1a75ce',  # Color del fondo de los encabezados
                align='center',  # Alineación de los textos
                font=dict(size=14, color='white'),  # Estilo de fuente para el encabezado
                height=30
            ),
            cells=dict(
                values=[niñx_familiares[col] for col in niñx_familiares.columns],  # Usar los valores de las columnas del DataFrame
                fill_color='white',  # Color del fondo de las celdas
                align='center',  # Alineación de los textos
                font=dict(size=13, color='black'),  # Tamaño y color del texto para las celdas
                height=30
            )
        )])
        tabla1.update_layout(
            height=250,  # Ajusta la altura de la tabla
            margin=dict(t=30, b=0)
        )
        # Mostrar la tabla en Streamlit
        st.plotly_chart(tabla1, use_container_width=True)

        niñx_familiares1 = niñx[['Año','Pulmón','Comentarios Pulmón']]
        niñx_familiares1 = niñx_familiares1.reset_index(drop=True)

        tabla2 = go.Figure(data=[go.Table(
            header=dict(
                values=list(niñx_familiares1.columns),  # Usar los nombres de las columnas del DataFrame
                fill_color='#1a75ce',  # Color del fondo de los encabezados
                align='center',  # Alineación de los textos
                font=dict(size=14, color='white'),  # Estilo de fuente para el encabezado
                height=30
            ),
            cells=dict(
                values=[niñx_familiares1[col] for col in niñx_familiares1.columns],  # Usar los valores de las columnas del DataFrame
                fill_color='white',  # Color del fondo de las celdas
                align='center',  # Alineación de los textos
                font=dict(size=13, color='black'),  # Tamaño y color del texto para las celdas
                height=30
            )
        )])

        tabla2.update_layout(
            height=250,  # Ajusta la altura de la tabla
            margin=dict(t=0, b=0)
        )
        # Mostrar la tabla en Streamlit
        st.plotly_chart(tabla2, use_container_width=True)

        niñx_familiares3 = niñx[['Año','Adams', 'Comentarios Adams']]
        niñx_familiares3 = niñx_familiares3.reset_index(drop=True)

        tabla3 = go.Figure(data=[go.Table(
            header=dict(
                values=list(niñx_familiares3.columns),  # Usar los nombres de las columnas del DataFrame
                fill_color='#1a75ce',  # Color del fondo de los encabezados
                align='center',  # Alineación de los textos
                font=dict(size=14, color='white'),  # Estilo de fuente para el encabezado
                height=30
            ),
            cells=dict(
                values=[niñx_familiares3[col] for col in niñx_familiares3.columns],  # Usar los valores de las columnas del DataFrame
                fill_color='white',  # Color del fondo de las celdas
                align='center',  # Alineación de los textos
                font=dict(size=13, color='black'),  # Tamaño y color del texto para las celdas
                height=30
            )
        )])

        tabla3.update_layout(
            height=250,  # Ajusta la altura de la tabla
            margin=dict(t=0, b=0)
        )
        # Mostrar la tabla en Streamlit
        st.plotly_chart(tabla3, use_container_width=True)


    elif st.session_state.selected == "oto":
        niñx_familiares = niñx[['Año','Pendientes y Perforaciones', 'Audición', 'Comentarios Audición', 'Otoscopia', 'Comentarios Otoscopia' ]]
        niñx_familiares = niñx_familiares.reset_index(drop=True)

        tabla1 = go.Figure(data=[go.Table(
            header=dict(
                values=list(niñx_familiares.columns),  # Usar los nombres de las columnas del DataFrame
                fill_color='#1a75ce',  # Color del fondo de los encabezados
                align='center',  # Alineación de los textos
                font=dict(size=14, color='white'),  # Estilo de fuente para el encabezado
                height=30
            ),
            cells=dict(
                values=[niñx_familiares[col] for col in niñx_familiares.columns],  # Usar los valores de las columnas del DataFrame
                fill_color='white',  # Color del fondo de las celdas
                align='center',  # Alineación de los textos
                font=dict(size=13, color='black'),  # Tamaño y color del texto para las celdas
                height=30
            )
        )])
        tabla1.update_layout(
            height=250,  # Ajusta la altura de la tabla
            margin=dict(t=30, b=0)
        )
        # Mostrar la tabla en Streamlit
        st.plotly_chart(tabla1, use_container_width=True)


    elif st.session_state.selected == "creci":
        niñx_familiares = niñx[['Año','Peso (Kg)', 'Talla (Cm)','IMC', 'Perímetro Branquial']]
        niñx_familiares = niñx_familiares.reset_index(drop=True)

        tabla1 = go.Figure(data=[go.Table(
            header=dict(
                values=list(niñx_familiares.columns),  # Usar los nombres de las columnas del DataFrame
                fill_color='#1a75ce',  # Color del fondo de los encabezados
                align='center',  # Alineación de los textos
                font=dict(size=14, color='white'),  # Estilo de fuente para el encabezado
                height=30
            ),
            cells=dict(
                values=[niñx_familiares[col] for col in niñx_familiares.columns],  # Usar los valores de las columnas del DataFrame
                fill_color='white',  # Color del fondo de las celdas
                align='center',  # Alineación de los textos
                font=dict(size=13, color='black'),  # Tamaño y color del texto para las celdas
                height=30
            )
        )])
        tabla1.update_layout(
            height=250,  # Ajusta la altura de la tabla
            margin=dict(t=30, b=0)
        )
        # Mostrar la tabla en Streamlit
        st.plotly_chart(tabla1, use_container_width=True)

    elif st.session_state.selected == "vacunas":
            niñx5 = niñx[(data['Año'] == 2025)]# & 
            niñx_familiares = niñx5[['Vacunas']]
 
            tabla1 = go.Figure(data=[go.Table(
            header=dict(
                values=list(niñx_familiares.columns),  # Usar los nombres de las columnas del DataFrame
                fill_color='#1a75ce',  # Color del fondo de los encabezados
                align='center',  # Alineación de los textos
                font=dict(size=14, color='white'),  # Estilo de fuente para el encabezado
                height=30
            ),
            cells=dict(
                values=[niñx_familiares[col] for col in niñx_familiares.columns],  # Usar los valores de las columnas del DataFrame
                fill_color='white',  # Color del fondo de las celdas
                align='center',  # Alineación de los textos
                font=dict(size=13, color='black'),  # Tamaño y color del texto para las celdas
                height=30
                )
            )])
            tabla1.update_layout(
                height=250,  # Ajusta la altura de la tabla
                margin=dict(t=30, b=0)
            )
            # Mostrar la tabla en Streamlit
            st.plotly_chart(tabla1, use_container_width=True)

    elif st.session_state.selected == "oftalmo":
            niñx_familiares = niñx[['Año','Oftalmología', 'Comentarios Oftalmología' ]]
            niñx_familiares = niñx_familiares.reset_index(drop=True)
 
            tabla1 = go.Figure(data=[go.Table(
            header=dict(
                values=list(niñx_familiares.columns),  # Usar los nombres de las columnas del DataFrame
                fill_color='#1a75ce',  # Color del fondo de los encabezados
                align='center',  # Alineación de los textos
                font=dict(size=14, color='white'),  # Estilo de fuente para el encabezado
                height=30
            ),
            cells=dict(
                values=[niñx_familiares[col] for col in niñx_familiares.columns],  # Usar los valores de las columnas del DataFrame
                fill_color='white',  # Color del fondo de las celdas
                align='center',  # Alineación de los textos
                font=dict(size=13, color='black'),  # Tamaño y color del texto para las celdas
                height=30
                )
            )])
            tabla1.update_layout(
                height=250,  # Ajusta la altura de la tabla
                margin=dict(t=30, b=0)
            )
            # Mostrar la tabla en Streamlit
            st.plotly_chart(tabla1, use_container_width=True)

    elif st.session_state.selected == "val":
            niñx5 = niñx[(niñx['Año'] == 2025)]# & 
            niñx_familiares = niñx5[['Observaciones', 'Revaluar']]
 
            tabla1 = go.Figure(data=[go.Table(
            header=dict(
                values=list(niñx_familiares.columns),  # Usar los nombres de las columnas del DataFrame
                fill_color='#1a75ce',  # Color del fondo de los encabezados
                align='center',  # Alineación de los textos
                font=dict(size=14, color='white'),  # Estilo de fuente para el encabezado
                height=30
            ),
            cells=dict(
                values=[niñx_familiares[col] for col in niñx_familiares.columns],  # Usar los valores de las columnas del DataFrame
                fill_color='white',  # Color del fondo de las celdas
                align='center',  # Alineación de los textos
                font=dict(size=13, color='black'),  # Tamaño y color del texto para las celdas
                height=30
                )
            )])
            tabla1.update_layout(
                height=250,  # Ajusta la altura de la tabla
                margin=dict(t=30, b=0)
            )
            # Mostrar la tabla en Streamlit
            st.plotly_chart(tabla1, use_container_width=True)
    


        
elif menu_opcion == "registrar":
    # Opciones del menú
    menu_opciones = {
        "modificar": "Modificar niño/a",
        "nuevo": "Añadir nuevo/a niño/a",
        "existente": "Actualizar niño/a existente"
    }
    # Crear un radio button para seleccionar la acción
    menu_seleccion = st.sidebar.radio(
        "",  # Texto vacío
        options=list(menu_opciones.keys()),  # Opciones internas
        format_func=lambda x: menu_opciones[x],  # Mostrar con texto personalizado
        key="menu1"
    )

    # Mostrar logo en la columna 1
    with col1:
        st.image('logo.jpg')  # Añadir la imagen de los niños

    # Opción "modificar"
    if menu_seleccion == "modificar":
        with col2:
            st.write(f"""
            # Modificar niño/a
            """)

        file_path = "niños_prep.xlsx"

        if "edited_df" not in st.session_state or "file_timestamp" not in st.session_state:
            st.session_state.edited_df = pd.read_excel(file_path, na_values=[])
            st.session_state.file_timestamp = os.path.getmtime(file_path)

        # Si el archivo ha cambiado, recargarlo automáticamente
        current_timestamp = os.path.getmtime(file_path)
        if current_timestamp > st.session_state.file_timestamp:
            st.session_state.edited_df = pd.read_excel(file_path, na_values=[])
            st.session_state.file_timestamp = current_timestamp

            # Mostrar el editor de datos en Streamlit
        st.markdown('⚠️ Para modificar registros, recuerda hacer clic en el botón de **Guardar cambios** ⚠️')
        st.session_state.edited_df = st.data_editor(st.session_state.edited_df, num_rows="dynamic")

            # Botón para guardar los cambios
        if st.button("Guardar cambios"):
            # Guardar el DataFrame editado en el archivo original            
            st.session_state.edited_df.to_excel('niños_prep.xlsx', index=False)
            st.success("Los cambios se han guardado correctamente.")

    elif menu_seleccion == "nuevo":
        
        with col2:
            st.write(f"""
                    # Fomulario para añadir nuevo niño/a:
                    """)
                
        st.markdown('⚠️ Porfavor, rellene todos los datos ⚠️')

        st.header('🌟 Datos Personales')

        col1, col2,col3 = st.columns([3, 0.1,2])  # Ajusta los valores para cambiar el tamaño relativo de las columnas
        with col1:    
            nombre = st.text_input(
                    "Nombre del niño/a", key="nombre"
            )
        with col3:
            sexo = st.radio(
                    "Selecciona un género:",
                    options=["Femenino", "Masculino"],
                    
            )
        
        st.text(' ')

        col1,col2,col3 = st.columns([1, 0.1,1])
        with col1:
            edad=st.number_input('Edad: ', step=1,format="%d")
        with col3:
            nacimiento=st.slider("Fecha de nacimiento: ", 2017, 2024, 2025-edad)    
        
        st.text(' ')
                
        hogar = st.text_input(
                    "Hogar: " ,key="hogar"
                )

        st.text(' ')

        unidad_familiar = st.text_input(
                    "Unidad Familiar: ",key="unidad_familiar"
        )
        
        st.text(' ')

        # uploaded_file = st.file_uploader("Sube una foto:", type=["jpg", "jpeg", "png"])
        # st.caption("⚠️ El nombre de la foto debe de corresponder con el nombre del niño/a.")


        # if uploaded_file is not None:
        #     image = Image.open(uploaded_file)
                
        #     st.image(image, caption="Foto subida", width=150)

        #     with open("foto_subida.jpg", "wb") as f:
        #         f.write(uploaded_file.getbuffer())
            
        # st.text(' ')

        st.header('🏠 Historia clínica y antecedentes')
        a_medicos = st.text_area(
            "Antecedentes médicos: ",key="a_medicos"
            " ",
            )
        st.text(' ')

        a_familiares = st.text_area(
                "Antecedentes familiares: ", key="a_familiares"
                " ",
            )
        st.text(' ')

        col1,col2 = st.columns([1,4])
        with col1:  
            alergias = st.radio(
                    "Alergias:",
                    options=["Sí", "No"],  index=1
                    
            )  
                
        with col2:
            comentarios_alergias = st.text_input(
                    "Comentarios acerca de las alergias: ", key="alergias"
            )
            st.text(' ')

        col1,col2 = st.columns([1,4])
        with col1:  
            medicacion = st.radio(
                    "Medicación:",
                    options=["Sí", "No"],  index=1
                    
            )  
                
        with col2:
            comentarios_medicacion = st.text_input(
                    "Comentarios acerca de la medicación: ", key="medicacion"
            )

        st.text(' ')
        if sexo=='Femenino':
            col1,col2 = st.columns([1,4])
            with col1:  
                menarquia = st.radio(
                        "Menarquia:",
                        options=["Sí", "No"],
                        
                )  
                    
            with col2:
                comentarios_menarquia = st.text_input(
                        "Comentarios acerca de la menarquia: ", key="menarquia"
                )
        else: 
            menarquia='N/A'
            comentarios_menarquia='N/A'
            
        st.text(' ')

        st.header('📏 Antropometría y crecimiento')
        col1,col2, col3= st.columns([3,3,3])
        with col1:  
            peso=st.number_input('Peso (kg): ', step=0.1, key='peso' )

                
        with col2:
            talla=st.number_input('Talla (cm): ', step=1, key='talla' )
            
        with col3:
            altura_m = talla / 100
            st.text(f'Índice de masa corporal: ')
            if peso==0 or talla==0:
                imc='N/A'
            else: 
                imc=round(peso / (altura_m ** 2), 2)
            st.markdown(f'{imc}')

        perimetro_b=st.number_input('Perímetro branquial: ', step=0.1, key='perimetro_b' )
        
        col1,col2 = st.columns([1,4])
        with col1:  
            genitales = st.radio(
                    "Genitales:",
                    options=["Normales", "Hallazgo"],
                    
            )  
        if genitales=='Hallazgo':   
            with col2:
                comentarios_genitales = st.text_input(
                        "Comentarios acerca de los genitales: ", key="genitales"
                )
        else:
            comentarios_genitales='N/A'
        
        st.text(' ')
        st.header('💉 Vacunas')
        st.text(' ')

        vacunas = st.text_area(
            "Vacunas: ",key="vacunas"
            " ",
            )
        st.text(' ')
        st.text(' ')

        st.header('🧠 Psicología y Comportamiento')
        st.text(' ')

        if edad>11:

            st.markdown('Nivel de autoestima: ')
            autoestima=st_star_rating(label='',maxValue = 5, defaultValue = 3, key = "autoestima", emoticons=True)

            st.markdown('Nivel de relacionalidad: ')
            relacional=st_star_rating(label='',maxValue = 5, defaultValue = 3, key = "relacional", emoticons=True)

            st.markdown('Nivel de organización: ')
            organizacion=st_star_rating(label='',maxValue = 5, defaultValue = 3, key = "organizacion", emoticons=True)

            st.markdown('Transtorno del sueño: ')
            insomnio=st_star_rating(label='',maxValue = 5, defaultValue = 3, key = "insomnio", emoticons=True)

            st.markdown('Nivel de ansiedad: ')
            ansiedad=st_star_rating(label='',maxValue = 5, defaultValue = 3, key = "ansiedad", emoticons=True)

            st.markdown('Alimentación: ')
            alimentacion=st_star_rating(label='',maxValue = 5, defaultValue = 3, key = "alimentacion", emoticons=True)
        
            st.markdown('Estado Anímico: ')
            estado_a=st_star_rating(label='',maxValue = 5, defaultValue = 3, key = "estado_a", emoticons=True)

            st.markdown('Ideación Autolítica: ')
            ideacion=st_star_rating(label='',maxValue = 5, defaultValue = 3, key = "ideacion", emoticons=True)
        else: 
            autoestima='N/A'
            relacional='N/A'
            organizacion='N/A'
            insomnio='N/A'
            ansiedad='N/A'
            alimentacion='N/A'        
            estado_a='N/A'
            ideacion='N/A'

        col1,col2 = st.columns([1,4])
        with col1:  
            abuso = st.radio(
                    "Abuso:",
                    options=["Sí", "No", "N/A"], index=2
                    
            )  
                
        with col2:
            comentarios_abuso = st.text_input(
                    "Comentarios: ", key="comentarios_abuso"
            )
            
        st.text(' ')

        comentarios_psicologa = st.text_area(
                "Comentarios psicóloga/o: ", key="comentarios_psicologa"
                " ",
        )
        st.text(' ')

        st.header('👁️ Oftalmología')
        st.text(' ')
        col1,col2 = st.columns([1,4])
        with col1:  
            ofta = st.radio(
                    "Revisado:",
                    options=["Sí", "No"],
                    
            )  

        if ofta == 'No':
            with col2:
                comentarios_oftalmo = st.text_input(
                    "Comentarios oftalmología: ", key="comentarios_oftalmo"
            )        
        else:
            comentarios_oftalmo='N/A'
            
        

        
            

        st.header('👂 Otorrino')
        st.text(' ')
        pendientes = st.radio(
                    "Pendientes: ",
                    options=["Sí", "No", "N/A"],
                    
            ) 
        col1,col2 = st.columns([1,4])
        with col1:  
            audicion = st.radio(
                    "Audicición: ",
                    options=["Correcta", "Sordera"],
                    
            )  
        if audicion == 'Sordera':
            
            with col2:
                comentarios_audicion = st.text_input(
                        "Comentarios acerca de la audición: ", key="comentarios_audicion"
                )
        else: 
            comentarios_audicion='N/A'

        col1,col2 = st.columns([1,4])
        with col1:  
            otoscopia = st.radio(
                    "Otoscopia: ",
                    options=["Correcta", "Tapón"],
                    
            )  
        if otoscopia == 'Tapón':
            
            with col2:
                comentarios_otoscopia = st.text_input(
                        "Comentarios acerca de la otoscopia: ", key="comentarios_otoscopia"
                )
        else: 
            comentarios_otoscopia='N/A'

        st.text(' ')

        st.header('🦷 Bucal')
        st.text(' ')

        col1,col2,col3 = st.columns([1.5,3,1.5])
        with col1:  
            bucal = st.radio(
                    "Bucal: ",
                    options=["Buena higiene bucal", "Caries"],
                    
            )  
        with col2:
                comentarios_bucal = st.text_input(
                        "Comentarios acerca de la higiene bucal: ", key="comentarios_bucal"
                )
        with col3:
                urgente = st.radio(
                        "Urgente: ",
                        options=["Sí", "No"], index=1
                        
                ) 
            
        
        st.text(' ')

        st.header('🫀 Auscultación')
        st.text(' ')
        col1,col2 = st.columns([1,4])
        with col1:  
            cardiaca = st.radio(
                    "Cardiaca: ",
                    options=["Correcta", "Hallazgo"],
                    
            )  
        if cardiaca == 'Hallazgo':
            
            with col2:
                comentarios_cardiaca = st.text_input(
                        "Comentarios acerca de la auscultación cardiaca: ", key="comentarios_cardiaca"
                )
        else: 
            comentarios_cardiaca='N/A'

        st.text(' ')
        col1,col2 = st.columns([1,4])
        with col1:  
            pulmon = st.radio(
                    "Pulmón: ",
                    options=["Correcto", "Hallazgo"],
                    
            )  
        if pulmon == 'Hallazgo':
            
            with col2:
                comentarios_pulmon = st.text_input(
                        "Comentarios acerca de los pulmones: ", key="comentarios_pulmon"
                )
        else: 
            comentarios_pulmon='N/A'

        st.text(' ')
        col1,col2 = st.columns([1,4])
        with col1:  
            adams = st.radio(
                    "Adams: ",
                    options=["Negativo", "Positivo"],
                    
            )  
        if adams == 'Negativo':
            
            with col2:
                comentarios_adams = st.text_input(
                        "Comentarios Adams: ", key="comentarios_adams"
                )
        else: 
            comentarios_adams='N/A'

        st.header('🖐️ Dermatología')

        st.text(' ')
        col1,col2 = st.columns([1,4])
        with col1:  
            abdomen = st.radio(
                    "Abdomen: ",
                    options=["Correcta", "Hallazgo"],
                    
            )  
        if abdomen == 'Hallazgo':
            
            with col2:
                comentarios_abdomen = st.text_input(
                        "Comentarios acerca de la auscultación cardiaca: ", key="comentarios_abdomen"
                )
        else: 
            comentarios_abdomen='N/A'


        st.text(' ')
        col1,col2 = st.columns([1,4])
        with col1:  
            piel = st.radio(
                    "Piel: ",
                    options=["Correcta", "Hallazgo"],
                    
            )  
        if piel == 'Hallazgo':
            col11,col12 = st.columns([4,1])
            
            with col11:
                patologias = st.text_input(
                        "Patologías: ", key="patlogias"
                )
        else: 
            patologias='N/A'
        
        col13,col23 = st.columns([3,3])
        with col13:
            tatuajes = st.radio(
                        "Tatuajes: ",
                        options=["Sí", "No"], index=1
                        
                )  
                
        st.text(' ')
        with col23:
            piojos = st.radio(
                        "Piojos: ",
                        options=["Sí", "No"], index=1
                        
                )  
            
            st.text(' ')

        st.header('📋 Valoración final')
        valoracion = st.text_area(
            "Valoración final: ",key="valoracion"
            " ",
            )
        st.text(' ')

        col1,col2 = st.columns([1,4])
        with col1:  

            revaluar = st.radio(
                        "Revalorar: ",
                        options=["Sí", "No"], index=1
                        
                ) 
        with col2: 
            if revaluar == "Sí":
                st.markdown("🔄 **Revalorar al niño/a**")
            else:
                st.markdown("✅ **No requiere revaluación**")


        if st.button("Guardar registro"):
            # try: 
            #         # foto
            #     save_path = "fotos"  
            #     if not os.path.exists(save_path):
            #         os.makedirs(save_path)  # Crear la ruta si no existe
                    
            #         # Guardar la imagen con su nombre original
            #     image.save(os.path.join(save_path, uploaded_file.name))
            #     #st.success("Los cambios se han guardado correctamente.")

            #         # datos
            # except: 
            #     st.warning('No se pudieron guardar los cambios, añada la foto correctamente.', icon="⚠️")
            
            new_data = {
                'Revaluar': revaluar,  # No coincide, se queda igual
                'Año': 2025,  # Coincide con columna
                'Nombre': nombre,  # Coincide con columna
                'Sexo': sexo,  # Coincide con columna
                'Hogar': hogar,  # Coincide con columna
                'Edad': edad,  # Coincide con columna
                'Fecha de nacimiento': nacimiento,  # Coincide con columna
                'Unidad Familiar': unidad_familiar,  # Coincide con columna
                'Antecedentes Médicos': a_medicos,  # Coincide con columna
                'Antecedentes Familiares': a_familiares,  # Coincide con columna
                'Medicación': medicacion,  # Coincide con columna
                'Alergias': alergias,  # Coincide con columna
                'Comentarios Alergias': comentarios_alergias,  # No coincide, se queda igual
                'Comentarios Medicación': comentarios_medicacion,  # No coincide, se queda igual
                'Menarquia': menarquia,  # Coincide con columna
                'Comentarios Menarquía': comentarios_menarquia,  # No coincide, se queda igual
                'Peso (Kg)': peso,  # Coincide con columna
                'Talla (Cm)': talla,  # Coincide con columna
                'IMC': imc,  # Coincide con columna
                'Perímetro Branquial': perimetro_b,  # Coincide con columna
                'Genitales':genitales,
                'Comentarios Genitales':comentarios_genitales, 
                'Vacunas': vacunas,  # No coincide, se queda igual
                'Autoestima/autoimagen': autoestima,  # Coincide con columna
                'Relacional': relacional,  # Coincide con columna
                'Organización': organizacion,  # No coincide, se queda igual
                'Transtorno del sueño': insomnio,  # Coincide con columna
                'Ansiedad': ansiedad,  # No coincide, se queda igual
                'Comentarios Psicología':comentarios_psicologa,
                'Abuso': abuso,  # No coincide, se queda igual
                'Comentarios Abuso': comentarios_abuso,  # No coincide, se queda igual
                #'Gafas': gafas,  # Coincide con columna
                #'Fecha de Compra Gafas': fecha_compra,  # No coincide, se queda igual
                #'Agudeza visual': agudeza_visual,  # Coincide con columna
                #'Oculomotores': oculomotores,  # Coincide con columna
                'Pendientes y Perforaciones': pendientes,  # Coincide con columna
                'Audición': audicion,  # Coincide con columna
                'Comentarios Audición': comentarios_audicion,  # No coincide, se queda igual
                'Otoscopia': otoscopia,  # Coincide con columna
                'Comentarios Otoscopia': comentarios_otoscopia,  # No coincide, se queda igual
                'Caries': bucal,  # Coincide con columna
                'Comentarios Higiene Bucal': comentarios_bucal,  # No coincide, se queda igual
                'Corazón': cardiaca,  # Coincide con columna
                'Comentarios Cardiaca': comentarios_cardiaca,  # No coincide, se queda igual
                'Pulmón': pulmon,  # Coincide con columna
                'Comentarios Pulmón': comentarios_pulmon,  # No coincide, se queda igual
                'Adams': adams,  # Coincide con columna
                'Comentarios Adams': comentarios_adams,  # No coincide, se queda igual
                'Abdomen': abdomen,  # Coincide con columna
                'Comentarios Abdomen': comentarios_abdomen,  # No coincide, se queda igual
                'Piojos': piojos,  # Coincide con columna
                'Piel': piel,
                'Lesiones': patologias,  # Coincide con columna
                'Tatuajes': tatuajes,  # Coincide con columna
                'Observaciones': valoracion,  # Coincide con columna
                
                'Oftalmología':ofta,
                'Comentarios Oftalmología': comentarios_oftalmo, 
                'Alimentación':alimentacion, 
                'Estado Anímico':estado_a,
                'Ideación Automítica':ideacion,
                'Urgente':urgente

            }


        # Convertir el diccionario a DataFrame
            new_row = pd.DataFrame(new_data, index=[0])
        
        # Concatenar con el DataFrame existente
            data = pd.concat([data, new_row], ignore_index=True)
    
            data.to_excel('niños_prep.xlsx', index=False)
            st.success("Los cambios se han guardado correctamente.")

    elif menu_seleccion == "existente":
        
        niñx = data[(data['Año'] == 2024)]
        nombres_ex=niñx['Nombre'].unique()
        opcion = st.sidebar.selectbox(
        "Elige un/a Niñ@: ", # refinar esto con Misael
        nombres_ex
        )

        niñx = niñx[(niñx['Nombre'] == opcion)]
        if not niñx.empty: 
            try: 
                
                with col2:
                    # print(niñx['Edad'].values[0])
                    st.write(f"""
                        #  {opcion}
                        """)
                    st.write(f"""
                        {niñx['Sexo'].values[0]}, {int(niñx['Edad'].values[0]+1)} años, nacid@ en {int(niñx['Fecha de nacimiento'].values[0])}
                        """)
                
                st.markdown('⚠️ Las celdas que aparecen escritas contienen registros del año anterior, pero se pueden modificar ⚠️')

                st.header('🌟 Datos Personales')

                nombre = niñx['Nombre'].values[0]
                sexo = niñx['Sexo'].values[0]
                edad=niñx['Edad'].values[0]+1
                nacimiento=niñx['Fecha de nacimiento'].values[0]
            except:
                with col2:
                    # print(niñx['Edad'].values[0])
                    st.write(f"""
                        #  {opcion}
                        """)
                    st.write(f"""
                        {niñx['Sexo'].values[0]}
                        """)
                
                st.markdown('⚠️ Las celdas que aparecen escritas contienen registros del año anterior, pero se pueden modificar ⚠️')

                st.header('🌟 Datos Personales')

                nombre = niñx['Nombre'].values[0]
                sexo = niñx['Sexo'].values[0]
                st.text(' ')
                st.markdown('⚠️ Porfavor añade la edad del niñ@ ⚠️')
                col1,col2,col3 = st.columns([1, 0.1,1])
                with col1:
                    edad=st.number_input('Edad: ', step=1,format="%d")
                with col3:
                    nacimiento=st.slider("Fecha de nacimiento: ", 2017, 2024, 2025-edad)    
                
                st.text(' ')
            
            st.text(' ')
                    
            hogar = st.text_input(
                        "Hogar: " ,key="hogar", value=niñx['Hogar'].values[0]
                    )

            st.text(' ')

            unidad_familiar = st.text_input(
                        "Unidad Familiar: ",key="unidad_familiar", value=niñx['Unidad Familiar'].values[0]
            )
            
            # st.text(' ')

            # uploaded_file = st.file_uploader("Sube una foto:", type=["jpg", "jpeg", "png"])
            # st.caption("⚠️ El nombre de la foto debe de corresponder con el nombre del niño/a.")


            # if uploaded_file is not None:
            #     image = Image.open(uploaded_file)
                    
            #     st.image(image, caption="Foto subida", width=150)

            #     with open("foto_subida.jpg", "wb") as f:
            #         f.write(uploaded_file.getbuffer())
                
            st.text(' ')

            st.header('🏠 Historia clínica y antecedentes')
            if niñx['Antecedentes Médicos'].values[0]== 'N/A':
                a_medicos = st.text_area(
                    "Antecedentes médicos: ",key="a_medicos"
                    
                    )
            else:
                a_medicos = st.text_area(
                    "Antecedentes médicos: ",key="a_medicos", value=niñx['Antecedentes Médicos'].values[0]
                    
                    )
            
            
            st.text(' ')

            if niñx['Antecedentes Familiares'].values[0]== 'N/A':
                a_familiares = st.text_area(
                    "Antecedentes familiares: ", key="a_familiares"
                    
                )

            else:
                a_familiares = st.text_area(
                    "Antecedentes familiares: ", key="a_familiares", value=niñx['Antecedentes Familiares'].values[0]
                    
                )
            st.text(' ')

            col1,col2 = st.columns([1,4])
            with col1:  
                alergias = st.radio(
                        "Alergias:",
                        options=["Sí", "No"],  index=1
                        
                )  
                    
            with col2:
                if niñx['Alergias'].values[0]== 'N/A':
                    comentarios_alergias = st.text_input(
                            "Comentarios acerca de las alergias: ", key="alergias"
                    )
                else:
                    comentarios_alergias = st.text_input(
                            "Comentarios acerca de las alergias: ", key="alergias",  value=niñx['Alergias'].values[0]
                    )
                st.text(' ')

            col1,col2 = st.columns([1,4])
            with col1:  
                medicacion = st.radio(
                        "Medicación:",
                        options=["Sí", "No"],  index=1
                        
                )  
                    
            with col2:
                if niñx['Medicación'].values[0]=='N/A':
                    comentarios_medicacion = st.text_input(
                        "Comentarios acerca de la medicación: ", key="medicacion"
                    )   
                
                else:
                    comentarios_medicacion = st.text_input(
                            "Comentarios acerca de la medicación: ", key="medicacion", value=niñx['Medicación'].values[0]
                    )

            st.text(' ')
            if sexo=='Femenino':
                col1,col2 = st.columns([1,4])
                with col1:  
                    menarquia = st.radio(
                            "Menarquia:",
                            options=["Sí", "No"],
                            
                    )  
                        
                with col2:
                    comentarios_menarquia = st.text_input(
                            "Comentarios acerca de la menarquia: ", key="menarquia"
                    )
            else: 
                menarquia='N/A'
                comentarios_menarquia='N/A'
                
            st.text(' ')

            st.header('📏 Antropometría y crecimiento')
            col1,col2, col3= st.columns([3,3,3])
            with col1:  
                peso=st.number_input('Peso (kg): ', step=0.1, key='peso' )

                    
            with col2:
                talla=st.number_input('Talla (cm): ', step=1, key='talla' )
                
            with col3:
                altura_m = talla / 100
                st.text(f'Índice de masa corporal: ')
                if peso==0 or talla==0:
                    imc='N/A'
                else: 
                    imc=round(peso / (altura_m ** 2), 2)
                st.markdown(f'{imc}')

            perimetro_b=st.number_input('Perímetro branquial: ', step=0.1, key='perimetro_b' )
            
            col1,col2 = st.columns([1,4])
            with col1:  
                genitales = st.radio(
                        "Genitales:",
                        options=["Normales", "Hallazgo"],
                        
                )  
            if genitales=='Hallazgo':   
                with col2:
                    comentarios_genitales = st.text_input(
                            "Comentarios acerca de los genitales: ", key="genitales"
                    )
            else:
                comentarios_genitales='N/A'
            
            st.text(' ')
            st.header('💉 Vacunas')
            st.text(' ')

            vacunas = st.text_area(
                "Vacunas: ",key="vacunas"
                " ",
                )
            st.text(' ')
            st.text(' ')

            st.header('🧠 Psicología y Comportamiento')
            st.text(' ')

            if edad>11:
                st.markdown('Nivel de autoestima: ')
                autoestima=st_star_rating(label='',maxValue = 5, defaultValue = 3, key = "autoestima", emoticons=True)

                st.markdown('Nivel de relacionalidad: ')
                relacional=st_star_rating(label='',maxValue = 5, defaultValue = 3, key = "relacional", emoticons=True)

                st.markdown('Nivel de organización: ')
                organizacion=st_star_rating(label='',maxValue = 5, defaultValue = 3, key = "organizacion", emoticons=True)

                st.markdown('Trastorno del sueño: ')
                insomnio=st_star_rating(label='',maxValue = 5, defaultValue = 3, key = "insomnio", emoticons=True)

                st.markdown('Nivel de ansiedad: ')
                ansiedad=st_star_rating(label='',maxValue = 5, defaultValue = 3, key = "ansiedad", emoticons=True)

                st.markdown('Alimentación: ')
                alimentacion=st_star_rating(label='',maxValue = 5, defaultValue = 3, key = "alimentacion", emoticons=True)

                st.markdown('Estado Anímico: ')
                estado_a=st_star_rating(label='',maxValue = 5, defaultValue = 3, key = "estado_a", emoticons=True)

                st.markdown('Ideación Autolítica: ')
                ideacion=st_star_rating(label='',maxValue = 5, defaultValue = 3, key = "ideacion", emoticons=True)
            else: 
                autoestima='N/A'
                relacional='N/A'
                organizacion='N/A'
                insomnio='N/A'
                ansiedad='N/A'
                alimentacion='N/A'        
                estado_a='N/A'
                ideacion='N/A'
                
            col1,col2 = st.columns([1,4])
            with col1:  
                abuso = st.radio(
                        "Abuso:",
                        options=["Sí", "No", "N/A"], index=2
                        
                )  
                    
            with col2:
                comentarios_abuso = st.text_input(
                        "Comentarios: ", key="comentarios_abuso"
                )
                
            st.text(' ')

            comentarios_psicologa = st.text_area(
                    "Comentarios psicóloga/o: ", key="comentarios_psicologa"
                    " ",
            )
            st.text(' ')

            st.header('👁️ Oftalmología')
            st.text(' ')
            col1,col2 = st.columns([1,4])
            # with col1:  
            ofta = st.radio(
                    "Revisado:",
                    options=["Sí", "No"],
                    
            )  

            if ofta == 'No':
                with col2:
                    comentarios_oftalmo = st.text_input(
                        "Comentarios oftalmología: ", key="comentarios_oftalmo"
                )        
            else:
                comentarios_oftalmo='N/A'

            st.header('👂 Otorrino')
            st.text(' ')
            pendientes = st.radio(
                        "Pendientes: ",
                        options=["Sí", "No", "N/A"],
                        
                ) 
            col1,col2 = st.columns([1,4])
            with col1:  
                audicion = st.radio(
                        "Audicición: ",
                        options=["Correcta", "Sordera"],
                        
                )  
            if audicion == 'Sordera':
                
                with col2:
                    comentarios_audicion = st.text_input(
                            "Comentarios acerca de la audición: ", key="comentarios_audicion"
                    )
            else: 
                comentarios_audicion='N/A'

            col1,col2 = st.columns([1,4])
            with col1:  
                otoscopia = st.radio(
                        "Otoscopia: ",
                        options=["Correcta", "Tapón"],
                        
                )  
            if otoscopia == 'Tapón':
                
                with col2:
                    comentarios_otoscopia = st.text_input(
                            "Comentarios acerca de la otoscopia: ", key="comentarios_otoscopia"
                    )
            else: 
                comentarios_otoscopia='N/A'

            st.text(' ')

            st.header('🦷 Bucal')
            st.text(' ')

            col1,col2,col3 = st.columns([1.5,3,1.5])
            with col1:  
                bucal = st.radio(
                        "Bucal: ",
                        options=["Buena higiene bucal", "Caries"],
                        
                )  
            with col2:
                comentarios_bucal = st.text_input(
                            "Comentarios acerca de la higiene bucal: ", key="comentarios_bucal"
                    )
                
            with col3:
                urgente = st.radio(
                        "Urgente: ",
                        options=["Sí", "No"], index=1
                        
                ) 
            
            st.text(' ')

            st.header('🫀 Auscultación')
            st.text(' ')
            col1,col2 = st.columns([1,4])
            with col1:  
                cardiaca = st.radio(
                        "Cardiaca: ",
                        options=["Correcta", "Hallazgo"],
                        
                )  
            if cardiaca == 'Hallazgo':
                
                with col2:
                    comentarios_cardiaca = st.text_input(
                            "Comentarios acerca de la auscultación cardiaca: ", key="comentarios_cardiaca"
                    )
            else: 
                comentarios_cardiaca='N/A'

            st.text(' ')
            col1,col2 = st.columns([1,4])
            with col1:  
                pulmon = st.radio(
                        "Pulmón: ",
                        options=["Correcto", "Hallazgo"],
                        
                )  
            if pulmon == 'Hallazgo':
                
                with col2:
                    comentarios_pulmon = st.text_input(
                            "Comentarios acerca de los pulmones: ", key="comentarios_pulmon"
                    )
            else: 
                comentarios_pulmon='N/A'

            st.text(' ')
            col1,col2 = st.columns([1,4])
            with col1:  
                adams = st.radio(
                        "Adams: ",
                        options=["Negativo", "Positivo"],
                        
                )  
            if adams == 'Negativo':
                
                with col2:
                    comentarios_adams = st.text_input(
                            "Comentarios Adams: ", key="comentarios_adams"
                    )
            else: 
                comentarios_adams='N/A'

            st.header('🖐️ Dermatología')

            st.text(' ')
            col1,col2 = st.columns([1,4])
            with col1:  
                abdomen = st.radio(
                        "Abdomen: ",
                        options=["Correcta", "Hallazgo"],
                        
                )  
            if abdomen == 'Hallazgo':
                
                with col2:
                    comentarios_abdomen = st.text_input(
                            "Comentarios acerca de la auscultación cardiaca: ", key="comentarios_abdomen"
                    )
            else: 
                comentarios_abdomen='N/A'


            st.text(' ')
            col1,col2 = st.columns([1,4])
            with col1:  
                piel = st.radio(
                        "Piel: ",
                        options=["Correcta", "Hallazgo"],
                        
                )  
            if piel == 'Hallazgo':
                col11,col12 = st.columns([4,1])
                
                with col11:
                    patologias = st.text_input(
                            "Patologías: ", key="patlogias"
                    )
            else: 
                patologias='N/A'
            
            col13,col23 = st.columns([3,3])
            with col13:
                tatuajes = st.radio(
                            "Tatuajes: ",
                            options=["Sí", "No"], index=1
                            
                    )  
                    
            st.text(' ')
            with col23:
                piojos = st.radio(
                            "Piojos: ",
                            options=["Sí", "No"], index=1
                            
                    )  
                
            
            st.text(' ')

            st.header('📋 Valoración final')
            valoracion = st.text_area(
                "Valoración final: ",key="valoracion"
                " ",
                )
            st.text(' ')

            col1,col2 = st.columns([1,4])
            with col1:  

                revaluar = st.radio(
                            "Revalorar: ",
                            options=["Sí", "No"], index=1
                            
                    ) 
            with col2: 
                if revaluar == "Sí":
                    st.markdown("🔄 **Revalorar al niño/a**")
                else:
                    st.markdown("✅ **No requiere revaluación**")


            if st.button("Guardar registro"):
            #     try: 
            #             # foto
            #         save_path = "fotos"  
            #         if not os.path.exists(save_path):
            #             os.makedirs(save_path)  # Crear la ruta si no existe
                        
            #             # Guardar la imagen con su nombre original
            #         image.save(os.path.join(save_path, uploaded_file.name))
            #         #st.success("Los cambios se han guardado correctamente.")

            #             # datos
            #     except: 
            #         st.warning('No se pudieron guardar los cambios, añada la foto correctamente.', icon="⚠️")
                
                new_data = {
                    'Revaluar': revaluar,  # No coincide, se queda igual
                    'Año': 2025,  # Coincide con columna
                    'Nombre': nombre,  # Coincide con columna
                    'Sexo': sexo,  # Coincide con columna
                    'Hogar': hogar,  # Coincide con columna
                    'Edad': edad,  # Coincide con columna
                    'Fecha de nacimiento': nacimiento,  # Coincide con columna
                    'Unidad Familiar': unidad_familiar,  # Coincide con columna
                    'Antecedentes Médicos': a_medicos,  # Coincide con columna
                    'Antecedentes Familiares': a_familiares,  # Coincide con columna
                    'Medicación': medicacion,  # Coincide con columna
                    'Alergias': alergias,  # Coincide con columna
                    'Comentarios Alergias': comentarios_alergias,  # No coincide, se queda igual
                    'Comentarios Medicación': comentarios_medicacion,  # No coincide, se queda igual
                    'Menarquia': menarquia,  # Coincide con columna
                    'Comentarios Menarquía': comentarios_menarquia,  # No coincide, se queda igual
                    'Peso (Kg)': peso,  # Coincide con columna
                    'Talla (Cm)': talla,  # Coincide con columna
                    'IMC': imc,
                    'Perímetro Branquial': perimetro_b,  # Coincide con columna
                    'Genitales':genitales,
                    'Comentarios Genitales':comentarios_genitales, 
                    'Vacunas': vacunas,  # No coincide, se queda igual
                    'Autoestima/autoimagen': autoestima,  # Coincide con columna
                    'Relacional': relacional,  # Coincide con columna
                    'Organización': organizacion,  # No coincide, se queda igual
                    'Transtorno del sueño': insomnio,  # Coincide con columna
                    'Ansiedad': ansiedad,  # No coincide, se queda igual
                    'Comentarios Psicología':comentarios_psicologa,
                    'Abuso': abuso,  # No coincide, se queda igual
                    'Comentarios Abuso': comentarios_abuso,  # No coincide, se queda igual
                    #'Gafas': gafas,  # Coincide con columna
                    #'Fecha de Compra Gafas': fecha_compra,  # No coincide, se queda igual
                    #'Agudeza visual': agudeza_visual,  # Coincide con columna
                    #'Oculomotores': oculomotores,  # Coincide con columna
                
                    'Pendientes y Perforaciones': pendientes,  # Coincide con columna
                    'Audición': audicion,  # Coincide con columna
                    'Comentarios Audición': comentarios_audicion,  # No coincide, se queda igual
                    'Otoscopia': otoscopia,  # Coincide con columna
                    'Comentarios Otoscopia': comentarios_otoscopia,  # No coincide, se queda igual
                    'Caries': bucal,  # Coincide con columna
                    'Comentarios Higiene Bucal': comentarios_bucal,  # No coincide, se queda igual
                    'Corazón': cardiaca,  # Coincide con columna
                    'Comentarios Cardiaca': comentarios_cardiaca,  # No coincide, se queda igual
                    'Pulmón': pulmon,  # Coincide con columna
                    'Comentarios Pulmón': comentarios_pulmon,  # No coincide, se queda igual
                    'Adams': adams,  # Coincide con columna
                    'Comentarios Adams': comentarios_adams,  # No coincide, se queda igual
                    'Abdomen': abdomen,  # Coincide con columna
                    'Comentarios Abdomen': comentarios_abdomen,  # No coincide, se queda igual
                    'Piojos': piojos,  # Coincide con columna
                    'Piel': piel,
                    'Lesiones': patologias,  # Coincide con columna
                    'Tatuajes': tatuajes,  # Coincide con columna
                    'Observaciones': valoracion,  # Coincide con columna
                    'Oftalmología':ofta,
                    'Comentarios Oftalmología': comentarios_oftalmo, 
                    'Alimentación':alimentacion,
                    'Estado Anímico':estado_a,
                    'Ideación Automítica': ideacion,
                    'Urgente':urgente
                }


            # Convertir el diccionario a DataFrame
                new_row = pd.DataFrame(new_data, index=[0])
            
            # Concatenar con el DataFrame existente
                data = pd.concat([data, new_row], ignore_index=True)
        
                data.to_excel('niños_prep.xlsx', index=False)
                st.success("Los cambios se han guardado correctamente.")
        else:
            st.write('No hay datos disponibles')
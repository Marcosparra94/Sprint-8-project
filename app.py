import streamlit as st
import pandas as pd
import plotly.express as px

st.markdown("<h1 style='text-align: center; color: #0A74DA;'>📊 Dashboard de Vehículos</h1>", unsafe_allow_html=True)

car_data = pd.read_csv('vehicles_us.csv')
car_data['date_posted'] = pd.to_datetime(car_data['date_posted'], errors='coerce')

# Sidebar con filtros
st.sidebar.header("Filtros")

precio_min, precio_max = int(car_data['price'].min()), int(car_data['price'].max())
precio_seleccion = st.sidebar.slider("Rango de Precio", precio_min, precio_max, (precio_min, precio_max))

tipos = car_data['type'].dropna().unique()
tipos_seleccion = st.sidebar.multiselect("Tipo de Vehículo", tipos, default=tipos)

filtro = (
    (car_data['price'] >= precio_seleccion[0]) &
    (car_data['price'] <= precio_seleccion[1]) &
    (car_data['type'].isin(tipos_seleccion))
)
df_filtrado = car_data.loc[filtro]

st.write(f"### Registros después del filtro: {df_filtrado.shape[0]}")

# Casillas para elegir qué gráficos mostrar
mostrar_histograma = st.checkbox('Mostrar Histograma de Kilometraje')
mostrar_barras = st.checkbox('Mostrar Conteo por Tipo de Vehículo')
mostrar_dispersion = st.checkbox('Mostrar Gráfico de Dispersión Precio vs Kilometraje')

if mostrar_histograma:
    odometer_data = df_filtrado['odometer'].dropna()
    fig_hist = px.histogram(odometer_data, nbins=50, title='Distribución del Kilometraje', labels={'value': 'Kilometraje'})
    st.plotly_chart(fig_hist, use_container_width=True)

if mostrar_barras:
    conteo_tipos = df_filtrado['type'].value_counts().reset_index()
    conteo_tipos.columns = ['Tipo', 'Cantidad']
    fig_bar = px.bar(conteo_tipos, x='Tipo', y='Cantidad', title='Cantidad de Vehículos por Tipo', labels={'Cantidad': 'Cantidad', 'Tipo': 'Tipo'})
    st.plotly_chart(fig_bar, use_container_width=True)

if mostrar_dispersion:
    df_disp = df_filtrado.dropna(subset=['odometer', 'price'])
    fig_scatter = px.scatter(df_disp, x='odometer', y='price', 
                             title='Precio vs Kilometraje',
                             labels={'odometer': 'Kilometraje', 'price': 'Precio'},
                             hover_data=['model', 'type'])
    st.plotly_chart(fig_scatter, use_container_width=True)

st.write("### Vista previa de datos filtrados:")
st.dataframe(df_filtrado.head(10))

st.markdown("---")
st.markdown("<p style='text-align:center; font-size:12px;'>Proyecto desarrollado por Marcos. &copy; 2025</p>", unsafe_allow_html=True)


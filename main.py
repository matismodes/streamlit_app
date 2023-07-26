import streamlit as st
import pandas as pd
import numpy as np
import plotly as plt
import plotly.graph_objects as go
import datetime
import locale


locale.setlocale(locale.LC_TIME, 'es_ES')

df_raw = pd.read_excel('raw_data.xlsx')

df = df_raw.copy()

df = df.sort_values('fecha')

default_date = min(df.fecha)

st.sidebar.title('Parámetros de Busqueda')
sel_Date = st.sidebar.date_input(label = 'Seleccionar fecha:', value = default_date, min_value = min(df.fecha), max_value = max(df.fecha))
sel_fDate = sel_Date + datetime.timedelta(days = 1)
dia = sel_Date.strftime('%Y-%m-%d')
diaf = sel_fDate.strftime('%Y-%m-%d')

sel_df = df[(df['fecha'] >= dia) & (df['fecha'] < diaf)]

st.header('Datos Meteorológicos y Calidad del Aire en Lima')

if len(sel_df) == 0:
    st.subheader(sel_Date.strftime('%d de %B de %Y'))
    st.caption('No se encontraron datos en la fecha seleccionada. Por favor intente otra fecha.')
else:
    st.subheader(sel_Date.strftime('%d de %B de %Y'))
    tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8 = st.tabs(["Punto de Recolección","Temperatura", "Presión", "Humedad", "UV", "Ruido", "Gases", "Material Particulado"])
    # Grafico 1
    layout = go.Layout(
        title='Concentración de H2S, NO2, O3, y SO2 a lo largo del día',
        yaxis=dict(title='Concentración (ug/m3)'),
        xaxis=dict(title='Hora')
    )

    fig1 = go.Figure(layout = layout)
    fig1.add_trace(go.Scatter(x=sel_df['fecha'], y=sel_df['h2s(ug/m3)'],\
                            mode='lines', name='H2S',
                            line = dict(color = 'red')))

    fig1.add_trace(go.Scatter(
        x=[min(sel_df['fecha']), max(sel_df['fecha'])],
        y=[50, 50],
        mode='lines',
        line=dict(color="red", dash="dash"),
        name='Límite H2S'
    ))

    fig1.add_trace(go.Scatter(x=sel_df['fecha'], y=sel_df['no2(ug/m3)'],\
                            mode='lines', name='NO2',
                            line = dict(color = 'blue')))

    fig1.add_trace(go.Scatter(
        x=[min(sel_df['fecha']), max(sel_df['fecha'])],
        y=[40, 40],
        mode='lines',
        line=dict(color="blue", dash="dash"),
        name='Límite NO2'
    ))


    fig1.add_trace(go.Scatter(x=sel_df['fecha'], y=sel_df['o3(ug/m3)'],\
                            mode='lines', name='O3',
                            line = dict(color = 'green')))

    fig1.add_trace(go.Scatter(
        x=[min(sel_df['fecha']), max(sel_df['fecha'])],
        y=[120, 120],
        mode='lines',
        line=dict(color="green", dash="dash"),
        name='Límite O3'
    ))


    fig1.add_trace(go.Scatter(x=sel_df['fecha'], y=sel_df['so2(ug/m3)'],\
                            mode='lines', name='SO2',
                            line = dict(color = 'orange')))

    fig1.add_trace(go.Scatter(
        x=[min(sel_df['fecha']), max(sel_df['fecha'])],
        y=[125, 125],
        mode='lines',
        line=dict(color="orange", dash="dash"),
        name='Límite SO2'
    ))


    # Grafico 2

    layout = go.Layout(
        title='Concentración de CO a lo largo del día',
        yaxis=dict(title='Concentración (ug/m3)'),
        xaxis=dict(title='Hora')
    )

    fig2 = go.Figure(layout = layout)
    fig2.add_trace(go.Scatter(x=sel_df['fecha'], y=sel_df['co(ug/m3)'],\
                            mode='lines', name='CO',
                            line = dict(color = 'purple')))

    fig2.add_trace(go.Scatter(
        x=[min(sel_df['fecha']), max(sel_df['fecha'])],
        y=[10000, 10000],
        mode='lines',
        line=dict(color="purple", dash="dash"),
        name='Límite Aceptable'
    ))

    fig2.update_layout(template='plotly_white')
    fig2.update_layout(legend=dict(title='Leyenda'))


    #Grafico 3

    layout = go.Layout(
        title='Concentración de PM10 y PM2.5 a lo largo del día',
        yaxis=dict(title='Concentración (ug/m3)'),
        xaxis=dict(title='Hora')
    )

    fig3 = go.Figure(layout = layout)
    fig3.add_trace(go.Scatter(x=sel_df['fecha'], y=sel_df['pm10(ug/m3)'],\
                            mode='lines', name='PM10',
                            line = dict(color = 'black')))

    fig3.add_trace(go.Scatter(
        x=[min(sel_df['fecha']), max(sel_df['fecha'])],
        y=[40, 40],
        mode='lines',
        line=dict(color="black", dash="dash"),
        name='Límite Aceptable'
    ))

    fig3.add_trace(go.Scatter(x=sel_df['fecha'], y=sel_df['pm2.5(ug/m3)'],\
                            mode='lines', name='PM2.5',
                            line = dict(color = 'grey')))

    fig3.add_trace(go.Scatter(
        x=[min(sel_df['fecha']), max(sel_df['fecha'])],
        y=[20, 20],
        mode='lines',
        line=dict(color="grey", dash="dash"),
        name='Límite Aceptable'
    ))

    fig3.update_layout(template='plotly_white')
    fig3.update_layout(legend=dict(title='Leyenda'))


    # Grafico 4 - Temperatura
    layout = go.Layout(
        title='Temperatura a lo largo del día',
        yaxis=dict(title='Grados Centígrados (grad. C)'),
        xaxis=dict(title='Hora')
    )
    fig4 = go.Figure(layout = layout)
    fig4.add_trace(go.Scatter(x=sel_df['fecha'], y=sel_df['temperatura(c)'],\
                            mode='lines', name='Temperatura',
                            line = dict(color = 'orange')))
    fig4.update_layout(template='plotly_white')

    # Grafico 5 - Presión
    layout = go.Layout(
        title='Presión a lo largo del día',
        yaxis=dict(title="Presión (Pa)"),
        xaxis=dict(title='Hora')
    )
    fig5 = go.Figure(layout = layout)
    fig5.add_trace(go.Scatter(x=sel_df['fecha'], y=sel_df['presion(pa)'],\
                            mode='lines', name='Presión',
                            line = dict(color = 'blue')))
    fig5.update_layout(template='plotly_white')


    # Grafico 6 - Humedad
    layout = go.Layout(
        title='Humedad a lo largo del día',
        yaxis=dict(title="humedad(%)"),
        xaxis=dict(title='Hora')
    )
    fig6 = go.Figure(layout = layout)
    fig6.add_trace(go.Scatter(x=sel_df['fecha'], y=sel_df['humedad(%)'],\
                            mode='lines', name='Humedad',
                            line = dict(color = 'cyan')))
    fig6.update_layout(template='plotly_white')


    # Grafico 7 - uv
    layout = go.Layout(
        title='Radiación uv a lo largo del día',
        yaxis=dict(title="uv"),
        xaxis=dict(title='Hora')
    )
    fig7 = go.Figure(layout = layout)
    fig7.add_trace(go.Scatter(x=sel_df['fecha'], y=sel_df['uv'],\
                            mode='lines', name='uv',
                            line = dict(color = 'magenta')))
    fig7.update_layout(template='plotly_white')


    # Grafico 8 - Ruido
    layout = go.Layout(
        title='Ruido a lo largo del día',
        yaxis=dict(title="ruido(db)"),
        xaxis=dict(title='Hora')
    )
    fig8 = go.Figure(layout = layout)
    fig8.add_trace(go.Scatter(x=sel_df['fecha'], y=sel_df['ruido(db)'],\
                            mode='lines', name='Ruido',
                            line = dict(color = 'red')))
    fig8.update_layout(template='plotly_white')

    tab1.header('Punto de Recolección')
    tab1.map(data = sel_df, latitude = 'latitud', longitude = 'longitud')

    tab2.header('Temperatura')
    tab2.plotly_chart(fig4, use_container_width = True)

    tab3.header('Presión')
    tab3.plotly_chart(fig5, use_container_width = True)

    tab4.header('Humedad')
    tab4.plotly_chart(fig6, use_container_width= True)

    tab5.header('uv')
    tab5.plotly_chart(fig7, use_container_width = True)

    tab6.header('Ruido')
    tab6.plotly_chart(fig8, use_container_width= True)

    tab7.header('Gases')
    tab7.plotly_chart(fig1, use_container_width = True)
    tab7.plotly_chart(fig2, use_container_width = True)

    tab8.header('Material Particulado')
    tab8.plotly_chart(fig3, use_container_width = True)



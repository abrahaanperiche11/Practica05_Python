#importamos 
import pandas as pd
import requests
import sqlite3

#definimos funciones
#funcion de limpieza
def limpieza(df):
    # Renombrar columnas eliminando espacios, tildes y convirtiendo a minúsculas
    df.columns = [col.strip().lower().replace(' ', '_').replace('á', 'a').replace('é', 'e').replace('í', 'i').replace('ó', 'o').replace('ú', 'u') for col in df.columns]
    
    return df
#funcion de hacer el cambio a dolar
def obtener_tipo_cambio_dolar():
    response = requests.get('https://api.apis.net.pe/v1/tipo-cambio-sunat')
    tipo_cambio = response.json()['venta']
    return tipo_cambio
#funcion que puntúa el estado en 3, 2, 1, 0
def puntua_estado(row):
    if row.estado=='ActosPrevios':
        return 1
    elif row.estado=='Resuelto':
        return 0
    elif row.estado=='Ejecucion':
        return 2
    elif row.estado=='Concluido':
        return 3
# Función para filtrar y guardar el top 5 de proyectos por región
def generar_reporte_por_region(region):
    df_region = df[df['region'] == region] 
    df_filt = df[(df['tipologia'] == 'Equipamiento Urbano') & (df['puntua_estado'].isin([1, 2, 3]))]
    df_filt = df_filt.sort_values(by='monto_de_inversion', ascending=False)
    top_5 = df_filt.head()
    excel_file = f"./REPORTES/{region}_top5_costo_inversion.xlsx"
    # Guardar en Excel solo si hay datos
    if not top_5.empty:
        top_5.to_excel(excel_file, index=False)
        print(f"Reporte para la región {region} generado correctamente en {excel_file}")
    else:
        print(f"No hay datos para la región {region}")

#importamos el archivo REACTIVA.xlsx
path_ = "./DATA/REACTIVA.xlsx"
df=pd.read_excel(path_,sheet_name='TRANSFERENCIAS 2020')
pd.set_option('display.max_columns',None)

df=limpieza(df)
#eliminar columna ID
df=df.drop(['id'],axis=1)
#eliminar columna repetida tipo_moneda.1
df = df.drop(['tipo_moneda.1'],axis=1)
#elimina el caracter coma de DISPOSITIVO LEGAL:
df['dispositivo_legal']=df['dispositivo_legal'].replace({',':''},regex=True)
#empleando el api SUNAT...

# Obtener el tipo de cambio actual del dólar
tipo_cambio_dolar = obtener_tipo_cambio_dolar()

# Dolarizar los valores del monto de inversión y montos de transferencia
df['monto_inversion_dolarizado'] = df['monto_de_inversion'] / tipo_cambio_dolar
df['monto_transferencia_dolarizado'] = df['monto_de_transferencia_2020'] / tipo_cambio_dolar

#para la columna estado
df['estado']=df['estado'].replace({'Actos Previos':'ActosPrevios',
                                   'Convenio y/o Contrato Resuelto':'Resuelto',
                                   'En Ejecución':'Ejecucion'},regex=True)

#crear una columna que puntue el estado segun:...
df['puntua_estado']=df.apply(puntua_estado,axis='columns')
print(df)

#GENERAR REPORTES:
df_ubigeos_unicos=df[['ubigeo', 'region', 'provincia', 'distrito']].drop_duplicates()

with sqlite3.connect('./DATA/db_ubigeo') as conn:
    table_name='ubigeo'
    df_ubigeos_unicos.to_sql(table_name,conn,index=False, if_exists='replace')

#para ver la base de datos en la tabla 
with sqlite3.connect('./DATA/db_ubigeo') as conn:
    query='SELECT * FROM ubigeo'
    df_db=pd.read_sql_query(query,conn)
    pass
print(df_db)

# Obtener la lista de regiones
regiones = df['region'].unique()

# Generar reporte para cada región
for region in regiones:
    generar_reporte_por_region(region)
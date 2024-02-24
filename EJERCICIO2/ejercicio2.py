import pandas as pd
df_winemag = pd.read_csv("./DATA/winemag-data-130k-v2.csv",encoding='utf-8')
pd.set_option('display.max_columns',None)
#Explore el dataframe según lo visto en clase
print(f'(Filas,Columnas):\n{df_winemag.shape}\n------------------')
print(f'Tipos de datos:\n{df_winemag.dtypes}\n------------------')
print(f'5 primeras filas:\n{df_winemag.head()}\n------------------')
print(f'5 últimas filas:\n{df_winemag.tail()}\n------------------')
print(f'Resumen de los datos:\n{df_winemag.describe()}\n------------------')
print(f'Paises evaluados:\n{df_winemag.country.unique()}\n------------------')

#Realice al menos 4 renombre de columna 
df_winemag.rename(columns={'Unnamed: 0':'index','taster_twitter_handle':'twitter','taster_name':'taster','title':'brand'},inplace=True)
#Crea 3 nuevas columnas según criterio. Deberá crear las columnas que crea conveniente. 
#Ejemplo: Según el país etiquetelos según continente.
def obtener_continente(pais):
    if pais in ['Italy', 'Portugal', 'Spain', 'France', 'Germany', 'Austria', 'Hungary',
                'Greece', 'Romania', 'Czech Republic', 'Slovenia', 'Luxembourg', 'Croatia',
                'Serbia', 'Moldova', 'Bulgaria', 'Switzerland', 'Bosnia and Herzegovina',
                'Ukraine', 'Slovakia', 'Macedonia']:
        return 'Europe'
    elif pais in ['US', 'Canada', 'Mexico']:
        return 'North America'
    elif pais in ['Argentina', 'Chile', 'Brazil', 'Uruguay', 'Peru']:
        return 'South America'
    elif pais in ['Australia', 'New Zealand']:
        return 'Oceania'
    elif pais in ['South Africa', 'Morocco']:
        return 'Africa'
    elif pais in ['Israel', 'Turkey', 'Lebanon', 'Georgia', 'India', 'Armenia', 'Cyprus']:
        return 'Asia'
    else:
        return None 
df_winemag['continent']=df_winemag['country'].apply(obtener_continente)

#Ejemplo2: Según su puntuación, tendrá un nuevo costo, por ejemplo si la puntuación es de 87 y cuesta 50, entonces su nuevo costo será 43.5 (87/100)*50
df_winemag['ajuste_precio']=df_winemag.points/100
df_winemag['new_price']=df_winemag.ajuste_precio*df_winemag.price

#ejemplo3: contar reviews, si existe taster, daremos 1 al review, de lo contrario se dará 0

def asignar_puntuacion(row):
    if row=='NaN':
        return 0
    else:
        return 1

df_winemag['review']=df_winemag['taster'].apply(asignar_puntuacion)
print(df_winemag)
#Genere 4 reportes por agrupamiento de datos. Deberá elegir que reportes realizar
#Ejemplo: Por contienente mostrar los vinos mejor puntuados
df_reporte1=df_winemag.groupby(['continent']).agg({'points':'max'})
df_reporte1=df_reporte1.sort_values(by='points', ascending=False)
print(f'------------------------------------------\nREPORTE 1:\n{df_reporte1}')
#Ejemplo2: Promedio de precio de vino y cantidad de reviews obtenidos según pais. 
#Ordenado de mejor a peor
df_reporte2=df_winemag.groupby(['country',]).agg({'price':'mean','review':'count'})
df_reporte2=df_reporte2.sort_values(by=['price','review'], ascending=[False,False])
print(f'------------------------------------------\nREPORTE 2:\n{df_reporte2}')
#Ejemplo3:Precio máximo, precio mínimo, cantidad de vinos y promedio dado el continente-país
df_reporte3=df_winemag.groupby(['continent','country']).agg({'price':['max','min'],'country':'count','points':'mean'})
print(f'------------------------------------------\nREPORTE 3:\n{df_reporte3}')
#Ejemplo4: País con el precio de vinos más barato segun el nuevo precio que usamos en el apartado anterior
df_reporte4=df_winemag.groupby(['country',]).agg({'new_price':'min'})
df_reporte4=df_reporte4.sort_values(by='new_price', ascending=True)
print(f'------------------------------------------\nREPORTE 4:\n{df_reporte4}')

#Al menos uno de estos datos agrupados deberán ser almacenados en excel o csv
path_="./DATA/reporte.xlsx"
df_reporte2.to_excel(path_, index=False, sheet_name='REPORTE')

import pandas as pd
df_airbnb = pd.read_csv("./DATA/airbnb.csv",encoding='utf-8')
pd.set_option('display.max_columns',None)

#CASO 01: Alicia va a ir a Lisboa durante una semana con su marido y sus 2 hijos.
#Están buscando un apartamento con habitaciones separadas para los padres y los hijos. (Entire home/apt)
#No les importa donde alojarse o el precio, simplemente quieren tener una experiencia agradable. 
#Esto significa que solo aceptan lugares con más de 10 críticas con una puntuación mayor de 4. 
#Cuando seleccionemos habitaciones para Alicia, tenemos que asegurarnos de ordenar las habitaciones de mejor a peor puntuación. 
#Para aquellas habitaciones que tienen la misma puntuación, debemos mostrar antes aquellas con más críticas. 
#Debemos darle 3 alternativas.

conditions=(df_airbnb.room_type=='Entire home/apt')&(df_airbnb.overall_satisfaction>4)&(df_airbnb.reviews>10)
df_alicia=df_airbnb[conditions].sort_values(by=['overall_satisfaction','reviews'],ascending=[False,False])
print(f'-----------------------------------------\nMejores 3 alternativas:\n{df_alicia.head(3)}')
import pandas as pd
df_airbnb = pd.read_csv("./DATA/airbnb.csv",encoding='utf-8')
pd.set_option('display.max_columns',None)
# Roberto es un casero que tiene una casa en Airbnb. 
# De vez en cuando nos llama preguntando sobre cuales son las críticas de su alojamiento. 
# Hoy está particularmente enfadado, ya que su hermana Clara ha puesto una casa en Airbnb
# y Roberto quiere asegurarse de que su casa tiene más críticas que las de Clara. 
# Tenemos que crear un dataframe con las propiedades de ambos.
# Las id de las casas de Roberto y Clara son 97503 y 90387 respectivamente.
# Finalmente guardamos este dataframe como excel llamado "roberto.xls

conditions_roberto=(df_airbnb.room_id==97503)|(df_airbnb.room_id==90387)
df_roberto=df_airbnb[conditions_roberto]
path_="./DATA/roberto.xlsx"
df_roberto.to_excel(path_, index=False, sheet_name='CASAS')
print(f'------------------------------------------------------------\nREPORTE DE ROBERTO:\n{df_roberto}')

import pandas as pd
df_airbnb = pd.read_csv("./DATA/airbnb.csv",encoding='utf-8')
pd.set_option('display.max_columns',None)

#Diana va a Lisboa a pasar 3 noches y quiere conocer a gente nueva. 
#Tiene un presupuesto de 50€ para su alojamiento. 
#Debemos buscarle las 10 propiedades más baratas, 
#dandole preferencia a aquellas que sean habitaciones compartidas (room_type == Shared room),
# y para aquellas viviendas compartidas debemos elegir aquellas con mejor puntuación.

conditions_diana=(df_airbnb.price <= 50)&(df_airbnb.room_type == 'Shared room')
df_diana=df_airbnb[conditions_diana].sort_values(by=['price','overall_satisfaction'],ascending=[True,False])
print(f'-----------------------------------------------------------\nREPORTE DIANA:\n{df_diana.head(10)}')
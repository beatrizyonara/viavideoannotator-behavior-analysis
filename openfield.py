import pandas as pd

csv = r"C:\Users\Cliente\Downloads\Demo-Video Annotation14May2024_01h14m43s_export.csv"
df = pd.read_csv(csv) 

# Separar os dados para cada animal
df['Animal'] = df['animal'].str.split(' ').str[1].str.split('.').str[0]  # Extrair o número do animal
df['Animal'] = df['Animal'] + '_' + (df.groupby('Animal').cumcount() + 1).astype(str)  # Adicionar o número de ocorrência do animal

resultados = []

for animal, dados_animal in df.groupby('Animal'):
    mean_speed = dados_animal['area'].count() / (dados_animal['end_time'].max() - dados_animal['start_time'].min())
    line_crossings = dados_animal[dados_animal['area'].shift() != dados_animal['area']]['area'].count()
    
    center_entries = dados_animal[dados_animal['area'].str.contains('center', case=False)]['area'].count()
    center_time = dados_animal[dados_animal['area'].str.contains('center', case=False)]['end_time'].sum() - dados_animal[dados_animal['area'].str.contains('center', case=False)]['start_time'].sum()
    center_avg_speed = center_entries / center_time
    center_mean_visit = center_time / center_entries
    
    periphery_entries = dados_animal[dados_animal['area'].str.contains('periphery', case=False)]['area'].count()
    periphery_time = dados_animal[dados_animal['area'].str.contains('periphery', case=False)]['end_time'].sum() - dados_animal[dados_animal['area'].str.contains('periphery', case=False)]['start_time'].sum()
    periphery_avg_speed = periphery_entries / periphery_time
    periphery_mean_visit = periphery_time / periphery_entries
    
    resultados.append({
        'Animal': animal,
        'Mean speed (m/s)': mean_speed,
        'Line crossings': line_crossings,
        'Center: entries': center_entries,
        'Center: time (s)': center_time,
        'Center: average speed (m/s)': center_avg_speed,
        'Center: mean visit (s)': center_mean_visit,
        'Periphery: entries': periphery_entries,
        'Periphery: time (s)': periphery_time,
        'Periphery: average speed (m/s)': periphery_avg_speed,
        'Periphery: mean visit (s)': periphery_mean_visit
    })

resultados_df = pd.DataFrame(resultados)
print(resultados_df)

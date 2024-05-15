import pandas as pd

file_path = r"C:\Users\Cliente\Downloads\Ligth_Dark_Bia06May2024_22h07m48s_export.csv"
df = pd.read_csv(file_path)

df['codigo_animal'] = df['codigo'].str.split('_').str[0]

df['start_Time'] = pd.to_numeric(df['start_Time'], errors='coerce')
df['end_Time'] = pd.to_numeric(df['end_Time'], errors='coerce')

# Criar 'duração'
df['duration'] = df['end_Time'] - df['start_Time']
df = df.dropna()

# Filtrar
light_data = df[df['area'] == 'Ligth']
dark_data = df[df['area'] == 'Dark']

selected_columns = ['codigo', 'animal', 'start_Time', 'end_Time', 'area']
selected_data = df[selected_columns]

light_data = selected_data[selected_data['area'].str.contains('Ligth')]
dark_data = selected_data[selected_data['area'].str.contains('Dark')]

# DataFrames separados
light_data.to_csv('light_data.csv', index=False)
dark_data.to_csv('dark_data.csv', index=False)

def calculate_parameters(df):
    # Light
    light_entries = len(df[df['area'] == 'Ligth']) - 1
    light_total_time_seconds = (df[df['area'] == 'Ligth']['duration']).sum()
    light_latency_to_1st_exit = df[df['area'] == 'Ligth']['start_Time'].iloc[1] - df[df['area'] == 'Ligth']['start_Time'].iloc[0] if len(df[df['area'] == 'Ligth']) > 0 else 0
    light_mean_visit = light_total_time_seconds / light_entries if light_entries > 0 else 0

    # Dark
    dark_entries = len(df[df['area'] == 'Dark'])
    dark_total_time_seconds = (df[df['area'] == 'Dark']['end_Time'] - df[df['area'] == 'Dark']['start_Time']).sum()
    dark_latency_to_1st_exit = df[df['area'] == 'Dark']['start_Time'].iloc[0] - df[df['area'] == 'Ligth']['start_Time'].iloc[0] if len(df[df['area'] == 'Dark']) > 0 else 0
    dark_mean_visit = dark_total_time_seconds / dark_entries if dark_entries > 0 else 0

    return light_entries, light_total_time_seconds, light_latency_to_1st_exit, light_mean_visit, dark_entries, dark_total_time_seconds, dark_mean_visit, dark_latency_to_1st_exit

# Para cada animal
animal_parameters = {}
for animal_id, animal_data in df.groupby('codigo_animal'):
    light_entries, light_total_time_seconds, light_latency_to_1st_exit, light_mean_visit, dark_entries, dark_total_time_seconds, dark_mean_visit, dark_latency_to_1st_exit = calculate_parameters(animal_data)
    animal_parameters[animal_id] = {
        'Light Entries': light_entries,
        'Light Total Time (s)': light_total_time_seconds,
        'Light Latency to 1st Exit (s)': light_latency_to_1st_exit,
        'Light Mean Visit (s)': light_mean_visit,
        'Dark Entries': dark_entries,
        'Dark Total Time (s)': dark_total_time_seconds,
        'Dark Mean Visit (s)': dark_mean_visit,
        'Dark Latency to 1st Exit (s)': dark_latency_to_1st_exit
    }

# Imprimir os parâmetros
print(animal_parameters)

animal_21_parameters = animal_parameters['21']
print(animal_21_parameters)

animal_22_parameters = animal_parameters['22']
print(animal_22_parameters)

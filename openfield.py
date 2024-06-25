import pandas as pd
from tkinter import Tk
from tkinter.filedialog import asksaveasfilename

csv = r"C:\Users\Biohacker\Documents\Bia Yonara\Code's VIA\OpenField_Rafa.csv"
df = pd.read_csv(csv)

df['start_time'] = pd.to_numeric(df['start_time'], errors='coerce')
df['end_time'] = pd.to_numeric(df['end_time'], errors='coerce')

df['Animal'] = df['animal'].str.split(' ').str[1].str.split('.').str[0]

resultados = []

for animal, dados_animal in df.groupby('Animal'):
    mean_speed = dados_animal['area'].count() / (dados_animal['end_time'].max() - dados_animal['start_time'].min())
    line_crossings = dados_animal[dados_animal['area'].shift() != dados_animal['area']]['area'].count()
    
    center_data = dados_animal[dados_animal['area'].str.contains('center', case=False)]
    center_entries = center_data['area'].count()
    center_time = center_data['end_time'].sum() - center_data['start_time'].sum()
    center_avg_speed = center_entries / center_time if center_time != 0 else 0
    center_mean_visit = center_time / center_entries if center_entries != 0 else 0
    
    periphery_data = dados_animal[dados_animal['area'].str.contains('periphery', case=False)]
    periphery_entries = periphery_data['area'].count()
    periphery_time = periphery_data['end_time'].sum() - periphery_data['start_time'].sum()
    periphery_avg_speed = periphery_entries / periphery_time if periphery_time != 0 else 0
    periphery_mean_visit = periphery_time / periphery_entries if periphery_entries != 0 else 0
    
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

root = Tk()
root.withdraw()

output_path = asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])

if output_path:
    resultados_df.to_csv(output_path, index=False)
    print(f"Resultados salvos em {output_path}")
else:
    print("Nenhum arquivo foi selecionado.")

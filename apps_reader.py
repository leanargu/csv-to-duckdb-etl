import numpy as np
import pandas as pd
import duckdb

# Cargar CSV
df = pd.read_csv("resources/ingest/googleplaystore.csv")

#   Pandas
#   Framework python
#   Pensado para manipulacion de grandes volumenes de datos
#       Dataframes

# Metadata del DF
print(df.shape)
print(df.columns)
print(df.head())

# Installs
# Remover + y ,, convertir a int
df['Installs'] = df['Installs'].str.replace(',', '').str.replace('+', '').str.replace('Free', '0').astype(int)
# Price
# Remover $, convertir a float
price_column = df['Price'].str.replace('$', '')
df['Price'] = pd.to_numeric(price_column, errors='coerce')
# Size
# Remover 'M', 'k', convertir a MB como float
#----------------------------------------------------------------------------------------
# Reemplazar 'Varies with device' por NaN
df['Size'] = df['Size'].replace('Varies with device', np.nan)

# Quitar 'M' y convertir directo
df['Size'] = df['Size'].str.replace('M', '', regex=False)

DIVISOR_TO_GET_MB_FROM_KB = 1024

# Convertir los valores en kB a MB
kb_mask = df['Size'].str.endswith('k', na=False)
df.loc[kb_mask, 'Size'] = df.loc[kb_mask, 'Size'].str.replace('k', '', regex=False)
df.loc[kb_mask, 'Size'] = df.loc[kb_mask, 'Size'].astype(float) / DIVISOR_TO_GET_MB_FROM_KB

# Convertir todo a float (las que ya estaban en MB o eran NaN)
df['Size'] = pd.to_numeric(df['Size'], errors='coerce')
#----------------------------------------------------------------------------------------
# Rating
# Convertir a float, eliminar nulos si es necesario

# Type
# Asegurarse que solo tenga Free, Paid o NaN
df['Type'] = df['Type'].str.replace('0', 'Free')

#Convert Installs field to int to can query it


# Guardar tabla en DuckDB (archivo local)
con = duckdb.connect("apps.duckdb")
con.execute("DROP TABLE IF EXISTS apps")
con.execute("CREATE TABLE IF NOT EXISTS apps AS SELECT * FROM df")

# Consultar desde DuckDB usando SQL
result = con.execute("SELECT Category, COUNT(*) AS total FROM apps GROUP BY Category ORDER BY total DESC").fetchdf()

#   Columns
#   'App', 'Category', 'Rating', 'Reviews', 'Size', 'Installs', 'Type',
#   'Price', 'Content Rating', 'Genres', 'Last Updated', 'Current Ver',
#   'Android Ver'

#Desafío 1 – Apps más pesadas por categoría
#   ¿Cuáles son las categorías con más apps de gran tamaño?
#       Agrupar las aplicaciones por categoría, sumando el tamaño de las aplicaciones que las
#       componen y ordenar decrescientemente


#Desafío 2 – Relación entre rating y precio
#   ¿Las apps más caras tienen mejor rating?
#Desafío 3 – Categorías con mejor puntuación promedio
#   ¿Qué categoría tiene las apps con mejor rating promedio?
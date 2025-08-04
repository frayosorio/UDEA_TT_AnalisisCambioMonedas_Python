import json
import pandas as pd
import matplotlib.pyplot as plt

with open("datos/Cambios Monedas Agrupado.json","r") as archivo:
    datos = json.load(archivo)

registros = []
for moneda, cambios in datos.items():
    for cambio in cambios:
        cambio["Moneda"]=moneda
        registros.append(cambio)

df = pd.DataFrame(registros)

df.info()
print(df.head())
print(df.tail())

df["Fecha"] = pd.to_datetime(df["Fecha"], dayfirst=True, errors="coerce")
df.info()

df.dropna(subset=["Fecha", "Cambio"], inplace=True)
print(df.head())

dfMonedas = df.pivot_table(index="Fecha", columns="Moneda", values="Cambio")
dfMonedas.sort_index(inplace=True)
print(dfMonedas.head(20))

monedas = dfMonedas.columns.to_list()
for moneda in monedas:
    plt.plot(dfMonedas.index, dfMonedas[moneda])
    plt.xlabel("Fecha")
    plt.ylabel(f"Cambios de {moneda}")
    plt.show()

plt.figure(figsize=(14,7))
for moneda in monedas:
    plt.plot(dfMonedas.index, dfMonedas[moneda], label=moneda)
plt.xlabel("Fecha")
plt.ylabel("Cambio")
plt.legend()
plt.show()

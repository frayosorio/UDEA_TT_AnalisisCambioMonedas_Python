import json
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

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
    if moneda=='COP':
        plt.plot(dfMonedas.index, dfMonedas[moneda]/1000, label=f"{moneda}/1000")
    else:
        plt.plot(dfMonedas.index, dfMonedas[moneda], label=moneda)
plt.xlabel("Fecha")
plt.ylabel("Cambio")
plt.legend()
plt.show()

#Correlacion
matrizCorrelacion= dfMonedas.corr(method="pearson")
plt.figure(figsize=(10, 8))
sns.heatmap(
    matrizCorrelacion,
    annot=True,
    cmap="coolwarm",
    cbar_kws={"label": "Coeficiente de Correlación"}
)
plt.show()

monedaAnalisis="COP"
dfMonedas[f"{monedaAnalisis}_MV"] = dfMonedas[monedaAnalisis].rolling(window=100).mean()
print(dfMonedas.head())

plt.figure(figsize=(12,6))
plt.plot(dfMonedas.index, dfMonedas[monedaAnalisis], label=monedaAnalisis)
plt.plot(dfMonedas.index, \
         dfMonedas[f"{monedaAnalisis}_MV"], \
         label=f"{monedaAnalisis} con media movil", \
         linestyle="--"
)
plt.legend()
plt.show()
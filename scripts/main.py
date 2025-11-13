import pandas as pd
import sklearn
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score  

# gerar grafico 
import matplotlib.pyplot as plt

dataCliente = pd.read_csv('Cliente.csv')

dataCompras = pd.read_csv('Compras.csv')

dataProdutos = pd.read_csv('produtos.csv')

dataMerge = pd.merge(dataCliente, dataCompras, on='cliente_id')
dataFinal = pd.merge(dataMerge, dataProdutos, on='produto_id')

dataFinal = dataFinal.dropna()

X = dataFinal.drop('target', axis=1)
y = dataFinal['target']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = RandomForestClassifier()
model.fit(X_train, y_train)

y_pred = model.predict(X_test)

print("Accuracy:", accuracy_score(y_test, y_pred))

#gerar grafico de barras com a importancia das features
importances = model.feature_importances_
plt.figure(figsize=(10, 6))
plt.barh(X.columns, importances)
plt.xlabel("Feature Importance")
plt.title("Feature Importance - Random Forest")
plt.show()
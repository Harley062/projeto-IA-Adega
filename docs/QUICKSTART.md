# Guia de Início Rápido

## Instalação

1. Certifique-se de ter Python 3.8 ou superior instalado

2. Instale as dependências:
```bash
pip install -r requirements.txt
```

## Execução Rápida

### Executar Pipeline Completo

```bash
python pipeline.py
```

Isso irá executar todas as etapas automaticamente:
- Carregar dados
- Análise exploratória
- Feature engineering
- Treinamento de modelos
- Avaliação e visualizações

### Tempo de Execução Esperado

- Pipeline completo: ~2-5 minutos (dependendo do hardware)

## Resultados

Após a execução, verifique:

1. **Logs**: `logs/` - Logs detalhados da execução
2. **Gráficos**: `output/plots/` - Todas as visualizações geradas
3. **Modelos**: `output/models/` - Modelos treinados salvos
4. **Relatórios**: `output/reports/` - Relatórios de avaliação

## Uso Modular (Avançado)

Se você quiser executar apenas partes específicas:

### Apenas Análise Exploratória

```python
from src.data.data_loader import DataLoader
from src.data.eda import ExploratoryAnalysis

# Carregar dados
loader = DataLoader()
loader.load_data()
loader.validate_data()
data = loader.merge_data()
data = loader.clean_data()

# EDA
eda = ExploratoryAnalysis(data)
eda.generate_full_report()
```

### Apenas Treinar Modelos

```python
from src.models.model_trainer import ModelTrainer
from sklearn.model_selection import train_test_split

# Assumindo que você já tem X e y preparados
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

trainer = ModelTrainer()
results = trainer.train_all_models(X_train, y_train, X_test, y_test)
```

### Apenas Visualizações de Negócio

```python
from src.visualization.plots import AdvancedPlotter

plotter = AdvancedPlotter(data)
plotter.generate_business_dashboard()
```

## Principais Visualizações Geradas

1. **missing_values.png** - Análise de valores ausentes
2. **numerical_distributions.png** - Distribuições de variáveis numéricas
3. **categorical_distributions.png** - Distribuições de variáveis categóricas
4. **correlation_matrix.png** - Matriz de correlação
5. **sales_over_time.png** - Vendas ao longo do tempo
6. **top_products.png** - Produtos mais vendidos
7. **customer_segmentation.png** - Segmentação de clientes
8. **wine_analysis.png** - Análise detalhada de vinhos
9. **rfm_analysis.png** - Análise RFM de clientes
10. **model_comparison.png** - Comparação de modelos
11. **confusion_matrix.png** - Matriz de confusão
12. **roc_curve.png** - Curva ROC
13. **feature_importance.png** - Importância das features

## Modelos Treinados

O sistema treina e compara 7 modelos diferentes:

1. Random Forest
2. Gradient Boosting
3. Logistic Regression
4. Decision Tree
5. K-Nearest Neighbors
6. Naive Bayes
7. AdaBoost

O melhor modelo é automaticamente salvo em `output/models/`

## Personalização

Para personalizar configurações, edite [config.yaml](config.yaml) ou [src/utils/config.py](src/utils/config.py)

Parâmetros principais:
- `TEST_SIZE`: Tamanho do conjunto de teste (padrão: 0.2)
- `CV_FOLDS`: Número de folds na validação cruzada (padrão: 5)
- `RANDOM_STATE`: Seed para reprodutibilidade (padrão: 42)

## Solução de Problemas

### Erro: ModuleNotFoundError

Certifique-se de estar no diretório do projeto e que instalou as dependências:
```bash
pip install -r requirements.txt
```

### Erro: FileNotFoundError

Verifique se os arquivos CSV estão no diretório raiz:
- Cliente.csv
- produtos.csv
- Compras.csv

### Warnings sobre delimitadores

Os CSVs usam ponto-e-vírgula (;) como delimitador. Isso é tratado automaticamente pelo DataLoader.

## Próximos Passos

1. Revise os logs em `logs/` para entender o que aconteceu
2. Explore as visualizações em `output/plots/`
3. Leia o relatório de avaliação em `output/reports/`
4. Experimente ajustar parâmetros em `config.yaml`
5. Tente otimizar hiperparâmetros do melhor modelo

## Suporte

Para problemas ou dúvidas, revise:
- [README.md](README.md) - Documentação completa
- Logs em `logs/` - Informações detalhadas de execução

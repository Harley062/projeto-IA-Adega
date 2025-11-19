# Sistema de Análise de Dados - Adega

Sistema robusto e completo de análise de dados e machine learning para uma adega, com foco em previsão de cancelamento de assinaturas e análise de comportamento de clientes.

## Características Principais

- **🌐 Dashboard Web Interativo** com Streamlit para visualização em tempo real
- **Análise Exploratória de Dados (EDA)** completa e automatizada
- **Feature Engineering** avançado com criação de features temporais, agregadas e de interação
- **Treinamento de múltiplos modelos** de ML com validação cruzada
- **Avaliação detalhada** com métricas abrangentes (Accuracy, Precision, Recall, F1, ROC-AUC)
- **Visualizações profissionais** de dados de negócio e métricas de modelo
- **Sistema de logging** completo para rastreamento
- **Arquitetura modular** e escalável

## Estrutura do Projeto

```
projeto IA Adega/
│
├── src/                            # Código fonte
│   ├── data/
│   │   ├── data_loader.py          # Carregamento e validação de dados
│   │   ├── eda.py                  # Análise exploratória
│   │   └── feature_engineering.py  # Engenharia de features
│   │
│   ├── models/
│   │   ├── model_trainer.py        # Treinamento de modelos
│   │   └── model_evaluation.py     # Avaliação de modelos
│   │
│   ├── visualization/
│   │   └── plots.py                # Visualizações de negócio
│   │
│   └── utils/
│       ├── logger.py               # Sistema de logging
│       └── config.py               # Configurações
│
├── data/                           # Dados do projeto
│   ├── Cliente.csv                 # Dados de clientes
│   ├── produtos.csv                # Dados de produtos/vinhos
│   ├── Compras.csv                 # Dados de compras
│   └── exemplo_predicao_lote.csv   # Exemplo para predições em lote
│
├── scripts/                        # Scripts executáveis
│   ├── pipeline.py                 # Pipeline principal
│   ├── main.py                     # Script original (legado)
│   ├── export_processed_data.py    # Exportação de dados processados
│   ├── test_system.py              # Testes do sistema
│   └── replace_emojis.py           # Utilitário
│
├── docs/                           # Documentação
│   ├── DASHBOARD_README.md         # Guia do dashboard
│   ├── GUIA_COMPLETO.md            # Guia completo do sistema
│   ├── QUICKSTART.md               # Início rápido
│   └── ...                         # Outras documentações
│
├── output/                         # Saídas geradas
│   ├── models/                     # Modelos treinados salvos
│   ├── plots/                      # Gráficos e visualizações
│   └── reports/                    # Relatórios de avaliação
│
├── assets/                         # Recursos estáticos
│   └── adega.png                   # Logo da adega
│
├── logs/                           # Logs de execução
│
├── app.py                          # Dashboard Streamlit
├── pages_prediction.py             # Páginas de predição
├── requirements.txt                # Dependências
├── config.yaml                     # Configurações em YAML
├── run_dashboard.bat               # Atalho para iniciar dashboard
└── README.md                       # Este arquivo

```

## Instalação

1. Clone o repositório ou navegue até o diretório do projeto

2. Crie e ative o ambiente virtual:
```bash
# Criar ambiente virtual
python -m venv venv

# Ativar (Windows)
venv\Scripts\activate

# Ativar (Linux/Mac)
source venv/bin/activate
```

3. Instale as dependências:
```bash
pip install -r requirements.txt
```

## Uso

### 🌐 Dashboard Web (Recomendado)

**Iniciar o Dashboard Interativo:**

```bash
streamlit run app.py
```

O dashboard abrirá automaticamente em `http://localhost:8501` com:
- 📊 Visualização interativa de dados
- 📈 Gráficos dinâmicos e filtros
- 🤖 Métricas de modelos em tempo real
- 💼 Insights de negócio
- ⚙️ Executar pipeline direto do navegador

**Para mais detalhes:** [DASHBOARD_README.md](docs/DASHBOARD_README.md)

### 💻 Executar Pipeline Completo (CLI)

Para executar o pipeline completo de análise via linha de comando:

```bash
python scripts/pipeline.py
```

O pipeline irá:
1. Carregar e validar os dados
2. Realizar análise exploratória completa
3. Criar features avançadas
4. Treinar múltiplos modelos de ML
5. Avaliar e comparar os modelos
6. Gerar visualizações e relatórios

### Resultados

Após a execução, os resultados estarão disponíveis em:

- **output/models/** - Modelos treinados salvos em formato .pkl
- **output/plots/** - Todos os gráficos e visualizações geradas
- **output/reports/** - Relatórios detalhados de avaliação
- **logs/** - Logs de execução com timestamps

## Módulos Principais

### 1. DataLoader
Responsável por carregar, validar e fazer merge dos dados de clientes, produtos e compras.

```python
from src.data.data_loader import DataLoader

loader = DataLoader(data_dir=".")
clientes, produtos, compras = loader.load_data()
data_merged = loader.merge_data()
```

### 2. ExploratoryAnalysis
Realiza análise exploratória completa com visualizações.

```python
from src.data.eda import ExploratoryAnalysis

eda = ExploratoryAnalysis(data)
eda.generate_full_report()
```

### 3. FeatureEngineer
Cria features temporais, agregadas e de interação.

```python
from src.data.feature_engineering import FeatureEngineer

engineer = FeatureEngineer()
data_with_features = engineer.engineer_all_features(data)
```

### 4. ModelTrainer
Treina múltiplos modelos com validação cruzada.

```python
from src.models.model_trainer import ModelTrainer

trainer = ModelTrainer()
results = trainer.train_all_models(X_train, y_train, X_test, y_test)
```

### 5. ModelEvaluator
Avalia modelos com métricas detalhadas e visualizações.

```python
from src.models.model_evaluation import ModelEvaluator

evaluator = ModelEvaluator()
metrics = evaluator.calculate_metrics(y_true, y_pred, y_pred_proba)
```

## Modelos Suportados

- Random Forest
- Gradient Boosting
- Logistic Regression
- Decision Tree
- K-Nearest Neighbors (KNN)
- Naive Bayes
- AdaBoost

## Métricas de Avaliação

- Accuracy
- Precision
- Recall
- F1-Score
- ROC-AUC
- Average Precision
- Matriz de Confusão
- Curva ROC
- Curva Precision-Recall

## Visualizações Geradas

### Análise Exploratória
- Distribuições de variáveis numéricas
- Distribuições de variáveis categóricas
- Matriz de correlação
- Boxplots para detecção de outliers
- Valores ausentes

### Análise de Negócio
- Vendas ao longo do tempo
- Top produtos mais vendidos
- Segmentação de clientes por cidade
- Análise de vinhos (país, safra, tipo de uva)
- Análise RFM (Recency, Frequency, Monetary)

### Avaliação de Modelos
- Matriz de confusão
- Curva ROC
- Curva Precision-Recall
- Comparação de modelos
- Importância de features

## Configuração

As configurações podem ser ajustadas em [config.yaml](config.yaml) ou através da classe `Config` em [src/utils/config.py](src/utils/config.py):

- Tamanho do conjunto de teste
- Número de folds para validação cruzada
- Método de normalização
- Features a serem criadas
- Parâmetros de visualização

## Requisitos

- Python 3.8+
- pandas >= 2.0.0
- numpy >= 1.24.0
- scikit-learn >= 1.3.0
- matplotlib >= 3.7.0
- seaborn >= 0.12.0
- joblib >= 1.3.0

## Logs

O sistema mantém logs detalhados de todas as operações em `logs/`. Cada execução cria um novo arquivo de log com timestamp.

## Melhorias em Relação ao Código Original

1. **Arquitetura Modular**: Código organizado em módulos especializados
2. **Validação de Dados**: Verificação de integridade e consistência
3. **Feature Engineering**: Criação automática de features avançadas
4. **Múltiplos Modelos**: Treinamento e comparação de 7 modelos diferentes
5. **Validação Cruzada**: Avaliação mais robusta com K-Fold
6. **Métricas Abrangentes**: Muito além de apenas accuracy
7. **Visualizações Profissionais**: Dashboard completo de análises
8. **Sistema de Logging**: Rastreamento completo de operações
9. **Configuração Flexível**: Parâmetros centralizados e editáveis
10. **Tratamento de Erros**: Sistema robusto de exception handling
11. **Salvamento de Modelos**: Persistência para uso futuro
12. **Relatórios Automatizados**: Documentação automática dos resultados

## Próximos Passos Sugeridos

- [ ] Adicionar suporte para deep learning (TensorFlow/PyTorch)
- [ ] Implementar AutoML para otimização automática
- [ ] Criar API REST para servir predições
- [ ] Adicionar testes unitários
- [ ] Implementar CI/CD
- [ ] Adicionar dashboard interativo (Streamlit/Dash)
- [ ] Integração com banco de dados
- [ ] Sistema de monitoramento de modelo em produção

## Licença

Projeto educacional - Livre para uso e modificação

## Autor

Sistema desenvolvido para análise de dados de adega com foco em previsão de churn de clientes.

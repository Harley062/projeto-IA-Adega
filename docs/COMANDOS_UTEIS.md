# Comandos Úteis - Sistema de Análise de Dados

## Instalação e Setup

### Instalar dependências
```bash
pip install -r requirements.txt
```

### Verificar instalação
```bash
python -c "import pandas; import sklearn; import matplotlib; print('✓ Todas as dependências instaladas')"
```

## Execução do Sistema

### Pipeline Completo (Recomendado)
```bash
python pipeline.py
```
Executa todas as etapas: carregamento, EDA, feature engineering, treinamento e avaliação.

### Teste do Sistema
```bash
python test_system.py
```
Executa testes rápidos para verificar se tudo está funcionando.

## Uso Individual dos Módulos

### 1. Apenas Carregar e Validar Dados
```python
from src.data.data_loader import DataLoader

loader = DataLoader()
clientes, produtos, compras = loader.load_data()
loader.validate_data()
data = loader.merge_data()
data = loader.clean_data()

# Ver resumo
print(loader.get_data_summary())
```

### 2. Apenas Análise Exploratória (EDA)
```python
from src.data.data_loader import DataLoader
from src.data.eda import ExploratoryAnalysis

# Carregar dados
loader = DataLoader()
loader.load_data()
data = loader.merge_data()

# EDA
eda = ExploratoryAnalysis(data)
eda.generate_full_report()
```

### 3. Apenas Feature Engineering
```python
from src.data.data_loader import DataLoader
from src.data.feature_engineering import FeatureEngineer

# Carregar dados
loader = DataLoader()
loader.load_data()
data = loader.merge_data()

# Feature engineering
engineer = FeatureEngineer()
data_with_features = engineer.engineer_all_features(data)
print(f"Total de features: {len(data_with_features.columns)}")
```

### 4. Apenas Treinar Modelos
```python
from src.models.model_trainer import ModelTrainer
from sklearn.model_selection import train_test_split

# Assumindo X e y já preparados
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

trainer = ModelTrainer()
results = trainer.train_all_models(X_train, y_train, X_test, y_test)

print(f"Melhor modelo: {trainer.best_model_name}")
print(f"Accuracy: {trainer.best_score:.4f}")
```

### 5. Apenas Validação Cruzada
```python
from src.models.model_trainer import ModelTrainer

trainer = ModelTrainer()
cv_results = trainer.cross_validate_models(X, y, cv=5)

for model_name, results in cv_results.items():
    print(f"{model_name}: {results['mean_score']:.4f} ± {results['std_score']:.4f}")
```

### 6. Otimizar Hiperparâmetros
```python
from src.models.model_trainer import ModelTrainer

trainer = ModelTrainer()

# Otimizar Random Forest
best_model, best_params = trainer.hyperparameter_tuning(
    'Random Forest',
    X_train,
    y_train,
    cv=3
)

print(f"Melhores parâmetros: {best_params}")
```

### 7. Carregar Modelo Salvo
```python
from src.models.model_trainer import ModelTrainer

trainer = ModelTrainer()
model = trainer.load_model('best_model_Random_Forest.pkl')

# Fazer predições
predictions = model.predict(X_new)
```

### 8. Visualizações de Negócio
```python
from src.visualization.plots import AdvancedPlotter

plotter = AdvancedPlotter(data)
plotter.generate_business_dashboard()

# Ou gráficos individuais
plotter.plot_sales_over_time()
plotter.plot_top_products()
plotter.plot_customer_segmentation()
plotter.plot_wine_analysis()
plotter.plot_rfm_analysis()
```

### 9. Avaliar Modelo
```python
from src.models.model_evaluation import ModelEvaluator

evaluator = ModelEvaluator()

# Calcular métricas
metrics = evaluator.calculate_metrics(y_test, y_pred, y_pred_proba)
evaluator.print_metrics(metrics)

# Gerar visualizações
evaluator.plot_confusion_matrix(y_test, y_pred)
evaluator.plot_roc_curve(y_test, y_pred_proba)
evaluator.plot_precision_recall_curve(y_test, y_pred_proba)

# Salvar relatório
report = evaluator.generate_classification_report(y_test, y_pred)
evaluator.save_evaluation_report(metrics, report)
```

## Personalização

### Modificar Configurações
Edite `config.yaml` ou `src/utils/config.py`:

```python
from src.utils.config import Config

config = Config()
config.TEST_SIZE = 0.3  # Mudar para 30% de teste
config.CV_FOLDS = 10    # Usar 10 folds
config.RANDOM_STATE = 123  # Mudar seed
```

### Adicionar Novo Modelo
Edite `src/models/model_trainer.py`:

```python
def get_models(self) -> Dict[str, Any]:
    models = {
        # ... modelos existentes ...
        'XGBoost': XGBClassifier(random_state=self.random_state),
        'LightGBM': LGBMClassifier(random_state=self.random_state),
    }
    return models
```

### Criar Feature Customizada
Edite `src/data/feature_engineering.py`:

```python
def create_custom_features(self, data: pd.DataFrame) -> pd.DataFrame:
    df = data.copy()

    # Sua lógica aqui
    df['minha_feature'] = df['coluna1'] * df['coluna2']

    return df
```

## Análise de Resultados

### Ver Logs
```bash
# Ver último log
ls -lt logs/ | head -2

# Ler log
cat logs/adega_ml_YYYYMMDD_HHMMSS.log

# Buscar erros
grep -i "error" logs/adega_ml_*.log
```

### Ver Gráficos Gerados
```bash
# Linux/Mac
open output/plots/

# Windows
explorer output\plots
```

### Ver Relatórios
```bash
cat output/reports/evaluation_report.txt
```

### Verificar Modelos Salvos
```bash
ls -lh output/models/
```

## Troubleshooting

### Erro: ModuleNotFoundError
```bash
# Instalar dependências
pip install -r requirements.txt

# Verificar instalação
pip list | grep -E "pandas|sklearn|matplotlib"
```

### Erro: FileNotFoundError (CSVs)
```bash
# Verificar se arquivos existem
ls -l *.csv

# Devem existir:
# - Cliente.csv
# - produtos.csv
# - Compras.csv
```

### Erro: Memory Error
```python
# Reduzir tamanho dos dados ou usar amostragem
data_sample = data.sample(frac=0.5, random_state=42)
```

### Limpar Outputs
```bash
# Limpar plots
rm output/plots/*.png

# Limpar modelos
rm output/models/*.pkl

# Limpar relatórios
rm output/reports/*.txt

# Limpar logs
rm logs/*.log
```

## Análise Rápida (One-Liners)

### Contar registros
```python
python -c "from src.data.data_loader import DataLoader; l=DataLoader(); l.load_data(); print(f'Total: {len(l.merge_data())}')"
```

### Ver colunas disponíveis
```python
python -c "from src.data.data_loader import DataLoader; l=DataLoader(); l.load_data(); d=l.merge_data(); print(list(d.columns))"
```

### Estatísticas rápidas
```python
python -c "from src.data.data_loader import DataLoader; l=DataLoader(); l.load_data(); d=l.merge_data(); print(d.describe())"
```

## Jupyter Notebook

### Criar notebook para experimentação
```python
# Em uma célula Jupyter

import sys
sys.path.append('src')

from data.data_loader import DataLoader
from data.eda import ExploratoryAnalysis
from models.model_trainer import ModelTrainer

# Seus experimentos aqui
```

## Produção

### Fazer Predição em Novos Dados
```python
from src.models.model_trainer import ModelTrainer
import pandas as pd

# Carregar modelo
trainer = ModelTrainer()
model = trainer.load_model('best_model_Random_Forest.pkl')

# Carregar novos dados
novos_dados = pd.read_csv('novos_clientes.csv')

# Preparar dados (aplicar mesmo preprocessing)
# ... (feature engineering, encoding, etc.)

# Predizer
predictions = model.predict(novos_dados_preparados)
probabilities = model.predict_proba(novos_dados_preparados)

# Salvar resultados
novos_dados['predicao_churn'] = predictions
novos_dados['probabilidade_churn'] = probabilities[:, 1]
novos_dados.to_csv('predicoes.csv', index=False)
```

## Performance

### Medir tempo de execução
```bash
time python pipeline.py
```

### Profile de código
```python
import cProfile
import pstats

cProfile.run('pipeline.run_full_pipeline()', 'stats.prof')
stats = pstats.Stats('stats.prof')
stats.sort_stats('cumulative')
stats.print_stats(10)
```

## Backup

### Fazer backup completo
```bash
# Criar arquivo tar.gz com data
tar -czf backup_$(date +%Y%m%d).tar.gz \
  --exclude=venv \
  --exclude=__pycache__ \
  --exclude=logs \
  .
```

## Automação

### Agendar execução diária (Linux/Mac)
```bash
# Editar crontab
crontab -e

# Adicionar linha (executa todo dia às 3h da manhã)
0 3 * * * cd /path/to/projeto && python pipeline.py
```

### Agendar execução diária (Windows)
Use o Agendador de Tarefas do Windows para executar:
```
python C:\path\to\projeto\pipeline.py
```

## Dicas Úteis

### Executar em background
```bash
nohup python pipeline.py > execution.log 2>&1 &
```

### Limitar uso de CPU
```python
# Modificar n_jobs nos modelos
model = RandomForestClassifier(n_jobs=2)  # Usar apenas 2 cores
```

### Ver progresso em tempo real
```bash
tail -f logs/adega_ml_*.log
```

---

**Dica:** Mantenha este arquivo como referência rápida para operações comuns!

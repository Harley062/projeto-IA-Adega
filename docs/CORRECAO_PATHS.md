# Correção de Caminhos - Projeto Reorganizado

## Problema Resolvido

Após reorganizar o projeto, os caminhos de importação precisaram ser ajustados.

## ✅ Correções Aplicadas

### 1. Pipeline (scripts/pipeline.py)

**Antes:**
```python
sys.path.append(str(Path(__file__).parent / 'src'))
```

**Depois:**
```python
# Pipeline está em scripts/, src está na raiz
sys.path.append(str(Path(__file__).parent.parent / 'src'))
```

### 2. Configuração (src/utils/config.py)

**Antes:**
```python
DATA_DIR: str = "."
```

**Depois:**
```python
DATA_DIR: str = "data"
```

### 3. Data Loader (src/data/data_loader.py)

**Mantido:**
```python
self.clientes = pd.read_csv(
    self.data_dir / 'Cliente.csv',  # Sem 'data/' redundante
    delimiter=';',
    encoding='utf-8'
)
```

**Explicação:** Como `DATA_DIR` já é `"data"`, não precisa de `'data/'` adicional.

## Como Executar Agora

### 1. Ativar Ambiente Virtual

**Windows:**
```bash
venv\Scripts\activate
```

**Linux/Mac:**
```bash
source venv/bin/activate
```

### 2. Executar Pipeline

```bash
python scripts/pipeline.py
```

### 3. Executar Dashboard

```bash
streamlit run app.py
```

ou use o atalho:
```bash
run_dashboard.bat
```

## Estrutura de Caminhos

```
projeto IA Adega/                    (raiz)
│
├── scripts/
│   └── pipeline.py                  → importa de ../src/
│
├── src/
│   ├── data/
│   │   └── data_loader.py           → carrega de data/ (configurado em config)
│   └── utils/
│       └── config.py                → DATA_DIR = "data"
│
├── data/
│   ├── Cliente.csv
│   ├── produtos.csv
│   └── Compras.csv
│
└── app.py                           → importa de src/

```

## Fluxo de Importação

1. **scripts/pipeline.py**
   - Adiciona `../src` ao sys.path
   - Importa: `from data.data_loader import DataLoader`
   - Localização real: `src/data/data_loader.py`

2. **src/utils/config.py**
   - Define: `DATA_DIR = "data"`
   - Caminho relativo à raiz do projeto

3. **src/data/data_loader.py**
   - Recebe: `DataLoader(data_dir="data")`
   - Carrega: `data_dir / 'Cliente.csv'` → `data/Cliente.csv`

## Verificação

Para verificar se tudo está correto:

```bash
# 1. Verificar se ambiente virtual está ativo
which python  # Linux/Mac
where python  # Windows
# Deve mostrar: .../venv/...

# 2. Verificar se módulos estão instalados
python -c "import pandas; print('OK')"

# 3. Testar imports do projeto
python -c "import sys; from pathlib import Path; sys.path.append('src'); from data.data_loader import DataLoader; print('OK')"

# 4. Verificar se arquivos de dados existem
ls data/Cliente.csv
ls data/produtos.csv
ls data/Compras.csv
```

## Troubleshooting

### Erro: "No module named 'pandas'"
**Solução:** Ative o ambiente virtual
```bash
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac
```

### Erro: "No module named 'data'"
**Solução:** Já corrigido! O pipeline agora adiciona o caminho correto.

### Erro: "FileNotFoundError: data/Cliente.csv"
**Solução:** Execute o script a partir da raiz do projeto:
```bash
cd "c:\Users\harle\Downloads\projeto IA Adega"
python scripts/pipeline.py
```

### Erro no app.py: "Não foi possível carregar os dados"
**Solução:** Execute o pipeline primeiro para gerar os dados processados:
```bash
python scripts/pipeline.py
```

## Arquivos Modificados

1. ✅ `scripts/pipeline.py` - Linha 8: path corrigido
2. ✅ `src/utils/config.py` - Linha 13: DATA_DIR = "data"
3. ✅ `src/data/data_loader.py` - Linhas 35-47: caminhos sem redundância
4. ✅ `app.py` - Linha 14: já estava correto

---

**Última atualização:** 13 de novembro de 2025
**Status:** ✅ Todos os caminhos corrigidos

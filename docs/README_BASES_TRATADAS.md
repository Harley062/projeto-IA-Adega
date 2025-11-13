# 📊 Bases de Dados Tratadas - Sistema de Análise Adega Bom Sabor

## Contexto do Sistema

A **Adega Bom Sabor** de Goiás enfrenta desafios importantes na gestão de clientes e vendas, especialmente no clube de assinaturas. Este Sistema de Apoio à Decisão (SAD) híbrido foi desenvolvido para ajudar a empresa a:

### Desafios Principais
- **Retenção de Assinantes**: Dificuldade para reter assinantes do clube
- **Identificação de Churn**: Detectar quem está próximo de cancelar
- **Reativação**: Entender quem pode voltar a comprar
- **Recomendações**: Sugerir vinhos adequados para cada perfil

### Abordagens do SAD

1. **Análise Descritiva**: Entender o presente
   - Perfil de clientes
   - Produtos mais vendidos
   - Níveis de engajamento
   - Comportamento de compra

2. **Análise Preditiva**: Prever o futuro
   - Risco de cancelamento (churn)
   - Chance de reativação
   - Preferências por grupo

3. **Análise Prescritiva**: Recomendar ações
   - Enviar cupons para clientes em risco
   - Sugerir vinhos alinhados ao perfil
   - Ações estratégicas personalizadas

## Arquivos Gerados

### 📁 Arquivos Principais

#### 1. **data_processed_complete.csv**
- **Descrição**: Base de dados completa com features + target
- **Dimensões**: 21 registros × 41 colunas
- **Uso**: Análise completa e treinamento de modelos
- **Formato**: CSV com separador `;` e encoding UTF-8

#### 2. **data_processed_features.csv**
- **Descrição**: Apenas features (variáveis independentes X)
- **Dimensões**: 21 registros × 40 colunas
- **Uso**: Input para predições
- **Características**: Todas as variáveis exceto o target

#### 3. **data_processed_target.csv**
- **Descrição**: Apenas target (variável dependente y)
- **Dimensões**: 21 registros
- **Variável**: `cancelou_assinatura` (0 = Não, 1 = Sim)
- **Distribuição**:
  - Não cancelou: 11 clientes (52.4%)
  - Cancelou: 10 clientes (47.6%)

#### 4. **data_processed_train.csv**
- **Descrição**: Base de treino (80% dos dados)
- **Dimensões**: 16 registros × 41 colunas
- **Uso**: Treinamento de modelos de ML
- **Split**: Estratificado por target

#### 5. **data_processed_test.csv**
- **Descrição**: Base de teste (20% dos dados)
- **Dimensões**: 5 registros × 41 colunas
- **Uso**: Validação e teste de modelos
- **Split**: Estratificado por target

#### 6. **data_processed_info.txt**
- **Descrição**: Documentação detalhada das features
- **Conteúdo**:
  - Lista completa de todas as 40 features
  - Tipos de dados de cada coluna
  - Quantidade de valores nulos e únicos
  - Distribuição do target

## 📋 Features Criadas (40 total)

### Identificadores (3)
1. `compra_id` - ID único da compra
2. `cliente_id` - ID único do cliente
3. `produto_id` - ID único do produto

### Dados Transacionais (2)
4. `valor` - Valor da compra em R$
5. `quantidade` - Quantidade de itens comprados

### Dados do Cliente (5)
6. `nome` - Nome do cliente (codificado)
7. `idade` - Idade do cliente
8. `cidade` - Cidade do cliente (codificada)
9. `pontuacao_engajamento` - Score de engajamento (0-10)
10. `assinante_clube` - Se é assinante do clube (0 = Não, 1 = Sim)

### Dados do Produto (4)
11. `nome_produto` - Nome do vinho (codificado)
12. `pais` - País de origem do vinho (codificado)
13. `safra` - Ano da safra
14. `tipo_uva` - Tipo de uva (codificado)

### Features Temporais (10)
15. `ano` - Ano da compra (2023)
16. `mes` - Mês da compra (1-12)
17. `dia` - Dia do mês (1-31)
18. `dia_semana` - Dia da semana (0-6)
19. `trimestre` - Trimestre (1-4)
20. `semana_ano` - Semana do ano (1-52)
21. `mes_sin` - Componente seno do mês (cíclica)
22. `mes_cos` - Componente cosseno do mês (cíclica)
23. `dia_semana_sin` - Componente seno do dia da semana (cíclica)
24. `dia_semana_cos` - Componente cosseno do dia da semana (cíclica)

### Features Agregadas - RFM (11)
25. `total_gasto` - Total gasto pelo cliente
26. `ticket_medio` - Valor médio das compras
27. `std_gasto` - Desvio padrão dos gastos
28. `num_compras` - Número de compras realizadas
29. `total_itens` - Total de itens comprados
30. `media_itens` - Média de itens por compra
31. `preco_medio_produto` - Preço médio do produto
32. `popularidade_produto` - Número de vendas do produto
33. `total_vendido_produto` - Quantidade total vendida do produto
34. `recencia` - Dias desde a última compra
35. `frequencia` - Frequência de compras
36. `valor_total` - Valor monetário total (RFM)

### Features de Interação (4)
37. `valor_por_unidade` - Valor dividido pela quantidade
38. `engajamento_por_idade` - Engajamento normalizado pela idade
39. `engajamento_x_idade` - Interação entre engajamento e idade
40. `valor_por_idade` - Valor normalizado pela idade

### Target (1)
41. `cancelou_assinatura` - Se o cliente cancelou (0 = Não, 1 = Sim)

## 🔄 Processo de Tratamento

### 1. Carregamento de Dados Brutos
- **Origem**: 3 tabelas CSV (Cliente.csv, produtos.csv, Compras.csv)
- **Separador**: `;` (ponto e vírgula)
- **Encoding**: UTF-8

### 2. Validação e Limpeza
- Verificação de valores nulos
- Remoção de registros inválidos
- Conversão de tipos de dados

### 3. Merge de Tabelas
- Join entre Compras, Clientes e Produtos
- Criação de dataset unificado

### 4. Feature Engineering
- **Temporais**: Extração de componentes de data/hora
- **Agregadas**: Cálculos de RFM (Recency, Frequency, Monetary)
- **Interação**: Combinações de variáveis existentes
- **Cíclicas**: Transformações trigonométricas para sazonalidade

### 5. Codificação
- **Label Encoding**: Variáveis categóricas → números
- Variáveis codificadas: nome, cidade, nome_produto, pais, tipo_uva, assinante_clube

### 6. Remoção de Colunas
- Coluna `data_compra` removida (já extraídas features temporais)
- Colunas datetime removidas

### 7. Split Treino/Teste
- **Proporção**: 80% treino / 20% teste
- **Método**: Estratificado (mantém proporção do target)
- **Random State**: 42 (reprodutibilidade)

## 📊 Estatísticas da Base

### Dimensões
- **Registros**: 21 clientes/compras
- **Features**: 40 variáveis independentes
- **Target**: 1 variável dependente

### Distribuição do Target
- **Classe 0** (Não cancelou): 11 registros (52.4%)
- **Classe 1** (Cancelou): 10 registros (47.6%)
- **Balanceamento**: Relativamente equilibrado

### Qualidade dos Dados
- **Valores Nulos**: Apenas em `std_gasto` (21 nulos)
- **Valores Únicos**: Alto para features importantes
- **Tipos de Dados**: Corretos após tratamento

## 🎯 Como Usar as Bases

### Para Análise Exploratória
```python
import pandas as pd

# Carregar base completa
df = pd.read_csv('data_processed_complete.csv', sep=';')

# Análise descritiva
print(df.describe())
print(df.info())
```

### Para Treinamento de Modelos
```python
# Carregar split treino/teste
train = pd.read_csv('data_processed_train.csv', sep=';')
test = pd.read_csv('data_processed_test.csv', sep=';')

X_train = train.drop('cancelou_assinatura', axis=1)
y_train = train['cancelou_assinatura']

X_test = test.drop('cancelou_assinatura', axis=1)
y_test = test['cancelou_assinatura']
```

### Para Predições
```python
# Carregar apenas features
X = pd.read_csv('data_processed_features.csv', sep=';')

# Fazer predições
predictions = model.predict(X)
```

## 🚀 Próximos Passos

1. **Análise Exploratória**: Use `data_processed_complete.csv`
2. **Treinamento**: Use `data_processed_train.csv`
3. **Validação**: Use `data_processed_test.csv`
4. **Predições**: Use `data_processed_features.csv`
5. **Dashboard**: Integre as bases no sistema web

## 📝 Observações Importantes

- **Separador**: Todos os CSVs usam `;` (ponto e vírgula)
- **Encoding**: UTF-8 (suporta acentuação)
- **Reprodutibilidade**: Random state = 42
- **Estratificação**: Target balanceado no split
- **Feature Engineering**: Idêntico ao pipeline de treinamento

## 📞 Suporte

Para dúvidas sobre a estrutura das bases ou processo de tratamento:
1. Consulte [data_processed_info.txt](data_processed_info.txt)
2. Revise [export_processed_data.py](export_processed_data.py)
3. Veja logs em: `logs/export_data_*.log`

---

**Gerado em**: 2025-11-12
**Sistema**: Adega Bom Sabor - SAD Híbrido
**Versão**: 1.0.0

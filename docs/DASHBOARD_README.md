# 🍷 Dashboard Web - Sistema de Análise de Dados da Adega

Dashboard interativo construído com Streamlit para visualização e análise de dados em tempo real.

## 📋 Índice

- [Instalação](#instalação)
- [Como Usar](#como-usar)
- [Funcionalidades](#funcionalidades)
- [Páginas do Dashboard](#páginas-do-dashboard)
- [Troubleshooting](#troubleshooting)

## 🚀 Instalação

### 1. Instalar Dependências

Primeiro, instale as novas dependências necessárias para o dashboard:

```bash
pip install streamlit plotly Pillow
```

Ou instale tudo de uma vez:

```bash
pip install -r requirements.txt
```

### 2. Executar o Pipeline (Primeira Vez)

Antes de usar o dashboard, você precisa executar o pipeline para gerar os dados e modelos:

```bash
python pipeline.py
```

Isso irá:
- ✅ Processar os dados
- ✅ Treinar os modelos
- ✅ Gerar visualizações
- ✅ Criar relatórios

## 🎯 Como Usar

### Iniciar o Dashboard

Execute o seguinte comando:

```bash
streamlit run app.py
```

O dashboard será aberto automaticamente no seu navegador em:
- **URL Local**: http://localhost:8501
- **URL de Rede**: http://[seu-ip]:8501

### Atalhos de Teclado

- `Ctrl + C` - Parar o servidor
- `R` - Recarregar o dashboard
- `C` - Limpar cache

## ✨ Funcionalidades

### 1. **Dashboard Principal** 🏠
- Visão geral das métricas chave
- Gráficos interativos de vendas
- Filtros dinâmicos de dados
- Tabela de dados completa

### 2. **Análise Exploratória** 📊
- Distribuições de variáveis numéricas e categóricas
- Matriz de correlação
- Detecção de outliers com boxplots
- Análise temporal de vendas

### 3. **Modelos e Predições** 🤖
- Métricas de performance do modelo
- Matriz de confusão
- Curvas ROC e Precision-Recall
- Comparação entre modelos
- Importância das features

### 4. **Insights de Negócio** 💼
- Análise de produtos mais vendidos
- Segmentação de clientes
- Análise RFM (Recency, Frequency, Monetary)
- Recomendações estratégicas

### 5. **Configurações** ⚙️
- Executar pipeline direto do dashboard
- Visualizar arquivos gerados
- Informações do sistema

## 📱 Páginas do Dashboard

### 🏠 Dashboard Principal

**Métricas Principais:**
- Total de Registros
- Clientes Únicos
- Produtos Cadastrados
- Total de Vendas

**Gráficos Interativos:**
- Distribuição de vendas (histograma)
- Vendas por cidade (gráfico de barras)

**Filtros Disponíveis:**
- Filtrar por cidade
- Filtrar por assinante do clube
- Faixa de valor de compra

**Tabela de Dados:**
- Visualização completa dos dados
- Filtros aplicados em tempo real
- Exportação possível

### 📊 Análise Exploratória

**4 Abas de Análise:**

1. **Distribuições**
   - Variáveis numéricas
   - Variáveis categóricas

2. **Correlações**
   - Matriz de correlação entre variáveis
   - Identifica relações entre features

3. **Outliers**
   - Boxplots para detecção
   - Identifica valores anormais

4. **Análise Temporal**
   - Vendas ao longo do tempo
   - Identifica sazonalidade

### 🤖 Modelos e Predições

**3 Abas:**

1. **Performance**
   - Relatório completo de métricas
   - Matriz de confusão
   - Curva ROC
   - Curva Precision-Recall
   - Comparação entre todos os modelos

2. **Predições**
   - Fazer predições em novos dados
   - Upload de CSV
   - Resultados em tempo real

3. **Análise do Modelo**
   - Importância das features
   - Quais variáveis são mais importantes
   - Insights para feature engineering

### 💼 Insights de Negócio

**4 Abas:**

1. **Análise de Produtos**
   - Top produtos mais vendidos
   - Análise por país, safra, tipo de uva
   - Oportunidades de estoque

2. **Segmentação de Clientes**
   - Segmentação por cidade
   - Assinantes vs Não assinantes
   - Métricas por segmento

3. **Análise RFM**
   - Recency: Quão recente foi a última compra
   - Frequency: Frequência de compras
   - Monetary: Valor total gasto
   - Identifica clientes VIP

4. **Recomendações**
   - Insights automáticos
   - Taxa de churn
   - Ações recomendadas
   - Estratégias de negócio

### ⚙️ Configurações

**Funcionalidades:**
- Executar pipeline completo direto do dashboard
- Visualizar modelos treinados
- Ver quantidade de visualizações geradas
- Informações de versão do sistema

## 🎨 Recursos Visuais

### Gráficos Interativos (Plotly)
- **Zoom**: Clique e arraste
- **Pan**: Shift + clique e arraste
- **Reset**: Duplo clique
- **Hover**: Informações ao passar o mouse
- **Download**: Botão de câmera para salvar

### Filtros Dinâmicos
- Filtros são aplicados em tempo real
- Métricas atualizam automaticamente
- Tabelas respondem instantaneamente

## 📊 Métricas Disponíveis

### Modelo de ML
- **Accuracy**: Precisão geral
- **Precision**: Precisão por classe
- **Recall**: Taxa de acerto
- **F1-Score**: Média harmônica
- **ROC-AUC**: Área sob a curva ROC
- **Average Precision**: Precisão média

### Negócio
- **Total de Vendas**: Soma de todas as vendas
- **Ticket Médio**: Valor médio por compra
- **Taxa de Churn**: % de cancelamentos
- **Clientes Ativos**: Total de clientes
- **Produtos Top**: Mais vendidos

## 🔄 Atualizando Dados

### Opção 1: Via Dashboard
1. Vá em **Configurações** ⚙️
2. Clique em **Executar Pipeline Completo**
3. Aguarde a conclusão
4. Dashboard será atualizado automaticamente

### Opção 2: Via Terminal
```bash
# Executar pipeline
python pipeline.py

# Reiniciar dashboard (se já estiver rodando)
# O Streamlit detecta mudanças automaticamente
```

## 🎯 Casos de Uso

### 1. Análise Diária
```
1. Abrir dashboard
2. Verificar Dashboard Principal
3. Revisar métricas do dia
4. Identificar anomalias
```

### 2. Reunião Semanal
```
1. Ir em Insights de Negócio
2. Revisar Top Produtos
3. Analisar RFM
4. Preparar ações baseadas em recomendações
```

### 3. Análise de Modelo
```
1. Ir em Modelos e Predições
2. Revisar performance
3. Verificar feature importance
4. Identificar oportunidades de melhoria
```

### 4. Investigação de Churn
```
1. Dashboard Principal - filtrar por cancelados
2. Insights de Negócio - análise RFM
3. Identificar padrões
4. Criar estratégia de retenção
```

## 🛠️ Troubleshooting

### Dashboard não abre

**Problema**: Porta 8501 já em uso

**Solução**:
```bash
streamlit run app.py --server.port 8502
```

### Visualizações não aparecem

**Problema**: Pipeline não foi executado

**Solução**:
```bash
python pipeline.py
```

### Erro ao carregar dados

**Problema**: Arquivos CSV não encontrados

**Solução**:
Verifique se os arquivos existem:
```bash
ls Cliente.csv produtos.csv Compras.csv
```

### Dashboard lento

**Problema**: Muitos dados em cache

**Solução**:
1. Pressione `C` no dashboard para limpar cache
2. Ou reinicie o servidor

### Gráficos não são interativos

**Problema**: Plotly não instalado

**Solução**:
```bash
pip install plotly
```

## 📱 Acesso Remoto

Para acessar o dashboard de outros dispositivos na mesma rede:

```bash
streamlit run app.py --server.address 0.0.0.0
```

Depois acesse de qualquer dispositivo:
```
http://[IP-DO-SERVIDOR]:8501
```

## 🔐 Segurança

### Produção
Para usar em produção, considere:

1. **Autenticação**:
   ```python
   # Adicionar em app.py
   import streamlit_authenticator as stauth
   ```

2. **HTTPS**:
   ```bash
   streamlit run app.py --server.enableCORS false --server.enableXsrfProtection false
   ```

3. **Firewall**:
   Configurar firewall para permitir apenas IPs confiáveis

## 📈 Performance

### Otimizações Implementadas
- ✅ Cache de dados com `@st.cache_data`
- ✅ Lazy loading de imagens
- ✅ Filtros eficientes
- ✅ Plots otimizados

### Dicas de Performance
1. Use filtros para reduzir dados mostrados
2. Limpe o cache regularmente (botão C)
3. Feche abas não utilizadas

## 🎨 Personalização

### Mudar Cores
Edite o CSS em `app.py`:
```python
st.markdown("""
<style>
    .main-header {
        color: #722F37;  /* Mude aqui */
    }
</style>
""", unsafe_allow_html=True)
```

### Adicionar Logo
Coloque sua logo na sidebar:
```python
st.sidebar.image("path/to/logo.png")
```

### Tema Escuro/Claro
No menu do Streamlit (canto superior direito):
Settings → Theme → Dark/Light

## 📞 Suporte

### Documentação Adicional
- [Documentação Streamlit](https://docs.streamlit.io)
- [Documentação Plotly](https://plotly.com/python/)
- [README Principal](README.md)

### Problemas Comuns
Consulte [COMANDOS_UTEIS.md](COMANDOS_UTEIS.md) para soluções rápidas

## 🚀 Próximas Funcionalidades

### Em Desenvolvimento
- [ ] Sistema de upload de novos dados via dashboard
- [ ] Predições em tempo real
- [ ] Exportação de relatórios em PDF
- [ ] Alertas automáticos
- [ ] Dashboard mobile otimizado
- [ ] Integração com banco de dados
- [ ] API REST

### Sugestões
Tem ideias? Contribua com o projeto!

---

**Dashboard desenvolvido com ❤️ usando Streamlit**

**Versão**: 1.0.0
**Última atualização**: 2025-11-05

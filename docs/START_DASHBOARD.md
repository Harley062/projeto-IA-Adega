# 🚀 Guia Rápido - Iniciar Dashboard

## Passo a Passo

### 1️⃣ Instalar Dependências do Dashboard

```bash
pip install streamlit plotly Pillow
```

### 2️⃣ Executar Pipeline (se ainda não executou)

```bash
python pipeline.py
```

Aguarde a conclusão (~2-5 minutos). Isso irá gerar:
- ✅ Modelos treinados
- ✅ Visualizações
- ✅ Relatórios

### 3️⃣ Iniciar o Dashboard

```bash
streamlit run app.py
```

### 4️⃣ Acessar no Navegador

O dashboard abrirá automaticamente em:
```
http://localhost:8501
```

Se não abrir automaticamente, copie e cole o link acima no seu navegador.

---

## 🎯 Pronto!

Agora você tem acesso a:

### 🏠 Dashboard Principal
- Métricas em tempo real
- Gráficos interativos
- Filtros dinâmicos

### 📊 Análise Exploratória
- 16 visualizações automáticas
- Correlações
- Outliers

### 🤖 Modelos ML
- Performance do modelo
- Métricas detalhadas
- Comparação entre modelos

### 💼 Insights de Negócio
- Top produtos
- Segmentação de clientes
- Análise RFM
- Recomendações

---

## ⚡ Comandos Rápidos

| Ação | Comando |
|------|---------|
| Iniciar dashboard | `streamlit run app.py` |
| Parar dashboard | `Ctrl + C` |
| Atualizar dados | `python pipeline.py` |
| Limpar cache | Pressione `C` no dashboard |
| Recarregar | Pressione `R` no dashboard |

---

## 🆘 Problemas?

### Dashboard não abre?
```bash
# Use outra porta
streamlit run app.py --server.port 8502
```

### Visualizações não aparecem?
```bash
# Execute o pipeline primeiro
python pipeline.py
```

### Erro ao carregar dados?
```bash
# Verifique se os CSVs existem
ls Cliente.csv produtos.csv Compras.csv
```

---

## 📚 Mais Informações

- [DASHBOARD_README.md](DASHBOARD_README.md) - Documentação completa
- [README.md](README.md) - Documentação do sistema
- [QUICKSTART.md](QUICKSTART.md) - Guia geral

---

**Aproveite seu dashboard! 🎉**

# Estrutura Organizada do Projeto

## Resumo da Reorganização

O projeto foi completamente reorganizado para melhor legibilidade e manutenção. Todos os arquivos foram categorizados em pastas específicas.

## Nova Estrutura

### Diretório Raiz
Contém apenas arquivos essenciais:
- `app.py` - Dashboard principal Streamlit
- `pages_prediction.py` - Páginas de predição do dashboard
- `config.yaml` - Configurações do sistema
- `requirements.txt` - Dependências Python
- `run_dashboard.bat` - Script para iniciar o dashboard
- `README.md` - Documentação principal

### 📂 data/
Todos os arquivos de dados do projeto:
- `Cliente.csv` - Dados dos clientes
- `Compras.csv` - Dados de compras
- `produtos.csv` - Catálogo de produtos
- `exemplo_predicao_lote.csv` - Exemplo para predições em lote
- `data_processed_*.csv` - Dados processados pelo pipeline
- `data_processed_info.txt` - Informações sobre os dados processados

### 📂 scripts/
Scripts executáveis e auxiliares:
- `pipeline.py` - Pipeline principal de ML
- `main.py` - Script legado
- `export_processed_data.py` - Exportação de dados processados
- `test_system.py` - Testes do sistema
- `replace_emojis.py` - Utilitário para emojis

### 📂 docs/
Toda a documentação do projeto:
- `DASHBOARD_README.md` - Guia do dashboard
- `GUIA_COMPLETO.md` - Guia completo do sistema
- `QUICKSTART.md` - Início rápido
- `SISTEMA_PREDITIVO.md` - Documentação do sistema preditivo
- `COMANDOS_UTEIS.md` - Comandos úteis
- `IMPROVEMENTS.md` - Melhorias implementadas
- `EXECUTIVE_SUMMARY.md` - Resumo executivo
- `README_BASES_TRATADAS.md` - Informações sobre bases tratadas
- `PREDICTOR_FIX.md` - Correções do preditor
- `LOGO_INTEGRATION.md` - Integração do logo
- `START_DASHBOARD.md` - Como iniciar o dashboard
- `ESTRUTURA_ORGANIZADA.md` - Este arquivo

### 📂 assets/
Recursos estáticos:
- `adega.png` - Logo da adega

### 📂 src/
Código fonte modular:
```
src/
├── data/
│   ├── data_loader.py          # Carregamento de dados
│   ├── eda.py                  # Análise exploratória
│   └── feature_engineering.py  # Engenharia de features
├── models/
│   ├── model_trainer.py        # Treinamento
│   └── model_evaluation.py     # Avaliação
├── visualization/
│   └── plots.py                # Visualizações
└── utils/
    ├── logger.py               # Sistema de logging
    └── config.py               # Configurações
```

### 📂 output/
Saídas geradas automaticamente:
```
output/
├── models/      # Modelos treinados (.pkl)
├── plots/       # Gráficos gerados (.png)
└── reports/     # Relatórios de avaliação
```

### 📂 logs/
Logs de execução do sistema (gerados automaticamente)

### 📂 venv/
Ambiente virtual Python (não versionado)

## Mudanças Importantes

### 1. Caminhos Atualizados
Os seguintes arquivos foram atualizados para refletir a nova estrutura:

**app.py:**
- Logo: `adega.png` → `assets/adega.png`
- Pipeline: `python pipeline.py` → `python scripts/pipeline.py`

**src/data/data_loader.py:**
- CSVs: `Cliente.csv` → `data/Cliente.csv`
- CSVs: `produtos.csv` → `data/produtos.csv`
- CSVs: `Compras.csv` → `data/Compras.csv`

**README.md:**
- Atualizado com a nova estrutura de pastas
- Links de documentação corrigidos

### 2. Como Executar

**Iniciar Dashboard:**
```bash
streamlit run app.py
```
ou
```bash
run_dashboard.bat
```

**Executar Pipeline:**
```bash
python scripts/pipeline.py
```

**Executar Testes:**
```bash
python scripts/test_system.py
```

### 3. Vantagens da Nova Estrutura

✅ **Organização Clara:** Cada tipo de arquivo tem seu lugar específico
✅ **Fácil Navegação:** Estrutura intuitiva e profissional
✅ **Manutenção Simples:** Fácil encontrar e modificar arquivos
✅ **Escalabilidade:** Estrutura preparada para crescimento
✅ **Documentação Centralizada:** Todos os docs em uma pasta
✅ **Dados Separados:** Dados isolados do código
✅ **Scripts Organizados:** Executáveis em pasta dedicada

## Checklist de Migração

- ✅ Criar estrutura de diretórios (data, scripts, docs, assets)
- ✅ Mover arquivos CSV para data/
- ✅ Mover scripts para scripts/
- ✅ Mover documentação para docs/
- ✅ Mover logo para assets/
- ✅ Atualizar referências em app.py
- ✅ Atualizar referências em data_loader.py
- ✅ Atualizar README.md
- ✅ Limpar arquivos temporários (__pycache__)
- ✅ Documentar nova estrutura

## Próximos Passos

1. **Testar o sistema** com a nova estrutura:
   ```bash
   python scripts/pipeline.py
   streamlit run app.py
   ```

2. **Verificar** se todos os caminhos estão corretos

3. **Atualizar** o .gitignore se necessário:
   ```
   venv/
   __pycache__/
   *.pyc
   logs/
   output/
   .env
   ```

4. **Considerar** adicionar:
   - Testes unitários em `tests/`
   - Notebooks de exploração em `notebooks/`
   - Scripts de deploy em `deploy/`

## Suporte

Para dúvidas sobre a estrutura:
1. Consulte o [README.md](../README.md) principal
2. Veja o [GUIA_COMPLETO.md](GUIA_COMPLETO.md)
3. Leia o [QUICKSTART.md](QUICKSTART.md)

---

**Última atualização:** 13 de novembro de 2025
**Status:** ✅ Reorganização Concluída

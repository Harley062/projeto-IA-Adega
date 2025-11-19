"""
Dashboard Web - Sistema de Análise de Dados da Adega
"""
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path
import sys
from PIL import Image

# Adicionar src ao path
sys.path.append(str(Path(__file__).parent / 'src'))

from data.data_loader import DataLoader
from models.model_trainer import ModelTrainer
from utils.glossario import FAQ, GLOSSARIO

# Configuração da página
st.set_page_config(
    page_title="Sistema de Análise - Adega",
    page_icon="🍷",  # ou use Image.open("adega.png") para usar o logo personalizado
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS customizado com Font Awesome
st.markdown("""
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        text-align: center;
        color: #722F37;
        margin-top: 0rem;
        margin-bottom: 1rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1.5rem;
        border-radius: 0.5rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 2rem;
    }
    /* Centralizar logo */
    [data-testid="column"] img {
        display: block;
        margin-left: auto;
        margin-right: auto;
    }
    /* Ícones personalizados */
    .icon {
        margin-right: 8px;
        color: #722F37;
    }
    .icon-success {
        color: #28a745;
    }
    .icon-warning {
        color: #ffc107;
    }
    .icon-danger {
        color: #dc3545;
    }
    .icon-info {
        color: #17a2b8;
    }
</style>
""", unsafe_allow_html=True)


# Funções helper para ícones
def icon(name, color=None):
    """Retorna HTML de um ícone Font Awesome"""
    color_class = f" icon-{color}" if color else ""
    return f'<i class="fas fa-{name} icon{color_class}"></i>'


# Função para carregar dados
@st.cache_data
def load_data():
    """Carrega e processa os dados"""
    try:
        loader = DataLoader(data_dir="data")
        loader.load_data()
        loader.validate_data()
        data = loader.merge_data()
        data = loader.clean_data()
        return data, loader
    except Exception as e:
        st.error(f"Erro ao carregar dados: {e}")
        return None, None


# Função para carregar imagens
def load_image(image_path):
    """Carrega uma imagem se existir"""
    try:
        if Path(image_path).exists():
            return Image.open(image_path)
        return None
    except Exception as e:
        st.error(f"Erro ao carregar imagem: {e}")
        return None


def main():
    """Função principal do dashboard"""

    # Header com logo
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        logo = load_image("assets/adega.png")
        if logo:
            st.image(logo, width=200)
        st.markdown('<h1 class="main-header">Sistema de Análise de Dados - Adega</h1>', unsafe_allow_html=True)

    # Sidebar
    with st.sidebar:
        # Logo na sidebar
        logo_sidebar = load_image("assets/adega.png")
        if logo_sidebar:
            st.image(logo_sidebar, width=120)
        else:
            st.image("https://img.icons8.com/color/96/000000/wine.png", width=100)

        st.title("Menu de Navegação")

        # Menu com ícones (usando emojis para evitar HTML não suportado)
        st.markdown("**Selecione uma página:**")
        page_options = {
            "Dashboard Principal": "🏠 Visão Geral",
            "Análise Exploratória": "📊 Gráficos e Tendências",
            "Modelos e Predições": "🔮 Previsões Inteligentes",
            "Insights de Negócio": "💡 Recomendações",
            "Ajuda": "❓ Ajuda e Glossário",
            "Configurações": "⚙️ Atualizar Dados"
        }

        page = st.radio(
            "menu_pages",
            options=list(page_options.keys()),
            format_func=lambda x: page_options[x],
            label_visibility="collapsed"
        )

        st.divider()

        # Informações do sistema
        st.markdown('<h3><i class="fas fa-info-circle icon"></i> Informações</h3>', unsafe_allow_html=True)

        # Verificar se pipeline foi executado
        model_exists = Path("output/models/best_model_Gradient_Boosting.pkl").exists()
        plots_exist = len(list(Path("output/plots").glob("*.png"))) > 0 if Path("output/plots").exists() else False

        if model_exists:
            st.markdown('<p style="color: #28a745;"><i class="fas fa-check-circle"></i> ✅ Sistema pronto</p>', unsafe_allow_html=True)
        else:
            st.markdown('<p style="color: #ffc107;"><i class="fas fa-exclamation-triangle"></i> ⚠️ Sistema precisa ser configurado</p>', unsafe_allow_html=True)

        if plots_exist:
            st.markdown('<p style="color: #28a745;"><i class="fas fa-check-circle"></i> ✅ Análises atualizadas</p>', unsafe_allow_html=True)
        else:
            st.markdown('<p style="color: #ffc107;"><i class="fas fa-exclamation-triangle"></i> ⚠️ Aguardando processamento</p>', unsafe_allow_html=True)

        st.divider()
        st.caption("Sistema v1.0.0")

    # Carregar dados
    data, loader = load_data()

    if data is None:
        st.error("❌ Não foi possível carregar os dados!")

        st.markdown("""
        ### 📋 Primeiros Passos

        Para começar a usar o sistema, siga estes passos:

        1. **Verifique os arquivos de dados**
           - Certifique-se de que os arquivos CSV estão na pasta `data/`
           - Arquivos necessários: `Cliente.csv`, `produtos.csv`, `Compras.csv`

        2. **Processe os dados**
           - Vá para a página **"⚙️ Atualizar Dados"** no menu lateral
           - Clique no botão **"▶️ Processar Dados"**
           - Aguarde 2-5 minutos (o sistema vai processar todos os dados)

        3. **Explore o dashboard**
           - Após o processamento, volte para esta página
           - Todas as análises e gráficos estarão disponíveis!

        💡 **Dica**: Você só precisa fazer isso uma vez, ou quando houver novos dados para processar.
        """)

        with st.expander("🔧 Para usuários técnicos - Como executar via terminal"):
            st.code("python scripts/pipeline.py", language="bash")

        return

    # Páginas
    if page == "Dashboard Principal":
        show_dashboard(data, loader)
    elif page == "Análise Exploratória":
        show_eda()
    elif page == "Modelos e Predições":
        show_models()
    elif page == "Insights de Negócio":
        show_business_insights(data)
    elif page == "Ajuda":
        show_help()
    elif page == "Configurações":
        show_settings()


def show_dashboard(data, loader):
    """Página principal do dashboard"""

    st.markdown('<h2><i class="fas fa-chart-line icon"></i> Visão Geral do Sistema</h2>', unsafe_allow_html=True)

    # Indicador de status do sistema
    model_exists = Path("output/models/best_model_Gradient_Boosting.pkl").exists()
    plots_exist = len(list(Path("output/plots").glob("*.png"))) > 0 if Path("output/plots").exists() else False

    if model_exists and plots_exist:
        st.success("✅ **Sistema pronto e atualizado!** Todas as análises e previsões estão disponíveis.")
    elif model_exists or plots_exist:
        st.info("ℹ️ **Sistema parcialmente configurado.** Vá em '⚙️ Atualizar Dados' para processar completamente.")
    else:
        st.warning("⚠️ **Sistema aguardando configuração inicial.** Vá em '⚙️ Atualizar Dados' para começar.")

    st.divider()

    # Métricas principais
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            label="Total de Registros",
            value=len(data),
            delta="Após limpeza"
        )

    with col2:
        st.metric(
            label="Clientes Únicos",
            value=data['cliente_id'].nunique()
        )

    with col3:
        st.metric(
            label="Produtos",
            value=data['produto_id'].nunique()
        )

    with col4:
        st.metric(
            label="Total Vendas",
            value=f"R$ {data['valor'].sum():,.2f}"
        )

    st.divider()

    # Gráficos interativos
    col1, col2 = st.columns(2)

    with col1:
        st.markdown('<h3><i class="fas fa-chart-bar icon"></i> Distribuição de Vendas</h3>', unsafe_allow_html=True)
        st.info("**O que significa:** Este gráfico mostra como os valores de compra estão distribuídos. Picos indicam faixas de preço mais comuns.\n\n"
                "**Insight para negócio:** Use para identificar o ticket médio e criar promoções estratégicas nessas faixas de valor.")

        fig = px.histogram(
            data,
            x='valor',
            nbins=20,
            title='Distribuição de Valores de Compra',
            labels={'valor': 'Valor (R$)', 'count': 'Frequência'},
            color_discrete_sequence=['#722F37']
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown('<h3><i class="fas fa-globe icon"></i> Vendas por Cidade</h3>', unsafe_allow_html=True)
        st.info("**O que significa:** Ranking das 10 cidades que mais geram receita para sua adega.\n\n"
                "**Insight para negócio:** Concentre investimentos em marketing e logística nas cidades de melhor desempenho. Cidades com baixo volume podem precisar de campanhas específicas.")

        city_sales = data.groupby('cidade')['valor'].sum().sort_values(ascending=False).head(10)
        fig = px.bar(
            x=city_sales.values,
            y=city_sales.index,
            orientation='h',
            title='Top 10 Cidades por Vendas',
            labels={'x': 'Total de Vendas (R$)', 'y': 'Cidade'},
            color_discrete_sequence=['#8B4513']
        )
        st.plotly_chart(fig, use_container_width=True)

    st.divider()

    # Tabela de dados
    st.markdown('<h3><i class="fas fa-table icon"></i> Visualização dos Dados</h3>', unsafe_allow_html=True)

    # Filtros
    col1, col2, col3 = st.columns(3)

    with col1:
        cities = ['Todas'] + sorted(data['cidade'].unique().tolist())
        selected_city = st.selectbox("Filtrar por Cidade:", cities)

    with col2:
        assinantes = ['Todos', 'Sim', 'Não']
        selected_assinante = st.selectbox("Assinante do Clube:", assinantes)

    with col3:
        min_valor = float(data['valor'].min())
        max_valor = float(data['valor'].max())
        valor_range = st.slider(
            "Faixa de Valor:",
            min_valor,
            max_valor,
            (min_valor, max_valor)
        )

    # Aplicar filtros
    filtered_data = data.copy()

    if selected_city != 'Todas':
        filtered_data = filtered_data[filtered_data['cidade'] == selected_city]

    if selected_assinante != 'Todos':
        filtered_data = filtered_data[filtered_data['assinante_clube'] == selected_assinante]

    filtered_data = filtered_data[
        (filtered_data['valor'] >= valor_range[0]) &
        (filtered_data['valor'] <= valor_range[1])
    ]

    st.dataframe(
        filtered_data[['cliente_id', 'nome', 'cidade', 'valor', 'quantidade',
                       'assinante_clube', 'cancelou_assinatura', 'pais', 'tipo_uva']],
        use_container_width=True,
        height=400
    )

    st.caption(f"Mostrando {len(filtered_data)} de {len(data)} registros")


def show_eda():
    """Página de Análise Exploratória de Dados"""

    st.markdown('<h2><i class="fas fa-chart-pie icon"></i> Gráficos e Análise de Tendências</h2>', unsafe_allow_html=True)

    st.markdown('<div class="icon-info"><i class="fas fa-lightbulb"></i> Todas as visualizações foram geradas automaticamente pelo pipeline.</div>', unsafe_allow_html=True)

    plots_dir = Path("output/plots")

    if not plots_dir.exists() or len(list(plots_dir.glob("*.png"))) == 0:
        st.warning("⚠️ Gráficos ainda não foram gerados!")

        st.info("""
        ### 📊 Como gerar os gráficos:

        1. Vá para a página **"⚙️ Atualizar Dados"** no menu lateral
        2. Clique no botão **"▶️ Processar Dados"**
        3. Aguarde alguns minutos
        4. Volte aqui para ver todos os gráficos!

        Os gráficos mostram padrões importantes nos seus dados de vendas e clientes.
        """)

        with st.expander("🔧 Executar via terminal (usuários técnicos)"):
            st.code("python scripts/pipeline.py", language="bash")

        return

    # Tabs para diferentes análises
    tab1, tab2, tab3, tab4 = st.tabs([
        "Distribuições",
        "Correlações",
        "Outliers",
        "Análise Temporal"
    ])

    with tab1:
        st.subheader("Distribuições de Variáveis")

        st.info("**O que significa:** Mostra como diferentes variáveis estão distribuídas nos seus dados (idade, valores, quantidade, etc).\n\n"
                "**Insight para negócio:** Identifique padrões de comportamento - ex: se a maioria dos clientes tem 30-40 anos, adapte sua comunicação para esse público.")

        col1, col2 = st.columns(2)

        with col1:
            img = load_image(plots_dir / "numerical_distributions.png")
            if img:
                st.image(img, caption="Distribuições Numéricas - Valores, idades, quantidades", use_container_width=True)

        with col2:
            img = load_image(plots_dir / "categorical_distributions.png")
            if img:
                st.image(img, caption="Distribuições Categóricas - Cidades, tipos de vinho, assinantes", use_container_width=True)

    with tab2:
        st.subheader("Matriz de Correlação")

        st.info("**O que significa:** Mostra quais variáveis estão relacionadas entre si. Valores próximos de 1 (vermelho) = forte relação positiva, próximos de -1 (azul) = relação negativa.\n\n"
                "**Insight para negócio:** Descubra o que influencia as vendas. Ex: se 'pontuação de engajamento' tem alta correlação com 'valor de compra', invista em engajamento!")

        img = load_image(plots_dir / "correlation_matrix.png")
        if img:
            st.image(img, caption="Correlação entre Variáveis - Identifique relações importantes", use_container_width=True)
        else:
            st.info("Matriz de correlação não disponível")

    with tab3:
        st.subheader("Detecção de Outliers")

        st.info("**O que significa:** Boxplots mostram valores atípicos (pontos fora das 'caixas'). Esses são clientes ou vendas muito diferentes do padrão.\n\n"
                "**Insight para negócio:** Outliers podem ser VIPs (gastam muito mais) ou oportunidades perdidas (gastam muito menos). Analise ambos!")

        img = load_image(plots_dir / "boxplots.png")
        if img:
            st.image(img, caption="Boxplots - Pontos fora das caixas são valores atípicos", use_container_width=True)
        else:
            st.info("Boxplots não disponíveis")

    with tab4:
        st.subheader("Análise Temporal de Vendas")

        st.info("**O que significa:** Mostra como suas vendas evoluem ao longo do tempo - tendências, sazonalidades e padrões.\n\n"
                "**Insight para negócio:** Identifique meses de alta/baixa, planeje estoque e promoções. Aproveite períodos de pico e crie estratégias para períodos fracos!")

        img = load_image(plots_dir / "sales_over_time.png")
        if img:
            st.image(img, caption="Vendas ao Longo do Tempo - Identifique sazonalidade e tendências", use_container_width=True)
        else:
            st.info("Análise temporal não disponível")


def show_models():
    """Página de Modelos e Predições"""

    st.markdown('<h2><i class="fas fa-robot icon"></i> Previsões Inteligentes</h2>', unsafe_allow_html=True)

    # Verificar se modelo existe
    model_path = Path("output/models/best_model_Gradient_Boosting.pkl")
    report_path = Path("output/reports/evaluation_report.txt")

    if not model_path.exists():
        st.warning("⚠️ Sistema de previsão ainda não está configurado!")

        st.info("""
        ### 🔮 Como ativar as previsões inteligentes:

        1. Vá para a página **"⚙️ Atualizar Dados"** no menu lateral
        2. Clique no botão **"▶️ Processar Dados"**
        3. Aguarde alguns minutos (o sistema vai treinar os modelos de IA)
        4. Volte aqui para fazer previsões!

        Com o sistema treinado, você poderá prever quais clientes têm risco de cancelar,
        estimar vendas futuras e muito mais.
        """)

        with st.expander("🔧 Executar via terminal (usuários técnicos)"):
            st.code("python scripts/pipeline.py", language="bash")

        return

    # Tabs
    tab1, tab2, tab3 = st.tabs(["Performance", "Predições", "Análise do Modelo"])

    with tab1:
        st.subheader("Performance do Modelo")

        st.info("**O que é isso:** O sistema foi treinado para prever se um cliente vai cancelar a assinatura ou continuar comprando.\n\n"
                "**Para que serve:** Identificar clientes em risco ANTES que eles cancelem, permitindo ações preventivas de retenção!")

        # Explicação das métricas
        with st.expander("📚 Entenda as Métricas do Modelo"):
            st.markdown("""
            **Accuracy (Acurácia):** % de previsões corretas no geral. Ex: 85% = acertou 85 de cada 100 previsões.

            **Precision (Precisão):** Quando o modelo diz que um cliente vai cancelar, qual a chance de estar certo? Alta precisão = menos alarmes falsos.

            **Recall (Sensibilidade):** De todos os clientes que realmente cancelaram, quantos o modelo identificou? Alto recall = pega mais casos reais.

            **F1-Score:** Equilíbrio entre Precision e Recall. Quanto maior, melhor o modelo como um todo.

            **ROC-AUC:** Mede a capacidade do modelo de distinguir entre quem cancela e quem não cancela. Quanto mais próximo de 1, melhor!

            💡 **Para seu negócio:** Um modelo com alto Recall é importante porque você NÃO quer perder nenhum cliente em risco!
            """)

        # Carregar relatório
        if report_path.exists():
            with open(report_path, 'r', encoding='utf-8') as f:
                report = f.read()

            st.text(report)

        st.divider()

        # Visualizações de performance
        col1, col2 = st.columns(2)

        plots_dir = Path("output/plots")

        with col1:
            st.markdown("##### Matriz de Confusão")
            st.caption("**O que mostra:** Compara previsões vs realidade. Diagonal = acertos, resto = erros.")
            img = load_image(plots_dir / "confusion_matrix.png")
            if img:
                st.image(img, use_container_width=True)
                st.success("✅ Verde na diagonal = modelo está acertando!")

            st.divider()

            st.markdown("##### Comparação de Modelos")
            st.caption("**O que mostra:** Ranking dos melhores modelos testados. O topo é o vencedor!")
            img = load_image(plots_dir / "model_comparison.png")
            if img:
                st.image(img, use_container_width=True)

        with col2:
            st.markdown("##### Curva ROC")
            st.caption("**O que mostra:** Quanto mais próxima do canto superior esquerdo, melhor o modelo.")
            img = load_image(plots_dir / "roc_curve.png")
            if img:
                st.image(img, use_container_width=True)
                st.info("📊 Área abaixo da curva (AUC) próxima de 1 = excelente!")

            st.divider()

            st.markdown("##### Curva Precision-Recall")
            st.caption("**O que mostra:** Equilíbrio entre não perder clientes em risco e evitar alarmes falsos.")
            img = load_image(plots_dir / "precision_recall_curve.png")
            if img:
                st.image(img, use_container_width=True)

    with tab2:
        st.markdown('<h3><i class="fas fa-bullseye icon"></i> Sistema Preditivo Completo</h3>', unsafe_allow_html=True)

        # Sub-tabs para diferentes tipos de predição
        pred_tab1, pred_tab2, pred_tab3, pred_tab4 = st.tabs([
            "Predição Individual",
            # "Predição em Lote",
            "Predição de Vendas",
            "Recomendação de Produtos"
        ])

        with pred_tab1:
            from pages_prediction import show_cancelamento_prediction
            show_cancelamento_prediction()

        with pred_tab2:
            from pages_prediction import show_batch_prediction
            show_batch_prediction()

        with pred_tab3:
            from pages_prediction import show_sales_prediction
            show_sales_prediction()

        with pred_tab4:
            from pages_prediction import show_product_recommendation
            show_product_recommendation()

    with tab3:
        st.subheader("🔍 Análise de Features")

        st.info("**O que significa:** Mostra quais fatores mais influenciam o cancelamento de assinatura.\n\n"
                "**Insight para negócio:** Foque nos fatores mais importantes! Se 'pontuação de engajamento' está no topo, invista em manter clientes engajados.")

        img = load_image(Path("output/plots") / "feature_importance.png")
        if img:
            st.image(img, caption="Importância das Características - Os fatores que mais preveem cancelamento", use_container_width=True)
            st.success("💡 As barras maiores são os fatores mais importantes para evitar cancelamentos!")
        else:
            st.info("Análise de features não disponível")


def show_business_insights(data):
    """Página de Insights de Negócio"""

    st.header("💡 Recomendações para Melhorar Vendas")

    plots_dir = Path("output/plots")

    # Tabs
    tab1, tab2, tab3, tab4 = st.tabs([
        "🍷 Análise de Produtos",
        "👥 Segmentação de Clientes",
        "📈 Análise RFM",
        "💡 Recomendações"
    ])

    with tab1:
        st.subheader("Análise de Produtos")

        st.info("**O que significa:** Mostra quais produtos vendem mais e as características dos vinhos preferidos.\n\n"
                "**Ação recomendada:** Garanta estoque dos top produtos, crie combos/kits, e faça promoções cruzadas!")

        col1, col2 = st.columns(2)

        with col1:
            img = load_image(plots_dir / "top_products.png")
            if img:
                st.image(img, caption="Top Produtos - Mantenha sempre em estoque!", use_container_width=True)
                st.warning("⚠️ **Risco:** Falta de estoque dos top produtos = perda de vendas")

        with col2:
            img = load_image(plots_dir / "wine_analysis.png")
            if img:
                st.image(img, caption="Análise de Vinhos - Preferências dos clientes", use_container_width=True)
                st.success("💡 **Oportunidade:** Diversifique na categoria mais vendida")

    with tab2:
        st.subheader("Segmentação de Clientes")

        st.info("**O que significa:** Divide seus clientes em grupos com comportamentos similares.\n\n"
                "**Ação recomendada:** Crie campanhas personalizadas para cada segmento - mensagens diferentes para públicos diferentes!")

        img = load_image(plots_dir / "customer_segmentation.png")
        if img:
            st.image(img, caption="Segmentação - Cada grupo precisa de uma estratégia diferente", use_container_width=True)

        # Métricas por segmento
        st.divider()
        st.subheader("Métricas por Segmento")

        col1, col2 = st.columns(2)

        with col1:
            assinantes = data[data['assinante_clube'] == 'Sim']
            st.metric(
                "💎 Assinantes do Clube",
                f"{len(assinantes)} clientes",
                f"R$ {assinantes['valor'].sum():,.2f} em vendas"
            )
            if len(assinantes) > 0:
                avg_assinante = assinantes['valor'].mean()
                st.caption(f"Ticket médio: R$ {avg_assinante:.2f}")
                st.success("✅ **Estratégia:** Mantenha benefícios exclusivos e engajamento alto!")

        with col2:
            nao_assinantes = data[data['assinante_clube'] == 'Não']
            st.metric(
                "👤 Não Assinantes",
                f"{len(nao_assinantes)} clientes",
                f"R$ {nao_assinantes['valor'].sum():,.2f} em vendas"
            )
            if len(nao_assinantes) > 0:
                avg_nao_assinante = nao_assinantes['valor'].mean()
                st.caption(f"Ticket médio: R$ {avg_nao_assinante:.2f}")
                st.warning("⚠️ **Oportunidade:** Converta para assinantes com trial gratuito!")

    with tab3:
        st.subheader("Análise RFM (Recency, Frequency, Monetary)")

        st.info("""
        **O que é RFM:** Classificação de clientes baseada em 3 fatores:
        - **Recency (Recência):** Há quanto tempo o cliente comprou pela última vez
        - **Frequency (Frequência):** Quantas vezes o cliente compra
        - **Monetary (Monetário):** Quanto dinheiro o cliente gasta

        **Para que serve:** Identifica seus melhores clientes (VIPs), clientes em risco e oportunidades!
        """)

        img = load_image(plots_dir / "rfm_analysis.png")
        if img:
            st.image(img, caption="Análise RFM - Segmentação por valor e comportamento", use_container_width=True)

        st.markdown("""
        ### 🎯 Como usar o RFM no seu negócio:

        **Champions (RFM Alto):** 🏆
        - São seus melhores clientes
        - **Ação:** Recompense com benefícios VIP, acesso antecipado a novos vinhos

        **At Risk (Monetary alto, Recency baixa):** ⚠️
        - Clientes valiosos que não compram há tempo
        - **Ação:** Campanha urgente de reativação com desconto especial

        **Lost (RFM Baixo):** 😢
        - Clientes perdidos
        - **Ação:** Pesquisa de satisfação, ofertas de "última chance"

        **Promising (Frequency baixa, Monetary crescente):** 🌱
        - Novos clientes com potencial
        - **Ação:** Nurturing, programa de fidelidade, conteúdo educativo sobre vinhos
        """)

    with tab4:
        st.subheader("💡 Recomendações Estratégicas Acionáveis")

        # Calcular insights detalhados
        taxa_cancelamento = (data['cancelou_assinatura'] == 'Sim').sum() / len(data) * 100
        total_cancelamentos = (data['cancelou_assinatura'] == 'Sim').sum()
        avg_ticket = data['valor'].mean()
        top_city = data.groupby('cidade')['valor'].sum().idxmax()
        top_city_revenue = data.groupby('cidade')['valor'].sum().max()

        # Análise de produtos
        if 'produto_id' in data.columns:
            top_products = data.groupby('produto_id')['quantidade'].sum().nlargest(3)

        # Análise de assinantes
        assinantes_count = (data['assinante_clube'] == 'Sim').sum()
        assinantes_revenue = data[data['assinante_clube'] == 'Sim']['valor'].sum()
        total_revenue = data['valor'].sum()
        assinante_contribution = (assinantes_revenue / total_revenue * 100) if total_revenue > 0 else 0

        # Painel de Alertas
        st.markdown("### 🚨 Alertas e Riscos Imediatos")

        col1, col2 = st.columns(2)

        with col1:
            if taxa_cancelamento > 15:
                st.error(f"**⚠️ ALERTA CRÍTICO: Taxa de Cancelamento Alta ({taxa_cancelamento:.1f}%)**")
                st.markdown(f"""
                **Situação:** {total_cancelamentos} clientes cancelaram a assinatura.

                **Ações URGENTES:**
                1. 📞 Entre em contato com os clientes que cancelaram nas últimas 2 semanas
                2. 🎁 Ofereça desconto de recuperação (15-20% off)
                3. 📧 Envie pesquisa de satisfação para entender os motivos
                4. 🔍 Use o sistema de previsão para identificar próximos em risco
                """)
            else:
                st.success(f"**✅ Taxa de Cancelamento Controlada ({taxa_cancelamento:.1f}%)**")
                st.markdown("Continue monitorando semanalmente.")

        with col2:
            if assinante_contribution < 40:
                st.warning(f"**⚠️ OPORTUNIDADE: Clube de Assinantes ({assinante_contribution:.1f}% da receita)**")
                st.markdown(f"""
                **Situação:** Apenas {assinantes_count} assinantes gerando {assinante_contribution:.1f}% da receita.

                **Ações RECOMENDADAS:**
                1. 🎯 Campanha de conversão para não-assinantes
                2. 🆓 Ofereça 1º mês grátis no clube
                3. 🎁 Crie benefícios exclusivos (frete grátis, degustações)
                4. 💰 Meta: Dobrar número de assinantes em 3 meses
                """)
            else:
                st.success(f"**✅ Clube de Assinantes Forte ({assinante_contribution:.1f}% da receita)**")

        st.divider()

        # Oportunidades de Crescimento
        st.markdown("### 🚀 Oportunidades de Crescimento")

        tab_promo, tab_expansao, tab_produto, tab_retencao = st.tabs([
            "📢 Promoções", "🌎 Expansão", "📦 Mix de Produtos", "🔒 Retenção"
        ])

        with tab_promo:
            st.markdown(f"""
            #### Quando e Como Fazer Promoções

            **1. Promoção de Ticket Médio (Atual: R$ {avg_ticket:.2f})**
            - **Quando:** Quinzenalmente
            - **Como:** "Compre 2, leve 3" ou desconto progressivo (5% acima de R$100, 10% acima de R$200)
            - **Objetivo:** Aumentar ticket médio em 20%

            **2. Promoção de Reativação**
            - **Quando:** Mensalmente para clientes inativos há mais de 60 dias
            - **Como:** Email com cupom de 15% + frete grátis
            - **Objetivo:** Recuperar 25% dos inativos

            **3. Promoção Sazonal**
            - **Quando:** Datas comemorativas (Dia dos Pais, Natal, Black Friday)
            - **Como:** Kits temáticos com 20-30% off
            - **Objetivo:** Aumentar volume de vendas em 50% no período

            **4. Flash Sale**
            - **Quando:** Sexta-feira, 18h-22h
            - **Como:** Produto selecionado com 40% off (estoque limitado)
            - **Objetivo:** Criar urgência e engajamento
            """)

        with tab_expansao:
            st.markdown(f"""
            #### Estratégia de Expansão Geográfica

            **Seu Melhor Mercado Atual: {top_city} (R$ {top_city_revenue:,.2f})**

            **Plano de Expansão:**

            **1. Fase 1 - Consolidar {top_city} (Mês 1-2)**
            - Aumentar investimento em marketing local
            - Parcerias com restaurantes locais
            - Meta: +30% de crescimento

            **2. Fase 2 - Replicar Sucesso (Mês 3-4)**
            - Identificar cidades similares demograficamente
            - Aplicar mesmas estratégias que funcionaram em {top_city}
            - Teste em 2-3 cidades novas

            **3. Fase 3 - Expansão Digital (Mês 5-6)**
            - Investir em ads geolocalizados
            - Criar programa de indicação
            - Expandir para 5 novas cidades

            **Cidades com Baixo Desempenho:**
            - Faça pesquisa local para entender barreiras
            - Considere parcerias com distribuidores locais
            - Ofereça frete grátis como teste por 30 dias
            """)

        with tab_produto:
            st.markdown(f"""
            #### Otimização de Mix de Produtos

            **Análise Atual:**
            - Identifique os Top 10 produtos (use a aba "Análise de Produtos")
            - Analise margem de lucro vs volume de vendas

            **Estratégias:**

            **1. Produtos "Estrela" (Alto volume, Alta margem)** ⭐
            - **Ação:** NUNCA deixe faltar estoque
            - **Promoção:** Use como "isca" em combos
            - **Exposição:** Destaque na home do site/loja

            **2. Produtos "Vaca Leiteira" (Alto volume, Baixa margem)** 🐄
            - **Ação:** Mantenha estoque, mas venda em combo com produtos de alta margem
            - **Exemplo:** "Compre vinho popular + vinho premium com 15% off"

            **3. Produtos "Oportunidade" (Baixo volume, Alta margem)** 💎
            - **Ação:** Invista em marketing educativo
            - **Exemplo:** Degustações, vídeos sobre harmonização
            - **Posicionamento:** Vinhos "premium" ou "exclusivos"

            **4. Produtos "Peso Morto" (Baixo volume, Baixa margem)** ⚠️
            - **Ação:** Liquidar em promoção relâmpago
            - **Decisão:** Substituir por produtos melhores

            **Novos Produtos:**
            - Analise produtos similares aos best-sellers
            - Teste em pequena escala (50-100 unidades)
            - Colete feedback antes de comprar estoque grande
            """)

        with tab_retencao:
            st.markdown(f"""
            #### Programa de Retenção e Fidelização

            **Seu Desafio: {total_cancelamentos} clientes já cancelaram ({taxa_cancelamento:.1f}%)**

            **Sistema de 3 Camadas:**

            **1. Prevenção (ANTES do cliente pensar em sair)** 🛡️
            - **Semana 1-2:** Email de boas-vindas + guia de vinhos
            - **Mês 1:** Pesquisa de satisfação + cupom de surpresa
            - **Mês 2-3:** Programa de pontos/cashback
            - **Trimestral:** Benefício exclusivo (degustação VIP, lançamentos antecipados)

            **2. Detecção Precoce (Sinais de risco)** 🔍
            - **Use o modelo preditivo semanalmente**
            - Monitore: Queda de engajamento, reclamações, redução de compras
            - **Ação imediata:** Contato proativo (telefone ou WhatsApp)

            **3. Recuperação (Cliente já cancelou)** 🔄
            - **Até 7 dias:** Email automático com desconto de 20%
            - **14 dias:** Ligação pessoal para entender motivo
            - **30 dias:** "Sentimos sua falta" + oferta irresistível
            - **90 dias:** Última tentativa com benefício único

            **KPIs para Monitorar:**
            - Taxa de cancelamento mensal (meta: <10%)
            - Taxa de recuperação (meta: >30%)
            - NPS - Net Promoter Score
            - Tempo médio de vida do cliente (CLV)
            """)

        st.divider()

        # Checklist Semanal
        st.markdown("### ✅ Checklist Semanal do Gestor")

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("""
            **Segunda-feira:**
            - [ ] Revisar vendas da semana anterior
            - [ ] Executar sistema de previsão de cancelamentos
            - [ ] Contactar top 5 clientes em risco

            **Quarta-feira:**
            - [ ] Analisar estoque dos top produtos
            - [ ] Revisar NPS e feedbacks
            - [ ] Planejar promoção de fim de semana
            """)

        with col2:
            st.markdown("""
            **Sexta-feira:**
            - [ ] Disparar campanha de promoção
            - [ ] Analisar performance das campanhas ativas
            - [ ] Planejar ações da próxima semana

            **Mensal:**
            - [ ] Análise completa de RFM
            - [ ] Revisão de mix de produtos
            - [ ] Planejamento estratégico do próximo mês
            """)

        st.divider()

        st.success(
            "💡 **DICA DE OURO:** Use este dashboard toda semana! "
            "Dados sem ação não geram resultado. Escolha 2-3 ações prioritárias e execute com consistência."
        )


def show_help():
    """Página de Ajuda e Glossário"""

    st.header("❓ Ajuda - Como Usar o Sistema")

    st.markdown("""
    Bem-vindo à central de ajuda! Aqui você encontra respostas para as dúvidas mais comuns
    e explicações sobre os termos usados no sistema.
    """)

    # Tabs para organizar o conteúdo
    tab1, tab2, tab3 = st.tabs(["❓ Perguntas Frequentes", "📚 Glossário", "🚀 Guia Rápido"])

    with tab1:
        st.subheader("Perguntas Frequentes (FAQ)")

        for faq_item in FAQ:
            with st.expander(f"❓ {faq_item['pergunta']}"):
                st.markdown(faq_item['resposta'])

    with tab2:
        st.subheader("Glossário de Termos")

        st.info("**Traduzimos os termos técnicos para você!** Aqui está o que cada termo significa:")

        # Busca no glossário
        busca = st.text_input("🔍 Buscar termo no glossário", placeholder="Digite um termo...")

        if busca:
            encontrados = [(t, s) for t, s in GLOSSARIO.items() if busca.lower() in t.lower() or busca.lower() in s.lower()]
            if encontrados:
                st.success(f"Encontrados {len(encontrados)} resultado(s):")
                for termo_tecnico, termo_simples in encontrados:
                    st.markdown(f"**{termo_tecnico}** → {termo_simples}")
            else:
                st.warning("Nenhum termo encontrado. Tente outra palavra-chave.")
        else:
            # Organizar glossário por categorias
            col1, col2 = st.columns(2)

            with col1:
                st.markdown("### 🤖 Termos de Inteligência Artificial")
                ml_terms = {
                    "Churn": "Cancelamento",
                    "Machine Learning": "Inteligência Artificial",
                    "Model": "Sistema Inteligente",
                    "Pipeline": "Processamento",
                    "Feature Engineering": "Preparação de Dados",
                }
                for tecnico, simples in ml_terms.items():
                    st.markdown(f"• **{tecnico}** = {simples}")

                st.markdown("### 📊 Métricas do Sistema")
                metric_terms = {
                    "Accuracy": "Precisão Geral",
                    "Precision": "Taxa de Acerto",
                    "Recall": "Taxa de Detecção",
                    "F1-Score": "Nota Geral",
                    "ROC-AUC": "Precisão do Sistema",
                }
                for tecnico, simples in metric_terms.items():
                    st.markdown(f"• **{tecnico}** = {simples}")

            with col2:
                st.markdown("### 📈 Termos de Negócio")
                business_terms = {
                    "Lifetime Value": "Valor Total do Cliente",
                    "RFM Analysis": "Análise RFM",
                    "Engagement Score": "Nível de Engajamento",
                    "Ticket Médio": "Valor Médio de Compra",
                }
                for tecnico, simples in business_terms.items():
                    st.markdown(f"• **{tecnico}** = {simples}")

                st.markdown("### 🔧 Operações")
                ops_terms = {
                    "Batch Prediction": "Análise em Lote",
                    "Predict": "Prever",
                }
                for tecnico, simples in ops_terms.items():
                    st.markdown(f"• **{tecnico}** = {simples}")

    with tab3:
        st.subheader("🚀 Guia Rápido - Primeiros Passos")

        st.markdown("""
        ### 1️⃣ Primeira Vez no Sistema

        Se é sua primeira vez, siga esta ordem:

        1. **Verifique os dados**
           - Os arquivos CSV devem estar na pasta `data/`
           - Arquivos: `Cliente.csv`, `produtos.csv`, `Compras.csv`

        2. **Processe os dados**
           - Vá em **"⚙️ Atualizar Dados"**
           - Clique em **"▶️ Processar Dados"**
           - Aguarde 2-5 minutos

        3. **Explore o dashboard**
           - Comece pela **"🏠 Visão Geral"**
           - Veja os **"📊 Gráficos e Tendências"**
           - Teste as **"🔮 Previsões Inteligentes"**
           - Leia as **"💡 Recomendações"**

        ---

        ### 2️⃣ Atalhos Úteis

        | Preciso... | Vá para... |
        |------------|-----------|
        | Ver números gerais | 🏠 Visão Geral |
        | Ver padrões nos dados | 📊 Gráficos e Tendências |
        | Prever cancelamentos | 🔮 Previsões Inteligentes |
        | Ter ideias de ações | 💡 Recomendações |
        | Processar novos dados | ⚙️ Atualizar Dados |
        | Tirar dúvidas | ❓ Ajuda |

        ---

        ### 3️⃣ Suporte

        **Problemas comuns e soluções:**

        - **"Não consigo ver os gráficos"**
          → Vá em "⚙️ Atualizar Dados" e processe os dados

        - **"Erro ao carregar dados"**
          → Verifique se os arquivos CSV estão na pasta `data/`

        - **"Sistema lento"**
          → Normal no primeiro processamento. Aguarde completar.

        - **"Não entendo um termo"**
          → Veja a aba "📚 Glossário" acima
        """)

        st.success("🎯 **Lembre-se**: O sistema é uma ferramenta para ajudar você a tomar decisões melhores. Use seu conhecimento do negócio junto com os dados!")


def show_settings():
    """Página de Configurações"""

    st.header("⚙️ Atualizar e Processar Dados")

    st.subheader("🔄 Executar Pipeline")

    st.info("Execute o pipeline completo para atualizar todos os dados e modelos.")

    if st.button("▶️ Executar Pipeline Completo", type="primary"):
        with st.spinner("Executando pipeline... Isso pode levar alguns minutos."):
            import subprocess
            try:
                result = subprocess.run(
                    [sys.executable, "scripts/pipeline.py"],
                    capture_output=True,
                    text=True,
                    timeout=300
                )

                if result.returncode == 0:
                    st.success("✅ Pipeline executado com sucesso!")
                    st.balloons()
                else:
                    st.error(f"❌ Erro ao executar pipeline:\n{result.stderr}")
            except Exception as e:
                st.error(f"❌ Erro: {e}")

    st.divider()

    st.subheader("📁 Gerenciar Arquivos")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**Modelos Treinados**")
        models_dir = Path("output/models")
        if models_dir.exists():
            models = list(models_dir.glob("*.pkl"))
            if models:
                for model in models:
                    size_mb = model.stat().st_size / 1024 / 1024
                    st.text(f"✅ {model.name} ({size_mb:.2f} MB)")
            else:
                st.text("Nenhum modelo encontrado")

    with col2:
        st.markdown("**Visualizações**")
        plots_dir = Path("output/plots")
        if plots_dir.exists():
            plots = list(plots_dir.glob("*.png"))
            st.text(f"📊 {len(plots)} gráficos gerados")
        else:
            st.text("Nenhuma visualização encontrada")

    st.divider()

    st.subheader("ℹ️ Informações do Sistema")

    col1, col2 = st.columns(2)

    with col1:
        st.text(f"Python: {sys.version.split()[0]}")
        st.text(f"Streamlit: {st.__version__}")
        st.text(f"Pandas: {pd.__version__}")

    with col2:
        st.text(f"NumPy: {np.__version__}")
        st.text("Sistema: v1.0.0")


if __name__ == "__main__":
    main()

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
        loader = DataLoader()
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
            "Dashboard Principal": "🏠 Dashboard Principal",
            "Análise Exploratória": "📊 Análise Exploratória",
            "Modelos e Predições": "🤖 Modelos e Predições",
            "Insights de Negócio": "💼 Insights de Negócio",
            "Configurações": "⚙️ Configurações"
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
            st.markdown('<p style="color: #28a745;"><i class="fas fa-check-circle"></i> Modelo treinado</p>', unsafe_allow_html=True)
        else:
            st.markdown('<p style="color: #ffc107;"><i class="fas fa-exclamation-triangle"></i> Execute o pipeline primeiro</p>', unsafe_allow_html=True)

        if plots_exist:
            st.markdown('<p style="color: #28a745;"><i class="fas fa-check-circle"></i> Visualizações geradas</p>', unsafe_allow_html=True)
        else:
            st.markdown('<p style="color: #ffc107;"><i class="fas fa-exclamation-triangle"></i> Execute o pipeline primeiro</p>', unsafe_allow_html=True)

        st.divider()
        st.caption("Sistema v1.0.0")

    # Carregar dados
    data, loader = load_data()

    if data is None:
        st.markdown('<p style="color: #dc3545;"><i class="fas fa-times-circle"></i> Não foi possível carregar os dados. Execute o pipeline primeiro.</p>', unsafe_allow_html=True)
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
    elif page == "Configurações":
        show_settings()


def show_dashboard(data, loader):
    """Página principal do dashboard"""

    st.markdown('<h2><i class="fas fa-chart-line icon"></i> Visão Geral do Sistema</h2>', unsafe_allow_html=True)

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

    st.markdown('<h2><i class="fas fa-chart-pie icon"></i> Análise Exploratória de Dados (EDA)</h2>', unsafe_allow_html=True)

    st.markdown('<div class="icon-info"><i class="fas fa-lightbulb"></i> Todas as visualizações foram geradas automaticamente pelo pipeline.</div>', unsafe_allow_html=True)

    plots_dir = Path("output/plots")

    if not plots_dir.exists() or len(list(plots_dir.glob("*.png"))) == 0:
        st.markdown('<p style="color: #ffc107;"><i class="fas fa-exclamation-triangle"></i> Nenhuma visualização encontrada. Execute o pipeline primeiro:</p>', unsafe_allow_html=True)
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

        col1, col2 = st.columns(2)

        with col1:
            img = load_image(plots_dir / "numerical_distributions.png")
            if img:
                st.image(img, caption="Distribuições Numéricas", use_column_width=True)

        with col2:
            img = load_image(plots_dir / "categorical_distributions.png")
            if img:
                st.image(img, caption="Distribuições Categóricas", use_column_width=True)

    with tab2:
        st.subheader("Matriz de Correlação")
        img = load_image(plots_dir / "correlation_matrix.png")
        if img:
            st.image(img, caption="Correlação entre Variáveis", use_column_width=True)
        else:
            st.info("Matriz de correlação não disponível")

    with tab3:
        st.subheader("Detecção de Outliers")
        img = load_image(plots_dir / "boxplots.png")
        if img:
            st.image(img, caption="Boxplots para Detecção de Outliers", use_column_width=True)
        else:
            st.info("Boxplots não disponíveis")

    with tab4:
        st.subheader("Análise Temporal de Vendas")
        img = load_image(plots_dir / "sales_over_time.png")
        if img:
            st.image(img, caption="Vendas ao Longo do Tempo", use_column_width=True)
        else:
            st.info("Análise temporal não disponível")


def show_models():
    """Página de Modelos e Predições"""

    st.markdown('<h2><i class="fas fa-robot icon"></i> Modelos de Machine Learning</h2>', unsafe_allow_html=True)

    # Verificar se modelo existe
    model_path = Path("output/models/best_model_Gradient_Boosting.pkl")
    report_path = Path("output/reports/evaluation_report.txt")

    if not model_path.exists():
        st.markdown('<p style="color: #ffc107;"><i class="fas fa-exclamation-triangle"></i> Modelo não encontrado. Execute o pipeline primeiro:</p>', unsafe_allow_html=True)
        st.code("python scripts/pipeline.py", language="bash")
        return

    # Tabs
    tab1, tab2, tab3 = st.tabs(["Performance", "Predições", "Análise do Modelo"])

    with tab1:
        st.subheader("Performance do Modelo")

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
            img = load_image(plots_dir / "confusion_matrix.png")
            if img:
                st.image(img, caption="Matriz de Confusão", use_column_width=True)

            img = load_image(plots_dir / "model_comparison.png")
            if img:
                st.image(img, caption="Comparação de Modelos", use_column_width=True)

        with col2:
            img = load_image(plots_dir / "roc_curve.png")
            if img:
                st.image(img, caption="Curva ROC", use_column_width=True)

            img = load_image(plots_dir / "precision_recall_curve.png")
            if img:
                st.image(img, caption="Curva Precision-Recall", use_column_width=True)

    with tab2:
        st.markdown('<h3><i class="fas fa-bullseye icon"></i> Sistema Preditivo Completo</h3>', unsafe_allow_html=True)

        # Sub-tabs para diferentes tipos de predição
        pred_tab1, pred_tab2, pred_tab3, pred_tab4 = st.tabs([
            "Predição Individual",
            "Predição em Lote",
            "Predição de Vendas",
            "Recomendação de Produtos"
        ])

        with pred_tab1:
            from pages_prediction import show_churn_prediction
            show_churn_prediction()

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

        img = load_image(Path("output/plots") / "feature_importance.png")
        if img:
            st.image(img, caption="Importância das Features", use_column_width=True)
        else:
            st.info("Análise de features não disponível")


def show_business_insights(data):
    """Página de Insights de Negócio"""

    st.header("💼 Insights de Negócio")

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

        col1, col2 = st.columns(2)

        with col1:
            img = load_image(plots_dir / "top_products.png")
            if img:
                st.image(img, caption="Top Produtos", use_column_width=True)

        with col2:
            img = load_image(plots_dir / "wine_analysis.png")
            if img:
                st.image(img, caption="Análise de Vinhos", use_column_width=True)

    with tab2:
        st.subheader("Segmentação de Clientes")

        img = load_image(plots_dir / "customer_segmentation.png")
        if img:
            st.image(img, caption="Segmentação por Cidade e Comportamento", use_column_width=True)

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

        with col2:
            nao_assinantes = data[data['assinante_clube'] == 'Não']
            st.metric(
                "👤 Não Assinantes",
                f"{len(nao_assinantes)} clientes",
                f"R$ {nao_assinantes['valor'].sum():,.2f} em vendas"
            )

    with tab3:
        st.subheader("Análise RFM (Recency, Frequency, Monetary)")

        img = load_image(plots_dir / "rfm_analysis.png")
        if img:
            st.image(img, caption="Análise RFM", use_column_width=True)

        st.info("""
        **RFM Analysis:**
        - **Recency**: Quão recentemente o cliente comprou
        - **Frequency**: Com que frequência o cliente compra
        - **Monetary**: Quanto o cliente gasta
        """)

    with tab4:
        st.subheader("💡 Recomendações Estratégicas")

        # Calcular insights
        churn_rate = (data['cancelou_assinatura'] == 'Sim').sum() / len(data) * 100
        avg_ticket = data['valor'].mean()
        top_city = data.groupby('cidade')['valor'].sum().idxmax()

        st.markdown(f"""
        ### 📊 Principais Insights

        1. **Taxa de Churn**: {churn_rate:.1f}%
           - {(data['cancelou_assinatura'] == 'Sim').sum()} clientes cancelaram assinatura
           - **Ação**: Implementar campanha de retenção direcionada

        2. **Ticket Médio**: R$ {avg_ticket:.2f}
           - **Ação**: Oportunidade de upsell e cross-sell

        3. **Melhor Mercado**: {top_city}
           - **Ação**: Replicar estratégias de sucesso em outras cidades

        4. **Vinhos Mais Vendidos**
           - **Ação**: Otimizar estoque dos produtos top

        ### 🎯 Próximas Ações Recomendadas

        - ✅ Criar campanha de retenção para clientes em risco
        - ✅ Implementar programa de fidelidade robusto
        - ✅ Desenvolver estratégia de marketing para {top_city}
        - ✅ Analisar feedback de clientes que cancelaram
        """)


def show_settings():
    """Página de Configurações"""

    st.header("⚙️ Configurações do Sistema")

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

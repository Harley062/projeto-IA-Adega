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
    page_icon="🍷", 
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
    # col1, col2, col3 = st.columns([1, 2, 1])
    # with col2:
        # logo = load_image("assets/adega.png")
        # if logo:
        #     st.image(logo, width=200)
        # st.markdown('<h1 class="main-header">Adega Bom Sabor</h1>', unsafe_allow_html=True)

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
            "Oportunidades de Negócio": "🎯 Análises Estratégicas",
            "Análises Avançadas": "🚀 Ferramentas Pro",
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
    elif page == "Oportunidades de Negócio":
        show_opportunities(data)
    elif page == "Análises Avançadas":
        show_advanced_analytics(data)
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
    # Tentar carregar dados ao vivo — se disponível, usaremos para gerar gráficos dinâmicos
    data_live, _ = load_data()

    has_plots = plots_dir.exists() and len(list(plots_dir.glob("*.png"))) > 0
    if (not has_plots) and (data_live is None or data_live.empty):
        st.warning("⚠️ Gráficos ainda não foram gerados e não há dados processados!")

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

        # Distribuições numéricas (coluna selecionável)
        with col1:
            if data_live is not None and not data_live.empty:
                numeric_cols = data_live.select_dtypes(include=[np.number]).columns.tolist()
                if numeric_cols:
                    selected_num = st.selectbox("Escolha variável numérica:", numeric_cols, key='dist_num')
                    try:
                        fig = px.histogram(
                            data_live,
                            x=selected_num,
                            nbins=30,
                            title=f'Distribuição de {selected_num}',
                            labels={selected_num: selected_num, 'count': 'Frequência'},
                            marginal='box',
                            color_discrete_sequence=['#722F37'],
                            template='plotly_white'
                        )
                        fig.update_traces(marker_line_width=0.5)
                        # formatar eixo de valores como moeda quando aplicável
                        if selected_num.lower() == 'valor':
                            fig.update_yaxes(title_text='Frequência')
                            fig.update_xaxes(tickformat=",.2f")
                        st.plotly_chart(fig, use_container_width=True)
                    except Exception as e:
                        st.error(f"Erro ao gerar histograma: {e}")
                else:
                    img = load_image(plots_dir / "numerical_distributions.png")
                    if img:
                        st.image(img, caption="Distribuições Numéricas - Valores, idades, quantidades", use_container_width=True)
                    else:
                        st.info("Nenhuma coluna numérica disponível para visualizar distribuições.")
            else:
                img = load_image(plots_dir / "numerical_distributions.png")
                if img:
                    st.image(img, caption="Distribuições Numéricas - Valores, idades, quantidades", use_container_width=True)
                else:
                    st.info("Distribuições numéricas não disponíveis")

        # Distribuições categóricas (coluna selecionável)
        with col2:
            if data_live is not None and not data_live.empty:
                cat_cols = data_live.select_dtypes(include=['object', 'category', 'bool']).columns.tolist()
                # filtrar colunas com cardinalidade muito alta
                cat_cols = [c for c in cat_cols if data_live[c].nunique() <= 50]
                if cat_cols:
                    selected_cat = st.selectbox("Escolha variável categórica:", cat_cols, key='dist_cat')
                    try:
                        counts = data_live[selected_cat].value_counts().nlargest(20).reset_index()
                        counts.columns = [selected_cat, 'count']
                        counts['percent'] = counts['count'] / counts['count'].sum() * 100
                        fig = px.bar(
                            counts,
                            x='count',
                            y=selected_cat,
                            orientation='h',
                            title=f'Distribuição de {selected_cat}',
                            labels={'count': 'Contagem', selected_cat: selected_cat},
                            color_discrete_sequence=['#8B4513'],
                            template='plotly_white',
                            hover_data={'count': True, 'percent': ':.1f'}
                        )
                        fig.update_traces(hovertemplate='%{y}: %{x} (%{customdata[1]:.1f}%)')
                        st.plotly_chart(fig, use_container_width=True)
                    except Exception as e:
                        st.error(f"Erro ao gerar gráfico categórico: {e}")
                else:
                    img = load_image(plots_dir / "categorical_distributions.png")
                    if img:
                        st.image(img, caption="Distribuições Categóricas - Cidades, tipos de vinho, assinantes", use_container_width=True)
                    else:
                        st.info("Nenhuma coluna categórica adequada para visualização encontrada.")
            else:
                img = load_image(plots_dir / "categorical_distributions.png")
                if img:
                    st.image(img, caption="Distribuições Categóricas - Cidades, tipos de vinho, assinantes", use_container_width=True)
                else:
                    st.info("Distribuições categóricas não disponíveis")

    with tab2:
        st.subheader("Matriz de Correlação")

        st.info("**O que significa:** Mostra quais variáveis estão relacionadas entre si. Valores próximos de 1 (vermelho) = forte relação positiva, próximos de -1 (azul) = relação negativa.\n\n"
                "**Insight para negócio:** Descubra o que influencia as vendas. Ex: se 'pontuação de engajamento' tem alta correlação com 'valor de compra', invista em engajamento!")

        # Gerar matriz de correlação dinamicamente quando possível
        if data_live is not None and not data_live.empty:
            numeric_cols = data_live.select_dtypes(include=[np.number]).columns.tolist()
            if numeric_cols and len(numeric_cols) > 1:
                try:
                    corr = data_live[numeric_cols].corr()
                    fig = px.imshow(
                        corr,
                        text_auto=True,
                        aspect='auto',
                        color_continuous_scale='RdBu_r',
                        title='Matriz de Correlação',
                        template='plotly_white'
                    )
                    fig.update_layout(margin=dict(l=40, r=40, t=60, b=40))
                    st.plotly_chart(fig, use_container_width=True)
                except Exception as e:
                    st.error(f"Erro ao gerar matriz de correlação: {e}")
            else:
                img = load_image(plots_dir / "correlation_matrix.png")
                if img:
                    st.image(img, caption="Correlação entre Variáveis - Identifique relações importantes", use_container_width=True)
                else:
                    st.info("Não há correlações suficientes para exibir (poucas colunas numéricas).")
        else:
            img = load_image(plots_dir / "correlation_matrix.png")
            if img:
                st.image(img, caption="Correlação entre Variáveis - Identifique relações importantes", use_container_width=True)
            else:
                st.info("Matriz de correlação não disponível")

    with tab3:
        st.subheader("Detecção de Outliers")

        st.info("**O que significa:** Boxplots mostram valores atípicos (pontos fora das 'caixas'). Esses são clientes ou vendas muito diferentes do padrão.\n\n"
                "**Insight para negócio:** Outliers podem ser VIPs (gastam muito mais) ou oportunidades perdidas (gastam muito menos). Analise ambos!")
        # Se os dados processados estiverem disponíveis, gerar boxplots dinâmicos
        if data_live is not None and not data_live.empty:
            numeric_cols = data_live.select_dtypes(include=[np.number]).columns.tolist()
            if numeric_cols:
                fig = go.Figure()
                for c in numeric_cols:
                    # evitar colunas com excesso de valores únicos que poluem o gráfico
                    series = data_live[c].dropna()
                    if series.empty:
                        continue
                    fig.add_trace(go.Box(y=series, name=c))
                fig.update_layout(title='Boxplots - Outliers nas Variáveis Numéricas')
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("Nenhuma coluna numérica detectada nos dados processados para gerar boxplots.")
        else:
            # fallback para imagens estáticas quando não houver dados processados
            img = load_image(plots_dir / "boxplots.png")
            if img:
                st.image(img, caption="Boxplots - Pontos fora das caixas são valores atípicos", use_container_width=True)
            else:
                st.info("Boxplots não disponíveis")

    with tab4:
        st.subheader("Análise Temporal de Vendas")

        st.info("**O que significa:** Mostra como suas vendas evoluem ao longo do tempo - tendências, sazonalidades e padrões.\n\n"
                "**Insight para negócio:** Identifique meses de alta/baixa, planeje estoque e promoções. Aproveite períodos de pico e crie estratégias para períodos fracos!")
        # Tentar gerar análise temporal a partir dos dados processados
        if data_live is not None and not data_live.empty:
            # Detectar coluna de data (heurística: nome contendo 'data'/'date' ou dtype datetime)
            date_col = None
            for c in data_live.columns:
                if 'data' in c.lower() or 'date' in c.lower():
                    date_col = c
                    break

            if date_col is None:
                for c in data_live.columns:
                    try:
                        if np.issubdtype(data_live[c].dtype, np.datetime64):
                            date_col = c
                            break
                    except Exception:
                        continue

            # Tentativa adicional: parse de coluna chamada 'data' se existir
            if date_col is None and 'data' in data_live.columns:
                try:
                    parsed = pd.to_datetime(data_live['data'], errors='coerce')
                    if parsed.notna().any():
                        data_live = data_live.copy()
                        data_live['data_parsed'] = parsed
                        date_col = 'data_parsed'
                except Exception:
                    date_col = None

            if date_col:
                # Verificar se existe coluna de valor para agregar
                if 'valor' in data_live.columns:
                    df = data_live.copy()
                    df[date_col] = pd.to_datetime(df[date_col], errors='coerce')
                    df = df.dropna(subset=[date_col])
                    if df.empty:
                        st.info("Dados de data presentes, mas nenhum registro válido após parsing.")
                    else:
                        # Agregação por mês (período mensais) e plot
                        df['month'] = df[date_col].dt.to_period('M').dt.to_timestamp()
                        sales = df.groupby('month')['valor'].sum().reset_index()
                        if sales.empty:
                            st.info("Não há vendas agregáveis para a análise temporal.")
                        else:
                            fig = px.line(
                                sales,
                                x='month',
                                y='valor',
                                title='Vendas ao Longo do Tempo',
                                labels={'month': 'Mês', 'valor': 'Total Vendas (R$)'}
                            )
                            fig.update_traces(mode='lines+markers')
                            st.plotly_chart(fig, use_container_width=True)
                else:
                    st.info("Não há coluna 'valor' para calcular vendas ao longo do tempo.")
            else:
                st.info("Nenhuma coluna de data detectada nos dados processados para análise temporal.")
        else:
            # fallback para imagem estática quando não houver dados processados
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

    # Seção de predições (removida a aba 'Análise do Modelo')
    st.markdown('<h3><i class="fas fa-bullseye icon"></i> Sistema Preditivo Completo</h3>', unsafe_allow_html=True)

    # Sub-tabs para diferentes tipos de predição
    pred_tab1, pred_tab2, pred_tab3, pred_tab4 = st.tabs([
        "Predição Individual",
        "Predição em Lote",
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

        # Seletor de métrica e top-N
        metric_options = [c for c in ['valor', 'quantidade'] if c in data.columns]
        if not metric_options:
            img = load_image(plots_dir / "top_products.png")
            if img:
                st.image(img, caption="Top Produtos - Mantenha sempre em estoque!", use_container_width=True)
            else:
                st.info("Não há colunas de produto/valor/quantidade disponíveis para análise de produtos.")
        else:
            metric = st.selectbox("Métrica para ranking", metric_options)
            top_n = st.slider("Top N produtos", 5, 30, 10)

            try:
                # Agregar e preparar tabela de ranking
                prod_df = data.groupby('produto_id')[metric].sum().reset_index()
                # tentar encontrar coluna de nome do produto no DataFrame
                name_col = None
                for cand in ['nome_produto', 'nome', 'produto_nome', 'nome_do_produto', 'nome_produto_prod']:
                    if cand in data.columns:
                        name_col = cand
                        break
                if name_col:
                    # construir mapeamento id -> nome
                    prod_names = data.dropna(subset=['produto_id', name_col]).drop_duplicates('produto_id').set_index('produto_id')[name_col].to_dict()
                    prod_df['produto_name'] = prod_df['produto_id'].map(prod_names)
                    # fallback para id como string quando nome ausente
                    prod_df['produto_name'] = prod_df['produto_name'].fillna(prod_df['produto_id'].astype(str))
                else:
                    prod_df['produto_name'] = prod_df['produto_id'].astype(str)
                prod_df = prod_df.sort_values(by=metric, ascending=False).head(top_n).reset_index(drop=True)
                total_metric = prod_df[metric].sum() if prod_df[metric].sum() > 0 else 1
                prod_df['percent'] = prod_df[metric] / total_metric * 100
                prod_df['cum_percent'] = prod_df['percent'].cumsum()
                prod_df['rank'] = prod_df.index + 1

                # Cores para top-3 (medalhas) e cor padrão para os demais
                def rank_color(r):
                    if r == 1:
                        return '#D4AF37'  # ouro
                    if r == 2:
                        return '#C0C0C0'  # prata
                    if r == 3:
                        return '#CD7F32'  # bronze
                    return '#8B4513'    # cor padrão (marrom)

                colors = [rank_color(r) for r in prod_df['rank']]

                # Formatação dos valores para exibição (moeda quando aplicável)
                if metric.lower() == 'valor':
                    display_vals = prod_df[metric].apply(lambda x: f"R$ {x:,.2f}")
                else:
                    display_vals = prod_df[metric].apply(lambda x: f"{int(x):,}")

                # Gráfico vertical (barras em pé) com destaque de ranking
                # ordenar para que o maior fique à direita
                prod_plot = prod_df.sort_values(by=metric, ascending=True).reset_index(drop=True)
                # recriar cores na ordem do plot
                colors_plot = [rank_color(r) for r in prod_plot['rank']]

                # Formatar valores para exibição no texto de anotações na ordem do plot
                if metric.lower() == 'valor':
                    display_vals_plot = prod_plot[metric].apply(lambda x: f"R$ {x:,.2f}")
                else:
                    display_vals_plot = prod_plot[metric].apply(lambda x: f"{int(x):,}")

                fig_prod = go.Figure()
                # usar text + textposition='outside' torna os valores posicionados dinamicamente acima das barras
                fig_prod.add_trace(go.Bar(
                    x=prod_plot['produto_name'].astype(str),
                    y=prod_plot[metric],
                    marker=dict(color=colors_plot),
                    text=display_vals_plot,
                    textposition='outside',
                    textfont=dict(size=11, color='black'),
                    hovertemplate='Produto: %{x}<br>' + f'{metric}: ' + '%{y:,}<br>Participação: %{customdata[0]:.1f}%<extra></extra>',
                    customdata=prod_plot[['percent']].values
                ))
                fig_prod.update_layout(
                    title=f'Top {top_n} Produtos por {metric} (Ranking)',
                    xaxis_title='Produto',
                    yaxis_title=metric,
                    template='plotly_white',
                    margin=dict(b=200),
                    uniformtext_minsize=8,
                    uniformtext_mode='hide'
                )

                # Garantir ordem das categorias no eixo X (maior à direita)
                fig_prod.update_xaxes(categoryorder='array', categoryarray=prod_plot['produto_name'].astype(str).tolist(), tickangle=-45)

                st.plotly_chart(fig_prod, use_container_width=True)

                # Exibir tabela com Rank, Produto, Valor, % e % Acumulada
                prod_table = prod_df.copy()
                prod_table['display_value'] = display_vals
                prod_table['percent'] = prod_table['percent'].round(1)
                prod_table['cum_percent'] = prod_table['cum_percent'].round(1)
                # Preferir mostrar o nome do produto em vez do ID
                if 'produto_name' in prod_table.columns:
                    prod_table = prod_table[['rank', 'produto_name', 'display_value', 'percent', 'cum_percent']]
                    prod_table.columns = ['Rank', 'Produto', metric.capitalize(), '% Participação', '% Acumulado']
                else:
                    prod_table = prod_table[['rank', 'produto_id', 'display_value', 'percent', 'cum_percent']]
                    prod_table.columns = ['Rank', 'Produto ID', metric.capitalize(), '% Participação', '% Acumulado']
                st.dataframe(prod_table, use_container_width=True)

                # Botão para download CSV (opcional)
                # incluir nome na exportação se disponível
                csv_df = prod_df.copy()
                if 'produto_name' in csv_df.columns:
                    csv_df = csv_df[['rank','produto_id','produto_name', metric, 'percent','cum_percent']]
                else:
                    csv_df = csv_df[['rank','produto_id', metric, 'percent','cum_percent']]
                csv = csv_df.to_csv(index=False).encode('utf-8')
                st.download_button(label='📥 Baixar ranking (CSV)', data=csv, file_name=f'top_{top_n}_produtos_{metric}.csv', mime='text/csv')
            except Exception as e:
                st.info(f"Erro ao gerar análise de produtos: {e}")

    with tab2:
        st.subheader("Segmentação de Clientes")

        st.info("**O que significa:** Divide seus clientes em grupos com comportamentos similares.\n\n"
                "**Ação recomendada:** Crie campanhas personalizadas para cada segmento - mensagens diferentes para públicos diferentes!")

        # Construir RFM básico para segmentação
        # Detectar coluna de data
        date_col = None
        for c in data.columns:
            if 'data' in c.lower() or 'date' in c.lower():
                date_col = c
                break
        if date_col is None:
            for c in data.columns:
                try:
                    if np.issubdtype(data[c].dtype, np.datetime64):
                        date_col = c
                        break
                except Exception:
                    continue

        if date_col is None:
            st.info("Nenhuma coluna de data detectada — não é possível calcular segmentação RFM.")
        else:
            df_rfm = data.copy()
            df_rfm[date_col] = pd.to_datetime(df_rfm[date_col], errors='coerce')
            ref_date = df_rfm[date_col].max() if not df_rfm[date_col].isna().all() else pd.Timestamp.today()
            # Agregar por cliente
            rfm = df_rfm.groupby('cliente_id').agg(
                recency_date=(date_col, 'max'),
                frequency=(date_col, 'count'),
                monetary=('valor', 'sum')
            ).reset_index()
            rfm['recency'] = (ref_date - rfm['recency_date']).dt.days

            # Pontuações R,F,M (1-4)
            try:
                rfm['r_score'] = pd.qcut(rfm['recency'], 4, labels=[4,3,2,1]).astype(int)
            except Exception:
                rfm['r_score'] = pd.cut(rfm['recency'], bins=4, labels=[4,3,2,1]).astype(int)
            try:
                rfm['f_score'] = pd.qcut(rfm['frequency'].rank(method='first'), 4, labels=[1,2,3,4]).astype(int)
            except Exception:
                rfm['f_score'] = pd.cut(rfm['frequency'].rank(method='first'), bins=4, labels=[1,2,3,4]).astype(int)
            try:
                rfm['m_score'] = pd.qcut(rfm['monetary'], 4, labels=[1,2,3,4]).astype(int)
            except Exception:
                rfm['m_score'] = pd.cut(rfm['monetary'], bins=4, labels=[1,2,3,4]).astype(int)

            rfm['RFM_Score'] = rfm['r_score'] + rfm['f_score'] + rfm['m_score']

            # Mapear segmentos simples
            def map_segment(score):
                if score >= 10:
                    return 'Champions'
                if score >= 8:
                    return 'Loyal'
                if score >= 6:
                    return 'Potential'
                return 'At Risk'

            rfm['segment'] = rfm['RFM_Score'].apply(map_segment)

            # Visualizações
            col_a, col_b = st.columns([2,1])
            with col_a:
                fig_seg = px.scatter(rfm, x='frequency', y='monetary', color='segment', size='monetary', hover_data=['cliente_id'], title='Segmentação: Frequency x Monetary')
                st.plotly_chart(fig_seg, use_container_width=True)

            with col_b:
                seg_counts = rfm['segment'].value_counts().reset_index()
                seg_counts.columns = ['segment', 'count']
                fig_segbar = px.bar(seg_counts, x='count', y='segment', orientation='h', title='Clientes por Segmento')
                st.plotly_chart(fig_segbar, use_container_width=True)

            st.markdown("#### Top clientes por receita")
            st.dataframe(rfm.sort_values('monetary', ascending=False).head(10)[['cliente_id','monetary','frequency','recency','segment']], use_container_width=True)

        # Mantém métricas por assinantes/nao-assinantes abaixo

    with tab3:
        st.subheader("Análise RFM (Recency, Frequency, Monetary)")

        st.info("""
        **O que é RFM:** Classificação de clientes baseada em 3 fatores:
        - **Recency (Recência):** Há quanto tempo o cliente comprou pela última vez
        - **Frequency (Frequência):** Quantas vezes o cliente compra
        - **Monetary (Monetário):** Quanto dinheiro o cliente gasta

        **Para que serve:** Identifica seus melhores clientes (VIPs), clientes em risco e oportunidades!
        """)
        # Gerar RFM de forma dinâmica (reaproveita cálculo se já feito)
        try:
            # tentar reusar rfm se existir (definido na tab2)
            rfm
        except Exception:
            # recalcular RFM se necessário
            date_col = None
            for c in data.columns:
                if 'data' in c.lower() or 'date' in c.lower():
                    date_col = c
                    break
            if date_col is None:
                for c in data.columns:
                    try:
                        if np.issubdtype(data[c].dtype, np.datetime64):
                            date_col = c
                            break
                    except Exception:
                        continue

            if date_col is None:
                st.info("Não há dados de data para calcular RFM.")
            else:
                df_rfm = data.copy()
                df_rfm[date_col] = pd.to_datetime(df_rfm[date_col], errors='coerce')
                ref_date = df_rfm[date_col].max() if not df_rfm[date_col].isna().all() else pd.Timestamp.today()
                rfm = df_rfm.groupby('cliente_id').agg(recency_date=(date_col,'max'), frequency=(date_col,'count'), monetary=('valor','sum')).reset_index()
                rfm['recency'] = (ref_date - rfm['recency_date']).dt.days
                # scores
                try:
                    rfm['r_score'] = pd.qcut(rfm['recency'], 4, labels=[4,3,2,1]).astype(int)
                except Exception:
                    rfm['r_score'] = pd.cut(rfm['recency'], bins=4, labels=[4,3,2,1]).astype(int)
                try:
                    rfm['f_score'] = pd.qcut(rfm['frequency'].rank(method='first'), 4, labels=[1,2,3,4]).astype(int)
                except Exception:
                    rfm['f_score'] = pd.cut(rfm['frequency'].rank(method='first'), bins=4, labels=[1,2,3,4]).astype(int)
                try:
                    rfm['m_score'] = pd.qcut(rfm['monetary'], 4, labels=[1,2,3,4]).astype(int)
                except Exception:
                    rfm['m_score'] = pd.cut(rfm['monetary'], bins=4, labels=[1,2,3,4]).astype(int)
                rfm['RFM_Score'] = rfm['r_score'] + rfm['f_score'] + rfm['m_score']

        # Visualizações RFM
        if 'rfm' in locals() and not rfm.empty:
            st.markdown("#### Distribuição de Scores RFM")
            fig_hist = px.histogram(rfm, x='RFM_Score', nbins=12, title='Distribuição de RFM Score')
            st.plotly_chart(fig_hist, use_container_width=True)

            st.markdown("#### Médias por Score")
            rfm_stats = rfm.groupby('RFM_Score')[['recency','frequency','monetary']].mean().reset_index()
            fig_heat = px.imshow(rfm_stats.set_index('RFM_Score').T, text_auto=True, title='Médias R/F/M por RFM Score')
            st.plotly_chart(fig_heat, use_container_width=True)
        else:
            st.info("RFM não disponível para visualização.")

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

        **Promising (Frequency baixa, Monetary crescendo):** 🌱
        - Novos clientes com potencial
        - **Ação:** Nurturing, programa de fidelidade, conteúdo educativo sobre vinhos
        """)

    with tab4:
        st.subheader("💡 Recomendações Estratégicas Acionáveis")

        # Calcular insights detalhados (robusto em relação ao schema)
        # Valores padrão / seguros caso colunas não existam
        taxa_cancelamento = 0.0
        total_cancelamentos = 0
        avg_ticket = float(data['valor'].mean()) if 'valor' in data.columns else 0.0
        top_city = None
        top_city_revenue = 0.0

        if 'cancelou_assinatura' in data.columns:
            total_cancelamentos = int((data['cancelou_assinatura'] == 'Sim').sum())
            taxa_cancelamento = (total_cancelamentos / len(data) * 100) if len(data) > 0 else 0.0

        if 'cidade' in data.columns and 'valor' in data.columns:
            city_sales = data.groupby('cidade')['valor'].sum()
            if not city_sales.empty:
                top_city = city_sales.idxmax()
                top_city_revenue = float(city_sales.max())

        # Análise de produtos
        top_products = None
        if 'produto_id' in data.columns and 'quantidade' in data.columns:
            top_products = data.groupby('produto_id')['quantidade'].sum().nlargest(3)

        # Análise de assinantes
        assinantes_count = 0
        assinantes_revenue = 0.0
        total_revenue = float(data['valor'].sum()) if 'valor' in data.columns else 0.0
        if 'assinante_clube' in data.columns and 'valor' in data.columns:
            assinantes = data[data['assinante_clube'] == 'Sim']
            assinantes_count = len(assinantes)
            assinantes_revenue = float(assinantes['valor'].sum())
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

        # Visualizações rápidas e métricas (dinâmicas)
        st.markdown("### 📊 Visualizações Rápidas")

        vcol1, vcol2, vcol3 = st.columns([1,1,1])

        with vcol1:
            st.metric("Taxa de Cancelamento", f"{taxa_cancelamento:.1f}%")
            st.metric("Total Cancelamentos", f"{total_cancelamentos}")
            st.metric("Ticket Médio", f"R$ {avg_ticket:,.2f}")

        with vcol2:
            if 'cidade' in data.columns and 'valor' in data.columns:
                try:
                    city_sales = data.groupby('cidade')['valor'].sum().sort_values(ascending=False).head(10)
                    fig_city = px.bar(
                        x=city_sales.values,
                        y=city_sales.index,
                        orientation='h',
                        title='Top 10 Cidades por Vendas',
                        labels={'x': 'Total Vendas (R$)', 'y': 'Cidade'},
                        color_discrete_sequence=['#8B4513'],
                        template='plotly_white'
                    )
                    fig_city.update_traces(hovertemplate='Cidade: %{y}<br>Vendas: R$ %{x:,.2f}')
                    fig_city.update_layout(margin=dict(l=100))
                    st.plotly_chart(fig_city, use_container_width=True)
                except Exception as e:
                    st.info(f"Não foi possível gerar gráfico de cidades: {e}")
            else:
                st.info("Dados de cidade/valor ausentes para gráfico de cidades")

        with vcol3:
            if 'assinante_clube' in data.columns and 'valor' in data.columns:
                try:
                    contrib = data.groupby('assinante_clube')['valor'].sum().reset_index()
                    fig_pie = px.pie(contrib, names='assinante_clube', values='valor', title='Participação por Assinante (Receita)')
                    st.plotly_chart(fig_pie, use_container_width=True)
                except Exception as e:
                    st.info(f"Não foi possível gerar gráfico de participação: {e}")
            else:
                st.info("Dados de assinantes/valor ausentes para participação")

        # Top produtos
        if 'produto_id' in data.columns and 'quantidade' in data.columns:
            try:
                prod_df_q = data.groupby('produto_id')['quantidade'].sum().reset_index()
                prod_df_q = prod_df_q.sort_values('quantidade', ascending=False).head(10).reset_index(drop=True)
                # mapear para nome do produto quando disponível
                name_col_q = None
                for cand in ['nome_produto', 'nome', 'produto_nome', 'nome_do_produto', 'nome_produto_prod']:
                    if cand in data.columns:
                        name_col_q = cand
                        break
                if name_col_q:
                    prod_names_q = data.dropna(subset=['produto_id', name_col_q]).drop_duplicates('produto_id').set_index('produto_id')[name_col_q].to_dict()
                    prod_df_q['produto_name'] = prod_df_q['produto_id'].map(prod_names_q)
                    prod_df_q['produto_name'] = prod_df_q['produto_name'].fillna(prod_df_q['produto_id'].astype(str))
                else:
                    prod_df_q['produto_name'] = prod_df_q['produto_id'].astype(str)
                total_q = prod_df_q['quantidade'].sum() if prod_df_q['quantidade'].sum() > 0 else 1
                prod_df_q['percent'] = prod_df_q['quantidade'] / total_q * 100
                prod_df_q['rank'] = prod_df_q.index + 1

                def rank_color_q(r):
                    if r == 1:
                        return '#D4AF37'
                    if r == 2:
                        return '#C0C0C0'
                    if r == 3:
                        return '#CD7F32'
                    return '#722F37'

                colors_q = [rank_color_q(r) for r in prod_df_q['rank']]

                # Gráfico vertical para quantidade vendida, ordenado para maior à direita
                prod_plot_q = prod_df_q.sort_values(by='quantidade', ascending=True).reset_index(drop=True)
                colors_plot_q = [rank_color_q(r) for r in prod_plot_q['rank']]

                fig_prod_q = go.Figure()
                # formatar valores como texto para exibir acima das barras
                display_q = prod_plot_q['quantidade'].apply(lambda x: f"{int(x):,}")
                fig_prod_q.add_trace(go.Bar(
                    x=prod_plot_q['produto_name'].astype(str),
                    y=prod_plot_q['quantidade'],
                    marker=dict(color=colors_plot_q),
                    text=display_q,
                    textposition='outside',
                    textfont=dict(size=11, color='black'),
                    hovertemplate='Produto: %{x}<br>Quantidade: %{y}<extra></extra>'
                ))
                fig_prod_q.update_layout(title='Top Produtos por Quantidade Vendida', xaxis_title='Produto ID', yaxis_title='Quantidade', template='plotly_white', margin=dict(b=200))
                fig_prod_q.update_xaxes(categoryorder='array', categoryarray=prod_plot_q['produto_id'].astype(str).tolist(), tickangle=-45)

                st.plotly_chart(fig_prod_q, use_container_width=True)
                # Mostrar tabela simplificada com rank
                prod_table_q = prod_df_q[['rank','produto_name','quantidade','percent']].copy() if 'produto_name' in prod_df_q.columns else prod_df_q[['rank','produto_id','quantidade','percent']].copy()
                prod_table_q['percent'] = prod_table_q['percent'].round(1)
                if 'produto_name' in prod_table_q.columns:
                    prod_table_q.columns = ['Rank','Produto','Quantidade','% Participação']
                else:
                    prod_table_q.columns = ['Rank','Produto ID','Quantidade','% Participação']
                st.dataframe(prod_table_q, use_container_width=True)
            except Exception as e:
                st.info(f"Não foi possível gerar gráfico de produtos: {e}")
        else:
            st.info("Dados de produto/quantidade ausentes para análise de mix de produtos")

        # Tendência de vendas (se houver coluna de data)
        date_col = None
        for c in data.columns:
            if 'data' in c.lower() or 'date' in c.lower():
                date_col = c
                break
        if date_col is None:
            for c in data.columns:
                try:
                    if np.issubdtype(data[c].dtype, np.datetime64):
                        date_col = c
                        break
                except Exception:
                    continue

        if date_col is not None and 'valor' in data.columns:
            try:
                df_t = data.copy()
                df_t[date_col] = pd.to_datetime(df_t[date_col], errors='coerce')
                df_t = df_t.dropna(subset=[date_col])
                if not df_t.empty:
                    df_t['month'] = df_t[date_col].dt.to_period('M').dt.to_timestamp()
                    sales = df_t.groupby('month')['valor'].sum().reset_index()
                    if sales.empty:
                        st.info("Não há vendas agregáveis para a análise temporal.")
                    else:
                        fig = px.line(
                            sales,
                            x='month',
                            y='valor',
                            title='Vendas ao Longo do Tempo',
                            labels={'month': 'Mês', 'valor': 'Total Vendas (R$)'},
                            template='plotly_white'
                        )
                        fig.update_traces(mode='lines+markers', hovertemplate='Mês: %{x|%Y-%m}<br>Vendas: R$ %{y:,.2f}')
                        # adicionar média móvel 3 períodos
                        try:
                            sales['rolling_3m'] = sales['valor'].rolling(window=3, min_periods=1).mean()
                            fig.add_scatter(x=sales['month'], y=sales['rolling_3m'], mode='lines', name='Média Móvel 3M', line=dict(dash='dash', color='#FF7F0E'))
                        except Exception:
                            pass
                        fig.update_xaxes(rangeslider_visible=True)
                        st.plotly_chart(fig, use_container_width=True)
            except Exception as e:
                st.info(f"Não foi possível gerar análise temporal: {e}")
        sections = []
        if 'valor' in data.columns:
            sections.append(('promo', '📢 Promoções'))
        if 'cidade' in data.columns and 'valor' in data.columns:
            sections.append(('expansao', '🌎 Expansão'))
        if 'produto_id' in data.columns and 'quantidade' in data.columns:
            sections.append(('produto', '📦 Mix de Produtos'))
        if 'cancelou_assinatura' in data.columns or 'assinante_clube' in data.columns:
            sections.append(('retencao', '🔒 Retenção'))

        # Se nada relevante estiver presente, mostrar uma visão geral
        if not sections:
            sections = [('overview', '🔍 Geral')]

        tabs = st.tabs([label for _, label in sections])

        for (key, _), tab in zip(sections, tabs):
            with tab:
                if key == 'promo':
                    st.markdown(f"""
                    #### Quando e Como Fazer Promoções

                    **1. Promoção de Ticket Médio (Atual: R$ {avg_ticket:.2f})**
                    - **Quando:** Quinzenalmente
                    - **Como:** "Compre 2, leve 3" ou desconto progressivo
                    - **Objetivo:** Aumentar ticket médio
                    """)

                    if 'valor' in data.columns:
                        st.info("Sugestão: Segmentar promoções por faixa de ticket para maximizar conversão.")
                    else:
                        st.info("Sem dados de valor; foque em promoções por frequência ou produtos.")

                elif key == 'expansao':
                    if top_city:
                        st.markdown(f"""
                        #### Estratégia de Expansão Geográfica

                        **Seu Melhor Mercado Atual: {top_city} (R$ {top_city_revenue:,.2f})**

                        **Ações:**
                        - Consolidar presença em {top_city}
                        - Replicar estratégias em cidades semelhantes
                        """)
                    else:
                        st.info("Necessário dados de cidade e valor para gerar plano de expansão geográfica.")

                elif key == 'produto':
                    st.markdown("#### Otimização de Mix de Produtos")
                    if top_products is not None and not top_products.empty:
                        st.markdown("**Top produtos por quantidade:**")
                        for pid, q in top_products.items():
                            st.write(f"- Produto {pid}: {int(q)} unidades")
                        st.info("Ação: garantir estoque dos best-sellers e criar combos com margem.")
                    else:
                        st.info("Sem dados estruturados de produto/quantidade para análises detalhadas.")

                elif key == 'retencao':
                    st.markdown("#### Programa de Retenção e Fidelização")
                    st.markdown(f"**Situação atual: {total_cancelamentos} cancelamentos (taxa {taxa_cancelamento:.1f}%)**")
                    st.markdown("**Recomendações rápidas:**")
                    st.write("- Rodar modelos preditivos semanalmente para detectar clientes em risco")
                    st.write("- Criar automações de reativação (cupons, e-mails personalizados)")
                    if assinantes_count:
                        st.write(f"- Focar em fidelização: {assinantes_count} assinantes gerando {assinante_contribution:.1f}% da receita")
                    else:
                        st.write("- Incentivar conversão para assinaturas com trials e benefícios")

                elif key == 'overview':
                    st.markdown("#### Visão Geral de Oportunidades")
                    st.info("Não há colunas suficientes para sugestões específicas. Considere processar os dados em '⚙️ Atualizar Dados'.")

        st.divider()

        # Checklist Semanal
        st.markdown("### ✅ Checklist Semanal")

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


def show_opportunities(data):
    """Página de Oportunidades de Negócio com 3 análises estratégicas"""

    st.header("🎯 Oportunidades de Negócio - Análises Estratégicas")

    st.info("""
    **Descubra oportunidades concretas para aumentar suas vendas!**

    Esta seção oferece 3 análises práticas:
    - **📅 Sazonalidade:** Identifique padrões de venda e planeje seu estoque
    - **📦 Gestão de Estoque:** Detecte produtos parados e otimize giro
    - **👑 Clientes VIP:** Foque nos clientes mais valiosos e evite perdê-los
    """)

    # Importar os analisadores
    try:
        import sys
        from pathlib import Path
        sys.path.append(str(Path(__file__).parent / 'src'))
        from visualization.advanced_analytics import SeasonalityAnalyzer, InventoryManager, VIPAnalyzer
    except ImportError as e:
        st.error(f"Erro ao carregar módulo de análises avançadas: {e}")
        return

    # Criar tabs para as 3 análises
    tab1, tab2, tab3 = st.tabs([
        "📅 Análise de Sazonalidade",
        "📦 Gestão de Estoque",
        "👑 Clientes VIP"
    ])

    with tab1:
        st.subheader("📅 Análise de Sazonalidade e Previsão de Demanda")

        st.markdown("""
        **O que você vai descobrir:**
        - Quais meses vendem mais e vendem menos
        - Padrões de venda por produto
        - Previsão de demanda para os próximos meses
        - Quando preparar estoque extra
        """)

        try:
            analyzer = SeasonalityAnalyzer(data)

            # Padrões mensais
            monthly = analyzer.get_monthly_patterns()

            if not monthly.empty:
                st.markdown("#### 📊 Vendas Mensais ao Longo do Tempo")

                # Gráfico de vendas mensais
                fig = go.Figure()

                for ano in monthly['ano'].unique():
                    df_ano = monthly[monthly['ano'] == ano]
                    fig.add_trace(go.Scatter(
                        x=df_ano['mes'],
                        y=df_ano['receita'],
                        mode='lines+markers',
                        name=f'{int(ano)}',
                        hovertemplate='%{x}/%{name}<br>Receita: R$ %{y:,.2f}<extra></extra>'
                    ))

                fig.update_layout(
                    title='Receita por Mês',
                    xaxis_title='Mês',
                    yaxis_title='Receita (R$)',
                    template='plotly_white',
                    hovermode='x unified'
                )

                st.plotly_chart(fig, use_container_width=True)

                # Identificar meses de pico
                peaks = analyzer.identify_peak_months()

                if peaks:
                    col1, col2, col3 = st.columns(3)

                    with col1:
                        st.metric(
                            "🔥 Melhor Mês",
                            peaks.get('melhor_mes', 'N/A'),
                            f"R$ {peaks.get('melhor_receita', 0):,.2f}"
                        )

                    with col2:
                        st.metric(
                            "📉 Pior Mês",
                            peaks.get('pior_mes', 'N/A'),
                            f"R$ {peaks.get('pior_receita', 0):,.2f}"
                        )

                    with col3:
                        st.metric(
                            "📊 Variação",
                            f"{peaks.get('variacao_percentual', 0):.1f}%",
                            "diferença pico/baixa"
                        )

                    # Recomendações baseadas em sazonalidade
                    st.markdown("#### 💡 Recomendações Estratégicas")

                    melhor_mes = peaks.get('melhor_mes')
                    pior_mes = peaks.get('pior_mes')

                    st.success(f"""
                    **✅ {melhor_mes} é seu mês de ouro!**
                    - Prepare estoque extra 2 semanas antes
                    - Lance produtos premium neste período
                    - Invista mais em marketing em {melhor_mes}
                    - Contrate reforço temporário se necessário
                    """)

                    st.warning(f"""
                    **⚠️ {pior_mes} precisa de atenção!**
                    - Faça promoções agressivas em {pior_mes}
                    - Crie campanhas temáticas para aquecer vendas
                    - Ofereça combos/kits com desconto
                    - Use este período para limpar estoque parado
                    """)

                # Previsão de demanda
                st.markdown("#### 🔮 Previsão de Demanda (Próximos 3 Meses)")

                forecast = analyzer.demand_forecast_simple(months_ahead=3)

                if not forecast.empty:
                    forecast['mes_ano'] = forecast.apply(lambda x: f"{int(x['mes'])}/{int(x['ano'])}", axis=1)

                    col1, col2 = st.columns(2)

                    with col1:
                        st.dataframe(
                            forecast[['mes_ano', 'receita_prevista', 'unidades_previstas']].rename(columns={
                                'mes_ano': 'Mês/Ano',
                                'receita_prevista': 'Receita Prevista (R$)',
                                'unidades_previstas': 'Unidades Previstas'
                            }),
                            use_container_width=True
                        )

                    with col2:
                        st.info("""
                        **Como usar esta previsão:**

                        ✅ **Planeje compras:** Peça estoque com antecedência baseado nas unidades previstas

                        ✅ **Gestão de caixa:** Prepare o capital de giro necessário

                        ✅ **Equipe:** Ajuste escala de funcionários conforme demanda

                        📝 **Nota:** Esta é uma previsão simples baseada em média móvel. Para maior precisão, acompanhe tendências semanalmente.
                        """)
                else:
                    st.info("Dados insuficientes para gerar previsão (mínimo 3 meses de histórico)")

                # Sazonalidade por produto
                st.markdown("#### 🍷 Sazonalidade por Produto")

                product_season = analyzer.product_seasonality()

                if not product_season.empty:
                    # Top 10 produtos com seu mês de pico
                    top_seasonal = product_season.nlargest(10, 'quantidade_pico')

                    meses_nome = {
                        1: 'Janeiro', 2: 'Fevereiro', 3: 'Março', 4: 'Abril',
                        5: 'Maio', 6: 'Junho', 7: 'Julho', 8: 'Agosto',
                        9: 'Setembro', 10: 'Outubro', 11: 'Novembro', 12: 'Dezembro'
                    }

                    top_seasonal['mes_nome'] = top_seasonal['mes_pico'].map(meses_nome)

                    # Adicionar nome do produto se disponível
                    if 'nome' in data.columns:
                        product_names = data.groupby('produto_id')['nome'].first().reset_index()
                        top_seasonal = top_seasonal.merge(product_names, on='produto_id', how='left')
                        display_col = 'nome'
                    else:
                        top_seasonal['nome'] = top_seasonal['produto_id'].astype(str)
                        display_col = 'nome'

                    st.dataframe(
                        top_seasonal[[display_col, 'mes_nome', 'quantidade_pico']].rename(columns={
                            display_col: 'Produto',
                            'mes_nome': 'Mês de Pico',
                            'quantidade_pico': 'Quantidade no Pico'
                        }),
                        use_container_width=True
                    )

                    st.success("""
                    💡 **Como usar:**
                    - Garanta estoque extra desses produtos 1 mês antes do pico
                    - Crie campanhas de marketing focadas nesses produtos no mês de pico
                    - Negocie melhores preços com fornecedores comprando antecipado
                    """)
                else:
                    st.info("Não há dados suficientes para análise de sazonalidade por produto")
            else:
                st.warning("Não há dados de data para análise de sazonalidade. Verifique se a coluna 'data_compra' está presente.")

        except Exception as e:
            st.error(f"Erro ao gerar análise de sazonalidade: {str(e)}")

    with tab2:
        st.subheader("📦 Gestão Inteligente de Estoque")

        st.markdown("""
        **O que você vai descobrir:**
        - Produtos parados (sem venda há muito tempo)
        - Taxa de giro de cada produto
        - Sugestões de promoções para liquidar estoque
        - Alertas de produtos em risco
        """)

        try:
            inventory = InventoryManager(data, dias_estoque_parado=30)

            # Alertas gerais
            alerts = inventory.stock_alerts()

            st.markdown("#### 🚨 Alertas de Estoque")

            col1, col2, col3, col4 = st.columns(4)

            with col1:
                st.metric(
                    "Produtos Parados",
                    alerts.get('produtos_parados', 0),
                    "≥30 dias sem venda"
                )

            with col2:
                st.metric(
                    "Receita em Risco",
                    f"R$ {alerts.get('receita_em_risco', 0):,.2f}",
                    "potencial perdido"
                )

            with col3:
                st.metric(
                    "Alto Giro",
                    alerts.get('produtos_alto_giro', 0),
                    "produtos"
                )

            with col4:
                st.metric(
                    "Baixo Giro",
                    alerts.get('produtos_baixo_giro', 0),
                    "produtos"
                )

            # Produtos parados
            st.markdown("#### ⏸️ Produtos Parados (Sem Venda ≥30 Dias)")

            slow_products = inventory.identify_slow_products()

            if not slow_products.empty:
                # Mostrar top 20 produtos parados
                display_cols = ['produto_id', 'dias_parado']
                rename_cols = {'produto_id': 'Produto ID', 'dias_parado': 'Dias Parado'}

                if 'nome' in slow_products.columns:
                    display_cols.insert(1, 'nome')
                    rename_cols['nome'] = 'Produto'

                if 'receita_potencial_perdida' in slow_products.columns:
                    display_cols.append('receita_potencial_perdida')
                    rename_cols['receita_potencial_perdida'] = 'Receita Potencial Perdida (R$)'

                st.dataframe(
                    slow_products.head(20)[display_cols].rename(columns=rename_cols),
                    use_container_width=True
                )

                st.error(f"""
                **⚠️ AÇÃO URGENTE NECESSÁRIA!**

                Você tem {len(slow_products)} produtos parados por 30+ dias.
                Receita potencial perdida: R$ {alerts.get('receita_em_risco', 0):,.2f}

                **O que fazer AGORA:**
                1. 🔥 Criar promoção "Queima de Estoque" para os top 10 produtos parados
                2. 📧 Enviar email marketing destacando esses produtos
                3. 🎁 Criar combos/kits incluindo produtos parados
                4. 💰 Considerar desconto de 15-30% para giro rápido
                """)
            else:
                st.success("✅ Ótimo! Nenhum produto parado detectado.")

            # Taxa de giro
            st.markdown("#### 🔄 Taxa de Giro de Estoque")

            st.info("""
            **O que é Giro de Estoque:**
            - **Alto Giro** (≥10/mês): Produtos que vendem muito rápido - mantenha estoque sempre!
            - **Médio Giro** (5-10/mês): Produtos com venda regular - monitore semanalmente
            - **Baixo Giro** (<5/mês): Produtos que vendem devagar - candidatos a promoção
            """)

            turnover = inventory.calculate_turnover_rate()

            if not turnover.empty:
                # Gráfico de giro por classificação
                turnover_summary = turnover['classificacao'].value_counts().reset_index()
                turnover_summary.columns = ['classificacao', 'quantidade']

                fig = px.pie(
                    turnover_summary,
                    names='classificacao',
                    values='quantidade',
                    title='Distribuição de Produtos por Taxa de Giro',
                    color_discrete_map={
                        'Alto Giro': '#28a745',
                        'Médio Giro': '#ffc107',
                        'Baixo Giro': '#dc3545'
                    }
                )

                st.plotly_chart(fig, use_container_width=True)

                # Tabela detalhada
                col1, col2 = st.columns(2)

                with col1:
                    st.markdown("**🔥 Top 10 - Alto Giro (Estrelas)**")
                    high_turnover = turnover[turnover['classificacao'] == 'Alto Giro'].head(10)

                    if not high_turnover.empty:
                        display_cols = ['produto_id', 'giro_mensal']
                        if 'nome' in high_turnover.columns:
                            display_cols.insert(1, 'nome')

                        st.dataframe(
                            high_turnover[display_cols],
                            use_container_width=True
                        )

                        st.success("💡 **Ação:** NUNCA deixe esses produtos faltarem! São seus best-sellers.")
                    else:
                        st.info("Nenhum produto com alto giro identificado.")

                with col2:
                    st.markdown("**⚠️ Top 10 - Baixo Giro (Atenção)**")
                    low_turnover = turnover[turnover['classificacao'] == 'Baixo Giro'].head(10)

                    if not low_turnover.empty:
                        display_cols = ['produto_id', 'giro_mensal']
                        if 'nome' in low_turnover.columns:
                            display_cols.insert(1, 'nome')

                        st.dataframe(
                            low_turnover[display_cols],
                            use_container_width=True
                        )

                        st.warning("💡 **Ação:** Avalie se vale a pena manter esses produtos. Considere promoção ou descontinuar.")
                    else:
                        st.success("Ótimo! Nenhum produto com baixo giro extremo.")
            else:
                st.info("Não há dados suficientes para calcular taxa de giro.")

            # Sugestões de promoção
            st.markdown("#### 🎯 Sugestões de Promoção")

            promo_suggestions = inventory.suggest_promotions()

            if not promo_suggestions.empty:
                st.markdown(f"**Encontramos {len(promo_suggestions)} produtos que precisam de promoção urgente!**")

                display_cols = ['produto_id', 'dias_parado', 'desconto_sugerido', 'urgencia']
                rename_cols = {
                    'produto_id': 'Produto ID',
                    'dias_parado': 'Dias Parado',
                    'desconto_sugerido': 'Desconto Sugerido',
                    'urgencia': 'Urgência'
                }

                if 'nome' in promo_suggestions.columns:
                    display_cols.insert(1, 'nome')
                    rename_cols['nome'] = 'Produto'

                if 'receita_potencial_perdida' in promo_suggestions.columns:
                    display_cols.append('receita_potencial_perdida')
                    rename_cols['receita_potencial_perdida'] = 'Receita em Risco (R$)'

                st.dataframe(
                    promo_suggestions[display_cols].rename(columns=rename_cols),
                    use_container_width=True
                )

                # Plano de ação
                urgentes = len(promo_suggestions[promo_suggestions['urgencia'] == 'URGENTE'])

                if urgentes > 0:
                    st.error(f"""
                    **🔥 {urgentes} PRODUTOS EM SITUAÇÃO URGENTE!**

                    **Plano de Ação - Próximos 7 Dias:**

                    **Dia 1-2:** Criar campanha de email marketing "Liquidação Relâmpago"
                    - Destacar os {min(5, urgentes)} produtos mais urgentes
                    - Desconto de 20-30%
                    - Frete grátis acima de 2 unidades

                    **Dia 3-5:** Posts nas redes sociais
                    - Mostrar produtos em promoção
                    - Stories com countdown de oferta
                    - Engajamento com sorteios

                    **Dia 6-7:** Promoção de combo
                    - "Leve 3, Pague 2" nos produtos parados
                    - Combinar com best-sellers para aumentar ticket

                    📊 **Meta:** Reduzir estoque parado em 50% em 2 semanas
                    """)

                # Botão de download
                csv = promo_suggestions.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label='📥 Baixar lista completa de produtos para promoção (CSV)',
                    data=csv,
                    file_name='produtos_promocao.csv',
                    mime='text/csv'
                )
            else:
                st.success("✅ Excelente! Seu estoque está girando bem. Nenhuma promoção urgente necessária.")

        except Exception as e:
            st.error(f"Erro ao gerar análise de estoque: {str(e)}")

    with tab3:
        st.subheader("👑 Análise de Clientes VIP")

        st.markdown("""
        **O que você vai descobrir:**
        - Quem são seus clientes mais valiosos (Top 20%)
        - VIPs inativos que podem estar em risco
        - Programa de fidelidade com tiers e benefícios
        - Quanto os VIPs contribuem para sua receita
        """)

        try:
            vip_analyzer = VIPAnalyzer(data)

            # Contribuição dos VIPs
            st.markdown("#### 💰 Contribuição dos VIPs para o Negócio")

            contribution = vip_analyzer.vip_contribution_analysis()

            if contribution:
                col1, col2, col3, col4 = st.columns(4)

                with col1:
                    st.metric(
                        "Clientes VIP",
                        contribution.get('num_vips', 0),
                        f"{contribution.get('percent_vips', 0):.1f}% do total"
                    )

                with col2:
                    st.metric(
                        "Receita VIPs",
                        f"R$ {contribution.get('receita_vips', 0):,.2f}",
                        f"{contribution.get('percent_receita_vips', 0):.1f}% do total"
                    )

                with col3:
                    st.metric(
                        "Ticket Médio VIP",
                        f"R$ {contribution.get('ticket_medio_vip', 0):.2f}"
                    )

                with col4:
                    st.metric(
                        "Ticket Médio Geral",
                        f"R$ {contribution.get('ticket_medio_geral', 0):.2f}"
                    )

                # Insight da Regra 80/20
                percent_receita = contribution.get('percent_receita_vips', 0)

                if percent_receita >= 70:
                    st.success(f"""
                    **🎯 Regra de Pareto Confirmada!**

                    Seus top 20% clientes geram {percent_receita:.1f}% da receita!

                    **Isso significa:**
                    - ✅ Seu negócio está saudável e previsível
                    - ✅ Você sabe quem são seus clientes-chave
                    - ⚠️ CUIDADO: Perder um VIP tem impacto ENORME

                    **Prioridade máxima:** Manter esses VIPs felizes e ativos!
                    """)
                else:
                    st.info(f"""
                    **📊 Análise da Base de Clientes**

                    Seus top 20% geram {percent_receita:.1f}% da receita.

                    **Oportunidade:** Trabalhar para aumentar o valor dos VIPs!
                    - Criar programa de benefícios exclusivos
                    - Oferecer produtos premium
                    - Eventos e degustações VIP
                    """)

            # Listagem de VIPs
            st.markdown("#### 👑 Seus Clientes VIP (Top 20%)")

            vips = vip_analyzer.identify_vip_customers(top_percent=20)

            if not vips.empty:
                # Distribuição por tier
                tier_counts = vips['tier_vip'].value_counts()

                col1, col2 = st.columns([2, 1])

                with col1:
                    # Tabela de VIPs
                    display_cols = ['cliente_id', 'tier_vip', 'receita_total', 'num_compras', 'ticket_medio']
                    rename_cols = {
                        'cliente_id': 'Cliente ID',
                        'tier_vip': 'Tier',
                        'receita_total': 'Receita Total (R$)',
                        'num_compras': 'Num. Compras',
                        'ticket_medio': 'Ticket Médio (R$)'
                    }

                    if 'nome' in vips.columns:
                        display_cols.insert(1, 'nome')
                        rename_cols['nome'] = 'Nome'

                    if 'cidade' in vips.columns:
                        display_cols.append('cidade')
                        rename_cols['cidade'] = 'Cidade'

                    st.dataframe(
                        vips.head(30)[display_cols].rename(columns=rename_cols),
                        use_container_width=True
                    )

                with col2:
                    # Gráfico de pizza dos tiers
                    tier_df = pd.DataFrame({
                        'tier': tier_counts.index,
                        'quantidade': tier_counts.values
                    })

                    fig = px.pie(
                        tier_df,
                        names='tier',
                        values='quantidade',
                        title='VIPs por Tier',
                        color_discrete_map={
                            'Platinum': '#E5E4E2',
                            'Gold': '#FFD700',
                            'Silver': '#C0C0C0'
                        }
                    )

                    st.plotly_chart(fig, use_container_width=True)

                # Botão de download
                csv = vips.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label='📥 Baixar lista completa de VIPs (CSV)',
                    data=csv,
                    file_name='clientes_vip.csv',
                    mime='text/csv'
                )
            else:
                st.info("Não há dados suficientes para identificar VIPs.")

            # VIPs inativos
            st.markdown("#### ⚠️ VIPs em Risco (Inativos ≥30 Dias)")

            inactive_vips = vip_analyzer.detect_inactive_vips(days_inactive=30)

            if not inactive_vips.empty:
                st.error(f"""
                **🚨 ALERTA CRÍTICO!**

                Você tem {len(inactive_vips)} VIPs inativos há 30+ dias!

                Esses clientes representam R$ {inactive_vips['receita_total'].sum():,.2f} em receita histórica.
                Perder esses clientes pode significar uma queda significativa no faturamento!
                """)

                # Tabela de VIPs inativos
                display_cols = ['cliente_id', 'dias_inativo', 'risco_churn', 'receita_total', 'acao_sugerida']
                rename_cols = {
                    'cliente_id': 'Cliente ID',
                    'dias_inativo': 'Dias Inativo',
                    'risco_churn': 'Risco',
                    'receita_total': 'Receita Total (R$)',
                    'acao_sugerida': 'Ação Sugerida'
                }

                if 'nome' in inactive_vips.columns:
                    display_cols.insert(1, 'nome')
                    rename_cols['nome'] = 'Nome'

                st.dataframe(
                    inactive_vips[display_cols].rename(columns=rename_cols),
                    use_container_width=True
                )

                # Plano de reativação
                criticos = len(inactive_vips[inactive_vips['risco_churn'] == 'CRÍTICO'])

                st.markdown(f"""
                #### 🎯 Plano de Reativação Urgente

                **Prioridade 1 - {criticos} VIPs em Risco CRÍTICO (90+ dias):**

                **Dia 1:**
                - 📞 Ligar PESSOALMENTE para cada um
                - Script: "Sentimos sua falta! Preparamos uma oferta exclusiva..."
                - Oferecer: Desconto de 25% + Frete Grátis + Brinde especial

                **Dia 2-3:**
                - 📧 Email personalizado com nome e histórico de compras
                - Mostrar produtos similares aos que já compraram
                - Voucher exclusivo válido por 7 dias

                **Dia 4-7:**
                - WhatsApp/SMS de lembrete do voucher
                - Criar senso de urgência (oferta expira em X dias)

                **Meta:** Reativar 50% dos VIPs críticos em 2 semanas
                """)

                # Botão de download
                csv_inactive = inactive_vips.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label='📥 Baixar lista de VIPs inativos para campanha (CSV)',
                    data=csv_inactive,
                    file_name='vips_inativos_reativacao.csv',
                    mime='text/csv'
                )
            else:
                st.success("✅ Excelente! Todos os seus VIPs estão ativos!")

            # Programa de Fidelidade
            st.markdown("#### 🏆 Programa de Fidelidade - Tiers e Benefícios")

            st.info("""
            **Sistema de Tiers Automático**

            Baseado na receita total e número de compras, seus clientes são automaticamente classificados em:
            """)

            loyalty = vip_analyzer.loyalty_program_tiers()

            if not loyalty.empty:
                # Resumo por tier
                tier_summary = loyalty.groupby('tier').agg({
                    'cliente_id': 'count',
                    'receita_total': 'sum'
                }).reset_index()

                tier_summary.columns = ['Tier', 'Num. Clientes', 'Receita Total']

                # Adicionar benefícios
                tier_benefits = {
                    'Platinum': '💎 Desconto 20% + Frete Grátis + Degustação Exclusiva',
                    'Gold': '🥇 Desconto 15% + Frete Grátis',
                    'Silver': '🥈 Desconto 10%',
                    'Bronze': '🥉 Desconto 5% na próxima compra'
                }

                tier_summary['Benefícios'] = tier_summary['Tier'].map(tier_benefits)

                st.dataframe(tier_summary, use_container_width=True)

                # Visualização
                fig = px.bar(
                    tier_summary,
                    x='Tier',
                    y='Receita Total',
                    title='Receita por Tier de Fidelidade',
                    color='Tier',
                    color_discrete_map={
                        'Platinum': '#E5E4E2',
                        'Gold': '#FFD700',
                        'Silver': '#C0C0C0',
                        'Bronze': '#CD7F32'
                    }
                )

                st.plotly_chart(fig, use_container_width=True)

                # Implementação do programa
                st.success("""
                **💡 Como Implementar Este Programa:**

                **1. Comunicação (Semana 1):**
                - Anunciar o novo programa de fidelidade
                - Email para toda base explicando os benefícios
                - Informar tier atual de cada cliente

                **2. Ativação (Semana 2):**
                - Enviar códigos de desconto personalizados
                - Criar badge/selo para emails (Platinum, Gold, etc)
                - Atualizar site com informações do programa

                **3. Engajamento (Mensalmente):**
                - Email mostrando progresso até próximo tier
                - Ofertas exclusivas por tier
                - Eventos especiais para Platinum/Gold

                **4. Monitoramento:**
                - Acompanhar taxa de upgrade entre tiers
                - Medir aumento no ticket médio por tier
                - ROI do programa (aumento de receita vs custo de descontos)
                """)

                # Download da lista completa
                csv_loyalty = loyalty.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label='📥 Baixar lista completa do programa de fidelidade (CSV)',
                    data=csv_loyalty,
                    file_name='programa_fidelidade_tiers.csv',
                    mime='text/csv'
                )
            else:
                st.info("Não há dados suficientes para criar programa de fidelidade.")

        except Exception as e:
            st.error(f"Erro ao gerar análise de VIPs: {str(e)}")


def show_advanced_analytics(data):
    """Página de Análises Avançadas com 6 ferramentas profissionais"""

    st.header("🚀 Ferramentas Pro - Análises Avançadas")

    st.info("""
    **Ferramentas profissionais para otimizar cada aspecto do seu negócio!**

    Esta seção oferece 6 análises avançadas:
    - **💰 Rentabilidade:** Identifique produtos mais lucrativos
    - **🛒 Cross-Selling:** Descubra produtos comprados juntos
    - **🔄 Jornada do Cliente:** Primeiro vs Recorrente
    - **🎯 Metas e KPIs:** Acompanhe performance vs objetivos
    - **🗺️ Análise Geográfica:** Oportunidades por região
    - **📞 Reativação:** Resgate clientes inativos
    """)

    # Importar os analisadores
    try:
        import sys
        from pathlib import Path
        sys.path.append(str(Path(__file__).parent / 'src'))
        from visualization.business_analytics import (
            ProfitabilityAnalyzer, BasketAnalyzer, CustomerJourneyAnalyzer,
            GoalTracker, GeographicAnalyzer, ReactivationAnalyzer
        )
    except ImportError as e:
        st.error(f"Erro ao carregar módulo de análises avançadas: {e}")
        return

    # Criar tabs para as 6 análises
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "💰 Rentabilidade",
        "🛒 Cross-Selling",
        "🔄 Jornada Cliente",
        "🎯 Metas & KPIs",
        "🗺️ Geografia",
        "📞 Reativação"
    ])

    with tab1:
        st.subheader("💰 Análise de Margem e Rentabilidade")

        st.markdown("""
        **O que você vai descobrir:**
        - Produtos com melhor margem de lucro
        - Classificação BCG: Estrela, Vaca Leiteira, Oportunidade, Peso Morto
        - Produtos com margem baixa que precisam de ação
        - Lucro total estimado por produto
        """)

        try:
            profit_analyzer = ProfitabilityAnalyzer(data)

            # Resumo de rentabilidade
            summary = profit_analyzer.profitability_summary()

            if summary:
                st.markdown("#### 📊 Resumo Geral de Rentabilidade")

                col1, col2, col3, col4 = st.columns(4)

                with col1:
                    st.metric(
                        "Receita Total",
                        f"R$ {summary.get('receita_total', 0):,.2f}"
                    )

                with col2:
                    st.metric(
                        "Lucro Estimado",
                        f"R$ {summary.get('lucro_total_estimado', 0):,.2f}",
                        f"{summary.get('margem_media', 0):.1f}% margem média"
                    )

                with col3:
                    st.metric(
                        "🌟 Produtos Estrela",
                        summary.get('num_estrelas', 0),
                        "alta receita + alta margem"
                    )

                with col4:
                    st.metric(
                        "⚠️ Peso Morto",
                        summary.get('num_peso_morto', 0),
                        "baixa receita + baixa margem"
                    )

                st.info(f"""
                **💡 Nota sobre margem:**
                Como não há dados de custo no sistema, estamos estimando uma margem conservadora de 35% (padrão do mercado de vinhos).
                Para análises mais precisas, adicione uma coluna de custo ao dataset.
                """)

            # Análise de margem por produto
            st.markdown("#### 💎 Matriz BCG - Classificação de Produtos")

            margins = profit_analyzer.calculate_profit_margins()

            if not margins.empty:
                # Gráfico de dispersão BCG
                fig = px.scatter(
                    margins,
                    x='receita_total',
                    y='margem_percentual',
                    size='lucro_total',
                    color='classificacao',
                    hover_data=['produto_id'] if 'nome' not in margins.columns else ['nome'],
                    title='Matriz BCG - Receita vs Margem',
                    labels={
                        'receita_total': 'Receita Total (R$)',
                        'margem_percentual': 'Margem (%)',
                        'classificacao': 'Classificação'
                    },
                    color_discrete_map={
                        'Estrela (Alta Receita + Alta Margem)': '#28a745',
                        'Vaca Leiteira (Alta Receita + Baixa Margem)': '#ffc107',
                        'Oportunidade (Baixa Receita + Alta Margem)': '#17a2b8',
                        'Peso Morto (Baixa Receita + Baixa Margem)': '#dc3545'
                    }
                )

                st.plotly_chart(fig, use_container_width=True)

                # Tabela detalhada
                st.markdown("#### 📋 Detalhamento por Produto")

                display_cols = ['produto_id', 'receita_total', 'margem_percentual', 'lucro_total', 'classificacao']
                if 'nome' in margins.columns:
                    display_cols.insert(1, 'nome')

                st.dataframe(
                    margins[display_cols].head(20).rename(columns={
                        'produto_id': 'ID',
                        'nome': 'Produto',
                        'receita_total': 'Receita (R$)',
                        'margem_percentual': 'Margem (%)',
                        'lucro_total': 'Lucro Estimado (R$)',
                        'classificacao': 'Classificação BCG'
                    }),
                    use_container_width=True
                )

                # Produtos com margem baixa
                st.markdown("#### ⚠️ Produtos com Margem Baixa (<25%)")

                low_margin = profit_analyzer.identify_low_margin_products(threshold=25)

                if not low_margin.empty:
                    st.warning(f"""
                    **ALERTA: {len(low_margin)} produtos com margem abaixo de 25%!**

                    Esses produtos estão comprometendo sua rentabilidade.
                    """)

                    display_cols_low = ['produto_id', 'margem_percentual', 'receita_total', 'acao_recomendada']
                    if 'nome' in low_margin.columns:
                        display_cols_low.insert(1, 'nome')

                    st.dataframe(
                        low_margin[display_cols_low].head(15),
                        use_container_width=True
                    )

                    st.error("""
                    **📋 Plano de Ação:**

                    **Curto Prazo (1-2 semanas):**
                    1. Renegociar preços com fornecedores dos produtos de margem <20%
                    2. Aumentar preços gradualmente (2-5%) nos produtos de margem 20-25%
                    3. Criar combos misturando baixa margem com alta margem

                    **Médio Prazo (1 mês):**
                    1. Avaliar descontinuar produtos de margem <15% e baixa receita
                    2. Substituir por produtos similares com melhor margem
                    3. Focar marketing nos produtos "Estrela"

                    **Meta:** Margem média acima de 35% em 3 meses
                    """)
                else:
                    st.success("✅ Excelente! Todos os produtos têm margem saudável (≥25%)")

            else:
                st.info("Não há dados suficientes para análise de rentabilidade.")

        except Exception as e:
            st.error(f"Erro ao gerar análise de rentabilidade: {str(e)}")

    with tab2:
        st.subheader("🛒 Cross-Selling e Análise de Cesta")

        st.markdown("""
        **O que você vai descobrir:**
        - Produtos frequentemente comprados juntos
        - Sugestões de combos/kits
        - Métricas da cesta de compras
        - Oportunidades de aumentar ticket médio
        """)

        try:
            basket_analyzer = BasketAnalyzer(data)

            # Métricas gerais da cesta
            st.markdown("#### 📊 Métricas da Cesta de Compras")

            basket_metrics = basket_analyzer.calculate_basket_metrics()

            if basket_metrics:
                col1, col2, col3 = st.columns(3)

                with col1:
                    st.metric(
                        "Produtos/Compra",
                        f"{basket_metrics.get('produtos_por_compra_medio', 0):.1f}",
                        f"máx: {basket_metrics.get('produtos_por_compra_max', 0)}"
                    )

                with col2:
                    st.metric(
                        "Compras Múltiplas",
                        f"{basket_metrics.get('percent_compras_multiplas', 0):.1f}%",
                        f"{basket_metrics.get('compras_multiplas', 0)} compras"
                    )

                with col3:
                    if 'valor_cesta_medio' in basket_metrics:
                        st.metric(
                            "Valor Médio Cesta",
                            f"R$ {basket_metrics.get('valor_cesta_medio', 0):.2f}",
                            f"máx: R$ {basket_metrics.get('valor_cesta_max', 0):.2f}"
                        )

                # Insight sobre oportunidade
                if basket_metrics.get('percent_compras_multiplas', 0) < 30:
                    st.warning(f"""
                    **⚠️ OPORTUNIDADE IDENTIFICADA!**

                    Apenas {basket_metrics.get('percent_compras_multiplas', 0):.1f}% das compras têm múltiplos produtos.

                    **Como aumentar:**
                    - Criar combos com desconto
                    - Sugerir produtos relacionados no checkout
                    - Oferecer frete grátis acima de X produtos
                    - Implementar "Compre 2, Leve 3"
                    """)
                else:
                    st.success(f"""
                    ✅ Ótimo! {basket_metrics.get('percent_compras_multiplas', 0):.1f}% das compras têm múltiplos produtos.
                    Continue incentivando cross-selling!
                    """)

            # Produtos comprados juntos
            st.markdown("#### 🔗 Produtos Frequentemente Comprados Juntos")

            associations = basket_analyzer.find_product_associations(min_support=2)

            if not associations.empty:
                st.markdown(f"**Encontramos {len(associations)} combinações de produtos!**")

                # Mostrar top 15 associações
                display_cols = ['produto_1', 'produto_2', 'frequencia', 'confianca_1_2']

                if 'nome_produto_1' in associations.columns:
                    display_cols = ['nome_produto_1', 'nome_produto_2', 'frequencia', 'confianca_1_2']

                st.dataframe(
                    associations.head(15)[display_cols].rename(columns={
                        'produto_1': 'Produto 1',
                        'produto_2': 'Produto 2',
                        'nome_produto_1': 'Produto 1',
                        'nome_produto_2': 'Produto 2',
                        'frequencia': 'Vezes Comprados Juntos',
                        'confianca_1_2': 'Confiança (%)'
                    }),
                    use_container_width=True
                )

                st.info("""
                **Como ler:**
                - **Frequência:** Quantas vezes os produtos foram comprados juntos
                - **Confiança:** % das vezes que Produto 2 é comprado quando Produto 1 é comprado
                - **Alta confiança (>50%):** Associação muito forte - crie combo!
                """)

            else:
                st.info("Poucas compras com múltiplos produtos. Incentive cross-selling!")

            # Sugestões de combos
            st.markdown("#### 🎁 Sugestões de Combos/Kits")

            bundles = basket_analyzer.suggest_bundles(min_freq=2)

            if not bundles.empty:
                st.success(f"**Identificamos {len(bundles)} oportunidades de combos!**")

                display_cols_bundle = ['produto_1', 'produto_2', 'frequencia', 'desconto_sugerido', 'tipo_bundle']

                if 'nome_produto_1' in bundles.columns:
                    display_cols_bundle = ['nome_produto_1', 'nome_produto_2', 'frequencia', 'desconto_sugerido', 'tipo_bundle']

                st.dataframe(
                    bundles[display_cols_bundle].rename(columns={
                        'produto_1': 'Produto 1',
                        'produto_2': 'Produto 2',
                        'nome_produto_1': 'Produto 1',
                        'nome_produto_2': 'Produto 2',
                        'frequencia': 'Força da Associação',
                        'desconto_sugerido': 'Desconto Sugerido',
                        'tipo_bundle': 'Tipo de Combo'
                    }),
                    use_container_width=True
                )

                st.success("""
                **💡 Como Implementar Combos:**

                **Exemplo de Campanha:**
                1. Nome: "Harmonização Perfeita"
                2. Oferta: "Compre [Produto 1] + [Produto 2] com 10% OFF!"
                3. Destaque: "Clientes que compraram isso também levaram..."
                4. Prazo: Oferta válida por 7 dias
                5. Canal: Email + Banner no site

                **Precificação:**
                - Desconto de 10-15% no combo
                - Ainda mantém margem saudável
                - Aumenta ticket médio significativamente

                **Métricas a acompanhar:**
                - Taxa de conversão do combo
                - Aumento no ticket médio
                - ROI da campanha
                """)

                # Download
                csv = bundles.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label='📥 Baixar sugestões de combos (CSV)',
                    data=csv,
                    file_name='sugestoes_combos.csv',
                    mime='text/csv'
                )

            else:
                st.info("Não há associações fortes o suficiente para sugerir combos ainda.")

        except Exception as e:
            st.error(f"Erro ao gerar análise de cross-selling: {str(e)}")

    with tab3:
        st.subheader("🔄 Jornada do Cliente - Primeira vs Compras Recorrentes")

        st.markdown("""
        **O que você vai descobrir:**
        - Taxa de conversão (primeira → segunda compra)
        - Tempo médio até segunda compra
        - Produtos que convertem melhor novos clientes
        - Estratégias para aumentar retenção
        """)

        try:
            journey_analyzer = CustomerJourneyAnalyzer(data)

            # Taxa de conversão
            st.markdown("#### 📈 Taxa de Conversão e Retenção")

            conversion = journey_analyzer.calculate_conversion_rate()

            if conversion:
                col1, col2, col3, col4 = st.columns(4)

                with col1:
                    st.metric(
                        "Total Clientes",
                        conversion.get('total_clientes', 0)
                    )

                with col2:
                    st.metric(
                        "Clientes Recorrentes",
                        conversion.get('clientes_recorrentes', 0),
                        f"{conversion.get('taxa_conversao', 0):.1f}% converteram"
                    )

                with col3:
                    st.metric(
                        "Taxa de Conversão",
                        f"{conversion.get('taxa_conversao', 0):.1f}%"
                    )

                with col4:
                    st.metric(
                        "Tempo Médio 2ª Compra",
                        f"{conversion.get('dias_medio_ate_segunda_compra', 0):.0f} dias"
                    )

                # Análise da taxa
                taxa = conversion.get('taxa_conversao', 0)

                if taxa < 30:
                    st.error(f"""
                    **🚨 TAXA DE CONVERSÃO BAIXA ({taxa:.1f}%)!**

                    Você está perdendo {conversion.get('clientes_one_time', 0)} clientes após a primeira compra!

                    **Ações Urgentes:**

                    **1. Email de Boas-Vindas (Enviar em 24h após 1ª compra):**
                    - Agradecer a compra
                    - Cupom de 10% para próxima compra (válido 30 dias)
                    - Sugerir produtos complementares

                    **2. Acompanhamento em 7 Dias:**
                    - "Como está gostando do [produto]?"
                    - Pedir feedback/avaliação
                    - Oferecer ajuda

                    **3. Lembrete em {int(conversion.get('dias_medio_ate_segunda_compra', 30))} dias:**
                    - "Hora de reabastecer!"
                    - Desconto especial para clientes
                    - Frete grátis na 2ª compra

                    **Meta:** Aumentar taxa para 50% em 3 meses
                    """)
                elif taxa < 50:
                    st.warning(f"""
                    **⚠️ Taxa de conversão razoável ({taxa:.1f}%), mas pode melhorar!**

                    Continue investindo em:
                    - Programa de fidelidade
                    - Email marketing pós-compra
                    - Experiência do cliente de primeira compra
                    """)
                else:
                    st.success(f"""
                    **✅ Excelente taxa de conversão ({taxa:.1f}%)!**

                    Você está fazendo um ótimo trabalho retendo clientes.
                    Continue focando na experiência do cliente!
                    """)

            # Produtos que convertem melhor
            st.markdown("#### 🏆 Produtos que Melhor Convertem Novos Clientes")

            first_purchase_products = journey_analyzer.analyze_first_purchase_products()

            if not first_purchase_products.empty:
                st.markdown("**Produtos de entrada ideais para atrair e reter clientes:**")

                display_cols = ['produto_id', 'clientes_primeira_compra', 'clientes_retornaram', 'taxa_retencao']

                if 'nome' in first_purchase_products.columns:
                    display_cols.insert(1, 'nome')

                st.dataframe(
                    first_purchase_products.head(15)[display_cols].rename(columns={
                        'produto_id': 'ID',
                        'nome': 'Produto',
                        'clientes_primeira_compra': 'Clientes 1ª Compra',
                        'clientes_retornaram': 'Retornaram',
                        'taxa_retencao': 'Taxa Retenção (%)'
                    }),
                    use_container_width=True
                )

                # Identificar melhor produto de entrada
                best_product = first_purchase_products.iloc[0]

                st.success(f"""
                **🌟 Produto Campeão de Conversão:**

                **Produto:** {best_product.get('nome', best_product['produto_id'])}
                **Taxa de Retenção:** {best_product['taxa_retencao']:.1f}%

                **Estratégia Recomendada:**
                1. Use este produto em campanhas de aquisição de novos clientes
                2. Ofereça como "produto de entrada" com desconto especial
                3. Destaque nos anúncios e landing pages
                4. Combine com programa "primeira compra com desconto"

                **Por que funciona:**
                Este produto tem a melhor taxa de converter novos clientes em recorrentes!
                """)

            else:
                st.info("Dados insuficientes para análise de primeira compra.")

        except Exception as e:
            st.error(f"Erro ao gerar análise de jornada: {str(e)}")

    with tab4:
        st.subheader("🎯 Dashboard de Metas e KPIs")

        st.markdown("""
        **O que você vai acompanhar:**
        - Progresso vs meta mensal
        - KPIs principais do negócio
        - Comparação período a período
        - Projeção de atingimento
        """)

        try:
            goal_tracker = GoalTracker(data)

            # Definir meta
            st.markdown("#### 🎯 Configure Sua Meta Mensal")

            col1, col2 = st.columns(2)

            with col1:
                target_revenue = st.number_input(
                    "Meta de Receita (R$)",
                    min_value=0.0,
                    value=50000.0,
                    step=5000.0
                )

            with col2:
                target_customers = st.number_input(
                    "Meta de Clientes",
                    min_value=0,
                    value=100,
                    step=10
                )

            # Acompanhar meta
            goal_status = goal_tracker.set_monthly_goal(target_revenue, target_customers)

            if goal_status:
                st.markdown("#### 📊 Status da Meta do Mês")

                col1, col2, col3 = st.columns(3)

                with col1:
                    st.metric(
                        "Receita Atual",
                        f"R$ {goal_status.get('receita_atual', 0):,.2f}",
                        f"{goal_status.get('progresso_receita', 0):.1f}% da meta"
                    )

                with col2:
                    st.metric(
                        "Projeção Fim Mês",
                        f"R$ {goal_status.get('projecao_fim_mes', 0):,.2f}",
                        "✅ Bate meta!" if goal_status.get('vai_bater_meta') else "⚠️ Abaixo da meta"
                    )

                with col3:
                    st.metric(
                        "Dias Restantes",
                        goal_status.get('dias_restantes', 0),
                        "dias para atingir meta"
                    )

                # Gráfico de progresso
                progress = goal_status.get('progresso_receita', 0) / 100
                fig = go.Figure(go.Indicator(
                    mode="gauge+number+delta",
                    value=goal_status.get('receita_atual', 0),
                    domain={'x': [0, 1], 'y': [0, 1]},
                    title={'text': "Progresso da Meta de Receita"},
                    delta={'reference': target_revenue},
                    gauge={
                        'axis': {'range': [None, target_revenue]},
                        'bar': {'color': "#28a745" if goal_status.get('vai_bater_meta') else "#ffc107"},
                        'steps': [
                            {'range': [0, target_revenue * 0.5], 'color': "#ffebee"},
                            {'range': [target_revenue * 0.5, target_revenue * 0.75], 'color': "#fff3cd"},
                            {'range': [target_revenue * 0.75, target_revenue], 'color': "#d4edda"}
                        ],
                        'threshold': {
                            'line': {'color': "red", 'width': 4},
                            'thickness': 0.75,
                            'value': target_revenue
                        }
                    }
                ))

                st.plotly_chart(fig, use_container_width=True)

                # Recomendações
                if not goal_status.get('vai_bater_meta'):
                    gap = target_revenue - goal_status.get('projecao_fim_mes', 0)
                    days_left = goal_status.get('dias_restantes', 1)
                    daily_needed = gap / days_left if days_left > 0 else gap

                    st.warning(f"""
                    **⚠️ Meta em Risco! Faltam R$ {gap:,.2f}**

                    **Plano de Recuperação:**

                    **1. Ação Imediata (Hoje):**
                    - Disparar campanha para clientes VIP inativos
                    - Email com oferta relâmpago 24h
                    - Desconto de 15% + Frete Grátis

                    **2. Próximos {days_left} dias:**
                    - Vender R$ {daily_needed:,.2f} por dia (média necessária)
                    - Promoção de combos/kits
                    - Ativar programa de indicação (indique e ganhe)

                    **3. Focar em:**
                    - Produtos de alto ticket médio
                    - Clientes de maior valor histórico
                    - Cross-selling agressivo

                    **Meta ajustada:** R$ {daily_needed:,.2f}/dia pelos próximos {days_left} dias
                    """)
                else:
                    st.success("""
                    **✅ Parabéns! Você está no caminho para bater a meta!**

                    Continue com o ritmo atual e você atingirá o objetivo.
                    """)

            # KPIs Gerais
            st.markdown("#### 📊 KPIs Principais")

            kpis = goal_tracker.calculate_kpis()

            if kpis:
                col1, col2, col3, col4 = st.columns(4)

                with col1:
                    st.metric("Receita Total", f"R$ {kpis.get('receita_total', 0):,.2f}")
                    st.metric("Ticket Médio", f"R$ {kpis.get('ticket_medio', 0):.2f}")

                with col2:
                    st.metric("Total Clientes", kpis.get('total_clientes', 0))
                    st.metric("Total Transações", kpis.get('total_transacoes', 0))

                with col3:
                    st.metric("Transações/Cliente", f"{kpis.get('transacoes_por_cliente', 0):.1f}")
                    st.metric("Produtos Únicos", kpis.get('produtos_unicos_vendidos', 0))

                with col4:
                    st.metric("Unidades Vendidas", kpis.get('unidades_vendidas', 0))
                    if 'taxa_churn' in kpis:
                        st.metric("Taxa Churn", f"{kpis.get('taxa_churn', 0):.1f}%")

            # Comparação de períodos
            st.markdown("#### 📅 Comparação Período a Período")

            period_type = st.selectbox(
                "Selecione o período de comparação:",
                ['month', 'quarter', 'year'],
                format_func=lambda x: {'month': 'Mês a Mês', 'quarter': 'Trimestre a Trimestre', 'year': 'Ano a Ano'}[x]
            )

            comparison = goal_tracker.compare_periods(period=period_type)

            if not comparison.empty:
                # Gráfico de evolução
                fig = go.Figure()

                fig.add_trace(go.Bar(
                    x=comparison['periodo'],
                    y=comparison['receita_total'],
                    name='Receita',
                    marker_color='#722F37'
                ))

                fig.update_layout(
                    title='Evolução da Receita por Período',
                    xaxis_title='Período',
                    yaxis_title='Receita (R$)',
                    template='plotly_white'
                )

                st.plotly_chart(fig, use_container_width=True)

                # Tabela de comparação
                st.dataframe(
                    comparison.rename(columns={
                        'periodo': 'Período',
                        'receita_total': 'Receita (R$)',
                        'ticket_medio': 'Ticket Médio (R$)',
                        'num_vendas': 'Num. Vendas',
                        'clientes_unicos': 'Clientes Únicos',
                        'var_receita': 'Variação Receita (%)',
                        'var_clientes': 'Variação Clientes (%)'
                    }),
                    use_container_width=True
                )

        except Exception as e:
            st.error(f"Erro ao gerar dashboard de metas: {str(e)}")

    with tab5:
        st.subheader("🗺️ Análise Geográfica Avançada")

        st.markdown("""
        **O que você vai descobrir:**
        - Performance detalhada por cidade
        - Oportunidades de expansão geográfica
        - Concentração de mercado
        - Cidades com alto potencial inexplorado
        """)

        try:
            geo_analyzer = GeographicAnalyzer(data)

            # Resumo geográfico
            summary = geo_analyzer.geographic_summary()

            if summary:
                st.markdown("#### 🌍 Resumo Geográfico")

                col1, col2, col3, col4 = st.columns(4)

                with col1:
                    st.metric(
                        "Cidades Atendidas",
                        summary.get('num_cidades', 0)
                    )

                with col2:
                    st.metric(
                        "Cidade Top",
                        summary.get('cidade_top', 'N/A'),
                        f"R$ {summary.get('receita_cidade_top', 0):,.2f}"
                    )

                with col3:
                    st.metric(
                        "Concentração Top 5",
                        f"{summary.get('concentracao_top_5', 0):.1f}%",
                        "da receita"
                    )

                with col4:
                    st.metric(
                        "Mercados Consolidados",
                        summary.get('mercados_consolidados', 0),
                        f"{summary.get('oportunidades_expansao', 0)} oportunidades"
                    )

            # Performance por cidade
            st.markdown("#### 📊 Performance Detalhada por Cidade")

            city_perf = geo_analyzer.city_performance()

            if not city_perf.empty:
                # Gráfico de barras
                fig = px.bar(
                    city_perf.head(15),
                    x='cidade',
                    y='receita_total',
                    color='classificacao',
                    title='Top 15 Cidades por Receita',
                    labels={'cidade': 'Cidade', 'receita_total': 'Receita (R$)'},
                    color_discrete_map={
                        'Mercado Consolidado': '#28a745',
                        'Mercado em Crescimento': '#ffc107',
                        'Mercado Potencial': '#17a2b8'
                    }
                )

                st.plotly_chart(fig, use_container_width=True)

                # Tabela detalhada
                st.dataframe(
                    city_perf.rename(columns={
                        'cidade': 'Cidade',
                        'receita_total': 'Receita (R$)',
                        'ticket_medio': 'Ticket Médio (R$)',
                        'num_vendas': 'Num. Vendas',
                        'clientes_unicos': 'Clientes',
                        'unidades_vendidas': 'Unidades',
                        'participacao_receita': 'Participação (%)',
                        'classificacao': 'Status'
                    }),
                    use_container_width=True
                )

            # Oportunidades de expansão
            st.markdown("#### 🚀 Oportunidades de Expansão")

            opportunities = geo_analyzer.identify_expansion_opportunities()

            if not opportunities.empty:
                st.success(f"""
                **Identificamos {len(opportunities)} cidades com alto potencial!**

                Essas cidades têm poucos clientes mas um ticket médio alto - sinal de que há demanda qualificada!
                """)

                st.dataframe(
                    opportunities[['cidade', 'clientes_unicos', 'ticket_medio', 'receita_total', 'potencial', 'acao_recomendada']].rename(columns={
                        'cidade': 'Cidade',
                        'clientes_unicos': 'Clientes Atuais',
                        'ticket_medio': 'Ticket Médio (R$)',
                        'receita_total': 'Receita Atual (R$)',
                        'potencial': 'Potencial',
                        'acao_recomendada': 'Ação Recomendada'
                    }),
                    use_container_width=True
                )

                st.info("""
                **📋 Plano de Expansão Geográfica (6 Meses):**

                **Fase 1 - Meses 1-2: Teste de Mercado**
                - Selecionar top 3 cidades oportunidade
                - Campanha de marketing local (Google Ads + Facebook geolocalizadas)
                - Budget: R$ 500-1000 por cidade
                - Oferta especial: "Chegamos em [Cidade]! 15% OFF"

                **Fase 2 - Meses 3-4: Consolidação**
                - Avaliar ROI das campanhas
                - Expandir investimento nas cidades com melhor resposta
                - Criar parcerias locais (restaurantes, eventos)
                - Implementar programa de indicação local

                **Fase 3 - Meses 5-6: Escala**
                - Aumentar penetração nas cidades bem-sucedidas
                - Replicar estratégia em novas cidades
                - Eventos de degustação locais
                - Criar "embaixadores" em cada cidade

                **Meta:** Dobrar número de cidades consolidadas em 6 meses
                """)

            else:
                st.info("""
                Não há oportunidades claras de expansão no momento.
                Foque em consolidar mercados existentes.
                """)

        except Exception as e:
            st.error(f"Erro ao gerar análise geográfica: {str(e)}")

    with tab6:
        st.subheader("📞 Análise de Reativação de Clientes")

        st.markdown("""
        **O que você vai descobrir:**
        - Clientes inativos há 30/60/90 dias
        - Priorização por valor histórico
        - Ofertas personalizadas de reativação
        - Campanha pronta para execução
        """)

        try:
            reactivation_analyzer = ReactivationAnalyzer(data)

            # Métricas de reativação
            st.markdown("#### 📊 Métricas de Inatividade")

            metrics = reactivation_analyzer.calculate_reactivation_metrics()

            if metrics:
                col1, col2, col3, col4 = st.columns(4)

                with col1:
                    st.metric(
                        "Inativos 30d",
                        metrics.get('clientes_inativos_30d', 0)
                    )

                with col2:
                    st.metric(
                        "Inativos 60d",
                        metrics.get('clientes_inativos_60d', 0),
                        f"{metrics.get('taxa_inatividade_60d', 0):.1f}% do total"
                    )

                with col3:
                    st.metric(
                        "Inativos 90d",
                        metrics.get('clientes_inativos_90d', 0),
                        "CRÍTICO"
                    )

                with col4:
                    st.metric(
                        "Receita em Risco",
                        f"R$ {metrics.get('receita_em_risco_60d', 0):,.2f}",
                        f"{metrics.get('clientes_alta_prioridade', 0)} VIPs"
                    )

                # Alerta
                if metrics.get('clientes_inativos_60d', 0) > 20:
                    st.error(f"""
                    **🚨 ALERTA: {metrics.get('clientes_inativos_60d', 0)} clientes inativos há 60+ dias!**

                    Você está em risco de perder R$ {metrics.get('receita_em_risco_60d', 0):,.2f} em receita histórica!
                    """)

            # Lista de clientes inativos
            st.markdown("#### 📋 Clientes Inativos para Reativação")

            days_filter = st.slider(
                "Filtrar por dias de inatividade:",
                min_value=30,
                max_value=180,
                value=60,
                step=30
            )

            inactive = reactivation_analyzer.identify_inactive_customers(days_threshold=days_filter)

            if not inactive.empty:
                st.warning(f"""
                **Encontramos {len(inactive)} clientes inativos há {days_filter}+ dias**

                **Classificação:**
                - **Alta Prioridade:** Clientes que gastaram muito - ligue pessoalmente!
                - **Média Prioridade:** Envie email personalizado
                - **Baixa Prioridade:** Email genérico de campanha
                """)

                # Filtro de prioridade
                priority_filter = st.multiselect(
                    "Filtrar por prioridade:",
                    ['Alta', 'Média', 'Baixa'],
                    default=['Alta', 'Média', 'Baixa']
                )

                filtered_inactive = inactive[inactive['prioridade'].isin(priority_filter)]

                display_cols = ['cliente_id', 'dias_inativo', 'receita_total', 'risco', 'prioridade', 'oferta_sugerida']

                if 'nome' in filtered_inactive.columns:
                    display_cols.insert(1, 'nome')

                st.dataframe(
                    filtered_inactive[display_cols].rename(columns={
                        'cliente_id': 'Cliente ID',
                        'nome': 'Nome',
                        'dias_inativo': 'Dias Inativo',
                        'receita_total': 'Receita Histórica (R$)',
                        'risco': 'Risco',
                        'prioridade': 'Prioridade',
                        'oferta_sugerida': 'Oferta Sugerida'
                    }),
                    use_container_width=True
                )

                # Criar campanha
                st.markdown("#### 🎯 Campanha de Reativação Pronta")

                num_clientes_campanha = st.slider(
                    "Quantos clientes incluir na campanha?",
                    min_value=10,
                    max_value=min(200, len(inactive)),
                    value=min(50, len(inactive)),
                    step=10
                )

                campaign = reactivation_analyzer.create_reactivation_campaign(
                    days_threshold=days_filter,
                    max_customers=num_clientes_campanha
                )

                if not campaign.empty:
                    st.success(f"""
                    **✅ Campanha criada com {len(campaign)} clientes!**

                    **Cronograma de Execução:**
                    """)

                    alta_prioridade = len(campaign[campaign['prioridade'] == 'Alta']) if 'prioridade' in campaign.columns else 0
                    media_prioridade = len(campaign[campaign['prioridade'] == 'Média']) if 'prioridade' in campaign.columns else 0

                    st.markdown(f"""
                    **Dia 1 (Hoje):**
                    - 📞 Ligar para {alta_prioridade} clientes de alta prioridade
                    - Script: "Olá [Nome], sentimos sua falta! Temos uma oferta especial para você..."

                    **Dia 2:**
                    - 📧 Enviar email personalizado para {media_prioridade} clientes média prioridade
                    - Assunto: "[Nome], preparamos uma surpresa para você!"
                    - Incluir histórico de compras e sugestões personalizadas

                    **Dia 3-4:**
                    - 📱 WhatsApp/SMS para clientes que não abriram email
                    - Mensagem curta com link direto para oferta

                    **Dia 5-7:**
                    - 🔔 Lembrete de expiração da oferta
                    - "Última chance! Sua oferta expira em 48h"
                    - Criar urgência

                    **Meta:** Reativar {int(len(campaign) * 0.3)} clientes (30% da campanha)
                    """)

                    # Prévia da tabela
                    st.dataframe(campaign.head(20), use_container_width=True)

                    # Download
                    csv = campaign.to_csv(index=False).encode('utf-8')
                    st.download_button(
                        label='📥 Baixar lista completa da campanha (CSV)',
                        data=csv,
                        file_name=f'campanha_reativacao_{days_filter}d.csv',
                        mime='text/csv'
                    )

                    st.info("""
                    **💡 Dicas para Aumentar Taxa de Reativação:**

                    **1. Personalização é Tudo:**
                    - Use o nome do cliente
                    - Mencione produtos que ele comprou antes
                    - Seja específico sobre quanto tempo sem comprar

                    **2. Oferta Irresistível:**
                    - Desconto significativo (20-30%)
                    - Frete grátis
                    - Brinde na primeira compra de volta
                    - Prazo limitado (cria urgência)

                    **3. Múltiplos Canais:**
                    - Email + SMS + WhatsApp
                    - Retargeting em redes sociais
                    - Não desista no primeiro contato

                    **4. Teste e Aprenda:**
                    - A/B test em assuntos de email
                    - Testar diferentes ofertas
                    - Acompanhar taxa de abertura e conversão
                    - Ajustar estratégia com base nos resultados
                    """)

            else:
                st.success("✅ Parabéns! Nenhum cliente inativo neste período!")

        except Exception as e:
            st.error(f"Erro ao gerar análise de reativação: {str(e)}")


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

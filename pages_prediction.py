"""
Páginas de Predições para o Dashboard
"""
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).parent / 'src'))

from models.predictor import ChurnPredictor, SalesPredictor, ProductRecommender


def show_churn_prediction():
    """Interface para predição de churn"""

    st.markdown('<h3><i class="fas fa-bullseye"></i> Predição de Churn de Clientes</h3>', unsafe_allow_html=True)

    st.info("""
    **Predição de Churn** identifica clientes em risco de cancelar a assinatura.
    Preencha os dados abaixo para obter uma predição instantânea.
    """)

    # Formulário para entrada de dados
    with st.form("churn_prediction_form"):
        st.markdown('### <i class="fas fa-clipboard-list"></i> Dados do Cliente', unsafe_allow_html=True)

        col1, col2 = st.columns(2)

        with col1:
            cliente_id = st.number_input("ID do Cliente", min_value=1, value=1)
            nome = st.text_input("Nome", value="Cliente Teste")
            idade = st.number_input("Idade", min_value=18, max_value=100, value=35)
            cidade = st.selectbox("Cidade", [
                "São Paulo", "Rio de Janeiro", "Belo Horizonte",
                "Brasília", "Salvador", "Fortaleza", "Curitiba",
                "Goiânia"
            ])
            pontuacao_engajamento = st.slider(
                "Pontuação de Engajamento (1-10)",
                min_value=1.0, max_value=10.0, value=5.0, step=0.1
            )

        with col2:
            assinante_clube = st.selectbox("Assinante do Clube", ["Sim", "Não"])
            valor = st.number_input("Valor da Última Compra (R$)", min_value=0.0, value=150.0, step=10.0)
            quantidade = st.number_input("Quantidade", min_value=1, max_value=10, value=2)
            pais = st.selectbox("País do Vinho Preferido", [
                "Brasil", "França", "Chile", "Argentina", "Itália",
                "Espanha", "Portugal", "África do Sul"
            ])
            tipo_uva = st.selectbox("Tipo de Uva Preferido", [
                "Merlot", "Cabernet Sauvignon", "Chardonnay",
                "Sauvignon Blanc", "Pinot Noir", "Malbec", "Syrah"
            ])

        submitted = st.form_submit_button("Fazer Predição", type="primary")

    if submitted:
        # Preparar dados
        customer_data = {
            'cliente_id': cliente_id,
            'nome': nome,
            'idade': idade,
            'cidade': cidade,
            'pontuacao_engajamento': pontuacao_engajamento,
            'assinante_clube': assinante_clube,
            'valor': valor,
            'quantidade': quantidade,
            'pais': pais,
            'tipo_uva': tipo_uva,
        }

        # Fazer predição
        with st.spinner("Analisando dados..."):
            try:
                predictor = ChurnPredictor()
                result = predictor.predict_churn(customer_data)

                # Mostrar resultado
                st.divider()
                st.markdown('### <i class="fas fa-chart-bar"></i> Resultado da Predição', unsafe_allow_html=True)

                # Métricas principais
                col1, col2, col3 = st.columns(3)

                with col1:
                    st.metric(
                        "Risco de Churn",
                        result['risk_level'],
                        f"{result['churn_probability']:.1%}"
                    )

                with col2:
                    st.metric(
                        "Probabilidade de Churn",
                        f"{result['churn_probability']:.1%}",
                        delta=f"-{result['retain_probability']:.1%}" if result['will_churn'] else None
                    )

                with col3:
                    st.metric(
                        "Probabilidade de Retenção",
                        f"{result['retain_probability']:.1%}",
                        delta=f"+{result['retain_probability']:.1%}" if not result['will_churn'] else None
                    )

                # Gráfico de probabilidades
                fig = go.Figure(data=[
                    go.Bar(
                        x=['Cancelar', 'Continuar'],
                        y=[result['churn_probability'], result['retain_probability']],
                        marker_color=['#FF6B6B', '#51CF66'],
                        text=[f"{result['churn_probability']:.1%}", f"{result['retain_probability']:.1%}"],
                        textposition='auto',
                    )
                ])

                fig.update_layout(
                    title="Probabilidades de Churn",
                    yaxis_title="Probabilidade",
                    yaxis_tickformat=".0%",
                    showlegend=False,
                    height=400
                )

                st.plotly_chart(fig, use_container_width=True)

                # Recomendações
                st.divider()
                st.markdown('### <i class="fas fa-lightbulb"></i> Recomendações', unsafe_allow_html=True)

                if result['risk_level'] == "Alto":
                    st.markdown('<p style="color: #dc3545; background-color: #f8d7da; padding: 10px; border-radius: 5px;"><i class="fas fa-exclamation-triangle"></i> ATENÇÃO: Cliente em alto risco de churn!</p>', unsafe_allow_html=True)
                elif result['risk_level'] == "Médio":
                    st.warning("⚡ Cliente em risco médio - ação recomendada")
                else:
                    st.markdown('<p style="color: #28a745; background-color: #d4edda; padding: 10px; border-radius: 5px;"><i class="fas fa-check-circle"></i> Cliente com baixo risco de churn</p>', unsafe_allow_html=True)

                for rec in result['recommendations']:
                    st.markdown(f"- {rec}")

            except Exception as e:
                st.error(f"Erro ao fazer predição: {e}")
                st.exception(e)


def show_batch_prediction():
    """Interface para predição em lote"""

    st.subheader("📊 Predição em Lote")

    st.info("""
    **Upload de arquivo CSV** com dados de múltiplos clientes para predição em massa.

    **Formato esperado:** CSV com colunas: cliente_id, idade, cidade, pontuacao_engajamento,
    assinante_clube, valor, quantidade, pais, tipo_uva
    """)

    uploaded_file = st.file_uploader("Escolha um arquivo CSV", type=['csv'])

    if uploaded_file is not None:
        try:
            # Ler CSV
            df = pd.read_csv(uploaded_file)

            st.success(f"✅ Arquivo carregado: {len(df)} clientes")

            # Mostrar preview
            with st.expander("👁️ Preview dos Dados"):
                st.dataframe(df.head(10))

            if st.button("🚀 Executar Predições", type="primary"):
                with st.spinner(f"Processando {len(df)} clientes..."):
                    predictor = ChurnPredictor()
                    results = predictor.predict_batch(df)

                    # Mostrar resultados
                    st.divider()
                    st.markdown("### 📊 Resultados")

                    # Métricas gerais
                    high_risk = len(results[results['risk_level'] == 'Alto'])
                    medium_risk = len(results[results['risk_level'] == 'Médio'])
                    low_risk = len(results[results['risk_level'] == 'Baixo'])

                    col1, col2, col3 = st.columns(3)

                    with col1:
                        st.metric("🔴 Alto Risco", high_risk, f"{high_risk/len(results)*100:.1f}%")
                    with col2:
                        st.metric("🟡 Médio Risco", medium_risk, f"{medium_risk/len(results)*100:.1f}%")
                    with col3:
                        st.metric("🟢 Baixo Risco", low_risk, f"{low_risk/len(results)*100:.1f}%")

                    # Gráfico de distribuição
                    fig = px.pie(
                        values=[high_risk, medium_risk, low_risk],
                        names=['Alto Risco', 'Médio Risco', 'Baixo Risco'],
                        title='Distribuição de Risco de Churn',
                        color_discrete_sequence=['#FF6B6B', '#FFD93D', '#51CF66']
                    )

                    st.plotly_chart(fig, use_container_width=True)

                    # Tabela de resultados
                    st.markdown("### 📋 Detalhes por Cliente")
                    results_display = results[[
                        'cliente_id', 'risk_level', 'churn_probability',
                        'retain_probability', 'will_churn'
                    ]].copy()

                    results_display['churn_probability'] = results_display['churn_probability'].apply(lambda x: f"{x:.1%}")
                    results_display['retain_probability'] = results_display['retain_probability'].apply(lambda x: f"{x:.1%}")

                    st.dataframe(results_display, use_container_width=True, height=400)

                    # Download dos resultados
                    csv = results.to_csv(index=False)
                    st.download_button(
                        label="📥 Download Resultados (CSV)",
                        data=csv,
                        file_name="predicoes_churn.csv",
                        mime="text/csv",
                    )

        except Exception as e:
            st.error(f"Erro ao processar arquivo: {e}")
            st.exception(e)


def show_sales_prediction():
    """Interface para predição de vendas"""

    st.subheader("📈 Predição de Vendas")

    tab1, tab2 = st.tabs(["Próxima Compra", "Receita Futura"])

    with tab1:
        st.markdown("### 🛒 Predição da Próxima Compra")

        st.info("Prevê quando e quanto um cliente gastará em sua próxima compra.")

        cliente_id = st.number_input("ID do Cliente", min_value=1, value=1, key="sales_customer")

        if st.button("🔮 Prever Próxima Compra", type="primary"):
            with st.spinner("Analisando histórico..."):
                try:
                    predictor = SalesPredictor()
                    predictor.load_historical_data()
                    result = predictor.predict_next_purchase(cliente_id)

                    if 'error' in result:
                        st.error(f"❌ {result['error']}")
                    else:
                        st.success("✅ Predição concluída!")

                        col1, col2, col3 = st.columns(3)

                        with col1:
                            st.metric(
                                "📅 Próxima Compra",
                                result['predicted_next_purchase_date'],
                                f"Em {result['days_until_next_purchase']} dias"
                            )

                        with col2:
                            st.metric(
                                "💰 Valor Esperado",
                                f"R$ {result['predicted_value']:.2f}",
                                f"{result['predicted_quantity']} itens"
                            )

                        with col3:
                            st.metric(
                                "🏆 Lifetime Value",
                                f"R$ {result['lifetime_value']:.2f}",
                                f"{result['total_historical_purchases']} compras"
                            )

                        # Informações adicionais
                        st.divider()
                        st.markdown("### 📊 Informações Adicionais")

                        col1, col2 = st.columns(2)

                        with col1:
                            st.info(f"""
                            **Padrão de Compra:**
                            - Intervalo médio: {result['avg_interval_days']} dias
                            - Tipo de vinho favorito: {result['favorite_wine_type']}
                            """)

                        with col2:
                            st.success(f"""
                            **Recomendação:**
                            - Enviar lembrete 3 dias antes da data prevista
                            - Oferecer {result['favorite_wine_type']} em promoção
                            - Sugerir compra de {result['predicted_quantity']} garrafas
                            """)

                except Exception as e:
                    st.error(f"Erro: {e}")
                    st.exception(e)

    with tab2:
        st.markdown("### 💹 Predição de Receita")

        st.info("Prevê a receita total baseada em tendências históricas.")

        months = st.slider("Número de meses à frente", min_value=1, max_value=12, value=3)

        if st.button("📊 Prever Receita", type="primary", key="revenue_predict"):
            with st.spinner("Calculando projeções..."):
                try:
                    predictor = SalesPredictor()
                    predictor.load_historical_data()
                    result = predictor.predict_revenue(months_ahead=months)

                    st.success("✅ Projeção concluída!")

                    col1, col2, col3 = st.columns(3)

                    with col1:
                        st.metric(
                            "💰 Receita Prevista",
                            f"R$ {result['predicted_total_revenue']:,.2f}",
                            f"{months} meses"
                        )

                    with col2:
                        st.metric(
                            "📊 Média Mensal",
                            f"R$ {result['predicted_monthly_avg']:,.2f}",
                            f"{result['growth_rate']*100:+.1f}% crescimento"
                        )

                    with col3:
                        st.metric(
                            "📈 Taxa de Crescimento",
                            f"{result['growth_rate']*100:.1f}%",
                            "ao mês"
                        )

                    # Gráfico de projeção
                    monthly_values = [result['predicted_monthly_avg']] * months
                    cumulative = [sum(monthly_values[:i+1]) for i in range(months)]

                    fig = go.Figure()

                    fig.add_trace(go.Scatter(
                        x=list(range(1, months+1)),
                        y=cumulative,
                        mode='lines+markers',
                        name='Receita Acumulada',
                        line=dict(color='#51CF66', width=3)
                    ))

                    fig.update_layout(
                        title=f"Projeção de Receita - {months} Meses",
                        xaxis_title="Mês",
                        yaxis_title="Receita Acumulada (R$)",
                        hovermode='x unified',
                        height=400
                    )

                    st.plotly_chart(fig, use_container_width=True)

                    st.info(f"**Confiança:** {result['confidence'].title()}")

                except Exception as e:
                    st.error(f"Erro: {e}")
                    st.exception(e)


def show_product_recommendation():
    """Interface para recomendação de produtos"""

    st.subheader("🍷 Recomendação de Produtos")

    st.info("""
    Sistema de recomendação baseado em compras anteriores e perfil do cliente.
    """)

    col1, col2 = st.columns(2)

    with col1:
        cliente_id = st.number_input("ID do Cliente", min_value=1, value=1, key="rec_customer")

    with col2:
        top_n = st.slider("Número de Recomendações", min_value=3, max_value=10, value=5)

    if st.button("🎯 Gerar Recomendações", type="primary"):
        with st.spinner("Analisando preferências..."):
            try:
                recommender = ProductRecommender()
                recommender.load_historical_data()
                recommendations = recommender.recommend_products(cliente_id, top_n)

                if not recommendations:
                    st.warning("Cliente não encontrado ou sem histórico suficiente.")
                else:
                    st.success(f"✅ {len(recommendations)} produtos recomendados!")

                    st.markdown("### 🏆 Top Recomendações")

                    for i, rec in enumerate(recommendations, 1):
                        with st.expander(f"#{i} - {rec['nome']} ({rec['tipo_uva']})"):
                            col1, col2 = st.columns(2)

                            with col1:
                                st.markdown(f"""
                                **Detalhes do Produto:**
                                - 🍇 Tipo: {rec['tipo_uva']}
                                - 🌍 País: {rec['pais']}
                                - 💰 Preço Médio: R$ {rec['avg_price']:.2f}
                                """)

                            with col2:
                                st.markdown(f"""
                                **Score de Recomendação:**
                                - ⭐ Popularidade: {rec['popularity_score']}
                                - 📊 Motivo: {rec['reason']}
                                """)

                                # Barra de popularidade
                                st.progress(min(rec['popularity_score'] / 10, 1.0))

            except Exception as e:
                st.error(f"Erro: {e}")
                st.exception(e)

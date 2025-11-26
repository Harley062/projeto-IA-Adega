"""
Módulo de Análises de Negócio Complementares
Contém: Margem/Rentabilidade, Cross-Selling, Primeiro vs Recorrente, Metas/KPIs, Geografia, Reativação
"""
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from typing import Dict, Tuple, List, Optional
import logging
from datetime import datetime, timedelta
from itertools import combinations

logger = logging.getLogger(__name__)


class ProfitabilityAnalyzer:
    """Análise de Margem e Rentabilidade"""

    def __init__(self, data: pd.DataFrame):
        self.data = data.copy()

    def calculate_profit_margins(self, cost_data: Optional[pd.DataFrame] = None) -> pd.DataFrame:
        """
        Calcula margens de lucro por produto
        Se cost_data não for fornecido, estima margem baseada em percentual padrão
        """
        if 'produto_id' not in self.data.columns or 'valor' not in self.data.columns:
            return pd.DataFrame()

        # Agregar vendas por produto
        product_sales = self.data.groupby('produto_id').agg({
            'valor': ['sum', 'mean', 'count'],
            'quantidade': 'sum' if 'quantidade' in self.data.columns else 'count'
        }).reset_index()

        product_sales.columns = ['produto_id', 'receita_total', 'preco_medio', 'num_vendas', 'unidades_vendidas']

        # Se não tiver dados de custo, estimar margem padrão (vinhos geralmente têm margem 30-50%)
        if cost_data is None:
            # Estimativa conservadora: margem de 35%
            product_sales['custo_estimado'] = product_sales['preco_medio'] * 0.65
            product_sales['lucro_unitario'] = product_sales['preco_medio'] - product_sales['custo_estimado']
            product_sales['margem_percentual'] = 35.0
            product_sales['lucro_total'] = product_sales['receita_total'] * 0.35
        else:
            # Usar dados reais de custo se fornecidos
            product_sales = product_sales.merge(cost_data, on='produto_id', how='left')
            product_sales['lucro_unitario'] = product_sales['preco_medio'] - product_sales['custo_unitario']
            product_sales['margem_percentual'] = (product_sales['lucro_unitario'] / product_sales['preco_medio'] * 100)
            product_sales['lucro_total'] = product_sales['lucro_unitario'] * product_sales['unidades_vendidas']

        # Classificar produtos por rentabilidade
        def classify_profitability(row):
            receita = row['receita_total']
            margem = row['margem_percentual']

            if receita > product_sales['receita_total'].quantile(0.75) and margem > 40:
                return 'Estrela (Alta Receita + Alta Margem)'
            elif receita > product_sales['receita_total'].quantile(0.75) and margem <= 40:
                return 'Vaca Leiteira (Alta Receita + Baixa Margem)'
            elif receita <= product_sales['receita_total'].quantile(0.75) and margem > 40:
                return 'Oportunidade (Baixa Receita + Alta Margem)'
            else:
                return 'Peso Morto (Baixa Receita + Baixa Margem)'

        product_sales['classificacao'] = product_sales.apply(classify_profitability, axis=1)

        # Adicionar nome do produto se disponível
        if 'nome' in self.data.columns:
            product_info = self.data.groupby('produto_id')['nome'].first().reset_index()
            product_sales = product_sales.merge(product_info, on='produto_id', how='left')

        return product_sales.sort_values('lucro_total', ascending=False)

    def identify_low_margin_products(self, threshold: float = 25.0) -> pd.DataFrame:
        """Identifica produtos com margem abaixo do threshold"""
        margins = self.calculate_profit_margins()

        if margins.empty:
            return pd.DataFrame()

        low_margin = margins[margins['margem_percentual'] < threshold].copy()
        low_margin['acao_recomendada'] = low_margin['margem_percentual'].apply(
            lambda x: 'URGENTE: Renegociar com fornecedor' if x < 20 else 'Aumentar preço gradualmente'
        )

        return low_margin.sort_values('receita_total', ascending=False)

    def profitability_summary(self) -> Dict:
        """Resumo geral de rentabilidade"""
        margins = self.calculate_profit_margins()

        if margins.empty:
            return {}

        return {
            'receita_total': float(margins['receita_total'].sum()),
            'lucro_total_estimado': float(margins['lucro_total'].sum()),
            'margem_media': float(margins['margem_percentual'].mean()),
            'produto_mais_lucrativo': margins.iloc[0]['produto_id'] if len(margins) > 0 else None,
            'lucro_produto_top': float(margins.iloc[0]['lucro_total']) if len(margins) > 0 else 0,
            'num_estrelas': len(margins[margins['classificacao'] == 'Estrela (Alta Receita + Alta Margem)']),
            'num_peso_morto': len(margins[margins['classificacao'] == 'Peso Morto (Baixa Receita + Baixa Margem)'])
        }


class BasketAnalyzer:
    """Análise de Cesta e Cross-Selling"""

    def __init__(self, data: pd.DataFrame):
        self.data = data.copy()

    def find_product_associations(self, min_support: int = 3) -> pd.DataFrame:
        """
        Encontra produtos frequentemente comprados juntos
        min_support: número mínimo de vezes que produtos devem aparecer juntos
        """
        if 'compra_id' not in self.data.columns or 'produto_id' not in self.data.columns:
            return pd.DataFrame()

        # Agrupar produtos por compra
        baskets = self.data.groupby('compra_id')['produto_id'].apply(list).reset_index()

        # Filtrar cestas com mais de 1 produto
        baskets = baskets[baskets['produto_id'].apply(len) > 1]

        if baskets.empty:
            return pd.DataFrame()

        # Encontrar pares de produtos
        pairs = []
        for _, row in baskets.iterrows():
            products = row['produto_id']
            # Gerar todas as combinações de pares
            for combo in combinations(sorted(set(products)), 2):
                pairs.append(combo)

        # Contar frequência de cada par
        pair_counts = pd.DataFrame(pairs, columns=['produto_1', 'produto_2'])
        pair_freq = pair_counts.groupby(['produto_1', 'produto_2']).size().reset_index(name='frequencia')

        # Filtrar por suporte mínimo
        pair_freq = pair_freq[pair_freq['frequencia'] >= min_support]

        # Calcular confiança (% das vezes que produto_2 é comprado quando produto_1 é comprado)
        product_counts = self.data.groupby('produto_id')['compra_id'].nunique().to_dict()

        pair_freq['confianca_1_2'] = pair_freq.apply(
            lambda row: (row['frequencia'] / product_counts.get(row['produto_1'], 1) * 100), axis=1
        )

        pair_freq['confianca_2_1'] = pair_freq.apply(
            lambda row: (row['frequencia'] / product_counts.get(row['produto_2'], 1) * 100), axis=1
        )

        # Adicionar nomes dos produtos se disponível
        if 'nome' in self.data.columns:
            product_names = self.data.groupby('produto_id')['nome'].first().to_dict()
            pair_freq['nome_produto_1'] = pair_freq['produto_1'].map(product_names)
            pair_freq['nome_produto_2'] = pair_freq['produto_2'].map(product_names)

        return pair_freq.sort_values('frequencia', ascending=False)

    def suggest_bundles(self, min_freq: int = 5) -> pd.DataFrame:
        """Sugere combos/kits baseado em produtos comprados juntos"""
        associations = self.find_product_associations(min_support=min_freq)

        if associations.empty:
            return pd.DataFrame()

        # Filtrar apenas associações fortes (confiança > 30%)
        strong_assoc = associations[
            (associations['confianca_1_2'] > 30) | (associations['confianca_2_1'] > 30)
        ].copy()

        # Sugerir desconto para o combo (5-15%)
        strong_assoc['desconto_sugerido'] = '10-15%'
        strong_assoc['tipo_bundle'] = strong_assoc['confianca_1_2'].apply(
            lambda x: 'Combo Premium' if x > 50 else 'Combo Básico'
        )

        return strong_assoc.head(20)

    def calculate_basket_metrics(self) -> Dict:
        """Calcula métricas gerais da cesta"""
        if 'compra_id' not in self.data.columns:
            return {}

        # Número de produtos por compra
        products_per_purchase = self.data.groupby('compra_id')['produto_id'].nunique()

        # Valor médio da cesta
        basket_value = self.data.groupby('compra_id')['valor'].sum() if 'valor' in self.data.columns else None

        metrics = {
            'produtos_por_compra_medio': float(products_per_purchase.mean()),
            'produtos_por_compra_max': int(products_per_purchase.max()),
            'compras_multiplas': int((products_per_purchase > 1).sum()),
            'percent_compras_multiplas': float((products_per_purchase > 1).sum() / len(products_per_purchase) * 100)
        }

        if basket_value is not None:
            metrics['valor_cesta_medio'] = float(basket_value.mean())
            metrics['valor_cesta_max'] = float(basket_value.max())

        return metrics


class CustomerJourneyAnalyzer:
    """Análise de Jornada do Cliente (Primeiro vs Recorrente)"""

    def __init__(self, data: pd.DataFrame):
        self.data = data.copy()
        if 'data_compra' in self.data.columns:
            self.data['data_compra'] = pd.to_datetime(self.data['data_compra'], errors='coerce')

    def identify_first_vs_recurring(self) -> pd.DataFrame:
        """Identifica primeira compra vs compras recorrentes"""
        if 'cliente_id' not in self.data.columns or 'data_compra' not in self.data.columns:
            return pd.DataFrame()

        df = self.data.dropna(subset=['data_compra']).copy()

        # Ordenar por cliente e data
        df = df.sort_values(['cliente_id', 'data_compra'])

        # Marcar primeira compra
        df['ordem_compra'] = df.groupby('cliente_id').cumcount() + 1
        df['primeira_compra'] = df['ordem_compra'] == 1

        return df

    def calculate_conversion_rate(self) -> Dict:
        """Calcula taxa de conversão de primeira para segunda compra"""
        journey = self.identify_first_vs_recurring()

        if journey.empty:
            return {}

        total_customers = journey['cliente_id'].nunique()
        customers_with_multiple = len(journey[journey['ordem_compra'] > 1]['cliente_id'].unique())

        conversion_rate = (customers_with_multiple / total_customers * 100) if total_customers > 0 else 0

        # Tempo médio até segunda compra
        df = journey[journey['ordem_compra'].isin([1, 2])].copy()
        first_purchases = df[df['ordem_compra'] == 1][['cliente_id', 'data_compra']].rename(
            columns={'data_compra': 'primeira_compra'}
        )
        second_purchases = df[df['ordem_compra'] == 2][['cliente_id', 'data_compra']].rename(
            columns={'data_compra': 'segunda_compra'}
        )

        merged = first_purchases.merge(second_purchases, on='cliente_id', how='inner')
        merged['dias_ate_segunda'] = (merged['segunda_compra'] - merged['primeira_compra']).dt.days

        avg_days = merged['dias_ate_segunda'].mean() if not merged.empty else 0

        return {
            'total_clientes': total_customers,
            'clientes_recorrentes': customers_with_multiple,
            'taxa_conversao': float(conversion_rate),
            'dias_medio_ate_segunda_compra': float(avg_days),
            'clientes_one_time': total_customers - customers_with_multiple
        }

    def analyze_first_purchase_products(self) -> pd.DataFrame:
        """Analisa quais produtos convertem melhor na primeira compra"""
        journey = self.identify_first_vs_recurring()

        if journey.empty or 'produto_id' not in journey.columns:
            return pd.DataFrame()

        # Produtos comprados na primeira compra
        first_purchases = journey[journey['primeira_compra']]

        product_stats = first_purchases.groupby('produto_id').agg({
            'cliente_id': 'nunique'
        }).reset_index()

        product_stats.columns = ['produto_id', 'num_primeiras_compras']

        # Calcular quantos desses clientes voltaram
        first_purchase_customers = first_purchases.groupby('produto_id')['cliente_id'].apply(set).to_dict()
        recurring_customers = journey[journey['ordem_compra'] > 1].groupby('produto_id')['cliente_id'].apply(set).to_dict()

        conversion_data = []
        for produto_id, first_customers in first_purchase_customers.items():
            recurring = recurring_customers.get(produto_id, set())
            returned = len(first_customers.intersection(recurring))
            total = len(first_customers)
            conversion_rate = (returned / total * 100) if total > 0 else 0

            conversion_data.append({
                'produto_id': produto_id,
                'clientes_primeira_compra': total,
                'clientes_retornaram': returned,
                'taxa_retencao': conversion_rate
            })

        result = pd.DataFrame(conversion_data)

        # Adicionar nome do produto
        if 'nome' in self.data.columns:
            product_names = self.data.groupby('produto_id')['nome'].first().reset_index()
            result = result.merge(product_names, on='produto_id', how='left')

        return result.sort_values('taxa_retencao', ascending=False)


class GoalTracker:
    """Dashboard de Metas e KPIs"""

    def __init__(self, data: pd.DataFrame):
        self.data = data.copy()
        if 'data_compra' in self.data.columns:
            self.data['data_compra'] = pd.to_datetime(self.data['data_compra'], errors='coerce')

    def set_monthly_goal(self, target_revenue: float, target_customers: int = None) -> Dict:
        """Define e acompanha meta mensal"""
        if 'data_compra' not in self.data.columns or 'valor' not in self.data.columns:
            return {}

        df = self.data.dropna(subset=['data_compra'])

        # Pegar mês atual (ou último mês nos dados)
        current_month = df['data_compra'].max().to_period('M')
        current_data = df[df['data_compra'].dt.to_period('M') == current_month]

        actual_revenue = current_data['valor'].sum()
        actual_customers = current_data['cliente_id'].nunique() if 'cliente_id' in current_data.columns else 0

        # Calcular progresso
        revenue_progress = (actual_revenue / target_revenue * 100) if target_revenue > 0 else 0
        customer_progress = (actual_customers / target_customers * 100) if target_customers and target_customers > 0 else None

        # Projeção para fim do mês
        days_in_month = current_month.days_in_month
        current_day = df['data_compra'].max().day
        days_remaining = days_in_month - current_day

        if current_day > 0:
            daily_avg = actual_revenue / current_day
            projected_revenue = daily_avg * days_in_month
        else:
            projected_revenue = 0

        return {
            'meta_receita': target_revenue,
            'receita_atual': float(actual_revenue),
            'progresso_receita': float(revenue_progress),
            'projecao_fim_mes': float(projected_revenue),
            'vai_bater_meta': projected_revenue >= target_revenue,
            'meta_clientes': target_customers,
            'clientes_atual': actual_customers,
            'progresso_clientes': float(customer_progress) if customer_progress else None,
            'dias_restantes': int(days_remaining)
        }

    def calculate_kpis(self) -> Dict:
        """Calcula KPIs principais do negócio"""
        if self.data.empty:
            return {}

        kpis = {}

        # Receita total
        if 'valor' in self.data.columns:
            kpis['receita_total'] = float(self.data['valor'].sum())
            kpis['ticket_medio'] = float(self.data['valor'].mean())
            kpis['ticket_mediano'] = float(self.data['valor'].median())

        # Clientes
        if 'cliente_id' in self.data.columns:
            kpis['total_clientes'] = int(self.data['cliente_id'].nunique())
            kpis['total_transacoes'] = int(self.data['compra_id'].nunique()) if 'compra_id' in self.data.columns else len(self.data)
            kpis['transacoes_por_cliente'] = float(kpis['total_transacoes'] / kpis['total_clientes']) if kpis['total_clientes'] > 0 else 0

        # Produtos
        if 'produto_id' in self.data.columns:
            kpis['produtos_unicos_vendidos'] = int(self.data['produto_id'].nunique())
            kpis['unidades_vendidas'] = int(self.data['quantidade'].sum()) if 'quantidade' in self.data.columns else len(self.data)

        # Taxa de churn (se disponível)
        if 'cancelou_assinatura' in self.data.columns:
            total = len(self.data)
            churned = (self.data['cancelou_assinatura'] == 'Sim').sum()
            kpis['taxa_churn'] = float(churned / total * 100) if total > 0 else 0

        return kpis

    def compare_periods(self, period: str = 'month') -> pd.DataFrame:
        """Compara performance entre períodos (mês a mês, ano a ano)"""
        if 'data_compra' not in self.data.columns or 'valor' not in self.data.columns:
            return pd.DataFrame()

        df = self.data.dropna(subset=['data_compra']).copy()

        if period == 'month':
            df['periodo'] = df['data_compra'].dt.to_period('M').astype(str)
        elif period == 'quarter':
            df['periodo'] = df['data_compra'].dt.to_period('Q').astype(str)
        elif period == 'year':
            df['periodo'] = df['data_compra'].dt.year.astype(str)
        else:
            df['periodo'] = df['data_compra'].dt.to_period('M').astype(str)

        comparison = df.groupby('periodo').agg({
            'valor': ['sum', 'mean', 'count'],
            'cliente_id': 'nunique' if 'cliente_id' in df.columns else 'count'
        }).reset_index()

        comparison.columns = ['periodo', 'receita_total', 'ticket_medio', 'num_vendas', 'clientes_unicos']

        # Calcular variação período a período
        comparison['var_receita'] = comparison['receita_total'].pct_change() * 100
        comparison['var_clientes'] = comparison['clientes_unicos'].pct_change() * 100

        return comparison.sort_values('periodo')


class GeographicAnalyzer:
    """Análise Geográfica Avançada"""

    def __init__(self, data: pd.DataFrame):
        self.data = data.copy()

    def city_performance(self) -> pd.DataFrame:
        """Análise detalhada por cidade"""
        if 'cidade' not in self.data.columns or 'valor' not in self.data.columns:
            return pd.DataFrame()

        city_stats = self.data.groupby('cidade').agg({
            'valor': ['sum', 'mean', 'count'],
            'cliente_id': 'nunique' if 'cliente_id' in self.data.columns else 'count',
            'quantidade': 'sum' if 'quantidade' in self.data.columns else 'count'
        }).reset_index()

        city_stats.columns = ['cidade', 'receita_total', 'ticket_medio', 'num_vendas', 'clientes_unicos', 'unidades_vendidas']

        # Calcular penetração de mercado (% de participação)
        city_stats['participacao_receita'] = city_stats['receita_total'] / city_stats['receita_total'].sum() * 100

        # Classificar cidades
        def classify_city(row):
            receita = row['receita_total']
            q75 = city_stats['receita_total'].quantile(0.75)
            q25 = city_stats['receita_total'].quantile(0.25)

            if receita >= q75:
                return 'Mercado Consolidado'
            elif receita >= q25:
                return 'Mercado em Crescimento'
            else:
                return 'Mercado Potencial'

        city_stats['classificacao'] = city_stats.apply(classify_city, axis=1)

        return city_stats.sort_values('receita_total', ascending=False)

    def identify_expansion_opportunities(self) -> pd.DataFrame:
        """Identifica oportunidades de expansão geográfica"""
        city_perf = self.city_performance()

        if city_perf.empty:
            return pd.DataFrame()

        # Cidades com poucos clientes mas alto ticket médio = oportunidade
        opportunities = city_perf[
            (city_perf['clientes_unicos'] < city_perf['clientes_unicos'].median()) &
            (city_perf['ticket_medio'] > city_perf['ticket_medio'].median())
        ].copy()

        opportunities['potencial'] = 'Alto - Poucos clientes mas gastam bem'
        opportunities['acao_recomendada'] = 'Investir em marketing local + parcerias'

        return opportunities.sort_values('ticket_medio', ascending=False)

    def geographic_summary(self) -> Dict:
        """Resumo geográfico"""
        city_perf = self.city_performance()

        if city_perf.empty:
            return {}

        return {
            'num_cidades': len(city_perf),
            'cidade_top': city_perf.iloc[0]['cidade'] if len(city_perf) > 0 else None,
            'receita_cidade_top': float(city_perf.iloc[0]['receita_total']) if len(city_perf) > 0 else 0,
            'concentracao_top_5': float(city_perf.head(5)['participacao_receita'].sum()),
            'mercados_consolidados': len(city_perf[city_perf['classificacao'] == 'Mercado Consolidado']),
            'oportunidades_expansao': len(city_perf[city_perf['classificacao'] == 'Mercado Potencial'])
        }


class ReactivationAnalyzer:
    """Análise de Reativação de Clientes"""

    def __init__(self, data: pd.DataFrame):
        self.data = data.copy()
        if 'data_compra' in self.data.columns:
            self.data['data_compra'] = pd.to_datetime(self.data['data_compra'], errors='coerce')

    def identify_inactive_customers(self, days_threshold: int = 60) -> pd.DataFrame:
        """Identifica clientes inativos"""
        if 'cliente_id' not in self.data.columns or 'data_compra' not in self.data.columns:
            return pd.DataFrame()

        df = self.data.dropna(subset=['data_compra'])
        ref_date = df['data_compra'].max()

        # Última compra de cada cliente
        last_purchase = df.groupby('cliente_id').agg({
            'data_compra': 'max',
            'valor': ['sum', 'mean', 'count']
        }).reset_index()

        last_purchase.columns = ['cliente_id', 'ultima_compra', 'receita_total', 'ticket_medio', 'num_compras']

        # Calcular dias de inatividade
        last_purchase['dias_inativo'] = (ref_date - last_purchase['ultima_compra']).dt.days

        # Filtrar inativos
        inactive = last_purchase[last_purchase['dias_inativo'] >= days_threshold].copy()

        # Classificar risco
        def classify_risk(days):
            if days >= 180:
                return 'Crítico'
            elif days >= 120:
                return 'Alto'
            else:
                return 'Médio'

        inactive['risco'] = inactive['dias_inativo'].apply(classify_risk)

        # Prioridade de reativação (baseado em receita histórica)
        inactive['prioridade'] = pd.qcut(
            inactive['receita_total'],
            q=3,
            labels=['Baixa', 'Média', 'Alta']
        )

        # Sugerir oferta de reativação
        def suggest_offer(row):
            if row['prioridade'] == 'Alta' and row['risco'] == 'Crítico':
                return 'Desconto 30% + Frete Grátis + Brinde'
            elif row['prioridade'] == 'Alta':
                return 'Desconto 20% + Frete Grátis'
            elif row['risco'] == 'Crítico':
                return 'Desconto 25%'
            else:
                return 'Desconto 15%'

        inactive['oferta_sugerida'] = inactive.apply(suggest_offer, axis=1)

        # Adicionar nome do cliente se disponível
        if 'nome' in self.data.columns:
            customer_names = self.data.groupby('cliente_id')['nome'].first().reset_index()
            inactive = inactive.merge(customer_names, on='cliente_id', how='left')

        return inactive.sort_values(['prioridade', 'receita_total'], ascending=[False, False])

    def calculate_reactivation_metrics(self) -> Dict:
        """Calcula métricas de reativação"""
        inactive_30 = self.identify_inactive_customers(days_threshold=30)
        inactive_60 = self.identify_inactive_customers(days_threshold=60)
        inactive_90 = self.identify_inactive_customers(days_threshold=90)

        total_customers = self.data['cliente_id'].nunique() if 'cliente_id' in self.data.columns else 0

        return {
            'clientes_inativos_30d': len(inactive_30),
            'clientes_inativos_60d': len(inactive_60),
            'clientes_inativos_90d': len(inactive_90),
            'taxa_inatividade_60d': float(len(inactive_60) / total_customers * 100) if total_customers > 0 else 0,
            'receita_em_risco_60d': float(inactive_60['receita_total'].sum()) if not inactive_60.empty else 0,
            'clientes_alta_prioridade': len(inactive_60[inactive_60['prioridade'] == 'Alta']) if not inactive_60.empty else 0
        }

    def create_reactivation_campaign(self, days_threshold: int = 60, max_customers: int = 100) -> pd.DataFrame:
        """Cria lista pronta para campanha de reativação"""
        inactive = self.identify_inactive_customers(days_threshold)

        if inactive.empty:
            return pd.DataFrame()

        # Selecionar top clientes por prioridade
        campaign = inactive.head(max_customers).copy()

        # Adicionar campos úteis para campanha
        campaign['canal_recomendado'] = campaign['prioridade'].apply(
            lambda x: 'Telefone + Email' if x == 'Alta' else 'Email'
        )

        campaign['timing'] = 'Enviar imediatamente'

        display_cols = ['cliente_id']
        if 'nome' in campaign.columns:
            display_cols.append('nome')

        display_cols.extend([
            'dias_inativo',
            'receita_total',
            'risco',
            'prioridade',
            'oferta_sugerida',
            'canal_recomendado'
        ])

        return campaign[display_cols]

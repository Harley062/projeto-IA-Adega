"""
Módulo de Análises Avançadas para Oportunidades de Negócio
Contém análises de: Sazonalidade, Gestão de Estoque, e Cliente VIP
"""
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from typing import Dict, Tuple, List
import logging
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


class SeasonalityAnalyzer:
    """Análise de Sazonalidade e Previsão de Demanda"""

    def __init__(self, data: pd.DataFrame):
        self.data = data.copy()
        if 'data_compra' in self.data.columns:
            self.data['data_compra'] = pd.to_datetime(self.data['data_compra'], errors='coerce')

    def get_monthly_patterns(self) -> pd.DataFrame:
        """Retorna padrões de venda mensais"""
        if 'data_compra' not in self.data.columns:
            return pd.DataFrame()

        df = self.data.dropna(subset=['data_compra'])
        df['mes'] = df['data_compra'].dt.month
        df['mes_nome'] = df['data_compra'].dt.strftime('%B')
        df['ano'] = df['data_compra'].dt.year

        monthly = df.groupby(['ano', 'mes', 'mes_nome']).agg({
            'valor': 'sum',
            'quantidade': 'sum',
            'compra_id': 'count'
        }).reset_index()

        monthly.columns = ['ano', 'mes', 'mes_nome', 'receita', 'unidades_vendidas', 'num_vendas']
        monthly['ticket_medio'] = monthly['receita'] / monthly['num_vendas']

        return monthly.sort_values(['ano', 'mes'])

    def identify_peak_months(self) -> Dict:
        """Identifica meses de pico e baixa"""
        monthly = self.get_monthly_patterns()

        if monthly.empty:
            return {}

        # Média por mês (agregando todos os anos)
        avg_by_month = monthly.groupby('mes_nome')['receita'].mean().sort_values(ascending=False)

        return {
            'melhor_mes': avg_by_month.index[0] if len(avg_by_month) > 0 else None,
            'melhor_receita': float(avg_by_month.iloc[0]) if len(avg_by_month) > 0 else 0,
            'pior_mes': avg_by_month.index[-1] if len(avg_by_month) > 0 else None,
            'pior_receita': float(avg_by_month.iloc[-1]) if len(avg_by_month) > 0 else 0,
            'variacao_percentual': float(((avg_by_month.iloc[0] - avg_by_month.iloc[-1]) / avg_by_month.iloc[-1] * 100)) if len(avg_by_month) > 1 and avg_by_month.iloc[-1] > 0 else 0
        }

    def product_seasonality(self) -> pd.DataFrame:
        """Retorna sazonalidade por produto"""
        if 'data_compra' not in self.data.columns or 'produto_id' not in self.data.columns:
            return pd.DataFrame()

        df = self.data.dropna(subset=['data_compra'])
        df['mes'] = df['data_compra'].dt.month

        product_season = df.groupby(['produto_id', 'mes']).agg({
            'quantidade': 'sum'
        }).reset_index()

        # Encontrar o mês de pico para cada produto
        idx = product_season.groupby('produto_id')['quantidade'].idxmax()
        peak_months = product_season.loc[idx][['produto_id', 'mes', 'quantidade']]
        peak_months.columns = ['produto_id', 'mes_pico', 'quantidade_pico']

        return peak_months

    def demand_forecast_simple(self, months_ahead: int = 3) -> pd.DataFrame:
        """Previsão simples de demanda baseada em média móvel"""
        monthly = self.get_monthly_patterns()

        if monthly.empty or len(monthly) < 3:
            return pd.DataFrame()

        # Calcular média móvel dos últimos 3 meses
        recent_avg = monthly.tail(3)['receita'].mean()
        recent_units = monthly.tail(3)['unidades_vendidas'].mean()

        # Gerar previsões
        last_date = monthly['ano'].max()
        last_month = monthly[monthly['ano'] == last_date]['mes'].max()

        forecasts = []
        for i in range(1, months_ahead + 1):
            next_month = last_month + i
            next_year = last_date
            if next_month > 12:
                next_month = next_month % 12
                next_year += 1

            forecasts.append({
                'mes': next_month,
                'ano': next_year,
                'receita_prevista': recent_avg,
                'unidades_previstas': recent_units,
                'tipo': 'previsao'
            })

        return pd.DataFrame(forecasts)


class InventoryManager:
    """Gestão Inteligente de Estoque"""

    def __init__(self, data: pd.DataFrame, dias_estoque_parado: int = 30):
        self.data = data.copy()
        self.dias_estoque_parado = dias_estoque_parado
        if 'data_compra' in self.data.columns:
            self.data['data_compra'] = pd.to_datetime(self.data['data_compra'], errors='coerce')

    def identify_slow_products(self) -> pd.DataFrame:
        """Identifica produtos parados (sem venda há X dias)"""
        if 'data_compra' not in self.data.columns or 'produto_id' not in self.data.columns:
            return pd.DataFrame()

        df = self.data.dropna(subset=['data_compra'])

        # Data de referência (data atual)
        ref_date = pd.Timestamp.now()

        # Última venda de cada produto
        last_sale = df.groupby('produto_id')['data_compra'].max().reset_index()
        last_sale.columns = ['produto_id', 'ultima_venda']

        # Calcular dias parado
        last_sale['dias_parado'] = (ref_date - last_sale['ultima_venda']).dt.days

        # Filtrar produtos parados
        slow_products = last_sale[last_sale['dias_parado'] >= self.dias_estoque_parado].copy()

        # Adicionar informações do produto
        # Procurar pela coluna correta de nome do produto
        nome_col = None
        for col in ['nome_produto', 'nome']:
            if col in self.data.columns:
                nome_col = col
                break

        if nome_col:
            product_info = self.data.groupby('produto_id')[nome_col].first().reset_index()
            product_info.columns = ['produto_id', 'nome']
            slow_products = slow_products.merge(product_info, on='produto_id', how='left')

        # Calcular receita perdida (média de vendas * dias parado)
        revenue_per_product = df.groupby('produto_id')['valor'].mean().reset_index()
        revenue_per_product.columns = ['produto_id', 'valor_medio']
        slow_products = slow_products.merge(revenue_per_product, on='produto_id', how='left')
        slow_products['receita_potencial_perdida'] = slow_products['valor_medio'] * (slow_products['dias_parado'] / 30)

        return slow_products.sort_values('dias_parado', ascending=False)

    def calculate_turnover_rate(self) -> pd.DataFrame:
        """Calcula taxa de giro de estoque por produto"""
        if 'produto_id' not in self.data.columns or 'quantidade' not in self.data.columns:
            return pd.DataFrame()

        # Total vendido por produto
        total_sold = self.data.groupby('produto_id')['quantidade'].sum().reset_index()
        total_sold.columns = ['produto_id', 'total_vendido']

        # Número de dias de vendas
        if 'data_compra' in self.data.columns:
            df = self.data.dropna(subset=['data_compra'])
            days_range = (df['data_compra'].max() - df['data_compra'].min()).days
            if days_range == 0:
                days_range = 1
        else:
            days_range = 30  # default

        # Giro = Total vendido / (dias / 30) -> vendas por mês
        total_sold['giro_mensal'] = total_sold['total_vendido'] / (days_range / 30)

        # Classificar produtos
        def classify_turnover(giro):
            if giro >= 10:
                return 'Alto Giro'
            elif giro >= 5:
                return 'Médio Giro'
            else:
                return 'Baixo Giro'

        total_sold['classificacao'] = total_sold['giro_mensal'].apply(classify_turnover)

        # Adicionar nome do produto se disponível
        # Procurar pela coluna correta de nome do produto
        nome_col = None
        for col in ['nome_produto', 'nome']:
            if col in self.data.columns:
                nome_col = col
                break

        if nome_col:
            product_info = self.data.groupby('produto_id')[nome_col].first().reset_index()
            product_info.columns = ['produto_id', 'nome']
            total_sold = total_sold.merge(product_info, on='produto_id', how='left')

        return total_sold.sort_values('giro_mensal', ascending=False)

    def suggest_promotions(self) -> pd.DataFrame:
        """Sugere produtos para promoção"""
        slow = self.identify_slow_products()
        turnover = self.calculate_turnover_rate()

        if slow.empty or turnover.empty:
            return pd.DataFrame()

        # Produtos de baixo giro com dias parado
        low_turnover = turnover[turnover['classificacao'] == 'Baixo Giro']['produto_id'].tolist()

        promo_candidates = slow[slow['produto_id'].isin(low_turnover)].copy()
        promo_candidates['desconto_sugerido'] = '15-25%'
        promo_candidates['urgencia'] = promo_candidates['dias_parado'].apply(
            lambda x: 'URGENTE' if x >= 60 else 'MÉDIA' if x >= 30 else 'BAIXA'
        )

        return promo_candidates.sort_values('receita_potencial_perdida', ascending=False)

    def stock_alerts(self) -> Dict:
        """Gera alertas de estoque"""
        slow = self.identify_slow_products()
        turnover = self.calculate_turnover_rate()

        alerts = {
            'produtos_parados': len(slow),
            'receita_em_risco': float(slow['receita_potencial_perdida'].sum()) if not slow.empty and 'receita_potencial_perdida' in slow.columns else 0,
            'produtos_alto_giro': len(turnover[turnover['classificacao'] == 'Alto Giro']) if not turnover.empty else 0,
            'produtos_baixo_giro': len(turnover[turnover['classificacao'] == 'Baixo Giro']) if not turnover.empty else 0
        }

        return alerts


class VIPAnalyzer:
    """Análise de Clientes VIP e Programa de Fidelidade"""

    def __init__(self, data: pd.DataFrame):
        self.data = data.copy()
        if 'data_compra' in self.data.columns:
            self.data['data_compra'] = pd.to_datetime(self.data['data_compra'], errors='coerce')

    def identify_vip_customers(self, top_percent: float = 20) -> pd.DataFrame:
        """Identifica clientes VIP (top X% por receita)"""
        if 'cliente_id' not in self.data.columns or 'valor' not in self.data.columns:
            return pd.DataFrame()

        # Agregar por cliente
        customer_stats = self.data.groupby('cliente_id').agg({
            'valor': ['sum', 'mean', 'count'],
            'data_compra': 'max' if 'data_compra' in self.data.columns else 'count'
        }).reset_index()

        customer_stats.columns = ['cliente_id', 'receita_total', 'ticket_medio', 'num_compras', 'ultima_compra']

        # Calcular percentil de receita
        threshold = customer_stats['receita_total'].quantile((100 - top_percent) / 100)

        vips = customer_stats[customer_stats['receita_total'] >= threshold].copy()

        # Adicionar informações do cliente
        if 'nome' in self.data.columns:
            customer_info = self.data.groupby('cliente_id')['nome'].first().reset_index()
            vips = vips.merge(customer_info, on='cliente_id', how='left')

        if 'cidade' in self.data.columns:
            city_info = self.data.groupby('cliente_id')['cidade'].first().reset_index()
            vips = vips.merge(city_info, on='cliente_id', how='left')

        # Classificar tier VIP
        def classify_vip_tier(row):
            if row['receita_total'] >= customer_stats['receita_total'].quantile(0.95):
                return 'Platinum'
            elif row['receita_total'] >= customer_stats['receita_total'].quantile(0.90):
                return 'Gold'
            else:
                return 'Silver'

        vips['tier_vip'] = vips.apply(classify_vip_tier, axis=1)

        return vips.sort_values('receita_total', ascending=False)

    def detect_inactive_vips(self, days_inactive: int = 30) -> pd.DataFrame:
        """Detecta VIPs inativos (sem compra há X dias)"""
        vips = self.identify_vip_customers()

        if vips.empty or 'ultima_compra' not in vips.columns:
            return pd.DataFrame()

        # Data de referência
        if 'data_compra' in self.data.columns:
            ref_date = self.data['data_compra'].max()
        else:
            ref_date = pd.Timestamp.now()

        # Calcular dias de inatividade
        vips['dias_inativo'] = (ref_date - vips['ultima_compra']).dt.days

        inactive_vips = vips[vips['dias_inativo'] >= days_inactive].copy()

        # Calcular risco de churn
        inactive_vips['risco_churn'] = inactive_vips['dias_inativo'].apply(
            lambda x: 'CRÍTICO' if x >= 90 else 'ALTO' if x >= 60 else 'MÉDIO'
        )

        # Sugerir ação
        def suggest_action(row):
            if row['dias_inativo'] >= 90:
                return f"URGENTE: Ligar pessoalmente + desconto 25% ({row.get('nome', row['cliente_id'])})"
            elif row['dias_inativo'] >= 60:
                return f"Campanha de reativação + brinde especial"
            else:
                return f"Email personalizado com novidades"

        inactive_vips['acao_sugerida'] = inactive_vips.apply(suggest_action, axis=1)

        return inactive_vips.sort_values('receita_total', ascending=False)

    def loyalty_program_tiers(self) -> pd.DataFrame:
        """Define tiers do programa de fidelidade"""
        if 'cliente_id' not in self.data.columns:
            return pd.DataFrame()

        customer_stats = self.data.groupby('cliente_id').agg({
            'valor': 'sum',
            'compra_id': 'count'
        }).reset_index()

        customer_stats.columns = ['cliente_id', 'receita_total', 'num_compras']

        # Definir tiers baseado em receita e frequência
        def assign_tier(row):
            receita = row['receita_total']
            compras = row['num_compras']

            # Platinum: Top 5% receita OU 15+ compras
            if receita >= customer_stats['receita_total'].quantile(0.95) or compras >= 15:
                return 'Platinum', 'Desconto 20% + Frete Grátis + Degustação Exclusiva'
            # Gold: Top 15% receita OU 10+ compras
            elif receita >= customer_stats['receita_total'].quantile(0.85) or compras >= 10:
                return 'Gold', 'Desconto 15% + Frete Grátis'
            # Silver: Top 30% receita OU 5+ compras
            elif receita >= customer_stats['receita_total'].quantile(0.70) or compras >= 5:
                return 'Silver', 'Desconto 10%'
            # Bronze: demais
            else:
                return 'Bronze', 'Desconto 5% na próxima compra'

        customer_stats[['tier', 'beneficios']] = customer_stats.apply(
            lambda row: pd.Series(assign_tier(row)), axis=1
        )

        # Adicionar nome do cliente
        if 'nome' in self.data.columns:
            customer_info = self.data.groupby('cliente_id')['nome'].first().reset_index()
            customer_stats = customer_stats.merge(customer_info, on='cliente_id', how='left')

        return customer_stats.sort_values('receita_total', ascending=False)

    def vip_contribution_analysis(self) -> Dict:
        """Análise da contribuição dos VIPs para o negócio"""
        vips = self.identify_vip_customers(top_percent=20)

        if vips.empty:
            return {}

        total_revenue = self.data['valor'].sum() if 'valor' in self.data.columns else 0
        vip_revenue = vips['receita_total'].sum()

        total_customers = self.data['cliente_id'].nunique() if 'cliente_id' in self.data.columns else 0
        vip_customers = len(vips)

        return {
            'num_vips': vip_customers,
            'percent_vips': (vip_customers / total_customers * 100) if total_customers > 0 else 0,
            'receita_vips': float(vip_revenue),
            'percent_receita_vips': (vip_revenue / total_revenue * 100) if total_revenue > 0 else 0,
            'ticket_medio_vip': float(vips['ticket_medio'].mean()),
            'ticket_medio_geral': float(self.data['valor'].mean()) if 'valor' in self.data.columns else 0
        }

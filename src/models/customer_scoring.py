"""
Sistema de Scoring de Clientes para Adega

Este módulo implementa um sistema abrangente de scoring de clientes que combina:
- RFM (Recency, Frequency, Monetary)
- Engajamento
- Fidelidade (Assinatura)
- CLV (Customer Lifetime Value)
- Risco de Churn

Autor: Sistema IA Adega
Data: 2025-11
"""

import pandas as pd
import numpy as np
from datetime import datetime
from typing import Dict, Tuple
import warnings
warnings.filterwarnings('ignore')


class CustomerScoring:
    """
    Classe para calcular scores abrangentes de clientes baseados em múltiplos fatores.
    """

    def __init__(self, data: pd.DataFrame, reference_date: datetime = None):
        """
        Inicializa o sistema de scoring.

        Args:
            data: DataFrame com dados de clientes e compras
            reference_date: Data de referência para cálculos (padrão: data atual)
        """
        self.data = data.copy()
        self.reference_date = reference_date or datetime.now()
        self.scores = None

    def calculate_rfm_scores(self) -> pd.DataFrame:
        """
        Calcula scores RFM (Recency, Frequency, Monetary) para cada cliente.

        Returns:
            DataFrame com colunas: cliente_id, recencia, frequencia, valor_total,
                                   r_score, f_score, m_score, rfm_score
        """
        # Garantir que data_compra está no formato datetime
        if 'data_compra' in self.data.columns:
            self.data['data_compra'] = pd.to_datetime(self.data['data_compra'], errors='coerce')

        # Filtrar apenas registros com dados válidos de cliente
        # (remover registros onde cliente_id não tem informações completas)
        valid_data = self.data.dropna(subset=['cliente_id', 'nome', 'idade', 'cidade'])

        # Calcular métricas RFM
        rfm = valid_data.groupby('cliente_id').agg({
            'data_compra': lambda x: (self.reference_date - x.max()).days,  # Recency
            'compra_id': 'count',                                            # Frequency
            'valor': 'sum'                                                   # Monetary
        }).reset_index()

        rfm.columns = ['cliente_id', 'recencia', 'frequencia', 'valor_total']

        # Calcular quartis e scores (1-4, onde 4 é o melhor)
        # Usar uma abordagem mais robusta que lida com duplicatas

        # Recency: menor é melhor (inverter ordem)
        try:
            rfm['r_score'] = pd.qcut(rfm['recencia'], q=4, labels=False, duplicates='drop')
            # Inverter: 0->4, 1->3, 2->2, 3->1
            rfm['r_score'] = rfm['r_score'].max() - rfm['r_score'] + 1
        except (ValueError, TypeError):
            # Se não conseguir fazer quartis, usar ranking simples
            if rfm['recencia'].nunique() == 1:
                # Todos os valores são iguais
                rfm['r_score'] = 2.5
            else:
                rfm['r_score'] = rfm['recencia'].rank(method='dense', ascending=True)
                range_val = rfm['r_score'].max() - rfm['r_score'].min()
                if range_val > 0:
                    rfm['r_score'] = (rfm['r_score'] - rfm['r_score'].min()) / range_val * 3 + 1
                    rfm['r_score'] = 5 - rfm['r_score']  # Inverter
                else:
                    rfm['r_score'] = 2.5

        # Frequency: maior é melhor
        try:
            rfm['f_score'] = pd.qcut(rfm['frequencia'], q=4, labels=False, duplicates='drop') + 1
        except (ValueError, TypeError):
            if rfm['frequencia'].nunique() == 1:
                rfm['f_score'] = 2.5
            else:
                rfm['f_score'] = rfm['frequencia'].rank(method='dense', ascending=True)
                range_val = rfm['f_score'].max() - rfm['f_score'].min()
                if range_val > 0:
                    rfm['f_score'] = (rfm['f_score'] - rfm['f_score'].min()) / range_val * 3 + 1
                else:
                    rfm['f_score'] = 2.5

        # Monetary: maior é melhor
        try:
            rfm['m_score'] = pd.qcut(rfm['valor_total'], q=4, labels=False, duplicates='drop') + 1
        except (ValueError, TypeError):
            if rfm['valor_total'].nunique() == 1:
                rfm['m_score'] = 2.5
            else:
                rfm['m_score'] = rfm['valor_total'].rank(method='dense', ascending=True)
                range_val = rfm['m_score'].max() - rfm['m_score'].min()
                if range_val > 0:
                    rfm['m_score'] = (rfm['m_score'] - rfm['m_score'].min()) / range_val * 3 + 1
                else:
                    rfm['m_score'] = 2.5

        # Tratar NaN e infinitos antes de converter
        rfm['r_score'] = rfm['r_score'].fillna(2.5).replace([np.inf, -np.inf], 2.5)
        rfm['f_score'] = rfm['f_score'].fillna(2.5).replace([np.inf, -np.inf], 2.5)
        rfm['m_score'] = rfm['m_score'].fillna(2.5).replace([np.inf, -np.inf], 2.5)

        # Converter para int
        rfm['r_score'] = rfm['r_score'].round().astype(int).clip(1, 4)
        rfm['f_score'] = rfm['f_score'].round().astype(int).clip(1, 4)
        rfm['m_score'] = rfm['m_score'].round().astype(int).clip(1, 4)

        # Score RFM combinado (3-12)
        rfm['rfm_score'] = rfm['r_score'] + rfm['f_score'] + rfm['m_score']

        return rfm

    def calculate_engagement_score(self) -> pd.DataFrame:
        """
        Calcula score de engajamento baseado em pontuacao_engajamento e atividade.

        Returns:
            DataFrame com colunas: cliente_id, engagement_score (0-100)
        """
        # Filtrar apenas dados válidos
        valid_data = self.data.dropna(subset=['cliente_id', 'nome', 'idade', 'cidade'])

        engagement = valid_data.groupby('cliente_id').agg({
            'pontuacao_engajamento': 'first',  # Pontuação de engajamento do cliente
            'compra_id': 'count'                # Número de compras
        }).reset_index()

        # Normalizar pontuação de engajamento para 0-100
        eng_min = engagement['pontuacao_engajamento'].min()
        eng_max = engagement['pontuacao_engajamento'].max()
        eng_range = eng_max - eng_min

        if eng_range > 0:
            engagement['eng_normalized'] = ((engagement['pontuacao_engajamento'] - eng_min) /
                                            eng_range * 70)  # 70% do peso
        else:
            # Se todos têm o mesmo engajamento, usar valor médio
            engagement['eng_normalized'] = 35.0  # Meio do range 0-70

        # Normalizar frequência de compras (30% do peso)
        freq_min = engagement['compra_id'].min()
        freq_max = engagement['compra_id'].max()
        freq_range = freq_max - freq_min

        if freq_range > 0:
            engagement['freq_normalized'] = ((engagement['compra_id'] - freq_min) /
                                             freq_range * 30)  # 30% do peso
        else:
            # Se todos têm a mesma frequência, usar valor médio
            engagement['freq_normalized'] = 15.0  # Meio do range 0-30

        # Score de engajamento final (0-100)
        engagement['engagement_score'] = (engagement['eng_normalized'] +
                                          engagement['freq_normalized']).round(2)

        return engagement[['cliente_id', 'engagement_score']]

    def calculate_loyalty_score(self) -> pd.DataFrame:
        """
        Calcula score de fidelidade baseado em assinatura e comportamento de compra.

        Returns:
            DataFrame com colunas: cliente_id, loyalty_score (0-100)
        """
        # Filtrar apenas dados válidos
        valid_data = self.data.dropna(subset=['cliente_id', 'nome', 'idade', 'cidade'])

        loyalty = valid_data.groupby('cliente_id').agg({
            'assinante_clube': 'first',
            'cancelou_assinatura': 'first',
            'compra_id': 'count',
            'data_compra': lambda x: (x.max() - x.min()).days if len(x) > 1 else 0
        }).reset_index()

        loyalty.columns = ['cliente_id', 'assinante_clube', 'cancelou_assinatura',
                          'num_compras', 'tempo_cliente_dias']

        # Inicializar score
        loyalty['loyalty_score'] = 0.0

        # Assinante ativo: +40 pontos
        loyalty.loc[loyalty['assinante_clube'] == 'Sim', 'loyalty_score'] += 40

        # Não cancelou assinatura: +20 pontos
        loyalty.loc[loyalty['cancelou_assinatura'] == 'Não', 'loyalty_score'] += 20

        # Tempo como cliente (normalizado, máx 20 pontos)
        if loyalty['tempo_cliente_dias'].max() > 0:
            loyalty['tempo_norm'] = (loyalty['tempo_cliente_dias'] /
                                     loyalty['tempo_cliente_dias'].max() * 20)
            loyalty['loyalty_score'] += loyalty['tempo_norm']

        # Número de compras (normalizado, máx 20 pontos)
        if loyalty['num_compras'].max() > 0:
            loyalty['compras_norm'] = (loyalty['num_compras'] /
                                       loyalty['num_compras'].max() * 20)
            loyalty['loyalty_score'] += loyalty['compras_norm']

        loyalty['loyalty_score'] = loyalty['loyalty_score'].round(2)

        return loyalty[['cliente_id', 'loyalty_score']]

    def calculate_clv(self, months_projection: int = 12) -> pd.DataFrame:
        """
        Calcula Customer Lifetime Value (CLV) projetado.

        CLV = (Valor Médio de Compra) × (Frequência de Compra) × (Tempo de Vida do Cliente)

        Args:
            months_projection: Meses para projetar o valor (padrão: 12 meses)

        Returns:
            DataFrame com colunas: cliente_id, clv, clv_score (0-100)
        """
        # Filtrar apenas dados válidos
        valid_data = self.data.dropna(subset=['cliente_id', 'nome', 'idade', 'cidade'])

        clv_data = valid_data.groupby('cliente_id').agg({
            'valor': ['mean', 'sum'],
            'compra_id': 'count',
            'data_compra': [lambda x: (x.max() - x.min()).days if len(x) > 1 else 30, 'count']
        }).reset_index()

        clv_data.columns = ['cliente_id', 'valor_medio', 'valor_total',
                           'num_compras', 'dias_ativo', 'num_transacoes']

        # Calcular frequência de compra (compras por mês)
        clv_data['frequencia_mensal'] = (clv_data['num_compras'] /
                                         (clv_data['dias_ativo'] / 30)).replace([np.inf, -np.inf], 0)
        clv_data['frequencia_mensal'] = clv_data['frequencia_mensal'].fillna(0)

        # CLV projetado
        clv_data['clv'] = (clv_data['valor_medio'] *
                          clv_data['frequencia_mensal'] *
                          months_projection).round(2)

        # Normalizar CLV para score 0-100
        if clv_data['clv'].max() > 0:
            clv_data['clv_score'] = ((clv_data['clv'] / clv_data['clv'].max()) * 100).round(2)
        else:
            clv_data['clv_score'] = 0

        return clv_data[['cliente_id', 'clv', 'clv_score']]

    def calculate_overall_score(self,
                                rfm_weight: float = 0.30,
                                engagement_weight: float = 0.25,
                                loyalty_weight: float = 0.25,
                                clv_weight: float = 0.20) -> pd.DataFrame:
        """
        Calcula o score geral do cliente combinando todos os componentes.

        Args:
            rfm_weight: Peso do RFM no score final (padrão: 30%)
            engagement_weight: Peso do engajamento (padrão: 25%)
            loyalty_weight: Peso da fidelidade (padrão: 25%)
            clv_weight: Peso do CLV (padrão: 20%)

        Returns:
            DataFrame completo com todos os scores e segmentação
        """
        # Validar pesos
        total_weight = rfm_weight + engagement_weight + loyalty_weight + clv_weight
        if not np.isclose(total_weight, 1.0):
            raise ValueError(f"Pesos devem somar 1.0. Soma atual: {total_weight}")

        # Calcular scores individuais
        rfm_scores = self.calculate_rfm_scores()
        engagement_scores = self.calculate_engagement_score()
        loyalty_scores = self.calculate_loyalty_score()
        clv_scores = self.calculate_clv()

        # Merge todos os scores
        scores = rfm_scores.merge(engagement_scores, on='cliente_id', how='left')
        scores = scores.merge(loyalty_scores, on='cliente_id', how='left')
        scores = scores.merge(clv_scores, on='cliente_id', how='left')

        # Normalizar RFM para 0-100
        scores['rfm_score_normalized'] = ((scores['rfm_score'] - 3) / (12 - 3) * 100).round(2)

        # Calcular score geral ponderado
        scores['overall_score'] = (
            scores['rfm_score_normalized'] * rfm_weight +
            scores['engagement_score'] * engagement_weight +
            scores['loyalty_score'] * loyalty_weight +
            scores['clv_score'] * clv_weight
        ).round(2)

        # Adicionar informações do cliente (filtrar dados válidos)
        valid_data = self.data.dropna(subset=['cliente_id', 'nome', 'idade', 'cidade'])
        cliente_info = valid_data.groupby('cliente_id').agg({
            'nome': 'first',
            'idade': 'first',
            'cidade': 'first',
            'assinante_clube': 'first',
            'cancelou_assinatura': 'first',
            'pontuacao_engajamento': 'first'
        }).reset_index()

        # Usar 'inner' join para garantir que só mantemos clientes com dados completos
        scores = scores.merge(cliente_info, on='cliente_id', how='inner')

        # Criar segmentação baseada no score geral
        scores['segment'] = pd.cut(scores['overall_score'],
                                   bins=[0, 40, 60, 75, 90, 100],
                                   labels=['Em Risco', 'Potencial', 'Regular', 'Valioso', 'VIP'],
                                   include_lowest=True)

        # Criar tier (nível) do cliente
        scores['tier'] = pd.cut(scores['overall_score'],
                               bins=[0, 50, 75, 100],
                               labels=['Bronze', 'Silver', 'Gold'],
                               include_lowest=True)

        self.scores = scores
        return scores

    def get_segment_summary(self) -> pd.DataFrame:
        """
        Retorna resumo estatístico por segmento.

        Returns:
            DataFrame com estatísticas por segmento
        """
        if self.scores is None:
            raise ValueError("Execute calculate_overall_score() primeiro")

        summary = self.scores.groupby('segment').agg({
            'cliente_id': 'count',
            'overall_score': ['mean', 'min', 'max'],
            'valor_total': ['sum', 'mean'],
            'frequencia': 'mean',
            'clv': ['sum', 'mean']
        }).round(2)

        summary.columns = ['_'.join(col).strip() for col in summary.columns.values]
        summary = summary.reset_index()

        # Renomear colunas para melhor legibilidade
        summary.columns = ['Segmento', 'Num_Clientes', 'Score_Medio', 'Score_Min',
                          'Score_Max', 'Valor_Total', 'Valor_Medio', 'Frequencia_Media',
                          'CLV_Total', 'CLV_Medio']

        return summary

    def get_top_customers(self, n: int = 10, metric: str = 'overall_score') -> pd.DataFrame:
        """
        Retorna os top N clientes baseado em uma métrica.

        Args:
            n: Número de clientes a retornar
            metric: Métrica para ordenação (overall_score, clv, valor_total, etc.)

        Returns:
            DataFrame com top N clientes
        """
        if self.scores is None:
            raise ValueError("Execute calculate_overall_score() primeiro")

        if metric not in self.scores.columns:
            raise ValueError(f"Métrica '{metric}' não encontrada. "
                           f"Disponíveis: {list(self.scores.columns)}")

        top_customers = self.scores.nlargest(n, metric)[[
            'cliente_id', 'nome', 'overall_score', 'segment', 'tier',
            'valor_total', 'frequencia', 'clv', 'loyalty_score',
            'engagement_score', 'cidade', 'assinante_clube'
        ]]

        return top_customers

    def get_at_risk_customers(self, threshold: float = 40) -> pd.DataFrame:
        """
        Identifica clientes em risco (score baixo).

        Args:
            threshold: Score abaixo do qual o cliente é considerado em risco

        Returns:
            DataFrame com clientes em risco
        """
        if self.scores is None:
            raise ValueError("Execute calculate_overall_score() primeiro")

        at_risk = self.scores[self.scores['overall_score'] < threshold].copy()
        at_risk = at_risk.sort_values('overall_score')[[
            'cliente_id', 'nome', 'overall_score', 'segment',
            'valor_total', 'recencia', 'cancelou_assinatura',
            'loyalty_score', 'engagement_score', 'cidade'
        ]]

        return at_risk

    def export_scores(self, filepath: str):
        """
        Exporta scores para arquivo CSV.

        Args:
            filepath: Caminho do arquivo para salvar
        """
        if self.scores is None:
            raise ValueError("Execute calculate_overall_score() primeiro")

        self.scores.to_csv(filepath, index=False, encoding='utf-8-sig', sep=';')
        print(f"✓ Scores exportados para: {filepath}")


def get_scoring_insights(scores: pd.DataFrame) -> Dict[str, any]:
    """
    Gera insights acionáveis baseados nos scores dos clientes.

    Args:
        scores: DataFrame com scores calculados

    Returns:
        Dicionário com insights e recomendações
    """
    insights = {}

    # Distribuição de segmentos
    insights['segment_distribution'] = scores['segment'].value_counts().to_dict()

    # Média de score por cidade
    insights['avg_score_by_city'] = scores.groupby('cidade')['overall_score'].mean().to_dict()

    # Taxa de churn por segmento
    churn_by_segment = (scores[scores['cancelou_assinatura'] == 'Sim']
                       .groupby('segment').size() / scores.groupby('segment').size() * 100)
    insights['churn_rate_by_segment'] = churn_by_segment.to_dict()

    # CLV médio por tier
    insights['avg_clv_by_tier'] = scores.groupby('tier')['clv'].mean().to_dict()

    # Clientes VIP sem assinatura (oportunidade)
    vip_no_subscription = scores[(scores['segment'] == 'VIP') &
                                 (scores['assinante_clube'] == 'Não')]
    insights['vip_no_subscription_count'] = len(vip_no_subscription)
    insights['vip_no_subscription_potential'] = vip_no_subscription['clv'].sum()

    # Clientes em risco com alto CLV (atenção urgente)
    at_risk_high_value = scores[(scores['segment'] == 'Em Risco') &
                                (scores['clv'] > scores['clv'].median())]
    insights['at_risk_high_value_count'] = len(at_risk_high_value)
    insights['at_risk_high_value_total'] = at_risk_high_value['clv'].sum()

    return insights


if __name__ == "__main__":
    """
    Exemplo de uso do sistema de scoring.
    """
    print("Sistema de Scoring de Clientes - Adega IA")
    print("=" * 60)

    # Este é apenas um exemplo. Na prática, os dados virão do DataLoader
    print("\nPara usar este módulo, importe-o no seu código principal:")
    print("\nfrom src.models.customer_scoring import CustomerScoring")
    print("\nscoring = CustomerScoring(data)")
    print("scores = scoring.calculate_overall_score()")
    print("summary = scoring.get_segment_summary()")
    print("top_customers = scoring.get_top_customers(n=10)")

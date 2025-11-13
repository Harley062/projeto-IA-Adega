"""
Módulo para Feature Engineering e Transformação de Dados
"""
import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder, StandardScaler, MinMaxScaler
from sklearn.feature_selection import SelectKBest, f_classif, mutual_info_classif
from typing import Tuple, List, Optional
import logging

logger = logging.getLogger(__name__)


class FeatureEngineer:
    """Classe para engenharia de features e transformação de dados"""

    def __init__(self):
        self.label_encoders = {}
        self.scaler = None
        self.selected_features = None

    def create_temporal_features(self, data: pd.DataFrame, date_column: str = 'data_compra') -> pd.DataFrame:
        """
        Cria features temporais a partir da data de compra

        Args:
            data: DataFrame com os dados
            date_column: Nome da coluna de data

        Returns:
            DataFrame com features temporais adicionadas
        """
        logger.info("Criando features temporais...")

        df = data.copy()

        if date_column not in df.columns:
            logger.warning(f"Coluna {date_column} não encontrada")
            return df

        # Garantir que é datetime
        df[date_column] = pd.to_datetime(df[date_column])

        # Extrair componentes temporais
        df['ano'] = df[date_column].dt.year
        df['mes'] = df[date_column].dt.month
        df['dia'] = df[date_column].dt.day
        df['dia_semana'] = df[date_column].dt.dayofweek
        df['trimestre'] = df[date_column].dt.quarter
        df['semana_ano'] = df[date_column].dt.isocalendar().week

        # Features cíclicas (para capturar a natureza circular do tempo)
        df['mes_sin'] = np.sin(2 * np.pi * df['mes'] / 12)
        df['mes_cos'] = np.cos(2 * np.pi * df['mes'] / 12)
        df['dia_semana_sin'] = np.sin(2 * np.pi * df['dia_semana'] / 7)
        df['dia_semana_cos'] = np.cos(2 * np.pi * df['dia_semana'] / 7)

        logger.info(f"Criadas features temporais: ano, mes, dia, dia_semana, trimestre, etc.")

        return df

    def create_aggregated_features(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Cria features agregadas baseadas em cliente e produto

        Args:
            data: DataFrame com os dados

        Returns:
            DataFrame com features agregadas
        """
        logger.info("Criando features agregadas...")

        df = data.copy()

        # Features agregadas por cliente
        if 'cliente_id' in df.columns:
            cliente_stats = df.groupby('cliente_id').agg({
                'valor': ['sum', 'mean', 'std', 'count'],
                'quantidade': ['sum', 'mean'],
            }).reset_index()

            cliente_stats.columns = ['cliente_id', 'total_gasto', 'ticket_medio', 'std_gasto',
                                      'num_compras', 'total_itens', 'media_itens']

            df = df.merge(cliente_stats, on='cliente_id', how='left', suffixes=('', '_agg'))

        # Features agregadas por produto
        if 'produto_id' in df.columns:
            produto_stats = df.groupby('produto_id').agg({
                'valor': ['mean', 'count'],
                'quantidade': 'sum'
            }).reset_index()

            produto_stats.columns = ['produto_id', 'preco_medio_produto', 'popularidade_produto',
                                      'total_vendido_produto']

            df = df.merge(produto_stats, on='produto_id', how='left', suffixes=('', '_prod'))

        # RFM (Recency, Frequency, Monetary) - se houver data
        if 'data_compra' in df.columns and 'cliente_id' in df.columns:
            df['data_compra'] = pd.to_datetime(df['data_compra'])
            data_ref = df['data_compra'].max()

            rfm = df.groupby('cliente_id').agg({
                'data_compra': lambda x: (data_ref - x.max()).days,  # Recency
                'compra_id': 'count',  # Frequency
                'valor': 'sum'  # Monetary
            }).reset_index()

            rfm.columns = ['cliente_id', 'recencia', 'frequencia', 'valor_total']

            df = df.merge(rfm, on='cliente_id', how='left', suffixes=('', '_rfm'))

        logger.info(f"Features agregadas criadas com sucesso")

        return df

    def create_interaction_features(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Cria features de interação entre variáveis

        Args:
            data: DataFrame com os dados

        Returns:
            DataFrame com features de interação
        """
        logger.info("Criando features de interação...")

        df = data.copy()

        # Valor por unidade
        if 'valor' in df.columns and 'quantidade' in df.columns:
            df['valor_por_unidade'] = df['valor'] / (df['quantidade'] + 1)  # +1 para evitar divisão por zero

        # Engajamento x Idade
        if 'pontuacao_engajamento' in df.columns and 'idade' in df.columns:
            df['engajamento_por_idade'] = df['pontuacao_engajamento'] / (df['idade'] + 1)
            df['engajamento_x_idade'] = df['pontuacao_engajamento'] * df['idade']

        # Ticket médio por idade
        if 'valor' in df.columns and 'idade' in df.columns:
            df['valor_por_idade'] = df['valor'] / (df['idade'] + 1)

        logger.info("Features de interação criadas")

        return df

    def encode_categorical_features(self, data: pd.DataFrame, columns: Optional[List[str]] = None) -> pd.DataFrame:
        """
        Codifica features categóricas usando Label Encoding

        Args:
            data: DataFrame com os dados
            columns: Lista de colunas para codificar (None = detectar automaticamente)

        Returns:
            DataFrame com features codificadas
        """
        logger.info("Codificando features categóricas...")

        df = data.copy()

        if columns is None:
            # Detectar colunas categóricas automaticamente
            columns = df.select_dtypes(include=['object']).columns.tolist()

        for col in columns:
            if col in df.columns:
                if col not in self.label_encoders:
                    self.label_encoders[col] = LabelEncoder()
                    df[col] = self.label_encoders[col].fit_transform(df[col].astype(str))
                else:
                    df[col] = self.label_encoders[col].transform(df[col].astype(str))

                logger.info(f"Coluna '{col}' codificada com {len(self.label_encoders[col].classes_)} classes")

        return df

    def scale_features(self, data: pd.DataFrame, method: str = 'standard') -> pd.DataFrame:
        """
        Normaliza/Padroniza features numéricas

        Args:
            data: DataFrame com os dados
            method: 'standard' para StandardScaler ou 'minmax' para MinMaxScaler

        Returns:
            DataFrame com features normalizadas
        """
        logger.info(f"Normalizando features usando método: {method}")

        df = data.copy()
        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()

        if len(numeric_cols) == 0:
            logger.warning("Nenhuma coluna numérica encontrada para normalização")
            return df

        if method == 'standard':
            if self.scaler is None:
                self.scaler = StandardScaler()
                df[numeric_cols] = self.scaler.fit_transform(df[numeric_cols])
            else:
                df[numeric_cols] = self.scaler.transform(df[numeric_cols])
        elif method == 'minmax':
            if self.scaler is None:
                self.scaler = MinMaxScaler()
                df[numeric_cols] = self.scaler.fit_transform(df[numeric_cols])
            else:
                df[numeric_cols] = self.scaler.transform(df[numeric_cols])

        logger.info(f"{len(numeric_cols)} features normalizadas")

        return df

    def select_features(self, X: pd.DataFrame, y: pd.Series, k: int = 10, method: str = 'f_classif') -> pd.DataFrame:
        """
        Seleciona as K melhores features

        Args:
            X: Features
            y: Target
            k: Número de features a selecionar
            method: 'f_classif' ou 'mutual_info'

        Returns:
            DataFrame com features selecionadas
        """
        logger.info(f"Selecionando top {k} features usando {method}...")

        if method == 'f_classif':
            selector = SelectKBest(f_classif, k=min(k, X.shape[1]))
        else:
            selector = SelectKBest(mutual_info_classif, k=min(k, X.shape[1]))

        X_selected = selector.fit_transform(X, y)
        selected_indices = selector.get_support(indices=True)
        self.selected_features = X.columns[selected_indices].tolist()

        logger.info(f"Features selecionadas: {self.selected_features}")

        return pd.DataFrame(X_selected, columns=self.selected_features, index=X.index)

    def engineer_all_features(self, data: pd.DataFrame, include_temporal: bool = True,
                               include_aggregated: bool = True, include_interactions: bool = True) -> pd.DataFrame:
        """
        Executa todo o pipeline de feature engineering

        Args:
            data: DataFrame com os dados
            include_temporal: Se deve incluir features temporais
            include_aggregated: Se deve incluir features agregadas
            include_interactions: Se deve incluir features de interação

        Returns:
            DataFrame com todas as features engineered
        """
        logger.info("Iniciando pipeline completo de feature engineering...")

        df = data.copy()

        if include_temporal:
            df = self.create_temporal_features(df)

        if include_aggregated:
            df = self.create_aggregated_features(df)

        if include_interactions:
            df = self.create_interaction_features(df)

        logger.info(f"Feature engineering concluído. Total de features: {len(df.columns)}")

        return df

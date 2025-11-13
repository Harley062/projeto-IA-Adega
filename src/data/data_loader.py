"""
Módulo para carregamento e validação de dados
"""
import pandas as pd
import numpy as np
from typing import Tuple, Optional
import logging
from pathlib import Path

logger = logging.getLogger(__name__)


class DataLoader:
    """Classe responsável por carregar e validar dados da adega"""

    def __init__(self, data_dir: str = "."):
        self.data_dir = Path(data_dir)
        self.clientes = None
        self.produtos = None
        self.compras = None
        self.data_merged = None

    def load_data(self) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
        """
        Carrega os dados de clientes, produtos e compras

        Returns:
            Tuple com os três DataFrames
        """
        try:
            logger.info("Carregando dados...")

            # Carregar CSVs com o delimitador correto
            self.clientes = pd.read_csv(
                self.data_dir / 'data' / 'Cliente.csv',
                delimiter=';',
                encoding='utf-8'
            )
            self.produtos = pd.read_csv(
                self.data_dir / 'data' / 'produtos.csv',
                delimiter=';',
                encoding='utf-8'
            )
            self.compras = pd.read_csv(
                self.data_dir / 'data' / 'Compras.csv',
                delimiter=';',
                encoding='utf-8'
            )

            logger.info(f"Clientes carregados: {len(self.clientes)} registros")
            logger.info(f"Produtos carregados: {len(self.produtos)} registros")
            logger.info(f"Compras carregadas: {len(self.compras)} registros")

            return self.clientes, self.produtos, self.compras

        except Exception as e:
            logger.error(f"Erro ao carregar dados: {e}")
            raise

    def validate_data(self) -> bool:
        """
        Valida a integridade dos dados

        Returns:
            True se os dados são válidos
        """
        logger.info("Validando integridade dos dados...")

        # Verificar valores nulos críticos
        assert not self.clientes['cliente_id'].isnull().any(), "IDs de clientes nulos encontrados"
        assert not self.produtos['produto_id'].isnull().any(), "IDs de produtos nulos encontrados"
        assert not self.compras['compra_id'].isnull().any(), "IDs de compras nulos encontrados"

        # Verificar duplicatas
        assert not self.clientes['cliente_id'].duplicated().any(), "IDs de clientes duplicados"
        assert not self.produtos['produto_id'].duplicated().any(), "IDs de produtos duplicados"
        assert not self.compras['compra_id'].duplicated().any(), "IDs de compras duplicados"

        # Verificar integridade referencial
        clientes_invalidos = ~self.compras['cliente_id'].isin(self.clientes['cliente_id'])
        if clientes_invalidos.any():
            logger.warning(f"Encontradas {clientes_invalidos.sum()} compras com cliente_id inválido")

        produtos_invalidos = ~self.compras['produto_id'].isin(self.produtos['produto_id'])
        if produtos_invalidos.any():
            logger.warning(f"Encontradas {produtos_invalidos.sum()} compras com produto_id inválido")

        logger.info("Validação concluída com sucesso!")
        return True

    def merge_data(self) -> pd.DataFrame:
        """
        Realiza o merge dos três datasets

        Returns:
            DataFrame com os dados combinados
        """
        logger.info("Realizando merge dos dados...")

        # Primeiro merge: compras + clientes
        data_merged = pd.merge(
            self.compras,
            self.clientes,
            on='cliente_id',
            how='left',
            suffixes=('', '_cliente')
        )

        # Segundo merge: resultado + produtos
        self.data_merged = pd.merge(
            data_merged,
            self.produtos,
            on='produto_id',
            how='left',
            suffixes=('', '_produto')
        )

        logger.info(f"Dados combinados: {len(self.data_merged)} registros")
        logger.info(f"Features disponíveis: {len(self.data_merged.columns)} colunas")

        return self.data_merged

    def get_data_summary(self) -> dict:
        """
        Retorna um resumo estatístico dos dados

        Returns:
            Dicionário com estatísticas dos dados
        """
        if self.data_merged is None:
            raise ValueError("Execute merge_data() primeiro")

        summary = {
            'total_registros': len(self.data_merged),
            'total_features': len(self.data_merged.columns),
            'valores_nulos': self.data_merged.isnull().sum().to_dict(),
            'tipos_dados': self.data_merged.dtypes.to_dict(),
            'clientes_unicos': self.data_merged['cliente_id'].nunique(),
            'produtos_unicos': self.data_merged['produto_id'].nunique(),
            'total_vendas': self.data_merged['valor'].sum(),
            'ticket_medio': self.data_merged['valor'].mean(),
        }

        return summary

    def clean_data(self, drop_na: bool = True) -> pd.DataFrame:
        """
        Limpa os dados removendo valores nulos e outliers

        Args:
            drop_na: Se deve remover linhas com valores nulos

        Returns:
            DataFrame limpo
        """
        logger.info("Limpando dados...")

        if self.data_merged is None:
            raise ValueError("Execute merge_data() primeiro")

        data_clean = self.data_merged.copy()

        # Remover valores nulos se solicitado
        if drop_na:
            antes = len(data_clean)
            data_clean = data_clean.dropna()
            depois = len(data_clean)
            logger.info(f"Removidos {antes - depois} registros com valores nulos")

        # Converter data_compra para datetime
        if 'data_compra' in data_clean.columns:
            data_clean['data_compra'] = pd.to_datetime(data_clean['data_compra'])

        # Garantir tipos numéricos corretos
        numeric_cols = ['valor', 'quantidade', 'idade', 'pontuacao_engajamento']
        for col in numeric_cols:
            if col in data_clean.columns:
                data_clean[col] = pd.to_numeric(data_clean[col], errors='coerce')

        self.data_merged = data_clean

        logger.info(f"Dados limpos: {len(data_clean)} registros mantidos")
        return data_clean

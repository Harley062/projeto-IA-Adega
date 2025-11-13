"""
Módulo para Análise Exploratória de Dados (EDA)
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from typing import Optional, List
import logging
from pathlib import Path

logger = logging.getLogger(__name__)


class ExploratoryAnalysis:
    """Classe para realizar análise exploratória de dados"""

    def __init__(self, data: pd.DataFrame, output_dir: str = "output/plots"):
        self.data = data
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

        # Configurar estilo dos gráficos
        sns.set_style("whitegrid")
        plt.rcParams['figure.figsize'] = (12, 6)

    def generate_summary_statistics(self) -> pd.DataFrame:
        """
        Gera estatísticas descritivas dos dados

        Returns:
            DataFrame com estatísticas descritivas
        """
        logger.info("Gerando estatísticas descritivas...")

        # Estatísticas numéricas
        numeric_stats = self.data.describe()

        # Estatísticas categóricas
        categorical_cols = self.data.select_dtypes(include=['object']).columns
        categorical_stats = pd.DataFrame({
            col: {
                'count': self.data[col].count(),
                'unique': self.data[col].nunique(),
                'top': self.data[col].mode()[0] if len(self.data[col].mode()) > 0 else None,
                'freq': self.data[col].value_counts().iloc[0] if len(self.data[col]) > 0 else 0
            }
            for col in categorical_cols
        }).T

        return numeric_stats, categorical_stats

    def plot_missing_values(self, save: bool = True) -> None:
        """
        Visualiza valores ausentes no dataset

        Args:
            save: Se deve salvar o gráfico
        """
        logger.info("Gerando visualização de valores ausentes...")

        missing = self.data.isnull().sum()
        missing = missing[missing > 0].sort_values(ascending=False)

        if len(missing) == 0:
            logger.info("Nenhum valor ausente encontrado!")
            return

        plt.figure(figsize=(10, 6))
        missing.plot(kind='barh')
        plt.xlabel('Quantidade de Valores Ausentes')
        plt.title('Valores Ausentes por Coluna')
        plt.tight_layout()

        if save:
            plt.savefig(self.output_dir / 'missing_values.png', dpi=300, bbox_inches='tight')
            logger.info(f"Gráfico salvo em: {self.output_dir / 'missing_values.png'}")

        plt.close()

    def plot_numerical_distributions(self, columns: Optional[List[str]] = None, save: bool = True) -> None:
        """
        Plota distribuições de variáveis numéricas

        Args:
            columns: Lista de colunas para plotar (None = todas numéricas)
            save: Se deve salvar os gráficos
        """
        logger.info("Gerando distribuições de variáveis numéricas...")

        if columns is None:
            columns = self.data.select_dtypes(include=[np.number]).columns.tolist()

        n_cols = min(3, len(columns))
        n_rows = (len(columns) + n_cols - 1) // n_cols

        fig, axes = plt.subplots(n_rows, n_cols, figsize=(15, 5 * n_rows))
        axes = axes.flatten() if n_rows * n_cols > 1 else [axes]

        for idx, col in enumerate(columns):
            if idx < len(axes):
                self.data[col].hist(bins=30, ax=axes[idx], edgecolor='black')
                axes[idx].set_title(f'Distribuição de {col}')
                axes[idx].set_xlabel(col)
                axes[idx].set_ylabel('Frequência')

        # Remover eixos extras
        for idx in range(len(columns), len(axes)):
            fig.delaxes(axes[idx])

        plt.tight_layout()

        if save:
            plt.savefig(self.output_dir / 'numerical_distributions.png', dpi=300, bbox_inches='tight')
            logger.info(f"Gráfico salvo em: {self.output_dir / 'numerical_distributions.png'}")

        plt.close()

    def plot_categorical_distributions(self, columns: Optional[List[str]] = None, save: bool = True) -> None:
        """
        Plota distribuições de variáveis categóricas

        Args:
            columns: Lista de colunas para plotar (None = todas categóricas)
            save: Se deve salvar os gráficos
        """
        logger.info("Gerando distribuições de variáveis categóricas...")

        if columns is None:
            columns = self.data.select_dtypes(include=['object']).columns.tolist()

        n_cols = min(2, len(columns))
        n_rows = (len(columns) + n_cols - 1) // n_cols

        fig, axes = plt.subplots(n_rows, n_cols, figsize=(15, 5 * n_rows))
        axes = axes.flatten() if n_rows * n_cols > 1 else [axes]

        for idx, col in enumerate(columns):
            if idx < len(axes):
                value_counts = self.data[col].value_counts().head(10)
                value_counts.plot(kind='barh', ax=axes[idx])
                axes[idx].set_title(f'Top 10 - {col}')
                axes[idx].set_xlabel('Frequência')

        # Remover eixos extras
        for idx in range(len(columns), len(axes)):
            fig.delaxes(axes[idx])

        plt.tight_layout()

        if save:
            plt.savefig(self.output_dir / 'categorical_distributions.png', dpi=300, bbox_inches='tight')
            logger.info(f"Gráfico salvo em: {self.output_dir / 'categorical_distributions.png'}")

        plt.close()

    def plot_correlation_matrix(self, save: bool = True) -> None:
        """
        Plota matriz de correlação das variáveis numéricas

        Args:
            save: Se deve salvar o gráfico
        """
        logger.info("Gerando matriz de correlação...")

        numeric_data = self.data.select_dtypes(include=[np.number])

        if numeric_data.shape[1] < 2:
            logger.warning("Não há colunas numéricas suficientes para correlação")
            return

        plt.figure(figsize=(12, 10))
        correlation = numeric_data.corr()

        sns.heatmap(
            correlation,
            annot=True,
            fmt='.2f',
            cmap='coolwarm',
            center=0,
            square=True,
            linewidths=1,
            cbar_kws={"shrink": 0.8}
        )

        plt.title('Matriz de Correlação', fontsize=14, fontweight='bold')
        plt.tight_layout()

        if save:
            plt.savefig(self.output_dir / 'correlation_matrix.png', dpi=300, bbox_inches='tight')
            logger.info(f"Gráfico salvo em: {self.output_dir / 'correlation_matrix.png'}")

        plt.close()

    def plot_boxplots(self, columns: Optional[List[str]] = None, save: bool = True) -> None:
        """
        Plota boxplots para identificar outliers

        Args:
            columns: Lista de colunas para plotar (None = todas numéricas)
            save: Se deve salvar os gráficos
        """
        logger.info("Gerando boxplots para detecção de outliers...")

        if columns is None:
            columns = self.data.select_dtypes(include=[np.number]).columns.tolist()

        n_cols = min(3, len(columns))
        n_rows = (len(columns) + n_cols - 1) // n_cols

        fig, axes = plt.subplots(n_rows, n_cols, figsize=(15, 5 * n_rows))
        axes = axes.flatten() if n_rows * n_cols > 1 else [axes]

        for idx, col in enumerate(columns):
            if idx < len(axes):
                self.data.boxplot(column=col, ax=axes[idx])
                axes[idx].set_title(f'Boxplot - {col}')

        # Remover eixos extras
        for idx in range(len(columns), len(axes)):
            fig.delaxes(axes[idx])

        plt.tight_layout()

        if save:
            plt.savefig(self.output_dir / 'boxplots.png', dpi=300, bbox_inches='tight')
            logger.info(f"Gráfico salvo em: {self.output_dir / 'boxplots.png'}")

        plt.close()

    def generate_full_report(self) -> None:
        """Gera relatório completo de EDA com todos os gráficos"""
        logger.info("Gerando relatório completo de EDA...")

        self.plot_missing_values()
        self.plot_numerical_distributions()
        self.plot_categorical_distributions()
        self.plot_correlation_matrix()
        self.plot_boxplots()

        logger.info("Relatório de EDA concluído!")

"""
Módulo para Visualizações Avançadas de Dados
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from typing import Optional, List
import logging
from pathlib import Path

logger = logging.getLogger(__name__)


class AdvancedPlotter:
    """Classe para visualizações avançadas de dados de negócio"""

    def __init__(self, data: pd.DataFrame, output_dir: str = "output/plots"):
        self.data = data
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

        # Configurar estilo
        sns.set_style("whitegrid")
        plt.rcParams['figure.figsize'] = (12, 6)

    def plot_sales_over_time(self, save: bool = True) -> None:
        """
        Plota vendas ao longo do tempo

        Args:
            save: Se deve salvar o gráfico
        """
        logger.info("Gerando gráfico de vendas ao longo do tempo...")

        if 'data_compra' not in self.data.columns:
            logger.warning("Coluna 'data_compra' não encontrada")
            return

        df_temp = self.data.copy()
        df_temp['data_compra'] = pd.to_datetime(df_temp['data_compra'])

        # Agrupar por data
        sales_by_date = df_temp.groupby(df_temp['data_compra'].dt.date)['valor'].sum().reset_index()

        plt.figure(figsize=(14, 6))
        plt.plot(sales_by_date['data_compra'], sales_by_date['valor'], marker='o', linewidth=2)
        plt.xlabel('Data', fontsize=12)
        plt.ylabel('Valor Total de Vendas (R$)', fontsize=12)
        plt.title('Vendas ao Longo do Tempo', fontsize=14, fontweight='bold')
        plt.xticks(rotation=45)
        plt.grid(alpha=0.3)
        plt.tight_layout()

        if save:
            plt.savefig(self.output_dir / 'sales_over_time.png', dpi=300, bbox_inches='tight')
            logger.info(f"Gráfico salvo em: {self.output_dir / 'sales_over_time.png'}")

        plt.close()

    def plot_top_products(self, top_n: int = 10, save: bool = True) -> None:
        """
        Plota os produtos mais vendidos

        Args:
            top_n: Número de produtos a mostrar
            save: Se deve salvar o gráfico
        """
        logger.info(f"Gerando gráfico dos top {top_n} produtos...")

        if 'nome_produto' not in self.data.columns or 'valor' not in self.data.columns:
            # Tentar com 'nome' se 'nome_produto' não existir
            nome_col = 'nome' if 'nome' in self.data.columns else None
            if nome_col is None:
                logger.warning("Colunas de produto não encontradas")
                return
        else:
            nome_col = 'nome_produto'

        # Agrupar por produto
        product_sales = self.data.groupby(nome_col)['valor'].agg(['sum', 'count']).reset_index()
        product_sales.columns = [nome_col, 'total_vendas', 'quantidade_vendida']
        product_sales = product_sales.sort_values('total_vendas', ascending=False).head(top_n)

        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(18, 6))

        # Gráfico de valor total
        ax1.barh(product_sales[nome_col], product_sales['total_vendas'], color='steelblue')
        ax1.set_xlabel('Valor Total de Vendas (R$)', fontsize=12)
        ax1.set_title(f'Top {top_n} Produtos por Valor', fontsize=14, fontweight='bold')
        ax1.invert_yaxis()

        # Gráfico de quantidade
        ax2.barh(product_sales[nome_col], product_sales['quantidade_vendida'], color='coral')
        ax2.set_xlabel('Quantidade Vendida', fontsize=12)
        ax2.set_title(f'Top {top_n} Produtos por Quantidade', fontsize=14, fontweight='bold')
        ax2.invert_yaxis()

        plt.tight_layout()

        if save:
            plt.savefig(self.output_dir / 'top_products.png', dpi=300, bbox_inches='tight')
            logger.info(f"Gráfico salvo em: {self.output_dir / 'top_products.png'}")

        plt.close()

    def plot_customer_segmentation(self, save: bool = True) -> None:
        """
        Plota segmentação de clientes

        Args:
            save: Se deve salvar o gráfico
        """
        logger.info("Gerando gráfico de segmentação de clientes...")

        if 'cidade' not in self.data.columns:
            logger.warning("Coluna 'cidade' não encontrada")
            return

        # Análise por cidade
        city_stats = self.data.groupby('cidade').agg({
            'valor': ['sum', 'mean', 'count']
        }).reset_index()

        city_stats.columns = ['cidade', 'total_vendas', 'ticket_medio', 'num_compras']
        city_stats = city_stats.sort_values('total_vendas', ascending=False).head(10)

        fig, axes = plt.subplots(2, 2, figsize=(16, 12))

        # Vendas por cidade
        axes[0, 0].barh(city_stats['cidade'], city_stats['total_vendas'], color='teal')
        axes[0, 0].set_xlabel('Total de Vendas (R$)', fontsize=11)
        axes[0, 0].set_title('Vendas por Cidade', fontsize=12, fontweight='bold')
        axes[0, 0].invert_yaxis()

        # Ticket médio por cidade
        axes[0, 1].barh(city_stats['cidade'], city_stats['ticket_medio'], color='orange')
        axes[0, 1].set_xlabel('Ticket Médio (R$)', fontsize=11)
        axes[0, 1].set_title('Ticket Médio por Cidade', fontsize=12, fontweight='bold')
        axes[0, 1].invert_yaxis()

        # Número de compras por cidade
        axes[1, 0].barh(city_stats['cidade'], city_stats['num_compras'], color='purple')
        axes[1, 0].set_xlabel('Número de Compras', fontsize=11)
        axes[1, 0].set_title('Número de Compras por Cidade', fontsize=12, fontweight='bold')
        axes[1, 0].invert_yaxis()

        # Distribuição de idade (se disponível)
        if 'idade' in self.data.columns:
            axes[1, 1].hist(self.data['idade'], bins=20, edgecolor='black', color='skyblue')
            axes[1, 1].set_xlabel('Idade', fontsize=11)
            axes[1, 1].set_ylabel('Frequência', fontsize=11)
            axes[1, 1].set_title('Distribuição de Idade dos Clientes', fontsize=12, fontweight='bold')
        else:
            fig.delaxes(axes[1, 1])

        plt.tight_layout()

        if save:
            plt.savefig(self.output_dir / 'customer_segmentation.png', dpi=300, bbox_inches='tight')
            logger.info(f"Gráfico salvo em: {self.output_dir / 'customer_segmentation.png'}")

        plt.close()

    def plot_wine_analysis(self, save: bool = True) -> None:
        """
        Análise específica de vinhos (país, safra, tipo de uva)

        Args:
            save: Se deve salvar o gráfico
        """
        logger.info("Gerando análise de vinhos...")

        fig, axes = plt.subplots(2, 2, figsize=(16, 12))

        # Vendas por país
        if 'pais' in self.data.columns:
            pais_sales = self.data.groupby('pais')['valor'].sum().sort_values(ascending=False).head(10)
            axes[0, 0].barh(pais_sales.index, pais_sales.values, color='maroon')
            axes[0, 0].set_xlabel('Total de Vendas (R$)', fontsize=11)
            axes[0, 0].set_title('Vendas por País de Origem', fontsize=12, fontweight='bold')
            axes[0, 0].invert_yaxis()
        else:
            fig.delaxes(axes[0, 0])

        # Vendas por tipo de uva
        if 'tipo_uva' in self.data.columns:
            uva_sales = self.data.groupby('tipo_uva')['valor'].sum().sort_values(ascending=False)
            axes[0, 1].barh(uva_sales.index, uva_sales.values, color='darkgreen')
            axes[0, 1].set_xlabel('Total de Vendas (R$)', fontsize=11)
            axes[0, 1].set_title('Vendas por Tipo de Uva', fontsize=12, fontweight='bold')
            axes[0, 1].invert_yaxis()
        else:
            fig.delaxes(axes[0, 1])

        # Distribuição de safras
        if 'safra' in self.data.columns:
            safra_count = self.data['safra'].value_counts().sort_index()
            axes[1, 0].bar(safra_count.index.astype(str), safra_count.values, color='goldenrod', edgecolor='black')
            axes[1, 0].set_xlabel('Safra', fontsize=11)
            axes[1, 0].set_ylabel('Quantidade', fontsize=11)
            axes[1, 0].set_title('Distribuição de Safras', fontsize=12, fontweight='bold')
            axes[1, 0].tick_params(axis='x', rotation=45)
        else:
            fig.delaxes(axes[1, 0])

        # Distribuição de valores
        if 'valor' in self.data.columns:
            axes[1, 1].hist(self.data['valor'], bins=30, edgecolor='black', color='lightcoral')
            axes[1, 1].set_xlabel('Valor da Compra (R$)', fontsize=11)
            axes[1, 1].set_ylabel('Frequência', fontsize=11)
            axes[1, 1].set_title('Distribuição de Valores de Compra', fontsize=12, fontweight='bold')
        else:
            fig.delaxes(axes[1, 1])

        plt.tight_layout()

        if save:
            plt.savefig(self.output_dir / 'wine_analysis.png', dpi=300, bbox_inches='tight')
            logger.info(f"Gráfico salvo em: {self.output_dir / 'wine_analysis.png'}")

        plt.close()

    def plot_rfm_analysis(self, save: bool = True) -> None:
        """
        Análise RFM (Recency, Frequency, Monetary)

        Args:
            save: Se deve salvar o gráfico
        """
        logger.info("Gerando análise RFM...")

        if 'cliente_id' not in self.data.columns or 'data_compra' not in self.data.columns:
            logger.warning("Colunas necessárias para RFM não encontradas")
            return

        df_temp = self.data.copy()
        df_temp['data_compra'] = pd.to_datetime(df_temp['data_compra'])
        data_ref = df_temp['data_compra'].max()

        # Calcular RFM
        rfm = df_temp.groupby('cliente_id').agg({
            'data_compra': lambda x: (data_ref - x.max()).days,
            'compra_id': 'count',
            'valor': 'sum'
        }).reset_index()

        rfm.columns = ['cliente_id', 'Recency', 'Frequency', 'Monetary']

        fig, axes = plt.subplots(1, 3, figsize=(18, 5))

        # Recency
        axes[0].hist(rfm['Recency'], bins=30, edgecolor='black', color='skyblue')
        axes[0].set_xlabel('Dias desde última compra', fontsize=11)
        axes[0].set_ylabel('Número de Clientes', fontsize=11)
        axes[0].set_title('Recency', fontsize=12, fontweight='bold')

        # Frequency
        axes[1].hist(rfm['Frequency'], bins=30, edgecolor='black', color='lightgreen')
        axes[1].set_xlabel('Número de Compras', fontsize=11)
        axes[1].set_ylabel('Número de Clientes', fontsize=11)
        axes[1].set_title('Frequency', fontsize=12, fontweight='bold')

        # Monetary
        axes[2].hist(rfm['Monetary'], bins=30, edgecolor='black', color='salmon')
        axes[2].set_xlabel('Valor Total Gasto (R$)', fontsize=11)
        axes[2].set_ylabel('Número de Clientes', fontsize=11)
        axes[2].set_title('Monetary', fontsize=12, fontweight='bold')

        plt.tight_layout()

        if save:
            plt.savefig(self.output_dir / 'rfm_analysis.png', dpi=300, bbox_inches='tight')
            logger.info(f"Gráfico salvo em: {self.output_dir / 'rfm_analysis.png'}")

        plt.close()

    def generate_business_dashboard(self) -> None:
        """Gera dashboard completo com todas as visualizações de negócio"""
        logger.info("Gerando dashboard completo de visualizações...")

        self.plot_sales_over_time()
        self.plot_top_products()
        self.plot_customer_segmentation()
        self.plot_wine_analysis()
        self.plot_rfm_analysis()

        logger.info("Dashboard completo gerado com sucesso!")

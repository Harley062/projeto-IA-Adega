"""
Módulo para Avaliação de Modelos de Machine Learning
"""
import pandas as pd
import numpy as np
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    confusion_matrix, classification_report, roc_auc_score, roc_curve,
    precision_recall_curve, average_precision_score
)
import matplotlib.pyplot as plt
import seaborn as sns
from typing import Dict, Any, Optional
import logging
from pathlib import Path

logger = logging.getLogger(__name__)


class ModelEvaluator:
    """Classe para avaliação detalhada de modelos de classificação"""

    def __init__(self, output_dir: str = "output/plots"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.metrics_history = []

    def calculate_metrics(self, y_true: np.ndarray, y_pred: np.ndarray,
                           y_pred_proba: Optional[np.ndarray] = None) -> Dict[str, float]:
        """
        Calcula métricas de avaliação do modelo

        Args:
            y_true: Labels verdadeiros
            y_pred: Predições do modelo
            y_pred_proba: Probabilidades preditas (opcional)

        Returns:
            Dicionário com métricas
        """
        logger.info("Calculando métricas de avaliação...")

        metrics = {
            'accuracy': accuracy_score(y_true, y_pred),
            'precision': precision_score(y_true, y_pred, average='weighted', zero_division=0),
            'recall': recall_score(y_true, y_pred, average='weighted', zero_division=0),
            'f1_score': f1_score(y_true, y_pred, average='weighted', zero_division=0),
        }

        # Se temos probabilidades, calcular AUC
        if y_pred_proba is not None:
            try:
                # Para classificação binária
                if len(np.unique(y_true)) == 2:
                    metrics['roc_auc'] = roc_auc_score(y_true, y_pred_proba[:, 1])
                    metrics['avg_precision'] = average_precision_score(y_true, y_pred_proba[:, 1])
                # Para classificação multiclasse
                else:
                    metrics['roc_auc'] = roc_auc_score(y_true, y_pred_proba, multi_class='ovr', average='weighted')
            except Exception as e:
                logger.warning(f"Não foi possível calcular AUC: {e}")

        # Armazenar histórico
        self.metrics_history.append(metrics)

        return metrics

    def print_metrics(self, metrics: Dict[str, float]) -> None:
        """
        Imprime métricas de forma formatada

        Args:
            metrics: Dicionário com métricas
        """
        logger.info("\n" + "="*50)
        logger.info("MÉTRICAS DE AVALIAÇÃO")
        logger.info("="*50)

        for metric_name, value in metrics.items():
            logger.info(f"{metric_name.upper():<20}: {value:.4f}")

        logger.info("="*50 + "\n")

    def plot_confusion_matrix(self, y_true: np.ndarray, y_pred: np.ndarray,
                                labels: Optional[list] = None, save: bool = True) -> None:
        """
        Plota matriz de confusão

        Args:
            y_true: Labels verdadeiros
            y_pred: Predições do modelo
            labels: Labels das classes
            save: Se deve salvar o gráfico
        """
        logger.info("Gerando matriz de confusão...")

        cm = confusion_matrix(y_true, y_pred)

        # Se labels não foi fornecido, usar as classes únicas
        if labels is None:
            labels = sorted(np.unique(np.concatenate([y_true, y_pred])))

        plt.figure(figsize=(10, 8))
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', square=True,
                     xticklabels=labels, yticklabels=labels)

        plt.title('Matriz de Confusão', fontsize=14, fontweight='bold')
        plt.ylabel('Valor Real', fontsize=12)
        plt.xlabel('Valor Predito', fontsize=12)
        plt.tight_layout()

        if save:
            plt.savefig(self.output_dir / 'confusion_matrix.png', dpi=300, bbox_inches='tight')
            logger.info(f"Matriz de confusão salva em: {self.output_dir / 'confusion_matrix.png'}")

        plt.close()

    def plot_roc_curve(self, y_true: np.ndarray, y_pred_proba: np.ndarray,
                        save: bool = True) -> None:
        """
        Plota curva ROC

        Args:
            y_true: Labels verdadeiros
            y_pred_proba: Probabilidades preditas
            save: Se deve salvar o gráfico
        """
        logger.info("Gerando curva ROC...")

        # Verificar se é classificação binária
        if len(np.unique(y_true)) != 2:
            logger.warning("Curva ROC disponível apenas para classificação binária")
            return

        fpr, tpr, _ = roc_curve(y_true, y_pred_proba[:, 1])
        roc_auc = roc_auc_score(y_true, y_pred_proba[:, 1])

        plt.figure(figsize=(10, 8))
        plt.plot(fpr, tpr, color='darkorange', lw=2, label=f'ROC curve (AUC = {roc_auc:.2f})')
        plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--', label='Random Classifier')

        plt.xlim([0.0, 1.0])
        plt.ylim([0.0, 1.05])
        plt.xlabel('Taxa de Falsos Positivos', fontsize=12)
        plt.ylabel('Taxa de Verdadeiros Positivos', fontsize=12)
        plt.title('Curva ROC (Receiver Operating Characteristic)', fontsize=14, fontweight='bold')
        plt.legend(loc="lower right")
        plt.grid(alpha=0.3)
        plt.tight_layout()

        if save:
            plt.savefig(self.output_dir / 'roc_curve.png', dpi=300, bbox_inches='tight')
            logger.info(f"Curva ROC salva em: {self.output_dir / 'roc_curve.png'}")

        plt.close()

    def plot_precision_recall_curve(self, y_true: np.ndarray, y_pred_proba: np.ndarray,
                                      save: bool = True) -> None:
        """
        Plota curva Precision-Recall

        Args:
            y_true: Labels verdadeiros
            y_pred_proba: Probabilidades preditas
            save: Se deve salvar o gráfico
        """
        logger.info("Gerando curva Precision-Recall...")

        # Verificar se é classificação binária
        if len(np.unique(y_true)) != 2:
            logger.warning("Curva Precision-Recall disponível apenas para classificação binária")
            return

        precision, recall, _ = precision_recall_curve(y_true, y_pred_proba[:, 1])
        avg_precision = average_precision_score(y_true, y_pred_proba[:, 1])

        plt.figure(figsize=(10, 8))
        plt.plot(recall, precision, color='blue', lw=2, label=f'PR curve (AP = {avg_precision:.2f})')

        plt.xlim([0.0, 1.0])
        plt.ylim([0.0, 1.05])
        plt.xlabel('Recall', fontsize=12)
        plt.ylabel('Precision', fontsize=12)
        plt.title('Curva Precision-Recall', fontsize=14, fontweight='bold')
        plt.legend(loc="lower left")
        plt.grid(alpha=0.3)
        plt.tight_layout()

        if save:
            plt.savefig(self.output_dir / 'precision_recall_curve.png', dpi=300, bbox_inches='tight')
            logger.info(f"Curva Precision-Recall salva em: {self.output_dir / 'precision_recall_curve.png'}")

        plt.close()

    def plot_feature_importance(self, feature_importance: pd.DataFrame, save: bool = True) -> None:
        """
        Plota importância das features

        Args:
            feature_importance: DataFrame com importância das features
            save: Se deve salvar o gráfico
        """
        logger.info("Gerando gráfico de importância das features...")

        if feature_importance.empty:
            logger.warning("DataFrame de importância vazio")
            return

        plt.figure(figsize=(12, 8))
        plt.barh(feature_importance['feature'].astype(str), feature_importance['importance'])
        plt.xlabel('Importância', fontsize=12)
        plt.ylabel('Features', fontsize=12)
        plt.title('Importância das Features', fontsize=14, fontweight='bold')
        plt.tight_layout()

        if save:
            plt.savefig(self.output_dir / 'feature_importance.png', dpi=300, bbox_inches='tight')
            logger.info(f"Gráfico de importância salvo em: {self.output_dir / 'feature_importance.png'}")

        plt.close()

    def plot_model_comparison(self, results: Dict[str, Dict], save: bool = True) -> None:
        """
        Plota comparação entre diferentes modelos

        Args:
            results: Dicionário com resultados dos modelos
            save: Se deve salvar o gráfico
        """
        logger.info("Gerando comparação de modelos...")

        # Extrair scores
        model_names = []
        scores = []

        for name, result in results.items():
            if result.get('trained', False):
                model_names.append(name)
                scores.append(result['test_score'])

        if not model_names:
            logger.warning("Nenhum modelo treinado para comparar")
            return

        # Criar DataFrame para facilitar plotagem
        comparison_df = pd.DataFrame({
            'Model': model_names,
            'Accuracy': scores
        }).sort_values('Accuracy', ascending=True)

        plt.figure(figsize=(12, 8))
        plt.barh(comparison_df['Model'], comparison_df['Accuracy'])
        plt.xlabel('Accuracy', fontsize=12)
        plt.ylabel('Modelo', fontsize=12)
        plt.title('Comparação de Modelos - Accuracy', fontsize=14, fontweight='bold')
        plt.xlim([0, 1])

        # Adicionar valores nas barras
        for idx, value in enumerate(comparison_df['Accuracy']):
            plt.text(value, idx, f' {value:.4f}', va='center')

        plt.tight_layout()

        if save:
            plt.savefig(self.output_dir / 'model_comparison.png', dpi=300, bbox_inches='tight')
            logger.info(f"Comparação de modelos salva em: {self.output_dir / 'model_comparison.png'}")

        plt.close()

    def generate_classification_report(self, y_true: np.ndarray, y_pred: np.ndarray,
                                         target_names: Optional[list] = None) -> str:
        """
        Gera relatório de classificação detalhado

        Args:
            y_true: Labels verdadeiros
            y_pred: Predições do modelo
            target_names: Nomes das classes

        Returns:
            String com o relatório
        """
        logger.info("Gerando relatório de classificação...")

        report = classification_report(y_true, y_pred, target_names=target_names, zero_division=0)

        logger.info("\n" + report)

        return report

    def save_evaluation_report(self, metrics: Dict[str, float], report: str,
                                 filename: str = "evaluation_report.txt") -> None:
        """
        Salva relatório de avaliação em arquivo texto

        Args:
            metrics: Dicionário com métricas
            report: Relatório de classificação
            filename: Nome do arquivo
        """
        output_path = Path("output/reports")
        output_path.mkdir(parents=True, exist_ok=True)

        filepath = output_path / filename

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write("="*60 + "\n")
            f.write("RELATÓRIO DE AVALIAÇÃO DO MODELO\n")
            f.write("="*60 + "\n\n")

            f.write("MÉTRICAS GERAIS:\n")
            f.write("-"*60 + "\n")
            for metric_name, value in metrics.items():
                f.write(f"{metric_name.upper():<20}: {value:.4f}\n")

            f.write("\n" + "="*60 + "\n")
            f.write("RELATÓRIO DE CLASSIFICAÇÃO:\n")
            f.write("="*60 + "\n\n")
            f.write(report)

        logger.info(f"Relatório salvo em: {filepath}")

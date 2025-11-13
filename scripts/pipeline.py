"""
Pipeline Principal de Análise de Dados da Adega
"""
import sys
from pathlib import Path

# Adicionar src ao path
sys.path.append(str(Path(__file__).parent / 'src'))

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split

# Imports dos módulos personalizados
from data.data_loader import DataLoader
from data.eda import ExploratoryAnalysis
from data.feature_engineering import FeatureEngineer
from models.model_trainer import ModelTrainer
from models.model_evaluation import ModelEvaluator
from visualization.plots import AdvancedPlotter
from utils.logger import setup_logger
from utils.config import Config

import warnings
warnings.filterwarnings('ignore')


class MLPipeline:
    """Pipeline completo de Machine Learning"""

    def __init__(self, config: Config = None):
        self.config = config if config else Config()
        self.logger = setup_logger('adega_ml', log_dir=self.config.LOGS_DIR)
        self.config.create_directories()

        # Componentes do pipeline
        self.data_loader = None
        self.feature_engineer = None
        self.model_trainer = None
        self.model_evaluator = None

        # Dados
        self.data_raw = None
        self.data_processed = None
        self.X_train = None
        self.X_test = None
        self.y_train = None
        self.y_test = None

    def run_data_loading(self):
        """Etapa 1: Carregamento de dados"""
        self.logger.info("="*60)
        self.logger.info("ETAPA 1: CARREGAMENTO DE DADOS")
        self.logger.info("="*60)

        self.data_loader = DataLoader(data_dir=self.config.DATA_DIR)
        clientes, produtos, compras = self.data_loader.load_data()

        # Validar dados
        self.data_loader.validate_data()

        # Fazer merge
        self.data_raw = self.data_loader.merge_data()

        # Limpar dados
        self.data_raw = self.data_loader.clean_data()

        # Resumo
        summary = self.data_loader.get_data_summary()
        self.logger.info(f"\nResumo dos dados:")
        for key, value in summary.items():
            if not isinstance(value, dict):
                self.logger.info(f"  {key}: {value}")

        return self.data_raw

    def run_eda(self):
        """Etapa 2: Análise Exploratória de Dados"""
        self.logger.info("\n" + "="*60)
        self.logger.info("ETAPA 2: ANÁLISE EXPLORATÓRIA DE DADOS (EDA)")
        self.logger.info("="*60)

        eda = ExploratoryAnalysis(self.data_raw, output_dir=self.config.PLOTS_DIR)

        # Gerar relatório completo
        eda.generate_full_report()

        # Estatísticas descritivas
        numeric_stats, categorical_stats = eda.generate_summary_statistics()
        self.logger.info("\nEstatísticas numéricas:")
        self.logger.info(str(numeric_stats))

        # Visualizações de negócio
        plotter = AdvancedPlotter(self.data_raw, output_dir=self.config.PLOTS_DIR)
        plotter.generate_business_dashboard()

        self.logger.info("\nEDA concluída! Gráficos salvos em: output/plots/")

    def run_feature_engineering(self):
        """Etapa 3: Feature Engineering"""
        self.logger.info("\n" + "="*60)
        self.logger.info("ETAPA 3: FEATURE ENGINEERING")
        self.logger.info("="*60)

        self.feature_engineer = FeatureEngineer()

        # Aplicar feature engineering
        self.data_processed = self.feature_engineer.engineer_all_features(
            self.data_raw,
            include_temporal=self.config.INCLUDE_TEMPORAL_FEATURES,
            include_aggregated=self.config.INCLUDE_AGGREGATED_FEATURES,
            include_interactions=self.config.INCLUDE_INTERACTION_FEATURES
        )

        self.logger.info(f"Features criadas: {len(self.data_processed.columns)} colunas")
        self.logger.info(f"Colunas: {list(self.data_processed.columns)}")

        return self.data_processed

    def prepare_data_for_ml(self):
        """Etapa 4: Preparação dos dados para ML"""
        self.logger.info("\n" + "="*60)
        self.logger.info("ETAPA 4: PREPARAÇÃO DOS DADOS PARA ML")
        self.logger.info("="*60)

        # Verificar se existe coluna target
        if 'target' not in self.data_processed.columns:
            self.logger.warning("Coluna 'target' não encontrada. Criando target baseado em 'cancelou_assinatura'")

            # Criar target baseado em cancelamento de assinatura
            if 'cancelou_assinatura' in self.data_processed.columns:
                # Codificar se ainda for string
                self.data_processed['target'] = self.data_processed['cancelou_assinatura'].apply(
                    lambda x: 1 if x == 'Sim' or x == 1 else 0
                )
            else:
                self.logger.error("Não foi possível criar target. Verifique os dados.")
                return

        # Separar features e target
        X = self.data_processed.drop('target', axis=1)
        y = self.data_processed['target']

        # Remover coluna data_compra (datetime não pode ser usada em ML)
        if 'data_compra' in X.columns:
            X = X.drop('data_compra', axis=1)
            self.logger.info("Coluna 'data_compra' removida (já extraímos features temporais dela)")

        # Codificar features categóricas
        X = self.feature_engineer.encode_categorical_features(X)

        # Garantir que todas as colunas são numéricas
        for col in X.columns:
            if X[col].dtype == 'object':
                self.logger.warning(f"Coluna {col} ainda é object, tentando converter...")
                X[col] = pd.to_numeric(X[col], errors='coerce')
            elif X[col].dtype == 'datetime64[ns]':
                self.logger.warning(f"Coluna {col} é datetime, removendo...")
                X = X.drop(col, axis=1)

        # Remover colunas com muitos NaN
        X = X.dropna(axis=1, thresh=len(X) * 0.5)

        # Preencher NaN restantes com a média
        numeric_cols = X.select_dtypes(include=[np.number]).columns
        X[numeric_cols] = X[numeric_cols].fillna(X[numeric_cols].mean())

        # Split train/test
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(
            X, y,
            test_size=self.config.TEST_SIZE,
            random_state=self.config.RANDOM_STATE,
            stratify=y
        )

        self.logger.info(f"Dados de treino: {self.X_train.shape}")
        self.logger.info(f"Dados de teste: {self.X_test.shape}")
        self.logger.info(f"Distribuição do target (treino): {self.y_train.value_counts().to_dict()}")

    def run_model_training(self):
        """Etapa 5: Treinamento de modelos"""
        self.logger.info("\n" + "="*60)
        self.logger.info("ETAPA 5: TREINAMENTO DE MODELOS")
        self.logger.info("="*60)

        self.model_trainer = ModelTrainer(random_state=self.config.RANDOM_STATE)

        # Treinar todos os modelos
        results = self.model_trainer.train_all_models(
            self.X_train, self.y_train,
            self.X_test, self.y_test
        )

        # Validação cruzada
        self.logger.info("\nExecutando validação cruzada...")
        cv_results = self.model_trainer.cross_validate_models(
            pd.concat([self.X_train, self.X_test]),
            pd.concat([self.y_train, self.y_test]),
            cv=self.config.CV_FOLDS
        )

        # Salvar melhor modelo
        if self.model_trainer.best_model:
            self.model_trainer.save_model(
                self.model_trainer.best_model,
                f'best_model_{self.model_trainer.best_model_name.replace(" ", "_")}.pkl',
                output_dir=self.config.MODELS_DIR
            )

        return results

    def run_model_evaluation(self, results):
        """Etapa 6: Avaliação de modelos"""
        self.logger.info("\n" + "="*60)
        self.logger.info("ETAPA 6: AVALIAÇÃO DE MODELOS")
        self.logger.info("="*60)

        self.model_evaluator = ModelEvaluator(output_dir=self.config.PLOTS_DIR)

        # Verificar se algum modelo foi treinado com sucesso
        if self.model_trainer.best_model is None:
            self.logger.error("Nenhum modelo foi treinado com sucesso. Pulando avaliação.")
            self.logger.error("Verifique os erros acima e corrija os dados de entrada.")
            return

        # Avaliar melhor modelo
        best_model = self.model_trainer.best_model
        y_pred = best_model.predict(self.X_test)
        y_pred_proba = best_model.predict_proba(self.X_test)

        # Calcular métricas
        metrics = self.model_evaluator.calculate_metrics(
            self.y_test.values,
            y_pred,
            y_pred_proba
        )

        self.model_evaluator.print_metrics(metrics)

        # Gerar visualizações
        self.model_evaluator.plot_confusion_matrix(self.y_test.values, y_pred)
        self.model_evaluator.plot_roc_curve(self.y_test.values, y_pred_proba)
        self.model_evaluator.plot_precision_recall_curve(self.y_test.values, y_pred_proba)

        # Comparação de modelos
        self.model_evaluator.plot_model_comparison(results)

        # Importância das features
        feature_importance = self.model_trainer.get_feature_importance()
        if not feature_importance.empty:
            # Mapear índices para nomes de colunas
            feature_importance['feature'] = feature_importance['feature'].map(
                lambda x: self.X_train.columns[x] if x < len(self.X_train.columns) else f'Feature_{x}'
            )
            self.model_evaluator.plot_feature_importance(feature_importance)

        # Gerar relatório
        report = self.model_evaluator.generate_classification_report(self.y_test.values, y_pred)
        self.model_evaluator.save_evaluation_report(metrics, report)

        self.logger.info("\nAvaliação concluída! Resultados salvos em: output/")

    def run_full_pipeline(self):
        """Executa o pipeline completo"""
        self.logger.info("\n" + "#"*60)
        self.logger.info("INICIANDO PIPELINE COMPLETO DE MACHINE LEARNING")
        self.logger.info("#"*60 + "\n")

        try:
            # Etapa 1: Carregar dados
            self.run_data_loading()

            # Etapa 2: EDA
            self.run_eda()

            # Etapa 3: Feature Engineering
            self.run_feature_engineering()

            # Etapa 4: Preparar dados
            self.prepare_data_for_ml()

            # Etapa 5: Treinar modelos
            results = self.run_model_training()

            # Etapa 6: Avaliar modelos
            self.run_model_evaluation(results)

            self.logger.info("\n" + "#"*60)
            self.logger.info("PIPELINE CONCLUÍDO COM SUCESSO!")
            self.logger.info("#"*60)
            self.logger.info(f"\nMelhor modelo: {self.model_trainer.best_model_name}")
            self.logger.info(f"Accuracy: {self.model_trainer.best_score:.4f}")
            self.logger.info("\nResultados salvos em:")
            self.logger.info(f"  - Modelos: {self.config.MODELS_DIR}")
            self.logger.info(f"  - Gráficos: {self.config.PLOTS_DIR}")
            self.logger.info(f"  - Relatórios: {self.config.REPORTS_DIR}")
            self.logger.info(f"  - Logs: {self.config.LOGS_DIR}")

        except Exception as e:
            self.logger.error(f"\nERRO NO PIPELINE: {e}", exc_info=True)
            raise


def main():
    """Função principal"""
    # Criar configuração
    config = Config()

    # Criar e executar pipeline
    pipeline = MLPipeline(config)
    pipeline.run_full_pipeline()


if __name__ == "__main__":
    main()

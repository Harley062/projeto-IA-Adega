"""
Módulo para Treinamento de Modelos de Machine Learning
"""
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV, StratifiedKFold
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier, AdaBoostClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.tree import DecisionTreeClassifier
from typing import Dict, Tuple, Any, Optional
import logging
import joblib
from pathlib import Path

logger = logging.getLogger(__name__)


class ModelTrainer:
    """Classe para treinamento e avaliação de modelos de ML"""

    def __init__(self, random_state: int = 42):
        self.random_state = random_state
        self.models = {}
        self.best_model = None
        self.best_model_name = None
        self.best_score = 0
        self.cv_results = {}

    def get_models(self) -> Dict[str, Any]:
        """
        Retorna dicionário com modelos de classificação

        Returns:
            Dicionário com modelos instanciados
        """
        models = {
            'Random Forest': RandomForestClassifier(random_state=self.random_state, n_jobs=-1),
            'Gradient Boosting': GradientBoostingClassifier(random_state=self.random_state),
            'Logistic Regression': LogisticRegression(random_state=self.random_state, max_iter=1000),
            'Decision Tree': DecisionTreeClassifier(random_state=self.random_state),
            'KNN': KNeighborsClassifier(),
            'Naive Bayes': GaussianNB(),
            'AdaBoost': AdaBoostClassifier(random_state=self.random_state),
        }

        return models

    def train_single_model(self, model: Any, X_train: pd.DataFrame, y_train: pd.Series,
                            X_test: pd.DataFrame, y_test: pd.Series) -> Tuple[Any, float]:
        """
        Treina um modelo individual

        Args:
            model: Modelo a ser treinado
            X_train: Features de treino
            y_train: Target de treino
            X_test: Features de teste
            y_test: Target de teste

        Returns:
            Tupla com modelo treinado e score
        """
        model.fit(X_train, y_train)
        score = model.score(X_test, y_test)

        return model, score

    def train_all_models(self, X_train: pd.DataFrame, y_train: pd.Series,
                          X_test: pd.DataFrame, y_test: pd.Series) -> Dict[str, Dict]:
        """
        Treina todos os modelos disponíveis

        Args:
            X_train: Features de treino
            y_train: Target de treino
            X_test: Features de teste
            y_test: Target de teste

        Returns:
            Dicionário com resultados de todos os modelos
        """
        logger.info("Iniciando treinamento de múltiplos modelos...")

        models = self.get_models()
        results = {}

        for name, model in models.items():
            logger.info(f"Treinando {name}...")

            try:
                trained_model, score = self.train_single_model(
                    model, X_train, y_train, X_test, y_test
                )

                self.models[name] = trained_model

                results[name] = {
                    'model': trained_model,
                    'test_score': score,
                    'trained': True
                }

                logger.info(f"{name} - Accuracy: {score:.4f}")

                # Atualizar melhor modelo
                if score > self.best_score:
                    self.best_score = score
                    self.best_model = trained_model
                    self.best_model_name = name

            except Exception as e:
                logger.error(f"Erro ao treinar {name}: {e}")
                results[name] = {
                    'model': None,
                    'test_score': 0,
                    'trained': False,
                    'error': str(e)
                }

        logger.info(f"\nMelhor modelo: {self.best_model_name} (Accuracy: {self.best_score:.4f})")

        return results

    def cross_validate_models(self, X: pd.DataFrame, y: pd.Series, cv: int = 5) -> Dict[str, Dict]:
        """
        Realiza validação cruzada em todos os modelos

        Args:
            X: Features
            y: Target
            cv: Número de folds

        Returns:
            Dicionário com resultados da validação cruzada
        """
        logger.info(f"Realizando validação cruzada com {cv} folds...")

        models = self.get_models()
        cv_results = {}

        skf = StratifiedKFold(n_splits=cv, shuffle=True, random_state=self.random_state)

        for name, model in models.items():
            logger.info(f"Validação cruzada: {name}...")

            try:
                scores = cross_val_score(model, X, y, cv=skf, scoring='accuracy', n_jobs=-1)

                cv_results[name] = {
                    'scores': scores,
                    'mean_score': scores.mean(),
                    'std_score': scores.std(),
                    'min_score': scores.min(),
                    'max_score': scores.max()
                }

                logger.info(f"{name} - CV Accuracy: {scores.mean():.4f} (+/- {scores.std():.4f})")

            except Exception as e:
                logger.error(f"Erro na validação cruzada de {name}: {e}")
                cv_results[name] = {
                    'error': str(e)
                }

        self.cv_results = cv_results
        return cv_results

    def hyperparameter_tuning(self, model_name: str, X_train: pd.DataFrame, y_train: pd.Series,
                               param_grid: Optional[Dict] = None, cv: int = 3) -> Tuple[Any, Dict]:
        """
        Realiza otimização de hiperparâmetros usando GridSearchCV

        Args:
            model_name: Nome do modelo para otimizar
            X_train: Features de treino
            y_train: Target de treino
            param_grid: Grade de parâmetros (None = usar padrão)
            cv: Número de folds

        Returns:
            Tupla com melhor modelo e melhores parâmetros
        """
        logger.info(f"Otimizando hiperparâmetros para {model_name}...")

        models = self.get_models()

        if model_name not in models:
            raise ValueError(f"Modelo {model_name} não encontrado")

        model = models[model_name]

        # Parâmetros padrão para cada modelo
        if param_grid is None:
            default_params = {
                'Random Forest': {
                    'n_estimators': [50, 100, 200],
                    'max_depth': [None, 10, 20, 30],
                    'min_samples_split': [2, 5, 10],
                    'min_samples_leaf': [1, 2, 4]
                },
                'Gradient Boosting': {
                    'n_estimators': [50, 100, 200],
                    'learning_rate': [0.01, 0.1, 0.2],
                    'max_depth': [3, 5, 7]
                },
                'Logistic Regression': {
                    'C': [0.001, 0.01, 0.1, 1, 10],
                    'penalty': ['l1', 'l2'],
                    'solver': ['liblinear', 'saga']
                },
                'Decision Tree': {
                    'max_depth': [None, 10, 20, 30],
                    'min_samples_split': [2, 5, 10],
                    'criterion': ['gini', 'entropy']
                },
                'KNN': {
                    'n_neighbors': [3, 5, 7, 9, 11],
                    'weights': ['uniform', 'distance'],
                    'metric': ['euclidean', 'manhattan']
                }
            }

            param_grid = default_params.get(model_name, {})

        if not param_grid:
            logger.warning(f"Sem parâmetros para otimizar em {model_name}")
            return model, {}

        grid_search = GridSearchCV(
            model,
            param_grid,
            cv=cv,
            scoring='accuracy',
            n_jobs=-1,
            verbose=1
        )

        grid_search.fit(X_train, y_train)

        logger.info(f"Melhores parâmetros: {grid_search.best_params_}")
        logger.info(f"Melhor score CV: {grid_search.best_score_:.4f}")

        return grid_search.best_estimator_, grid_search.best_params_

    def save_model(self, model: Any, filename: str, output_dir: str = "output/models") -> None:
        """
        Salva modelo treinado em disco

        Args:
            model: Modelo a ser salvo
            filename: Nome do arquivo
            output_dir: Diretório de saída
        """
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)

        filepath = output_path / filename
        joblib.dump(model, filepath)

        logger.info(f"Modelo salvo em: {filepath}")

    def load_model(self, filename: str, output_dir: str = "output/models") -> Any:
        """
        Carrega modelo salvo do disco

        Args:
            filename: Nome do arquivo
            output_dir: Diretório onde está o modelo

        Returns:
            Modelo carregado
        """
        filepath = Path(output_dir) / filename

        if not filepath.exists():
            raise FileNotFoundError(f"Modelo não encontrado: {filepath}")

        model = joblib.load(filepath)
        logger.info(f"Modelo carregado de: {filepath}")

        return model

    def get_feature_importance(self, model_name: Optional[str] = None, top_n: int = 10) -> pd.DataFrame:
        """
        Retorna a importância das features do modelo

        Args:
            model_name: Nome do modelo (None = usar melhor modelo)
            top_n: Número de features mais importantes

        Returns:
            DataFrame com importância das features
        """
        if model_name is None:
            model = self.best_model
            model_name = self.best_model_name
        else:
            model = self.models.get(model_name)

        if model is None:
            raise ValueError(f"Modelo {model_name} não encontrado")

        # Verificar se o modelo possui feature_importances_
        if not hasattr(model, 'feature_importances_'):
            logger.warning(f"{model_name} não possui feature importance")
            return pd.DataFrame()

        importances = model.feature_importances_

        # Criar DataFrame com importâncias
        feature_importance = pd.DataFrame({
            'feature': range(len(importances)),
            'importance': importances
        }).sort_values('importance', ascending=False).head(top_n)

        return feature_importance

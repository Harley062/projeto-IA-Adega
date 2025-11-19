"""
Módulo de configuração do projeto
"""
from dataclasses import dataclass
from pathlib import Path


@dataclass
class Config:
    """Configurações do projeto"""

    # Diretórios
    DATA_DIR: str = "data"
    OUTPUT_DIR: str = "output"
    MODELS_DIR: str = "output/models"
    PLOTS_DIR: str = "output/plots"
    REPORTS_DIR: str = "output/reports"
    LOGS_DIR: str = "logs"

    # Arquivos de dados
    CLIENTES_FILE: str = "Cliente.csv"
    PRODUTOS_FILE: str = "produtos.csv"
    COMPRAS_FILE: str = "Compras.csv"

    # Parâmetros de ML
    TEST_SIZE: float = 0.2
    RANDOM_STATE: int = 42
    CV_FOLDS: int = 5

    # Feature Engineering
    INCLUDE_TEMPORAL_FEATURES: bool = True
    INCLUDE_AGGREGATED_FEATURES: bool = True
    INCLUDE_INTERACTION_FEATURES: bool = True

    # Normalização
    SCALER_METHOD: str = "standard"  # 'standard' ou 'minmax'

    # Seleção de features
    N_FEATURES_TO_SELECT: int = 20
    FEATURE_SELECTION_METHOD: str = "f_classif"  # 'f_classif' ou 'mutual_info'

    # Visualizações
    FIGURE_DPI: int = 300
    FIGURE_SIZE: tuple = (12, 6)

    def create_directories(self):
        """Cria todos os diretórios necessários"""
        directories = [
            self.OUTPUT_DIR,
            self.MODELS_DIR,
            self.PLOTS_DIR,
            self.REPORTS_DIR,
            self.LOGS_DIR
        ]

        for directory in directories:
            Path(directory).mkdir(parents=True, exist_ok=True)

    def get_data_path(self, filename: str) -> Path:
        """Retorna caminho completo para arquivo de dados"""
        return Path(self.DATA_DIR) / filename

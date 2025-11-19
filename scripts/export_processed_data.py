"""
Script para exportar a base de dados tratada usada no treinamento
"""
import sys
from pathlib import Path

# Adicionar src ao path (script está em scripts/, src está na raiz)
sys.path.append(str(Path(__file__).parent.parent / 'src'))

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split

# Imports dos módulos personalizados
from data.data_loader import DataLoader
from data.feature_engineering import FeatureEngineer
from utils.logger import setup_logger

import warnings
warnings.filterwarnings('ignore')


def export_processed_data():
    """Exporta a base de dados processada usada no treinamento"""

    logger = setup_logger('export_data')
    logger.info("=" * 80)
    logger.info("EXPORTANDO BASE DE DADOS TRATADA")
    logger.info("=" * 80)

    # 1. CARREGAR DADOS BRUTOS
    logger.info("\n[1/4] Carregando dados brutos...")
    data_loader = DataLoader(data_dir="data")
    data_loader.load_data()
    data_loader.validate_data()
    data = data_loader.merge_data()
    data = data_loader.clean_data()
    logger.info(f"✓ Dados carregados: {len(data)} registros")

    # 2. FEATURE ENGINEERING
    logger.info("\n[2/4] Aplicando Feature Engineering...")
    feature_engineer = FeatureEngineer()

    # Criar todas as features
    data = feature_engineer.engineer_all_features(
        data,
        include_temporal=True,
        include_aggregated=True,
        include_interactions=True
    )
    logger.info(f"✓ Features criadas: {len(data.columns)} colunas")

    # 3. CODIFICAR VARIÁVEIS CATEGÓRICAS
    logger.info("\n[3/4] Codificando variáveis categóricas...")
    data = feature_engineer.encode_categorical_features(data)
    logger.info(f"✓ Variáveis categóricas codificadas")

    # 4. EXPORTAR DADOS
    logger.info("\n[4/4] Exportando dados...")

    # Separar features e target
    target_column = 'cancelou_assinatura'

    if target_column in data.columns:
        y = data[target_column]
        X = data.drop(target_column, axis=1)
    else:
        logger.warning(f"Coluna target '{target_column}' não encontrada")
        y = None
        X = data

    # Remover coluna data_compra se existir
    if 'data_compra' in X.columns:
        X = X.drop('data_compra', axis=1)
        logger.info("✓ Coluna 'data_compra' removida")

    # Remover colunas datetime restantes
    datetime_cols = X.select_dtypes(include=['datetime64']).columns
    if len(datetime_cols) > 0:
        X = X.drop(datetime_cols, axis=1)
        logger.info(f"✓ Removidas {len(datetime_cols)} colunas datetime")

    # Dataset completo (features + target)
    if y is not None:
        data_complete = X.copy()
        data_complete[target_column] = y

        output_file_complete = "data_processed_complete.csv"
        data_complete.to_csv(output_file_complete, index=False, sep=';', encoding='utf-8')
        logger.info(f"✓ Base completa exportada: {output_file_complete}")
        logger.info(f"  - Dimensões: {data_complete.shape}")
        logger.info(f"  - Colunas: {len(data_complete.columns)}")

    # Dataset apenas features (X)
    output_file_features = "data_processed_features.csv"
    X.to_csv(output_file_features, index=False, sep=';', encoding='utf-8')
    logger.info(f"✓ Features exportadas: {output_file_features}")
    logger.info(f"  - Dimensões: {X.shape}")
    logger.info(f"  - Colunas: {len(X.columns)}")

    # Dataset apenas target (y)
    if y is not None:
        output_file_target = "data_processed_target.csv"
        y.to_csv(output_file_target, index=False, sep=';', encoding='utf-8', header=True)
        logger.info(f"✓ Target exportado: {output_file_target}")
        logger.info(f"  - Dimensões: {len(y)}")

    # Salvar informações sobre as colunas
    output_file_info = "data_processed_info.txt"
    with open(output_file_info, 'w', encoding='utf-8') as f:
        f.write("=" * 80 + "\n")
        f.write("INFORMAÇÕES DA BASE DE DADOS TRATADA\n")
        f.write("=" * 80 + "\n\n")

        f.write(f"Total de Registros: {len(X)}\n")
        f.write(f"Total de Features: {len(X.columns)}\n\n")

        f.write("=" * 80 + "\n")
        f.write("LISTA DE FEATURES\n")
        f.write("=" * 80 + "\n\n")

        for i, col in enumerate(X.columns, 1):
            dtype = X[col].dtype
            null_count = X[col].isnull().sum()
            unique_count = X[col].nunique()
            f.write(f"{i:2d}. {col:30s} | Tipo: {str(dtype):10s} | "
                   f"Nulos: {null_count:5d} | Únicos: {unique_count:5d}\n")

        if y is not None:
            f.write("\n" + "=" * 80 + "\n")
            f.write("TARGET (cancelou_assinatura)\n")
            f.write("=" * 80 + "\n\n")
            f.write(f"Distribuição:\n")
            f.write(str(y.value_counts()))
            f.write("\n\n")
            f.write(f"Proporção:\n")
            f.write(str(y.value_counts(normalize=True)))
            f.write("\n")

    logger.info(f"✓ Informações exportadas: {output_file_info}")

    # Criar split treino/teste
    if y is not None:
        logger.info("\n[BÔNUS] Criando split treino/teste (80/20)...")
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )

        # Exportar split
        train_data = X_train.copy()
        train_data[target_column] = y_train
        train_data.to_csv("data_processed_train.csv", index=False, sep=';', encoding='utf-8')
        logger.info(f"✓ Base de treino: data_processed_train.csv ({len(train_data)} registros)")

        test_data = X_test.copy()
        test_data[target_column] = y_test
        test_data.to_csv("data_processed_test.csv", index=False, sep=';', encoding='utf-8')
        logger.info(f"✓ Base de teste: data_processed_test.csv ({len(test_data)} registros)")

    logger.info("\n" + "=" * 80)
    logger.info("✓ EXPORTAÇÃO CONCLUÍDA COM SUCESSO!")
    logger.info("=" * 80)

    print("\n" + "=" * 80)
    print("ARQUIVOS GERADOS:")
    print("=" * 80)
    print("1. data_processed_complete.csv  - Base completa (features + target)")
    print("2. data_processed_features.csv  - Apenas features (X)")
    print("3. data_processed_target.csv    - Apenas target (y)")
    print("4. data_processed_train.csv     - Base de treino (80%)")
    print("5. data_processed_test.csv      - Base de teste (20%)")
    print("6. data_processed_info.txt      - Informações detalhadas")
    print("=" * 80)


if __name__ == "__main__":
    export_processed_data()

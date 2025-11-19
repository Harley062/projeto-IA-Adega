"""
Script de teste rápido do sistema
"""
import sys
from pathlib import Path

# Adicionar src ao path (script está em scripts/, src está na raiz)
sys.path.append(str(Path(__file__).parent.parent / 'src'))

from data.data_loader import DataLoader
from utils.logger import setup_logger

def test_data_loading():
    """Testa carregamento de dados"""
    print("\n" + "="*60)
    print("TESTE 1: Carregamento de Dados")
    print("="*60)

    try:
        loader = DataLoader(data_dir="data")
        clientes, produtos, compras = loader.load_data()

        print(f"✓ Clientes carregados: {len(clientes)} registros")
        print(f"✓ Produtos carregados: {len(produtos)} registros")
        print(f"✓ Compras carregadas: {len(compras)} registros")

        # Validar
        loader.validate_data()
        print("✓ Validação concluída com sucesso")

        # Merge
        data = loader.merge_data()
        print(f"✓ Merge realizado: {len(data)} registros combinados")

        # Limpeza
        data_clean = loader.clean_data()
        print(f"✓ Dados limpos: {len(data_clean)} registros mantidos")

        return True

    except Exception as e:
        print(f"✗ ERRO: {e}")
        return False


def test_feature_engineering():
    """Testa feature engineering"""
    print("\n" + "="*60)
    print("TESTE 2: Feature Engineering")
    print("="*60)

    try:
        from data.feature_engineering import FeatureEngineer

        loader = DataLoader(data_dir="data")
        loader.load_data()
        loader.validate_data()
        data = loader.merge_data()
        data = loader.clean_data()

        engineer = FeatureEngineer()

        print(f"Features originais: {len(data.columns)}")

        # Criar features temporais
        data = engineer.create_temporal_features(data)
        print(f"✓ Features temporais criadas")

        # Criar features agregadas
        data = engineer.create_aggregated_features(data)
        print(f"✓ Features agregadas criadas")

        # Criar features de interação
        data = engineer.create_interaction_features(data)
        print(f"✓ Features de interação criadas")

        print(f"Total de features: {len(data.columns)}")

        return True

    except Exception as e:
        print(f"✗ ERRO: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_visualization():
    """Testa geração de visualizações"""
    print("\n" + "="*60)
    print("TESTE 3: Visualizações")
    print("="*60)

    try:
        from data.eda import ExploratoryAnalysis

        loader = DataLoader(data_dir="data")
        loader.load_data()
        loader.validate_data()
        data = loader.merge_data()
        data = loader.clean_data()

        eda = ExploratoryAnalysis(data, output_dir="output/plots")

        print("✓ Gerando matriz de correlação...")
        eda.plot_correlation_matrix()

        print("✓ Gerando distribuições numéricas...")
        eda.plot_numerical_distributions()

        print("✓ Visualizações geradas com sucesso")
        print(f"✓ Verifique os gráficos em: output/plots/")

        return True

    except Exception as e:
        print(f"✗ ERRO: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Executa todos os testes"""
    print("\n" + "#"*60)
    print("TESTES DO SISTEMA DE ANÁLISE DE DADOS")
    print("#"*60)

    results = []

    # Teste 1
    results.append(("Carregamento de Dados", test_data_loading()))

    # Teste 2
    results.append(("Feature Engineering", test_feature_engineering()))

    # Teste 3
    results.append(("Visualizações", test_visualization()))

    # Resumo
    print("\n" + "="*60)
    print("RESUMO DOS TESTES")
    print("="*60)

    for test_name, result in results:
        status = "✓ PASSOU" if result else "✗ FALHOU"
        print(f"{test_name:<30} {status}")

    total_passed = sum(1 for _, result in results if result)
    total_tests = len(results)

    print("\n" + "="*60)
    print(f"RESULTADO FINAL: {total_passed}/{total_tests} testes passaram")
    print("="*60)

    if total_passed == total_tests:
        print("\n🎉 Todos os testes passaram! Sistema funcionando corretamente.")
        print("\nPróximos passos:")
        print("1. Execute 'python pipeline.py' para rodar o pipeline completo")
        print("2. Verifique os resultados em 'output/'")
    else:
        print("\n⚠️  Alguns testes falharam. Verifique os erros acima.")


if __name__ == "__main__":
    main()

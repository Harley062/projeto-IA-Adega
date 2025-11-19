"""
Módulo para Predições em Tempo Real
"""
import pandas as pd
import numpy as np
import joblib
from pathlib import Path
import logging
from typing import Dict, Any, Tuple
import sys

# Adicionar src ao path
sys.path.append(str(Path(__file__).parent.parent))

from data.feature_engineering import FeatureEngineer

logger = logging.getLogger(__name__)


class ChurnPredictor:
    """Classe para fazer predições de churn em tempo real"""

    def __init__(self, model_path: str = "output/models/best_model_Gradient_Boosting.pkl"):
        self.model_path = Path(model_path)
        self.model = None
        self.feature_engineer = FeatureEngineer()
        self.feature_names = None

    def load_model(self):
        """Carrega o modelo treinado"""
        if not self.model_path.exists():
            raise FileNotFoundError(f"Modelo não encontrado em: {self.model_path}")

        self.model = joblib.load(self.model_path)
        logger.info(f"Modelo carregado de: {self.model_path}")

    def prepare_single_prediction(self, customer_data: Dict[str, Any]) -> pd.DataFrame:
        """
        Prepara dados de um único cliente para predição

        Args:
            customer_data: Dicionário com dados do cliente

        Returns:
            DataFrame preparado para predição
        """
        from datetime import datetime
        from sklearn.preprocessing import LabelEncoder

        # Converter para DataFrame
        df = pd.DataFrame([customer_data])

        # Adicionar IDs padrão se não existirem
        if 'compra_id' not in df.columns:
            df['compra_id'] = 1
        if 'produto_id' not in df.columns:
            df['produto_id'] = 1
        if 'cliente_id' not in df.columns:
            df['cliente_id'] = customer_data.get('cliente_id', 1)

        # Criar features temporais usando data atual
        now = datetime.now()
        df['ano'] = now.year
        df['mes'] = now.month
        df['dia'] = now.day
        df['dia_semana'] = now.weekday()
        df['trimestre'] = (now.month - 1) // 3 + 1
        df['semana_ano'] = now.isocalendar()[1]

        # Features cíclicas
        df['mes_sin'] = np.sin(2 * np.pi * df['mes'] / 12)
        df['mes_cos'] = np.cos(2 * np.pi * df['mes'] / 12)
        df['dia_semana_sin'] = np.sin(2 * np.pi * df['dia_semana'] / 7)
        df['dia_semana_cos'] = np.cos(2 * np.pi * df['dia_semana'] / 7)

        # Adicionar campos de produto se não existirem
        if 'nome_produto' not in df.columns:
            df['nome_produto'] = 'Vinho Padrão'
        if 'safra' not in df.columns:
            df['safra'] = 2020  # Ano padrão

        # Features agregadas (valores padrão baseados em médias típicas)
        df['total_gasto'] = df['valor'] if 'valor' in df.columns else 0
        df['ticket_medio'] = df['valor'] if 'valor' in df.columns else 0
        df['num_compras'] = 1
        df['total_itens'] = df['quantidade'] if 'quantidade' in df.columns else 1
        df['media_itens'] = df['quantidade'] if 'quantidade' in df.columns else 1

        # Features de produto
        df['preco_medio_produto'] = df['valor'] if 'valor' in df.columns else 0
        df['popularidade_produto'] = 1
        df['total_vendido_produto'] = df['quantidade'] if 'quantidade' in df.columns else 1

        # Features RFM
        df['recencia'] = 0  # Cliente atual
        df['frequencia'] = 1
        df['valor_total'] = df['valor'] if 'valor' in df.columns else 0

        # Feature engineering de interação
        if 'valor' in df.columns and 'quantidade' in df.columns:
            df['valor_por_unidade'] = df['valor'] / (df['quantidade'] + 1)

        if 'pontuacao_engajamento' in df.columns and 'idade' in df.columns:
            df['engajamento_por_idade'] = df['pontuacao_engajamento'] / (df['idade'] + 1)
            df['engajamento_x_idade'] = df['pontuacao_engajamento'] * df['idade']

        if 'valor' in df.columns and 'idade' in df.columns:
            df['valor_por_idade'] = df['valor'] / (df['idade'] + 1)

        # Adicionar coluna cancelou_assinatura (target) como 0 por padrão
        df['cancelou_assinatura'] = 0

        # Codificar variáveis categóricas
        categorical_cols = ['nome', 'cidade', 'assinante_clube', 'nome_produto', 'pais', 'tipo_uva']
        for col in categorical_cols:
            if col in df.columns:
                # Usar LabelEncoder simples com tratamento de valores desconhecidos
                le = LabelEncoder()
                # Criar um conjunto de valores conhecidos (exemplos básicos)
                known_values = {
                    'nome': [f'Cliente {i}' for i in range(1, 101)] + ['Cliente Teste', 'Maria Santos'],
                    'cidade': ['São Paulo', 'Rio de Janeiro', 'Belo Horizonte', 'Brasília',
                              'Salvador', 'Fortaleza', 'Curitiba', 'Goiânia'],
                    'assinante_clube': ['Sim', 'Não'],
                    'nome_produto': [f'Vinho {i}' for i in range(1, 51)] + ['Vinho Padrão'],
                    'pais': ['Brasil', 'França', 'Chile', 'Argentina', 'Itália',
                            'Espanha', 'Portugal', 'África do Sul'],
                    'tipo_uva': ['Merlot', 'Cabernet Sauvignon', 'Chardonnay',
                                'Sauvignon Blanc', 'Pinot Noir', 'Malbec', 'Syrah', 'Tempranillo']
                }

                if col in known_values:
                    le.fit(known_values[col])
                    try:
                        df[col] = le.transform(df[col].astype(str))
                    except ValueError:
                        # Valor desconhecido, usar 0
                        df[col] = 0
                else:
                    df[col] = 0

        # Remover apenas colunas de data que não precisamos
        cols_to_drop = ['data_compra']
        for col in cols_to_drop:
            if col in df.columns:
                df = df.drop(col, axis=1)

        # Garantir que safra é numérica
        if 'safra' in df.columns:
            df['safra'] = pd.to_numeric(df['safra'], errors='coerce').fillna(2020).astype(int)

        # Garantir que todas as colunas restantes são numéricas
        # (nome, cidade, assinante_clube, nome_produto, pais, tipo_uva já foram codificadas acima)
        for col in df.columns:
            if df[col].dtype == 'object':
                try:
                    df[col] = pd.to_numeric(df[col], errors='coerce')
                except:
                    # Se não conseguir converter, deixar como está (já deve estar codificada)
                    pass

        # Preencher NaN com 0
        df = df.fillna(0)

        # Reordenar colunas para corresponder à ordem esperada pelo modelo
        expected_columns = [
            'compra_id', 'cliente_id', 'produto_id', 'valor', 'quantidade',
            'nome', 'idade', 'cidade', 'pontuacao_engajamento', 'assinante_clube',
            'cancelou_assinatura', 'nome_produto', 'pais', 'safra', 'tipo_uva',
            'ano', 'mes', 'dia', 'dia_semana', 'trimestre', 'semana_ano',
            'mes_sin', 'mes_cos', 'dia_semana_sin', 'dia_semana_cos',
            'total_gasto', 'ticket_medio', 'num_compras', 'total_itens', 'media_itens',
            'preco_medio_produto', 'popularidade_produto', 'total_vendido_produto',
            'recencia', 'frequencia', 'valor_total',
            'valor_por_unidade', 'engajamento_por_idade', 'engajamento_x_idade', 'valor_por_idade'
        ]

        # Garantir que todas as colunas esperadas existem
        for col in expected_columns:
            if col not in df.columns:
                df[col] = 0

        # Reordenar para corresponder exatamente
        df = df[expected_columns]

        return df

    def predict_churn(self, customer_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Faz predição de churn para um cliente

        Args:
            customer_data: Dicionário com dados do cliente

        Returns:
            Dicionário com resultado da predição
        """
        if self.model is None:
            self.load_model()

        # Preparar dados
        df = self.prepare_single_prediction(customer_data)

        # Fazer predição
        prediction = self.model.predict(df)[0]
        probability = self.model.predict_proba(df)[0]

        # Interpretar resultado
        will_churn = bool(prediction == 1)
        churn_probability = float(probability[1])
        retain_probability = float(probability[0])

        # Classificar risco
        if churn_probability >= 0.7:
            risk_level = "Alto"
            risk_color = "red"
        elif churn_probability >= 0.4:
            risk_level = "Médio"
            risk_color = "orange"
        else:
            risk_level = "Baixo"
            risk_color = "green"

        # Gerar recomendações
        recommendations = self._generate_recommendations(customer_data, churn_probability)

        return {
            'will_churn': will_churn,
            'churn_probability': churn_probability,
            'retain_probability': retain_probability,
            'risk_level': risk_level,
            'risk_color': risk_color,
            'recommendations': recommendations,
            'customer_data': customer_data
        }

    def predict_batch(self, customers_df: pd.DataFrame) -> pd.DataFrame:
        """
        Faz predições em lote para múltiplos clientes

        Args:
            customers_df: DataFrame com dados de múltiplos clientes

        Returns:
            DataFrame com predições
        """
        if self.model is None:
            self.load_model()

        results = []

        for idx, row in customers_df.iterrows():
            customer_data = row.to_dict()
            try:
                prediction = self.predict_churn(customer_data)
                prediction['cliente_id'] = customer_data.get('cliente_id', idx)
                results.append(prediction)
            except Exception as e:
                logger.error(f"Erro ao processar cliente {idx}: {e}")
                results.append({
                    'cliente_id': customer_data.get('cliente_id', idx),
                    'error': str(e)
                })

        return pd.DataFrame(results)

    def _generate_recommendations(self, customer_data: Dict[str, Any], churn_prob: float) -> list:
        """
        Gera recomendações baseadas no perfil do cliente

        Args:
            customer_data: Dados do cliente
            churn_prob: Probabilidade de churn

        Returns:
            Lista de recomendações
        """
        recommendations = []

        # Baseado no risco
        if churn_prob >= 0.7:
            recommendations.append("🚨 URGENTE: Contato imediato necessário")
            recommendations.append("💎 Oferecer desconto especial ou upgrade gratuito")
            recommendations.append("📞 Ligar pessoalmente para entender insatisfação")

        elif churn_prob >= 0.4:
            recommendations.append("⚠️ Monitorar de perto este cliente")
            recommendations.append("📧 Enviar email com ofertas personalizadas")
            recommendations.append("🎁 Considerar programa de fidelidade")

        else:
            recommendations.append("✅ Cliente satisfeito - manter engajamento")
            recommendations.append("📈 Oportunidade de upsell")

        # Baseado em assinatura
        if customer_data.get('assinante_clube') == 'Não':
            recommendations.append("🌟 Promover benefícios do Clube de Assinantes")

        # Baseado em engajamento
        engajamento = customer_data.get('pontuacao_engajamento', 0)
        if engajamento < 5:
            recommendations.append("📊 Engajamento baixo - enviar conteúdo educativo sobre vinhos")

        # Baseado em valor
        valor = customer_data.get('valor', 0)
        if valor > 300:
            recommendations.append("💰 Cliente de alto valor - tratamento VIP")

        # Baseado em cidade
        cidade = customer_data.get('cidade', '')
        if cidade:
            recommendations.append(f"🌍 Evento exclusivo em {cidade}")

        return recommendations

    def get_feature_importance(self, customer_data: Dict[str, Any]) -> Dict[str, float]:
        """
        Retorna a importância das features para a predição

        Args:
            customer_data: Dados do cliente

        Returns:
            Dicionário com importância das features
        """
        if self.model is None:
            self.load_model()

        # Verificar se o modelo tem feature_importances_
        if not hasattr(self.model, 'feature_importances_'):
            return {}

        df = self.prepare_single_prediction(customer_data)

        importance_dict = {}
        for col, importance in zip(df.columns, self.model.feature_importances_):
            importance_dict[col] = float(importance)

        # Ordenar por importância
        importance_dict = dict(sorted(importance_dict.items(), key=lambda x: x[1], reverse=True))

        return importance_dict

    def explain_prediction(self, customer_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Explica a predição detalhadamente

        Args:
            customer_data: Dados do cliente

        Returns:
            Explicação detalhada da predição
        """
        prediction = self.predict_churn(customer_data)
        feature_importance = self.get_feature_importance(customer_data)

        # Top 5 features mais importantes
        top_features = list(feature_importance.items())[:5]

        explanation = {
            'prediction': prediction,
            'top_features': top_features,
            'reasoning': []
        }

        # Gerar explicações baseadas nas features
        for feature, importance in top_features:
            if importance > 0.1:  # Apenas features relevantes
                value = customer_data.get(feature, 'N/A')
                explanation['reasoning'].append(
                    f"'{feature}' (valor: {value}) tem importância de {importance:.2%}"
                )

        return explanation


class SalesPredictor:
    """Classe para predição de vendas"""

    def __init__(self):
        self.historical_data = None

    def load_historical_data(self, data_path: str = "data"):
        """Carrega dados históricos para análise de tendências"""
        from data.data_loader import DataLoader

        loader = DataLoader(data_dir=data_path)
        loader.load_data()
        loader.validate_data()
        self.historical_data = loader.merge_data()

    def predict_next_purchase(self, customer_id: int) -> Dict[str, Any]:
        """
        Prediz quando e quanto será a próxima compra do cliente

        Args:
            customer_id: ID do cliente

        Returns:
            Predição da próxima compra
        """
        if self.historical_data is None:
            raise ValueError("Carregue os dados históricos primeiro")

        # Filtrar compras do cliente
        customer_purchases = self.historical_data[
            self.historical_data['cliente_id'] == customer_id
        ]

        if len(customer_purchases) == 0:
            # Verificar se o cliente existe no cadastro
            from data.data_loader import DataLoader
            loader = DataLoader(data_dir="data")
            clientes, _, _ = loader.load_data()

            if customer_id in clientes['cliente_id'].values:
                return {
                    'error': f'Cliente #{customer_id} existe no cadastro, mas não possui histórico de compras. Para fazer previsões, o cliente precisa ter feito pelo menos uma compra.',
                    'customer_id': customer_id,
                    'suggestion': 'Tente com um cliente que já tenha realizado compras (exemplo: ID 5, 7, 8, 10, etc.)'
                }
            else:
                return {
                    'error': f'Cliente #{customer_id} não encontrado no sistema.',
                    'customer_id': customer_id,
                    'suggestion': 'Verifique se o ID está correto.'
                }


        # Calcular estatísticas
        avg_value = customer_purchases['valor'].mean()
        total_purchases = len(customer_purchases)
        avg_quantity = customer_purchases['quantidade'].mean()

        # Calcular intervalo médio entre compras
        if 'data_compra' in customer_purchases.columns and total_purchases > 1:
            customer_purchases = customer_purchases.sort_values('data_compra')
            customer_purchases['data_compra'] = pd.to_datetime(customer_purchases['data_compra'])

            intervals = customer_purchases['data_compra'].diff().dt.days.dropna()
            avg_interval = intervals.mean() if len(intervals) > 0 else 30

            last_purchase = customer_purchases['data_compra'].max()
            next_purchase_date = last_purchase + pd.Timedelta(days=avg_interval)
        else:
            avg_interval = 30
            next_purchase_date = pd.Timestamp.now() + pd.Timedelta(days=30)

        # Produtos preferidos
        if 'tipo_uva' in customer_purchases.columns:
            favorite_wine = customer_purchases['tipo_uva'].mode()[0] if len(customer_purchases['tipo_uva'].mode()) > 0 else 'N/A'
        else:
            favorite_wine = 'N/A'

        return {
            'customer_id': customer_id,
            'predicted_next_purchase_date': next_purchase_date.strftime('%Y-%m-%d'),
            'days_until_next_purchase': int((next_purchase_date - pd.Timestamp.now()).days),
            'predicted_value': float(avg_value),
            'predicted_quantity': int(round(avg_quantity)),
            'avg_interval_days': int(round(avg_interval)),
            'total_historical_purchases': total_purchases,
            'favorite_wine_type': favorite_wine,
            'lifetime_value': float(customer_purchases['valor'].sum())
        }

    def predict_revenue(self, months_ahead: int = 3) -> Dict[str, Any]:
        """
        Prediz receita futura baseada em tendências históricas

        Args:
            months_ahead: Número de meses para predizer

        Returns:
            Predição de receita
        """
        if self.historical_data is None:
            raise ValueError("Carregue os dados históricos primeiro")

        # Calcular receita histórica
        total_revenue = self.historical_data['valor'].sum()
        avg_monthly_revenue = total_revenue / 12  # Assumindo dados de 1 ano

        # Predição simples baseada em média
        predicted_revenue = avg_monthly_revenue * months_ahead

        # Calcular tendência
        if 'data_compra' in self.historical_data.columns:
            self.historical_data['data_compra'] = pd.to_datetime(self.historical_data['data_compra'])
            monthly_revenue = self.historical_data.groupby(
                self.historical_data['data_compra'].dt.to_period('M')
            )['valor'].sum()

            if len(monthly_revenue) > 1:
                # Calcular taxa de crescimento
                growth_rate = monthly_revenue.pct_change().mean()

                # Aplicar crescimento à predição
                for i in range(months_ahead):
                    predicted_revenue *= (1 + growth_rate)
        else:
            growth_rate = 0

        return {
            'months_ahead': months_ahead,
            'predicted_total_revenue': float(predicted_revenue),
            'predicted_monthly_avg': float(predicted_revenue / months_ahead),
            'historical_monthly_avg': float(avg_monthly_revenue),
            'growth_rate': float(growth_rate),
            'confidence': 'medium'  # Seria calculado com modelo mais sofisticado
        }


class ProductRecommender:
    """Classe para recomendação de produtos"""

    def __init__(self):
        self.historical_data = None

    def load_historical_data(self, data_path: str = "data"):
        """Carrega dados históricos"""
        from data.data_loader import DataLoader

        loader = DataLoader(data_dir=data_path)
        loader.load_data()
        loader.validate_data()
        self.historical_data = loader.merge_data()

    def recommend_products(self, customer_id: int, top_n: int = 5) -> list:
        """
        Recomenda produtos para um cliente

        Args:
            customer_id: ID do cliente
            top_n: Número de recomendações

        Returns:
            Lista de produtos recomendados
        """
        if self.historical_data is None:
            raise ValueError("Carregue os dados históricos primeiro")

        # Filtrar compras do cliente
        customer_purchases = self.historical_data[
            self.historical_data['cliente_id'] == customer_id
        ]

        if len(customer_purchases) == 0:
            return []

        # Produtos já comprados
        purchased_products = customer_purchases['produto_id'].unique()

        # Encontrar clientes similares (mesmo tipo de vinho, mesma faixa de preço)
        similar_customers = self.historical_data[
            (self.historical_data['cliente_id'] != customer_id)
        ]

        # Produtos populares entre clientes similares
        product_popularity = similar_customers[
            ~similar_customers['produto_id'].isin(purchased_products)
        ].groupby('produto_id').agg({
            'valor': 'mean',
            'compra_id': 'count'
        }).reset_index()

        product_popularity.columns = ['produto_id', 'avg_price', 'purchase_count']
        product_popularity = product_popularity.sort_values('purchase_count', ascending=False)

        # Adicionar informações do produto
        recommendations = []
        for _, row in product_popularity.head(top_n).iterrows():
            product_info = self.historical_data[
                self.historical_data['produto_id'] == row['produto_id']
            ].iloc[0]

            recommendations.append({
                'produto_id': int(row['produto_id']),
                'nome': product_info.get('nome_produto', 'N/A'),
                'tipo_uva': product_info.get('tipo_uva', 'N/A'),
                'pais': product_info.get('pais', 'N/A'),
                'avg_price': float(row['avg_price']),
                'popularity_score': int(row['purchase_count']),
                'reason': 'Popular entre clientes similares'
            })

        return recommendations

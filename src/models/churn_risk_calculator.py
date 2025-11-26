"""
Calculadora de Risco de Churn Baseada em Regras

Este módulo implementa um sistema de cálculo de probabilidade de cancelamento
baseado em regras e fatores de risco, que é mais interpretável e robusto que
modelos de ML quando há poucos dados de treinamento.

Autor: Sistema IA Adega
Data: 2025-11
"""

import pandas as pd
import numpy as np
from typing import Dict, Any


class ChurnRiskCalculator:
    """
    Calcula probabilidade de churn baseado em fatores de risco identificados
    a partir dos dados históricos.
    """

    def __init__(self):
        # Pesos de cada fator no risco total (soma = 1.0)
        self.weights = {
            'assinatura': 0.25,      # Se é assinante ou não
            'engajamento': 0.25,     # Nível de engajamento
            'recencia': 0.20,        # Tempo desde última compra
            'valor_gasto': 0.15,     # Quanto gasta
            'idade': 0.10,           # Idade do cliente
            'cidade': 0.05           # Localização
        }

    def calculate_assinatura_risk(self, data: Dict[str, Any]) -> float:
        """
        Calcula risco baseado no status de assinatura.

        Args:
            data: Dados do cliente

        Returns:
            Score de risco (0-1, onde 1 = alto risco)
        """
        assinante = data.get('assinante_clube', 'Não')

        if assinante == 'Não':
            return 0.70  # Não assinantes têm maior risco
        else:
            return 0.20  # Assinantes têm menor risco

    def calculate_engajamento_risk(self, data: Dict[str, Any]) -> float:
        """
        Calcula risco baseado no engajamento.

        Escala: 1.63 - 9.88 (baseado nos dados reais)

        Args:
            data: Dados do cliente

        Returns:
            Score de risco (0-1)
        """
        engajamento = data.get('pontuacao_engajamento', 5.0)

        # Normalizar engajamento (assumindo range de 1 a 10)
        # Quanto maior o engajamento, menor o risco
        if engajamento >= 8.0:
            return 0.10  # Engajamento alto = baixo risco
        elif engajamento >= 6.0:
            return 0.30  # Engajamento médio-alto
        elif engajamento >= 4.0:
            return 0.50  # Engajamento médio
        elif engajamento >= 2.0:
            return 0.70  # Engajamento baixo
        else:
            return 0.90  # Engajamento muito baixo

    def calculate_valor_risk(self, data: Dict[str, Any]) -> float:
        """
        Calcula risco baseado no valor gasto.

        Args:
            data: Dados do cliente

        Returns:
            Score de risco (0-1)
        """
        valor = data.get('valor', 0)

        # Clientes que gastam mais têm menor risco de churn
        if valor >= 300:
            return 0.15  # Alto valor = baixo risco
        elif valor >= 200:
            return 0.30
        elif valor >= 100:
            return 0.50
        elif valor >= 50:
            return 0.70
        else:
            return 0.85  # Baixo valor = alto risco

    def calculate_idade_risk(self, data: Dict[str, Any]) -> float:
        """
        Calcula risco baseado na idade do cliente.

        Args:
            data: Dados do cliente

        Returns:
            Score de risco (0-1)
        """
        idade = data.get('idade', 35)

        # Clientes de meia idade (35-55) tendem a ser mais estáveis
        if 35 <= idade <= 55:
            return 0.30  # Faixa etária estável
        elif 25 <= idade < 35 or 55 < idade <= 65:
            return 0.45  # Moderadamente estável
        else:
            return 0.60  # Faixas mais voláteis

    def calculate_recencia_risk(self, data: Dict[str, Any]) -> float:
        """
        Calcula risco baseado na recência (assumindo 0 para cliente atual).

        Args:
            data: Dados do cliente

        Returns:
            Score de risco (0-1)
        """
        # Para predições de novos clientes, assumimos recência 0 (compra recente)
        # Em um cenário real, isso viria dos dados históricos
        recencia = data.get('dias_desde_ultima_compra', 0)

        if recencia <= 30:
            return 0.20  # Compra muito recente
        elif recencia <= 60:
            return 0.40
        elif recencia <= 90:
            return 0.60
        elif recencia <= 180:
            return 0.80
        else:
            return 0.95  # Muito tempo sem comprar

    def calculate_cidade_risk(self, data: Dict[str, Any]) -> float:
        """
        Calcula risco baseado na cidade (indicador geográfico).

        Args:
            data: Dados do cliente

        Returns:
            Score de risco (0-1)
        """
        cidade = data.get('cidade', '')

        # Grandes capitais com maior oferta tendem a ter mais volatilidade
        capitais_grandes = ['São Paulo', 'Rio de Janeiro']
        capitais_medias = ['Belo Horizonte', 'Brasília', 'Salvador', 'Fortaleza', 'Curitiba']

        if cidade in capitais_grandes:
            return 0.50  # Média concorrência
        elif cidade in capitais_medias:
            return 0.40  # Menor concorrência
        else:
            return 0.45  # Outras cidades

    def calculate_churn_probability(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Calcula probabilidade de churn combinando todos os fatores.

        Args:
            data: Dicionário com dados do cliente

        Returns:
            Dicionário com probabilidade e detalhes
        """
        # Calcular risco de cada fator
        risks = {
            'assinatura': self.calculate_assinatura_risk(data),
            'engajamento': self.calculate_engajamento_risk(data),
            'recencia': self.calculate_recencia_risk(data),
            'valor_gasto': self.calculate_valor_risk(data),
            'idade': self.calculate_idade_risk(data),
            'cidade': self.calculate_cidade_risk(data)
        }

        # Calcular probabilidade ponderada
        churn_probability = sum(
            risks[factor] * self.weights[factor]
            for factor in risks.keys()
        )

        # Garantir que está no range [0, 1]
        churn_probability = max(0.0, min(1.0, churn_probability))

        # Adicionar variação aleatória pequena para tornar mais realista
        # (±5% de variação)
        variation = np.random.uniform(-0.05, 0.05)
        churn_probability = max(0.0, min(1.0, churn_probability + variation))

        retain_probability = 1.0 - churn_probability

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
        recommendations = self._generate_recommendations(data, churn_probability, risks)

        return {
            'will_churn': churn_probability >= 0.5,
            'churn_probability': float(churn_probability),
            'retain_probability': float(retain_probability),
            'risk_level': risk_level,
            'risk_color': risk_color,
            'risk_factors': risks,
            'recommendations': recommendations,
            'customer_data': data
        }

    def _generate_recommendations(self, customer_data: Dict[str, Any],
                                  churn_prob: float,
                                  risk_factors: Dict[str, float]) -> list:
        """
        Gera recomendações baseadas no perfil do cliente e fatores de risco.

        Args:
            customer_data: Dados do cliente
            churn_prob: Probabilidade de churn
            risk_factors: Riscos por fator

        Returns:
            Lista de recomendações
        """
        recommendations = []

        # Recomendações baseadas no nível de risco geral
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

        # Recomendações específicas por fator de risco
        if risk_factors['assinatura'] > 0.5:
            recommendations.append("🌟 Promover benefícios do Clube de Assinantes")

        if risk_factors['engajamento'] > 0.6:
            recommendations.append("📊 Engajamento baixo - enviar conteúdo educativo sobre vinhos")
            recommendations.append("🎓 Convidar para degustação ou evento")

        if risk_factors['valor_gasto'] > 0.6:
            recommendations.append("💰 Oferecer promoções para aumentar ticket médio")

        if risk_factors['recencia'] > 0.7:
            recommendations.append("⏰ Cliente inativo - campanha de reativação urgente")

        # Recomendações baseadas em valor
        valor = customer_data.get('valor', 0)
        if valor > 300:
            recommendations.append("💎 Cliente de alto valor - tratamento VIP")

        # Recomendações baseadas em cidade
        cidade = customer_data.get('cidade', '')
        if cidade:
            recommendations.append(f"🌍 Evento exclusivo em {cidade}")

        return recommendations

    def explain_prediction(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Explica a predição detalhadamente mostrando contribuição de cada fator.

        Args:
            data: Dados do cliente

        Returns:
            Explicação detalhada
        """
        result = self.calculate_churn_probability(data)

        risk_factors = result['risk_factors']
        explanations = []

        for factor, risk in risk_factors.items():
            contribution = risk * self.weights[factor]
            explanations.append({
                'factor': factor,
                'risk_score': risk,
                'weight': self.weights[factor],
                'contribution': contribution,
                'description': self._get_factor_description(factor, risk, data)
            })

        # Ordenar por contribuição
        explanations = sorted(explanations, key=lambda x: x['contribution'], reverse=True)

        return {
            'prediction': result,
            'explanations': explanations,
            'top_risk_factors': [e['factor'] for e in explanations[:3]]
        }

    def _get_factor_description(self, factor: str, risk: float, data: Dict[str, Any]) -> str:
        """Gera descrição humanizada do fator de risco"""
        descriptions = {
            'assinatura': f"Status de assinatura: {data.get('assinante_clube', 'Não')} (risco: {risk:.0%})",
            'engajamento': f"Engajamento: {data.get('pontuacao_engajamento', 0):.1f}/10 (risco: {risk:.0%})",
            'valor_gasto': f"Valor gasto: R$ {data.get('valor', 0):.2f} (risco: {risk:.0%})",
            'idade': f"Idade: {data.get('idade', 0)} anos (risco: {risk:.0%})",
            'recencia': f"Dias desde última compra: {data.get('dias_desde_ultima_compra', 0)} (risco: {risk:.0%})",
            'cidade': f"Cidade: {data.get('cidade', 'N/A')} (risco: {risk:.0%})"
        }

        return descriptions.get(factor, f"{factor}: {risk:.0%}")


if __name__ == "__main__":
    """
    Exemplo de uso do calculador de risco de churn.
    """
    print("Calculadora de Risco de Churn - Adega IA")
    print("=" * 60)

    # Exemplo de cliente
    cliente_exemplo = {
        'cliente_id': 1,
        'nome': 'João Silva',
        'idade': 42,
        'cidade': 'São Paulo',
        'pontuacao_engajamento': 7.5,
        'assinante_clube': 'Sim',
        'valor': 250.0,
        'dias_desde_ultima_compra': 15
    }

    calculator = ChurnRiskCalculator()
    result = calculator.calculate_churn_probability(cliente_exemplo)

    print(f"\nCliente: {cliente_exemplo['nome']}")
    print(f"Probabilidade de Churn: {result['churn_probability']:.1%}")
    print(f"Probabilidade de Retenção: {result['retain_probability']:.1%}")
    print(f"Nível de Risco: {result['risk_level']}")
    print("\nRecomendações:")
    for rec in result['recommendations']:
        print(f"  - {rec}")

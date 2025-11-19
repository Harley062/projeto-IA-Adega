"""
Glossário de traduções: termos técnicos para linguagem amigável
"""

# Traduções de termos técnicos para linguagem simples
GLOSSARIO = {
    # Termos principais
    "Churn": "Cancelamento",
    "Churn Rate": "Taxa de Cancelamento",
    "churn": "cancelamento",
    "churn_prediction": "previsão_de_cancelamento",
    "predict_churn": "prever_cancelamento",

    # Termos de Machine Learning
    "Machine Learning": "Inteligência Artificial",
    "Model": "Sistema Inteligente",
    "Pipeline": "Processamento",
    "Feature Engineering": "Preparação de Dados",
    "Feature": "Característica",
    "Training": "Treinamento",
    "Testing": "Teste",
    "Validation": "Validação",
    "Cross-validation": "Validação Cruzada",

    # Modelos
    "Gradient Boosting": "Modelo Avançado",
    "Random Forest": "Modelo de Decisões",
    "Logistic Regression": "Modelo de Regressão",
    "Decision Tree": "Árvore de Decisão",
    "K-Nearest Neighbors": "Modelo de Vizinhos",
    "Naive Bayes": "Modelo Bayesiano",
    "AdaBoost": "Modelo Adaptativo",

    # Métricas
    "Accuracy": "Precisão Geral",
    "Precision": "Taxa de Acerto",
    "Recall": "Taxa de Detecção",
    "F1-Score": "Nota Geral",
    "ROC-AUC": "Precisão do Sistema",
    "Average Precision": "Precisão Média",

    # Operações
    "Batch Prediction": "Análise em Lote",
    "Batch": "Lote",
    "Label Encoder": "Codificador",
    "Scaler": "Normalizador",
    "Transform": "Transformar",
    "Fit": "Treinar",
    "Predict": "Prever",

    # Termos de negócio (já bons, mas com versões simplificadas)
    "Lifetime Value": "Valor Total do Cliente",
    "Customer Lifetime Value": "Valor Vitalício do Cliente",
    "RFM Analysis": "Análise RFM (Recência, Frequência, Valor)",
    "Engagement Score": "Nível de Engajamento",
    "Ticket Médio": "Valor Médio de Compra",
}


# Tooltips explicativos para campos e conceitos
TOOLTIPS = {
    # Campos de formulário
    "engajamento": (
        "Mede o quanto o cliente interage com a adega.\n\n"
        "Como calcular:\n"
        "• Abre emails marketing: +2 pontos\n"
        "• Participa de eventos/degustações: +3 pontos\n"
        "• Responde pesquisas: +2 pontos\n"
        "• Compra regularmente: +3 pontos\n\n"
        "Classificação:\n"
        "• 1-3: Baixo engajamento\n"
        "• 4-7: Médio engajamento\n"
        "• 8-10: Alto engajamento"
    ),

    "recencia": (
        "Há quanto tempo o cliente fez a última compra.\n\n"
        "Quanto menor, melhor:\n"
        "• 0-30 dias: Cliente muito ativo\n"
        "• 31-90 dias: Cliente ativo\n"
        "• 91-180 dias: Cliente em risco\n"
        "• 181+ dias: Cliente inativo"
    ),

    "frequencia": (
        "Quantas vezes o cliente comprou no último ano.\n\n"
        "Interpretação:\n"
        "• 0-2 compras: Cliente ocasional\n"
        "• 3-6 compras: Cliente regular\n"
        "• 7-12 compras: Cliente frequente\n"
        "• 13+ compras: Cliente VIP"
    ),

    "valor_total": (
        "Quanto o cliente gastou no total (em reais).\n\n"
        "Indica o valor que o cliente representa para o negócio."
    ),

    "ticket_medio": (
        "Valor médio que o cliente gasta por compra.\n\n"
        "Calculado como: Valor Total ÷ Número de Compras"
    ),

    "assinante_clube": (
        "Se o cliente é membro do clube de vinhos.\n\n"
        "Membros do clube:\n"
        "• Recebem vinhos mensalmente\n"
        "• Têm descontos especiais\n"
        "• Geralmente são clientes mais fiéis"
    ),

    # Conceitos do sistema
    "rfm": (
        "RFM é uma técnica que classifica clientes em 3 fatores:\n\n"
        "• Recência (R): Comprou recentemente?\n"
        "• Frequência (F): Compra sempre?\n"
        "• Monetário (M): Gasta muito?\n\n"
        "Cada fator recebe uma nota de 1 a 5.\n"
        "Clientes com notas altas (555) são os melhores!"
    ),

    "risco_cancelamento": (
        "Probabilidade do cliente cancelar sua assinatura.\n\n"
        "Níveis de risco:\n"
        "• 🟢 Baixo (0-30%): Cliente satisfeito\n"
        "• 🟡 Médio (31-60%): Monitorar de perto\n"
        "• 🔴 Alto (61-100%): Ação urgente necessária"
    ),

    "confiabilidade_sistema": (
        "Quão confiável são as previsões do sistema.\n\n"
        "Baseado em testes com dados históricos:\n"
        "• 85-100%: Excelente\n"
        "• 70-84%: Bom\n"
        "• 50-69%: Regular\n"
        "• Abaixo de 50%: Não confiável"
    ),

    "matriz_confusao": (
        "Mostra quantas previsões o sistema acertou e errou.\n\n"
        "Quadrantes:\n"
        "• Verde (Acertos): Sistema previu corretamente\n"
        "• Vermelho (Erros): Sistema errou a previsão\n\n"
        "Quanto mais verde, melhor!"
    ),

    "recomendacoes": (
        "Ações sugeridas com base nos dados e previsões.\n\n"
        "São específicas e práticas, como:\n"
        "• Enviar oferta especial para cliente X\n"
        "• Ligar para clientes em risco\n"
        "• Repor produto Y no estoque"
    ),
}


# Descrições detalhadas para a página de Ajuda
DESCRICOES_DETALHADAS = {
    "dashboard": {
        "titulo": "📊 Dashboard Principal",
        "o_que_e": "Visão geral dos números mais importantes do negócio",
        "para_que_serve": "Ver rapidamente como está a saúde da adega: vendas, clientes ativos, produtos mais vendidos",
        "como_usar": "Basta abrir o sistema. O dashboard é a primeira tela que aparece.",
    },

    "graficos": {
        "titulo": "📈 Gráficos e Tendências",
        "o_que_e": "Visualizações dos dados de vendas, clientes e produtos",
        "para_que_serve": "Identificar padrões, tendências e oportunidades de negócio",
        "como_usar": "Use os filtros na lateral para explorar diferentes períodos, cidades ou tipos de clientes.",
    },

    "previsoes": {
        "titulo": "🔮 Previsões Inteligentes",
        "o_que_e": "Sistema que prevê quais clientes têm risco de cancelar a assinatura",
        "para_que_serve": "Agir antes que clientes valiosos cancelem, oferecendo atenção personalizada",
        "como_usar": (
            "1. Escolha um cliente específico ou carregue uma lista\n"
            "2. Sistema analisa o histórico e comportamento\n"
            "3. Veja o risco de cancelamento e ações recomendadas"
        ),
    },

    "recomendacoes": {
        "titulo": "💡 Recomendações",
        "o_que_e": "Sugestões práticas de ações para melhorar o negócio",
        "para_que_serve": "Transformar dados em ações concretas que aumentam vendas e fidelizam clientes",
        "como_usar": "Leia as recomendações e marque as que você vai implementar na checklist semanal.",
    },

    "atualizar_dados": {
        "titulo": "⚙️ Atualizar Dados",
        "o_que_e": "Processa os dados mais recentes para atualizar todas as análises",
        "para_que_serve": "Manter o sistema atualizado com as vendas e clientes mais recentes",
        "como_usar": (
            "1. Coloque os arquivos CSV atualizados na pasta 'data/'\n"
            "2. Clique em 'Processar Dados'\n"
            "3. Aguarde 2-5 minutos\n"
            "4. Pronto! Sistema atualizado"
        ),
        "quando_fazer": "Semanalmente ou quando houver mudanças significativas nos dados",
    },
}


# Perguntas Frequentes (FAQ)
FAQ = [
    {
        "pergunta": "O que significa 'risco de cancelamento'?",
        "resposta": (
            "É a probabilidade de um cliente cancelar a assinatura do clube de vinhos. "
            "O sistema analisa o comportamento do cliente (frequência de compras, valor gasto, engajamento) "
            "e compara com padrões de clientes que cancelaram no passado. "
            "Quanto maior o risco, mais urgente é agir para manter o cliente."
        ),
    },
    {
        "pergunta": "Como o sistema faz as previsões?",
        "resposta": (
            "O sistema usa Inteligência Artificial (Machine Learning) para aprender com dados históricos. "
            "Ele analisa milhares de exemplos de clientes que cancelaram e que continuaram, "
            "identifica padrões comuns e usa esses padrões para prever comportamentos futuros. "
            "É como ter um especialista que analisou milhares de casos e pode dar uma opinião muito rápido!"
        ),
    },
    {
        "pergunta": "Com que frequência devo atualizar os dados?",
        "resposta": (
            "Recomendamos atualizar semanalmente ou sempre que houver mudanças significativas "
            "(muitas vendas novas, novos produtos, campanhas especiais). "
            "A atualização leva apenas 2-5 minutos e garante que as previsões sejam precisas."
        ),
    },
    {
        "pergunta": "O que fazer quando o sistema identifica um cliente em risco?",
        "resposta": (
            "Aja rápido! Sugestões:\n"
            "1. Entre em contato pessoal (telefone é melhor que email)\n"
            "2. Ofereça um desconto especial ou brinde\n"
            "3. Convide para degustação exclusiva\n"
            "4. Pergunte se há algo que possamos melhorar\n"
            "5. Mostre que o cliente é importante para você"
        ),
    },
    {
        "pergunta": "Preciso saber programação para usar o sistema?",
        "resposta": (
            "Não! O sistema foi desenhado para ser usado por qualquer pessoa. "
            "Basta clicar nos botões, preencher formulários simples e ler os resultados. "
            "Todas as partes técnicas ficam escondidas 'nos bastidores'."
        ),
    },
    {
        "pergunta": "O que é a análise RFM?",
        "resposta": (
            "RFM significa Recência, Frequência e Monetário. É uma técnica clássica de segmentação:\n\n"
            "• Recência: Há quanto tempo o cliente comprou (quanto menor, melhor)\n"
            "• Frequência: Quantas vezes compra (quanto mais, melhor)\n"
            "• Monetário: Quanto gasta (quanto mais, melhor)\n\n"
            "Clientes com RFM alto (555) são seus melhores clientes!"
        ),
    },
    {
        "pergunta": "Por que alguns gráficos não aparecem?",
        "resposta": (
            "Isso acontece quando você ainda não processou os dados. "
            "Vá em '⚙️ Atualizar Dados' no menu e clique em 'Processar Dados'. "
            "Aguarde alguns minutos e volte para o dashboard. Os gráficos aparecerão!"
        ),
    },
    {
        "pergunta": "Posso confiar nas previsões do sistema?",
        "resposta": (
            "As previsões são muito boas (geralmente acima de 85% de precisão), mas não são perfeitas. "
            "Use-as como uma ferramenta de apoio à decisão, não como verdade absoluta. "
            "O sistema identifica padrões nos dados, mas o julgamento humano é sempre importante!"
        ),
    },
]


def traduzir(termo_tecnico: str) -> str:
    """
    Retorna versão amigável do termo técnico

    Args:
        termo_tecnico: Termo técnico original

    Returns:
        Versão em linguagem simples, ou o termo original se não houver tradução
    """
    return GLOSSARIO.get(termo_tecnico, termo_tecnico)


def tooltip(chave: str) -> str:
    """
    Retorna texto de ajuda para o campo/conceito

    Args:
        chave: Identificador do campo/conceito

    Returns:
        Texto explicativo, ou string vazia se não houver tooltip
    """
    return TOOLTIPS.get(chave, "")


def descricao(secao: str) -> dict:
    """
    Retorna descrição detalhada de uma seção do sistema

    Args:
        secao: Identificador da seção

    Returns:
        Dicionário com informações detalhadas
    """
    return DESCRICOES_DETALHADAS.get(secao, {})


def buscar_no_glossario(termo_busca: str) -> list:
    """
    Busca termos no glossário (útil para página de ajuda)

    Args:
        termo_busca: Termo para buscar

    Returns:
        Lista de tuplas (termo_tecnico, traducao) que correspondem à busca
    """
    termo_busca = termo_busca.lower()
    resultados = []

    for tecnico, simples in GLOSSARIO.items():
        if termo_busca in tecnico.lower() or termo_busca in simples.lower():
            resultados.append((tecnico, simples))

    return resultados

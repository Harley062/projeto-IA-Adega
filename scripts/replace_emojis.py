"""Script para substituir emojis por ícones no pages_prediction.py"""

# Mapeamento de substituições
replacements = [
    ('st.subheader("📊 Predição em Lote")', 'st.markdown(\'<h3><i class="fas fa-chart-bar"></i> Predição em Lote</h3>\', unsafe_allow_html=True)'),
    ('st.success(f"✅ Arquivo carregado: {len(df)} clientes")', 'st.markdown(f\'<p style="color: #28a745;"><i class="fas fa-check-circle"></i> Arquivo carregado: {len(df)} clientes</p>\', unsafe_allow_html=True)'),
    ('with st.expander("👁️ Preview dos Dados"):', 'with st.expander("Preview dos Dados"):'),
    ('if st.button("🚀 Executar Predições", type="primary"):', 'if st.button("Executar Predições", type="primary"):'),
    ('st.markdown("### 📊 Resultados")', 'st.markdown(\'### <i class="fas fa-chart-bar"></i> Resultados\', unsafe_allow_html=True)'),
    ('st.metric("🔴 Alto Risco",', 'st.metric("Alto Risco",'),
    ('st.metric("🟡 Médio Risco",', 'st.metric("Médio Risco",'),
    ('st.metric("🟢 Baixo Risco",', 'st.metric("Baixo Risco",'),
    ('st.markdown("### 📋 Detalhes por Cliente")', 'st.markdown(\'### <i class="fas fa-table"></i> Detalhes por Cliente\', unsafe_allow_html=True)'),
    ('label="📥 Download Resultados (CSV)",', 'label="Download Resultados (CSV)",'),
    ('st.subheader("📈 Predição de Vendas")', 'st.markdown(\'<h3><i class="fas fa-chart-line"></i> Predição de Vendas</h3>\', unsafe_allow_html=True)'),
    ('if st.button("🔮 Prever Próxima Compra", type="primary"):', 'if st.button("Prever Próxima Compra", type="primary"):'),
    ('st.error(f"❌ {result[\'error\']}")', 'st.markdown(f\'<p style="color: #dc3545;"><i class="fas fa-times-circle"></i> {result["error"]}</p>\', unsafe_allow_html=True)'),
    ('st.success("✅ Predição concluída!")', 'st.markdown(\'<p style="color: #28a745;"><i class="fas fa-check-circle"></i> Predição concluída!</p>\', unsafe_allow_html=True)'),
    ('"📅 Próxima Compra",', '"Próxima Compra",'),
    ('"💰 Valor Esperado",', '"Valor Esperado",'),
    ('"🏆 Lifetime Value",', '"Lifetime Value",'),
    ('st.markdown("### 📊 Informações Adicionais")', 'st.markdown(\'### <i class="fas fa-info-circle"></i> Informações Adicionais\', unsafe_allow_html=True)'),
    ('if st.button("📊 Prever Receita", type="primary", key="revenue_predict"):', 'if st.button("Prever Receita", type="primary", key="revenue_predict"):'),
    ('st.success("✅ Projeção concluída!")', 'st.markdown(\'<p style="color: #28a745;"><i class="fas fa-check-circle"></i> Projeção concluída!</p>\', unsafe_allow_html=True)'),
    ('"💰 Receita Prevista",', '"Receita Prevista",'),
    ('"📊 Média Mensal",', '"Média Mensal",'),
    ('"📈 Taxa de Crescimento",', '"Taxa de Crescimento",'),
    ('st.subheader("🍷 Recomendação de Produtos")', 'st.markdown(\'<h3><i class="fas fa-wine-bottle"></i> Recomendação de Produtos</h3>\', unsafe_allow_html=True)'),
    ('if st.button("🎯 Gerar Recomendações", type="primary"):', 'if st.button("Gerar Recomendações", type="primary"):'),
    ('st.success(f"✅ {len(recommendations)} produtos recomendados!")', 'st.markdown(f\'<p style="color: #28a745;"><i class="fas fa-check-circle"></i> {len(recommendations)} produtos recomendados!</p>\', unsafe_allow_html=True)'),
    ('st.markdown("### 🏆 Top Recomendações")', 'st.markdown(\'### <i class="fas fa-trophy"></i> Top Recomendações\', unsafe_allow_html=True)'),
]

# Ler arquivo
with open('pages_prediction.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Aplicar substituições
for old, new in replacements:
    content = content.replace(old, new)

# Salvar arquivo
with open('pages_prediction.py', 'w', encoding='utf-8') as f:
    f.write(content)

print(f"✓ {len(replacements)} substituições realizadas com sucesso!")

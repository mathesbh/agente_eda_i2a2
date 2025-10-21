import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

def generate_plot(user_query, df):
    """Gera gráficos relevantes baseados na query do usuário"""
    
    # Identificar coluna NCM
    ncm_cols = [col for col in df.columns if 'ncm' in col.lower()]
    
    if "distribuição" in user_query.lower() or "gráfico" in user_query.lower():
        if ncm_cols:
            st.write("**📊 Gráfico: Distribuição de NCMs**")
            fig, ax = plt.subplots(figsize=(10, 6))
            ncm_counts = df[ncm_cols[0]].value_counts().head(10)
            ncm_counts.plot(kind='bar', ax=ax, color='steelblue')
            ax.set_title('Top 10 NCMs Mais Frequentes')
            ax.set_xlabel('NCM')
            ax.set_ylabel('Quantidade')
            plt.xticks(rotation=45, ha='right')
            plt.tight_layout()
            st.pyplot(fig)
    
    elif "valor" in user_query.lower() and ncm_cols:
        valor_cols = [col for col in df.columns if 'valor' in col.lower() or 'total' in col.lower()]
        if valor_cols:
            st.write("**💰 Gráfico: Valores por NCM**")
            fig, ax = plt.subplots(figsize=(10, 6))
            # Agrupa por NCM e soma valores
            grouped = df.groupby(ncm_cols[0])[valor_cols[0]].sum().sort_values(ascending=False).head(10)
            grouped.plot(kind='bar', ax=ax, color='green')
            ax.set_title('Top 10 NCMs por Valor Total')
            ax.set_xlabel('NCM')
            ax.set_ylabel('Valor Total (R$)')
            plt.xticks(rotation=45, ha='right')
            plt.tight_layout()
            st.pyplot(fig)

def auto_validate_ncm(df):
    """
    Função auxiliar para validação básica de NCM
    (O agente fará a validação principal, esta é apenas um helper)
    """
    ncm_cols = [col for col in df.columns if 'ncm' in col.lower()]
    
    if not ncm_cols:
        return None
    
    ncm_col = ncm_cols[0]
    issues = []
    
    for idx, row in df.iterrows():
        ncm = str(row[ncm_col])
        
        # Remove pontos e espaços
        ncm_clean = ncm.replace('.', '').replace(' ', '').replace('-', '')
        
        # Verifica formato (deve ter 8 dígitos)
        if not ncm_clean.isdigit() or len(ncm_clean) != 8:
            issues.append({
                'linha': idx + 1,
                'ncm': ncm,
                'problema': 'Formato inválido (deve ter 8 dígitos)',
                'severidade': 'CRÍTICA'
            })
    
    return issues

def display_validation_results(response):
    """Exibe resultados da validação de forma estruturada"""
    
    st.markdown("---")
    st.subheader("📋 Resultado da Validação de Conformidade")
    
    # Tenta identificar severidades na resposta
    if "CRÍTICA" in response or "ALTA" in response:
        st.error("⚠️ Foram encontradas irregularidades que precisam de atenção imediata!")
    elif "MÉDIA" in response or "BAIXA" in response:
        st.warning("⚡ Foram encontradas algumas inconsistências menores.")
    else:
        st.success("✅ Nenhuma irregularidade crítica encontrada!")
    
    # Exibe a resposta completa
    st.markdown(response)
    
    # Cria seção de ações recomendadas
    with st.expander("🎯 Ações Recomendadas"):
        st.markdown("""
        Com base nos problemas identificados:
        
        1. **Irregularidades CRÍTICAS**: Corrija imediatamente antes de emitir novas notas
        2. **Irregularidades ALTAS**: Planeje correção em até 7 dias
        3. **Irregularidades MÉDIAS**: Revise e ajuste no próximo ciclo
        4. **Irregularidades BAIXAS**: Monitore e corrija quando oportuno
        
        💡 **Dica**: Use o chat abaixo para fazer perguntas específicas sobre cada problema.
        """)
    
    st.markdown("---")

def create_ncm_summary_chart(validation_data):
    """Cria gráfico resumo de validação (se houver dados estruturados)"""
    
    # Esta função pode ser expandida se você quiser processar
    # a resposta do agente e criar visualizações automáticas
    pass
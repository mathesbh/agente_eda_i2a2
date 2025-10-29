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
            # Normaliza NCMs para agrupamento
            ncm_normalized = df[ncm_cols[0]].astype(str).str.replace('.', '').str.replace('-', '')
            ncm_counts = ncm_normalized.value_counts().head(10)
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
            # Normaliza NCMs
            df_temp = df.copy()
            df_temp['NCM_norm'] = df_temp[ncm_cols[0]].astype(str).str.replace('.', '').str.replace('-', '')
            # Agrupa por NCM e soma valores
            grouped = df_temp.groupby('NCM_norm')[valor_cols[0]].sum().sort_values(ascending=False).head(10)
            grouped.plot(kind='bar', ax=ax, color='green')
            ax.set_title('Top 10 NCMs por Valor Total')
            ax.set_xlabel('NCM')
            ax.set_ylabel('Valor Total (R$)')
            plt.xticks(rotation=45, ha='right')
            plt.tight_layout()
            st.pyplot(fig)

def quick_ncm_validation(df):
    """
    Validação rápida e manual de NCM quando o agente falhar
    """
    st.subheader("🔧 Validação Manual Rápida")
    
    # Identifica colunas
    ncm_cols = [col for col in df.columns if 'ncm' in col.lower()]
    desc_cols = [col for col in df.columns if any(x in col.lower() for x in ['descri', 'produto', 'desc'])]
    
    if not ncm_cols:
        st.error("❌ Coluna NCM não encontrada no arquivo")
        st.info(f"Colunas disponíveis: {df.columns.tolist()}")
        return
    
    ncm_col = ncm_cols[0]
    desc_col = desc_cols[0] if desc_cols else None
    
    st.success(f"✅ Coluna NCM encontrada: **{ncm_col}**")
    if desc_col:
        st.success(f"✅ Coluna Descrição encontrada: **{desc_col}**")
    
    # Normaliza NCMs
    df_temp = df.copy()
    df_temp['NCM_normalizado'] = df_temp[ncm_col].astype(str).str.replace('.', '').str.replace('-', '').str.strip()
    
    # Estatísticas básicas
    col1, col2, col3 = st.columns(3)
    with col1:
        total_registros = len(df_temp)
        st.metric("Total de Produtos", total_registros)
    with col2:
        ncms_unicos = df_temp['NCM_normalizado'].nunique()
        st.metric("NCMs Únicos", ncms_unicos)
    with col3:
        ncms_validos = df_temp['NCM_normalizado'].str.len().eq(8).sum()
        perc_valido = (ncms_validos / total_registros * 100)
        st.metric("NCMs com 8 dígitos", f"{perc_valido:.1f}%")
    
    # Lista NCMs únicos
    st.write("### 📋 NCMs Encontrados")
    
    if desc_col:
        ncm_summary = df_temp.groupby('NCM_normalizado').agg({
            desc_col: 'first',
            ncm_col: 'count'
        }).rename(columns={ncm_col: 'Quantidade'})
        ncm_summary = ncm_summary.reset_index()
        ncm_summary.columns = ['NCM', 'Exemplo de Produto', 'Quantidade']
    else:
        ncm_summary = df_temp['NCM_normalizado'].value_counts().reset_index()
        ncm_summary.columns = ['NCM', 'Quantidade']
    
    st.dataframe(ncm_summary, use_container_width=True)
    
    # NCMs comuns do setor pet
    st.write("### ✅ NCMs Comuns no Setor Pet")
    ncms_corretos_pet = {
        '23099010': 'Rações para cães/gatos',
        '23099030': 'Rações para equinos',
        '23099090': 'Outras preparações para animais',
        '30049099': 'Medicamentos veterinários',
        '30023000': 'Vacinas veterinárias',
        '90183100': 'Seringas',
        '42050000': 'Coleiras e acessórios',
        '25051000': 'Areia sanitária',
        '38089490': 'Antipulgas e antiparasitários',
        '33051000': 'Shampoos',
        '94049000': 'Camas e almofadas',
    }
    
    ncms_encontrados = df_temp['NCM_normalizado'].unique()
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**✅ NCMs Conhecidos Encontrados:**")
        encontrados_corretos = [ncm for ncm in ncms_encontrados if ncm in ncms_corretos_pet]
        if encontrados_corretos:
            for ncm in encontrados_corretos:
                st.write(f"- `{ncm}` - {ncms_corretos_pet[ncm]}")
        else:
            st.write("_Nenhum NCM padrão encontrado_")
    
    with col2:
        st.write("**⚠️ NCMs que Precisam Validação:**")
        encontrados_desconhecidos = [ncm for ncm in ncms_encontrados if ncm not in ncms_corretos_pet]
        if encontrados_desconhecidos:
            for ncm in encontrados_desconhecidos[:10]:  # Limita a 10
                count = (df_temp['NCM_normalizado'] == ncm).sum()
                st.write(f"- `{ncm}` ({count} produtos)")
        else:
            st.write("_Todos os NCMs são conhecidos!_")

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
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns

def generate_plot(user_query, df):
    if "histograma" in user_query.lower() or "distribuição" in user_query.lower():
        st.write("**Gráfico Gerado (Exemplo: Histograma):**")
        fig, ax = plt.subplots()
        sns.histplot(df.select_dtypes(include=['number']).iloc[:, 0], ax=ax)
        st.pyplot(fig)
    elif "dispersão" in user_query.lower() or "correlação" in user_query.lower():
        st.write("**Gráfico Gerado (Exemplo: Gráfico de Dispersão):**")
        num_cols = df.select_dtypes(include=['number']).columns
        if len(num_cols) >= 2:
            fig, ax = plt.subplots()
            sns.scatterplot(x=df[num_cols[0]], y=df[num_cols[1]], ax=ax)
            st.pyplot(fig)

def check_for_conclusions(response, agent):
    if "conclusão" not in response.lower():
        conclusion_query = "Quais conclusões você tira dos dados analisados?"
        conclusion = agent.run(conclusion_query)
        st.write("**Conclusões Adicionais:**")
        st.write(conclusion)
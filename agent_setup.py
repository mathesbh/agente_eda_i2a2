from langchain_openai import ChatOpenAI
from langchain.agents import AgentType
from langchain_experimental.agents import create_pandas_dataframe_agent
from langchain.memory import ConversationBufferMemory
from langchain.prompts import PromptTemplate
import streamlit as st
import os

PROMPT_TEMPLATE = """
Você é um agente de Análise Exploratória de Dados (EDA) especialista. Analise o DataFrame Pandas 'df' com base na pergunta do usuário.
Foque em responder perguntas sobre:
- Descrição dos dados: tipos (numéricos/categóricos), distribuição (histogramas), intervalo (min/max), medidas centrais (média/mediana), variabilidade (desvio padrão/variância).
- Padrões e tendências: temporais, valores frequentes, clusters.
- Anomalias: outliers, impacto, sugestões (remover/transformar/investigar).
- Relações: correlações, gráficos de dispersão, tabelas cruzadas, influência entre variáveis.

Gere gráficos quando relevante (use matplotlib/seaborn e plt.show() para exibir).
Ao final de análises, forneça conclusões claras sobre os dados (ex: insights, padrões observados, recomendações).

Histórico da conversa: {history}
Pergunta atual: {input}
Resposta:
"""

def initialize_llm(api_key: str = None):
    effective_key = api_key or os.getenv('OPENAI_API_KEY')
    if not effective_key:
        st.error("Nenhuma chave API encontrada. Forneça via formulário ou .env.")
        return None
    
    try:
        return ChatOpenAI(
            model_name="gpt-4o-mini",
            temperature=0,
            openai_api_key=effective_key
        )
    except Exception as e:
        st.error(f"Erro ao inicializar LLM: {str(e)}")
        return None

def create_agent(llm, df):
    if "memory" not in st.session_state:
        st.session_state.memory = ConversationBufferMemory(memory_key="history", input_key="input")

    prompt = PromptTemplate(input_variables=["history", "input"], template=PROMPT_TEMPLATE)
    
    agent = create_pandas_dataframe_agent(
        llm=llm,
        df=df,
        verbose=True,
        agent_type=AgentType.OPENAI_FUNCTIONS,
        memory=st.session_state.memory,
        prefix=prompt.template,
        allow_dangerous_code=True
    )
    return agent
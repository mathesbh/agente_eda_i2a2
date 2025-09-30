import streamlit as st
import pandas as pd
import zipfile
import chardet
import io
from agent_setup import initialize_llm, create_agent
from utils import generate_plot, check_for_conclusions
from dotenv import load_dotenv

load_dotenv()

def main():
    st.title("Agente de EDA Inteligente com LangChain + GPT-4 Mini")

    uploaded_file = st.file_uploader("Faça upload do arquivo zip com o CSV", type="zip")

    if uploaded_file is not None:
        df = load_data(uploaded_file)
        if df is None:
            return
        
        display_data_preview(df)

        if "openai_api_key" not in st.session_state:
            st.session_state.openai_api_key = ""

        st.subheader("Insira sua chave OpenAI API")
        api_key_input = st.text_input("Chave OpenAI API:", type="password", value=st.session_state.openai_api_key)

        if api_key_input:
            st.session_state.openai_api_key = api_key_input
            st.success("Chave API configurada com sucesso!")

            llm = initialize_llm(st.session_state.openai_api_key)

            if llm:
                agent = create_agent(llm, df)

                st.subheader("Faça perguntas sobre os dados")
                user_query = st.text_input("Sua pergunta:")

                if st.button("Enviar") and user_query:
                    with st.spinner("Analisando..."):
                        try:
                            response = agent.run(user_query)
                            display_response(response)

                            generate_plot(user_query, df)

                            check_for_conclusions(response, agent)
                        except Exception as e:
                            st.error(f"Erro ao processar: {str(e)}")
            else:
                st.error("Chave API inválida ou não fornecida. Por favor, insira uma chave válida.")
        else:
            st.warning("Por favor, insira sua chave OpenAI API para continuar.")
    else:
        st.info("Por favor, faça upload de um arquivo zip contendo o CSV.")


def load_data(uploaded_file):
    try:
        with zipfile.ZipFile(uploaded_file, 'r') as z:
            nomes = z.namelist()
            if not nomes:
                raise ValueError("ZIP vazio.")
            with z.open(nomes[0]) as f:
                amostra = f.read(4096)
                enc_detectado = chardet.detect(amostra)['encoding'] or 'utf-8'
                f.seek(0)
                conteudo = f.read().decode(enc_detectado, errors='replace')
                buffer = io.StringIO(conteudo)
                df = pd.read_csv(buffer, sep=None, engine='python')

        st.success(f"Arquivo carregado com sucesso usando codificação '{enc_detectado}'!")
        return df

    except UnicodeDecodeError:
        st.error("Não foi possível descompactar e decodificar o arquivo. Verifique o arquivo enviado.")
        return None

def display_data_preview(df):
    st.write("Pré-visualização dos dados:")
    st.dataframe(df.head())

def display_response(response):
    st.write("**Resposta do Agente:**")
    st.write(response)

if __name__ == "__main__":
    main()
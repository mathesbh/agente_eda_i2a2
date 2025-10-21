import streamlit as st
import pandas as pd
import zipfile
import chardet
import io
from agent_setup_ncm import initialize_llm, create_agent
from utils_ncm import generate_plot, auto_validate_ncm, display_validation_results
from dotenv import load_dotenv

load_dotenv()

def main():
    st.title("🐾 Agente de Conformidade Fiscal NCM - Setor Pet")
    st.markdown("**Validação automática de NCM em notas fiscais para clínicas veterinárias e pet shops**")

    uploaded_file = st.file_uploader("Faça upload do arquivo zip com o CSV de notas fiscais", type="zip")

    if uploaded_file is not None:
        df = load_data(uploaded_file)
        if df is None:
            return
        
        display_data_preview(df)

        if "openai_api_key" not in st.session_state:
            st.session_state.openai_api_key = ""

        st.subheader("🔑 Insira sua chave OpenAI API")
        api_key_input = st.text_input("Chave OpenAI API:", type="password", value=st.session_state.openai_api_key)

        if api_key_input:
            st.session_state.openai_api_key = api_key_input
            st.success("✅ Chave API configurada com sucesso!")

            llm = initialize_llm(st.session_state.openai_api_key)

            if llm:
                agent = create_agent(llm, df)

                # VALIDAÇÃO AUTOMÁTICA AO CARREGAR
                st.subheader("🔍 Validação Automática de Conformidade")
                if st.button("🚀 Iniciar Validação Automática de NCM"):
                    with st.spinner("Validando NCMs das notas fiscais..."):
                        try:
                            validation_query = """
                            Faça uma validação de conformidade de NCM das notas fiscais neste DataFrame:
                            
                            PASSO 1 - Exploração básica:
                            - Mostre df.shape para ver quantos registros existem
                            - Mostre df.columns para identificar as colunas
                            - Identifique qual coluna contém NCM
                            - Mostre df['NCM'].value_counts() para ver os NCMs mais comuns
                            
                            PASSO 2 - Análise dos NCMs:
                            Para cada NCM único encontrado, verifique:
                            - Se tem 8 dígitos (removendo pontos)
                            - Se é um NCM válido na tabela TIPI
                            - Se é apropriado para produtos do setor pet
                            
                            PASSO 3 - Identifique problemas:
                            Liste os NCMs com problemas e explique:
                            - Qual NCM está incorreto
                            - Em quais produtos aparece
                            - Por que está incorreto
                            - Qual deveria ser o NCM correto
                            - Nível de severidade
                            
                            PASSO 4 - Resumo:
                            - Percentual aproximado de conformidade
                            - Principais problemas encontrados
                            - Ações recomendadas
                            
                            IMPORTANTE: Use apenas operações pandas simples. Não crie funções complexas.
                            """
                            
                            response = agent.run(validation_query)
                            display_validation_results(response)
                            
                        except Exception as e:
                            st.error(f"❌ Erro ao processar validação: {str(e)}")
                            st.info("💡 Tente fazer perguntas mais simples no chat abaixo.")

                # CHAT INTERATIVO
                st.subheader("💬 Faça perguntas sobre os dados")
                st.markdown("*Exemplos: 'Quais NCMs estão incorretos?', 'Mostre produtos com problemas fiscais', 'Análise detalhada da nota X'*")
                
                user_query = st.text_input("Sua pergunta:")

                if st.button("Enviar") and user_query:
                    with st.spinner("Analisando..."):
                        try:
                            response = agent.run(user_query)
                            display_response(response)

                            generate_plot(user_query, df)

                        except Exception as e:
                            st.error(f"Erro ao processar: {str(e)}")
            else:
                st.error("❌ Chave API inválida ou não fornecida. Por favor, insira uma chave válida.")
        else:
            st.warning("⚠️ Por favor, insira sua chave OpenAI API para continuar.")
    else:
        st.info("📁 Por favor, faça upload de um arquivo zip contendo o CSV de notas fiscais.")


def load_data(uploaded_file):
    try:
        with zipfile.ZipFile(uploaded_file, 'r') as z:
            nomes = z.namelist()
            if not nomes:
                raise ValueError("ZIP vazio.")
            
            # Filtra apenas arquivos CSV
            csv_files = [f for f in nomes if f.lower().endswith('.csv')]
            if not csv_files:
                st.error("❌ Nenhum arquivo CSV encontrado no ZIP.")
                return None
            
            arquivo_csv = csv_files[0]
            st.info(f"📄 Lendo arquivo: {arquivo_csv}")
            
            with z.open(arquivo_csv) as f:
                # Detecta encoding
                amostra = f.read(10000)
                resultado_deteccao = chardet.detect(amostra)
                enc_detectado = resultado_deteccao['encoding'] or 'utf-8'
                confianca = resultado_deteccao['confidence']
                
                st.info(f"🔍 Encoding detectado: {enc_detectado} (confiança: {confianca:.1%})")
                
                # Lê o arquivo completo
                f.seek(0)
                conteudo = f.read().decode(enc_detectado, errors='replace')
                
                # Tenta diferentes delimitadores
                delimitadores = [',', ';', '\t', '|']
                df = None
                
                for delim in delimitadores:
                    try:
                        buffer = io.StringIO(conteudo)
                        df_temp = pd.read_csv(buffer, sep=delim, encoding=enc_detectado, on_bad_lines='skip')
                        
                        # Verifica se conseguiu ler corretamente (mais de 1 coluna)
                        if len(df_temp.columns) > 1:
                            df = df_temp
                            st.success(f"✅ Arquivo carregado com delimitador '{delim}' e encoding '{enc_detectado}'!")
                            break
                    except Exception:
                        continue
                
                if df is None:
                    st.error("❌ Não foi possível determinar o formato do CSV. Tente usar um delimitador padrão (vírgula ou ponto-e-vírgula).")
                    return None
                
                return df

    except zipfile.BadZipFile:
        st.error("❌ Arquivo ZIP corrompido ou inválido.")
        return None
    except UnicodeDecodeError as e:
        st.error(f"❌ Erro de decodificação: {str(e)}")
        st.info("💡 Tente salvar o CSV com encoding UTF-8 antes de compactar.")
        return None
    except Exception as e:
        st.error(f"❌ Erro ao processar arquivo: {str(e)}")
        return None

def display_data_preview(df):
    st.write("📊 **Pré-visualização dos dados:**")
    st.dataframe(df.head())
    
    # Informações adicionais sobre o arquivo
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total de Registros", len(df))
    with col2:
        st.metric("Colunas", len(df.columns))
    with col3:
        # Tentar identificar coluna NCM
        ncm_cols = [col for col in df.columns if 'ncm' in col.lower()]
        if ncm_cols:
            st.metric("Coluna NCM Detectada", ncm_cols[0])
        else:
            st.metric("Coluna NCM", "Não detectada")

def display_response(response):
    st.write("**💡 Resposta do Agente:**")
    st.write(response)

if __name__ == "__main__":
    main()
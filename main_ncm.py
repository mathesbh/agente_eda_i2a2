import streamlit as st
import pandas as pd
import zipfile
import chardet
import io
import os
from agent_setup_ncm import initialize_llm, create_agent
from utils_ncm import generate_plot, display_validation_results, quick_ncm_validation
from email_service import email_service
from pdf_generator import pdf_generator
from dotenv import load_dotenv

load_dotenv()

def main():
    st.title("🐾 Agente de Conformidade Fiscal NCM - Setor Pet")
    st.markdown("**Validação automática de NCM em notas fiscais para clínicas veterinárias e pet shops**")

    # Configuração de E-mail (sidebar)
    with st.sidebar:
        st.header("📧 Configurações de E-mail")
        email_destinatario = st.text_input(
            "E-mail para receber relatório:",
            placeholder="seu@email.com",
            help="Digite o e-mail onde deseja receber o relatório"
        )
        
        enviar_email_auto = st.checkbox(
            "Enviar e-mail automaticamente após validação",
            value=False,
            help="Se marcado, envia e-mail assim que a validação terminar"
        )
        
        st.divider()
        st.caption("💡 O relatório PDF será gerado automaticamente")

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

                # VALIDAÇÃO MANUAL RÁPIDA (backup se o agente falhar)
                with st.expander("🔧 Validação Manual Rápida (não usa IA)"):
                    st.info("Use esta opção se a validação automática com IA apresentar problemas")
                    if st.button("Executar Validação Manual"):
                        quick_ncm_validation(df)

                # VALIDAÇÃO AUTOMÁTICA COM IA
                st.subheader("🔍 Validação Automática de Conformidade com IA")
                if st.button("🚀 Iniciar Validação Automática de NCM"):
                    with st.spinner("Validando NCMs das notas fiscais..."):
                        try:
                            validation_query = """
                            Faça validação de conformidade de NCM seguindo EXATAMENTE estes passos:
                            
                            PASSO 1 - Identificar colunas (CRÍTICO):
                            Execute: df.columns.tolist()
                            Mostre TODAS as colunas encontradas.
                            
                            PASSO 2 - Encontrar colunas NCM e Descrição:
                            Encontre a coluna que contém NCM (pode ser 'NCM', 'CODIGO_NCM', etc.)
                            Encontre a coluna com descrição do produto (pode ser 'DESCRICAO_PRODUTO', 'PRODUTO', etc.)
                            Use os nomes EXATOS (case-sensitive) das colunas.
                            
                            PASSO 3 - Normalizar NCMs:
                            Execute: df['NCM_norm'] = df[nome_coluna_ncm].astype(str).str.replace('.','').str.replace('-','')
                            Mostre: df['NCM_norm'].value_counts()
                            
                            PASSO 4 - Agrupar e analisar:
                            Para cada NCM único, pegue um exemplo de descrição de produto.
                            Execute: df.groupby('NCM_norm')[nome_coluna_descricao].first()
                            
                            PASSO 5 - Identificar problemas:
                            Analise cada NCM único e verifique:
                            - Se tem 8 dígitos
                            - Se é válido para setor pet
                            - Se está adequado à descrição do produto
                            
                            Liste os NCMs com problemas em formato de tabela markdown:
                            | NCM | Produto Exemplo | Problema | NCM Sugerido | Severidade |
                            
                            PASSO 6 - Resumo final:
                            - Total de NCMs únicos
                            - NCMs com problemas
                            - Percentual de conformidade
                            - Principais ações recomendadas
                            
                            IMPORTANTE: 
                            - Use astype(str) ANTES de qualquer operação de string no NCM
                            - Use os nomes EXATOS das colunas que aparecem em df.columns
                            - Não crie funções separadas - use apenas operações pandas inline
                            """
                            
                            response = agent.run(validation_query)
                            
                            # Armazena resultado na sessão para usar no PDF/email
                            st.session_state.validation_response = response
                            st.session_state.validation_df = df
                            
                            display_validation_results(response)
                            
                            # Gera relatório automaticamente
                            gerar_e_exibir_relatorio(df, response, email_destinatario, enviar_email_auto)
                            
                        except Exception as e:
                            st.error(f"❌ Erro ao processar validação: {str(e)}")
                            st.info("💡 Tente usar a Validação Manual Rápida acima ou fazer perguntas mais simples no chat abaixo.")
                            
                            # Mostra informações de debug
                            with st.expander("🔍 Informações de Debug"):
                                st.write("**Colunas do DataFrame:**")
                                st.write(df.columns.tolist())
                                st.write("\n**Primeiras linhas:**")
                                st.write(df.head())

                # CHAT INTERATIVO
                st.subheader("💬 Faça perguntas sobre os dados")
                st.markdown("*Exemplos: 'Mostre os NCMs únicos', 'O NCM 23099010 está correto?', 'Liste produtos com NCM 9503'*")
                
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


def gerar_e_exibir_relatorio(df, response, email_destinatario, enviar_auto):
    """Gera PDF e envia e-mail se configurado"""
    
    st.markdown("---")
    st.subheader("📄 Relatório")
    
    # Extrai métricas da resposta
    total_produtos = len(df)
    ncm_cols = [col for col in df.columns if 'ncm' in col.lower()]
    
    if ncm_cols:
        df_temp = df.copy()
        df_temp['NCM_norm'] = df_temp[ncm_cols[0]].astype(str).str.replace('.', '').str.replace('-', '')
        ncms_unicos = df_temp['NCM_norm'].nunique()
    else:
        ncms_unicos = 0
    
    # Tenta extrair número de problemas da resposta
    ncms_problemas = response.lower().count('problema') // 2  # Estimativa
    percentual_conformidade = ((total_produtos - ncms_problemas) / total_produtos * 100) if total_produtos > 0 else 100
    
    # Gera PDF
    pdf_filename = "relatorio_ncm.pdf"
    
    try:
        with st.spinner("Gerando relatório PDF..."):
            # Cria DataFrame de problemas (simplificado)
            problemas_df = pd.DataFrame({
                'Status': ['Análise Completa'],
                'Detalhes': ['Verifique o relatório completo para detalhes']
            })
            
            pdf_path = pdf_generator.gerar_relatorio_pdf(
                filename=pdf_filename,
                total_produtos=total_produtos,
                ncms_unicos=ncms_unicos,
                ncms_problemas=ncms_problemas,
                percentual_conformidade=percentual_conformidade,
                problemas_df=problemas_df,
                observacoes=response[:500]  # Primeiros 500 caracteres
            )
        
        # Botões de Download e E-mail
        col1, col2 = st.columns(2)
        
        with col1:
            with open(pdf_filename, "rb") as pdf_file:
                pdf_bytes = pdf_file.read()
                st.download_button(
                    label="📥 Baixar Relatório PDF",
                    data=pdf_bytes,
                    file_name="relatorio_conformidade_ncm.pdf",
                    mime="application/pdf",
                    use_container_width=True
                )
        
        with col2:
            if email_destinatario:
                if st.button("📧 Enviar Relatório por E-mail", use_container_width=True):
                    enviar_relatorio_email(
                        email_destinatario, 
                        total_produtos,
                        ncms_problemas,
                        percentual_conformidade,
                        response,
                        pdf_filename
                    )
            else:
                st.info("Configure o e-mail na sidebar para enviar relatório")
        
        # Envio automático
        if enviar_auto and email_destinatario:
            enviar_relatorio_email(
                email_destinatario, 
                total_produtos,
                ncms_problemas,
                percentual_conformidade,
                response,
                pdf_filename
            )
        
        st.success("✅ Relatório PDF gerado com sucesso!")
        
    except Exception as e:
        st.error(f"Erro ao gerar relatório: {str(e)}")


def enviar_relatorio_email(destinatario, total, problemas, conformidade, response, pdf_path):
    """Envia relatório por e-mail"""
    
    with st.spinner("Enviando e-mail..."):
        # Prepara lista de problemas HTML
        problemas_html = response.replace('\n', '<br>') if problemas > 0 else ""
        
        # Gera corpo do e-mail
        corpo_html = email_service.gerar_corpo_email_html(
            total_produtos=total,
            ncms_problemas=problemas,
            percentual_conformidade=conformidade,
            problemas_lista=problemas_html
        )
        
        # Envia e-mail
        sucesso = email_service.enviar_relatorio_email(
            destinatario=destinatario,
            assunto="Relatório de Conformidade NCM - Setor Pet",
            corpo_html=corpo_html,
            pdf_path=pdf_path
        )
        
        if sucesso:
            st.success(f"✅ E-mail enviado para {destinatario}!")
        else:
            st.error("❌ Erro ao enviar e-mail. Verifique as configurações.")


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
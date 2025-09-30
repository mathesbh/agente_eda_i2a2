# Agente de EDA Inteligente com LangChain + GPT-4 Mini

## Frameworks Utilizados

- [Streamlit](https://streamlit.io/): Interface web interativa para o usuário.
- [Pandas](https://pandas.pydata.org/): Manipulação e análise de dados tabulares.
- [LangChain](https://python.langchain.com/): Orquestração de agentes LLM e integração com ferramentas.
- [LangChain OpenAI](https://python.langchain.com/docs/integrations/openai): Integração do LangChain com modelos OpenAI.
- [LangChain Experimental](https://python.langchain.com/docs/modules/experimental): Ferramentas experimentais, como agentes para DataFrames Pandas.
- [Matplotlib](https://matplotlib.org/): Visualização de dados.
- [Seaborn](https://seaborn.pydata.org/): Visualização estatística de dados.
- [Tabulate](https://pypi.org/project/tabulate/): Exibição tabular de dados.
- [python-dotenv](https://pypi.org/project/python-dotenv/): Carregamento de variáveis de ambiente.

## Estrutura da Solução

### Descrição dos Arquivos

- **[main.py](main.py)**  
  - Ponto de entrada da aplicação Streamlit.
  - Gerencia o upload do arquivo ZIP com CSV, coleta da chave OpenAI, inicialização do agente, interface de perguntas e exibição de respostas.
  - Chama funções auxiliares para carregar dados, exibir pré-visualização, processar perguntas e mostrar gráficos/conclusões.

- **[agent_setup.py](agent_setup.py)**  
  - Define o template de prompt para o agente de EDA.
  - Implementa [`initialize_llm`](agent_setup.py) para inicializar o modelo GPT-4o-mini via OpenAI.
  - Implementa [`create_agent`](agent_setup.py) para criar o agente LangChain especializado em DataFrames Pandas, com memória de conversação e prompt customizado.

- **[utils.py](utils.py)**  
  - Implementa [`generate_plot`](utils.py) para gerar gráficos (histograma, dispersão) conforme a pergunta do usuário usando Matplotlib/Seaborn.
  - Implementa [`check_for_conclusions`](utils.py) para garantir que conclusões sejam apresentadas ao final da análise.

- **[requirements.txt](requirements.txt)**  
  - Lista as dependências do projeto.

- **.env**  
  - (Opcional) Permite definir variáveis de ambiente, como a chave `OPENAI_API_KEY`.

## Como funciona

1. O usuário faz upload de um arquivo ZIP contendo um CSV.
2. O app carrega e pré-visualiza os dados.
3. O usuário insere sua chave OpenAI API.
4. Um agente LangChain é inicializado, especializado em EDA sobre DataFrames Pandas.
5. O usuário faz perguntas sobre os dados; o agente responde, gera gráficos relevantes e apresenta conclusões.

---
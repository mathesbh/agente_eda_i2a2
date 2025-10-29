# 🐾 Agente de Conformidade Fiscal NCM - Setor Pet

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)](https://streamlit.io/)
[![LangChain](https://img.shields.io/badge/LangChain-0.1+-green.svg)](https://python.langchain.com/)

Sistema inteligente de validação automática de códigos NCM (Nomenclatura Comum do Mercosul) em notas fiscais para clínicas veterinárias, pet shops e estabelecimentos do setor pet.

## 📋 Índice

- [Sobre o Projeto](#-sobre-o-projeto)
- [Características](#-características)
- [Arquitetura](#-arquitetura)
- [Tecnologias Utilizadas](#-tecnologias-utilizadas)
- [Instalação](#-instalação)
- [Configuração](#-configuração)
- [Como Usar](#-como-usar)
- [Estrutura do Projeto](#-estrutura-do-projeto)
- [Exemplos de Uso](#-exemplos-de-uso)
- [Contribuindo](#-contribuindo)
- [Licença](#-licença)
- [Contato](#-contato)

## 🎯 Sobre o Projeto

O **Agente de Conformidade Fiscal NCM** é uma solução automatizada que utiliza Inteligência Artificial (GPT-4) para identificar inconsistências e irregularidades em códigos NCM de notas fiscais do setor pet. O sistema analisa CSVs de notas fiscais, valida a conformidade dos NCMs com a legislação brasileira e gera relatórios detalhados em PDF.

### Problema Resolvido

Empresas do setor pet frequentemente enfrentam:
- **Erros de classificação fiscal**: NCMs incorretos levam a tributação inadequada
- **Multas e autuações**: Fiscalização rigorosa da Receita Federal
- **Perda de tempo**: Validação manual é demorada e suscetível a erros
- **Falta de conhecimento técnico**: Dificuldade em interpretar tabela NCM

### Solução

Sistema automatizado que:
- ✅ Valida NCMs em segundos usando IA
- ✅ Identifica incompatibilidades entre NCM e descrição do produto
- ✅ Gera relatórios executivos em PDF
- ✅ Envia alertas por e-mail
- ✅ Oferece chat interativo para dúvidas específicas

## ✨ Características

### 🤖 Validação Inteligente com IA
- Análise automática de NCMs usando GPT-4o-mini
- Detecção de incompatibilidades entre código e produto
- Sugestões de NCMs corretos
- Classificação de severidade dos problemas

### 📊 Análise Detalhada
- Identificação de produtos com NCM incorreto
- Estatísticas de conformidade
- Comparação com tabela de referência do setor pet
- Validação de formato (8 dígitos)

### 📄 Relatórios Profissionais
- Geração automática de PDF executivo
- Gráficos e métricas visuais
- Tabelas de problemas identificados
- Recomendações de ações corretivas

### 📧 Envio Automático por E-mail
- Envio de relatórios por e-mail (Mailtrap/SMTP)
- Anexo de PDF completo
- Resumo executivo em HTML
- Notificações automáticas

### 💬 Chat Interativo
- Perguntas em linguagem natural sobre os dados
- Memória de conversação
- Análises customizadas sob demanda

## 🏗️ Arquitetura

```
┌─────────────────────────────────────────────────────┐
│                   Interface Web                      │
│                   (Streamlit)                        │
└────────────────┬────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────┐
│              Camada de Aplicação                     │
│  ┌──────────────┐  ┌──────────────┐  ┌────────────┐│
│  │   main_ncm   │  │ utils_ncm    │  │ncm.reference││
│  │     .py      │  │    .py       │  │    .py     ││
│  └──────────────┘  └──────────────┘  └────────────┘│
└────────────────┬────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────┐
│              Camada de Agente IA                     │
│  ┌──────────────────────────────────────────────┐  │
│  │        agent_setup_ncm.py                     │  │
│  │  (LangChain + GPT-4 + Pandas Agent)          │  │
│  └──────────────────────────────────────────────┘  │
└────────────────┬────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────┐
│              Serviços Externos                       │
│  ┌──────────────┐  ┌──────────────┐  ┌────────────┐│
│  │pdf_generator │  │email_service │  │  OpenAI    ││
│  │     .py      │  │     .py      │  │    API     ││
│  └──────────────┘  └──────────────┘  └────────────┘│
└─────────────────────────────────────────────────────┘
```

## 🛠️ Tecnologias Utilizadas

### Frameworks e Bibliotecas

- **[Streamlit](https://streamlit.io/)**: Interface web interativa
- **[LangChain](https://python.langchain.com/)**: Orquestração de agentes LLM
- **[LangChain OpenAI](https://python.langchain.com/docs/integrations/openai)**: Integração com GPT-4
- **[LangChain Experimental](https://python.langchain.com/docs/modules/experimental)**: Agentes para DataFrames Pandas
- **[Pandas](https://pandas.pydata.org/)**: Manipulação e análise de dados
- **[ReportLab](https://www.reportlab.com/)**: Geração de relatórios PDF
- **[Matplotlib](https://matplotlib.org/)** / **[Seaborn](https://seaborn.pydata.org/)**: Visualização de dados
- **[python-dotenv](https://pypi.org/project/python-dotenv/)**: Gerenciamento de variáveis de ambiente
- **[chardet](https://pypi.org/project/chardet/)**: Detecção automática de encoding

### APIs e Serviços

- **OpenAI GPT-4o-mini**: Modelo de linguagem para análise inteligente
- **Mailtrap / SMTP**: Envio de e-mails

## 🚀 Instalação

### Pré-requisitos

- Python 3.8 ou superior
- pip (gerenciador de pacotes Python)
- Chave de API da OpenAI

### Passos

1. **Clone o repositório**
```bash
git clone https://github.com/mathesbh/agente_eda_i2a2.git
cd agente_eda_i2a2
```

2. **Crie um ambiente virtual (recomendado)**
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

3. **Instale as dependências**
```bash
pip install -r requirements.txt
```

## ⚙️ Configuração

### 1. Variáveis de Ambiente

Crie um arquivo `.env` na raiz do projeto:

```env
# OpenAI API Key
OPENAI_API_KEY=sk-proj-xxxxxxxxxxxxxxxxxx

# Configurações de E-mail (Mailtrap para testes)
MAILTRAP_USERNAME=seu_username_mailtrap
MAILTRAP_PASSWORD=sua_senha_mailtrap

# Configurações de E-mail (Produção - Gmail)
EMAIL_APP_PASSWORD=sua_senha_app_gmail
```

### 2. Obter Chave OpenAI

1. Acesse [platform.openai.com](https://platform.openai.com/)
2. Crie uma conta ou faça login
3. Vá em **API Keys** → **Create new secret key**
4. Copie a chave e adicione ao `.env`
5. Ou inclua a chave no campo da interface

### 3. Configurar E-mail (Opcional)

**Para Testes (Mailtrap):**
1. Crie conta gratuita em [mailtrap.io](https://mailtrap.io/)
2. Acesse **Email Testing** → **Inboxes** → **SMTP Settings**
3. Copie Username e Password para o `.env`

**Para Produção (Gmail):**
1. Ative a verificação em 2 etapas na sua conta Google
2. Gere uma "Senha de App" em [myaccount.google.com/apppasswords](https://myaccount.google.com/apppasswords)
3. Adicione ao `.env` como `EMAIL_APP_PASSWORD`
4. Em `email_service.py`, mude `self.use_mailtrap = False`

## 📖 Como Usar

### 1. Iniciar a Aplicação

```bash
streamlit run main_ncm.py
```

A aplicação abrirá automaticamente no navegador em `http://localhost:8501`

### 2. Preparar os Dados

Seu arquivo CSV deve conter pelo menos:
- **Coluna NCM**: Com códigos NCM (pode ser com ou sem pontos)
- **Coluna Descrição**: Com descrição dos produtos

Exemplo de CSV:
```csv
NCM,DESCRICAO_PRODUTO,VALOR
2309.10.00,Ração para cães Premium 15kg,125.00
3004.90.69,Antibiótico veterinário,45.50
```

Compacte o CSV em formato ZIP.

### 3. Fluxo de Uso

1. **Upload**: Faça upload do arquivo ZIP
2. **API Key**: Insira sua chave OpenAI API
3. **Validação**: Clique em "Iniciar Validação Automática"
4. **Resultados**: Visualize análise, métricas e problemas
5. **Relatório**: Baixe o PDF ou envie por e-mail
6. **Chat**: Faça perguntas específicas sobre os dados

### 4. Exemplos de Perguntas no Chat

```
"Mostre os 10 NCMs mais frequentes"
"Quais produtos têm NCM 2309.10.00?"
"O NCM 9503.00.10 está correto para brinquedo de pet?"
"Liste todos os produtos com NCM inválido"
"Mostre gráfico de distribuição de NCMs"
```

## 📁 Estrutura do Projeto

```
agente-ncm-validator/
│
├── main_ncm.py                 # Aplicação principal Streamlit
├── agent_setup_ncm.py          # Configuração do agente LangChain
├── utils_ncm.py                # Funções auxiliares e validação manual
├── email_service.py            # Serviço de envio de e-mails
├── pdf_generator.py            # Geração de relatórios PDF
├── ncm_reference.py            # Gerenciamento da tabela de referência
│
├── ncm_petshop.csv             # Tabela de NCMs válidos do setor pet
├── requirements.txt            # Dependências do projeto
├── .env                        # Variáveis de ambiente (não versionado)
├── README.md                   # Documentação do projeto
│
└── README.md (original)        # Documentação original do EDA
```

### Descrição dos Arquivos

#### **main_ncm.py**
Arquivo principal da aplicação Streamlit. Responsável por:
- Interface do usuário
- Upload e processamento de arquivos ZIP/CSV
- Gerenciamento de sessão e estado
- Integração com agente de validação
- Exibição de resultados e métricas
- Geração e download de relatórios PDF
- Envio de e-mails

#### **agent_setup_ncm.py**
Configura o agente de IA especializado em conformidade fiscal. Contém:
- **PROMPT_TEMPLATE**: Instruções detalhadas para o GPT-4 sobre validação NCM
- **initialize_llm()**: Inicializa o modelo GPT-4o-mini
- **create_agent()**: Cria agente Pandas com memória de conversação
- Configurações de timeout e limitações de iteração
- Tratamento de erros de parsing

#### **utils_ncm.py**
Funções utilitárias para visualização e validação. Implementa:
- **generate_plot()**: Gera gráficos de distribuição e valores
- **quick_ncm_validation()**: Validação manual rápida (backup do agente)
- **display_validation_results()**: Formatação de resultados
- Estatísticas e métricas de conformidade

#### **email_service.py**
Serviço completo de envio de e-mails. Recursos:
- Suporte para Mailtrap (testes) e SMTP real (produção)
- **enviar_relatorio_email()**: Envia relatório com PDF anexado
- **gerar_corpo_email_html()**: Template HTML responsivo e profissional
- Formatação de métricas e status visual
- Tratamento de erros de autenticação SMTP

#### **pdf_generator.py**
Geração profissional de relatórios PDF. Características:
- Uso de ReportLab para PDFs de alta qualidade
- **PDFReportGenerator**: Classe principal de geração
- Templates customizados com cores e estilos
- Tabelas formatadas de problemas
- Métricas visuais e gráficos
- Seções: resumo executivo, detalhes, ações recomendadas

#### **ncm_reference.py**
Gerencia tabela de referência de NCMs válidos. Funcionalidades:
- **NCMReference**: Classe para consulta de NCMs
- Busca por código, descrição ou categoria
- Validação contra tabela oficial
- **get_ncm_info()**: Retorna detalhes de um NCM
- **search_by_description()**: Busca por palavra-chave
- Integração com prompt do agente

#### **ncm_petshop.csv**
Base de dados de referência contendo:
- NCMs válidos para o setor pet
- Categorias (Alimentos, Higiene, Medicamentos, Acessórios)
- Descrições e exemplos de produtos
- Observações sobre tributação e ST

## 💡 Exemplos de Uso

### Caso de Uso 1: Validação Completa de Notas

```python
# 1. Usuário faz upload de "notas_janeiro_2025.zip"
# 2. Sistema detecta 150 produtos
# 3. Validação identifica:
#    - 10 NCMs incorretos (brinquedo com 9503.00.10)
#    - 5 NCMs com formato inválido
#    - 135 produtos em conformidade (90%)
# 4. Gera PDF com recomendações
# 5. Envia para contador@empresa.com
```

### Caso de Uso 2: Consulta Específica via Chat

```
Usuário: "Qual NCM correto para ração de gato?"
Agente: "Para ração de gatos, o NCM correto é 2309.10.00 
         (Preparações para alimentação de cães ou gatos 
         acondicionadas para venda a retalho)"
```

### Caso de Uso 3: Análise de Produto Suspeito

```
Usuário: "O NCM 6802.93.90 está correto para areia sanitária?"
Agente: "❌ INCORRETO! O NCM 6802.93.90 é para granito/pedras 
         ornamentais. Para areia sanitária de gatos, use:
         ✅ 2505.10.00 (Areias siliciosas e areias quartzosas)"
```

## 🧪 Testes

### Testar Validação Manual

```python
# Usar o botão "Executar Validação Manual" na interface
# ou executar diretamente:
from utils_ncm import quick_ncm_validation
quick_ncm_validation(df)
```

### Testar Envio de E-mail

1. Configure Mailtrap no `.env`
2. Marque "Enviar e-mail automaticamente"
3. Execute validação
4. Verifique inbox do Mailtrap

## 🤝 Contribuindo

Contribuições são bem-vindas! Por favor, siga estas diretrizes:

1. **Fork** o projeto
2. Crie uma **branch** para sua feature (`git checkout -b feature/NovaFuncionalidade`)
3. **Commit** suas mudanças (`git commit -m 'Add: Nova funcionalidade X'`)
4. **Push** para a branch (`git push origin feature/NovaFuncionalidade`)
5. Abra um **Pull Request**

### Padrões de Código

- Use **docstrings** em todas as funções
- Siga **PEP 8** para formatação
- Adicione **type hints** quando possível
- Escreva **testes** para novas funcionalidades

## 📝 Roadmap

- [ ] Suporte para múltiplos CSVs simultaneamente
- [ ] Integração com API da Receita Federal
- [ ] Dashboard de histórico de validações
- [ ] Exportação para Excel
- [ ] Modo offline (sem OpenAI)
- [ ] Suporte para outros setores além de pet
- [ ] API REST para integração com ERPs

## 🐛 Problemas Conhecidos

- **Timeout em arquivos grandes (>5000 linhas)**: Use validação manual
- **Encoding UTF-8**: Salve CSVs em UTF-8 antes de compactar
- **Memória do agente**: Reseta após 10 interações

## 📄 Licença

Este projeto está licenciado sob a **Licença MIT** - veja o arquivo [LICENSE](LICENSE) para detalhes.

```
MIT License

Copyright (c) 2025 [Seu Nome]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

## 🙏 Agradecimentos

- [Anthropic](https://www.anthropic.com/) - Claude para documentação
- [OpenAI](https://openai.com/) - GPT-4 para validação inteligente
- [Streamlit](https://streamlit.io/) - Framework de interface
- [LangChain](https://langchain.com/) - Orquestração de agentes
- Comunidade Python e desenvolvedores open source

---

<p align="center">
  Feito com ❤️ e ☕ para ajudar empresas do setor pet a manterem conformidade fiscal
</p>

<p align="center">
  <sub>⭐ Se este projeto te ajudou, considere dar uma estrela!</sub>
</p>
"""
Serviço de envio de e-mail usando Mailtrap (para testes) ou SMTP real
"""
import requests
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
import smtplib
from typing import Optional
import streamlit as st
import os

class EmailService:
    """Serviço de envio de e-mails"""
    
    def __init__(self):
        # Configuração Mailtrap (padrão para testes)
        self.use_mailtrap = True  # Mude para False para usar SMTP real
        
        # Configurações Mailtrap
        self.mailtrap_host = "sandbox.smtp.mailtrap.io"
        self.mailtrap_port = 2525
        self.mailtrap_username = st.secrets["smtp"]["username"]
        self.mailtrap_password = st.secrets["smtp"]["password"]
        
        # Configurações SMTP Real (Gmail, Outlook, etc)
        self.smtp_server = "smtp.gmail.com"
        self.smtp_port = 587
        self.sender_email = "noreply.ncmvalidator@gmail.com"
        
    def enviar_relatorio_email(
        self, 
        destinatario: str, 
        assunto: str, 
        corpo_html: str,
        pdf_path: Optional[str] = None
    ) -> bool:
        """
        Envia relatório por e-mail
        
        Args:
            destinatario: E-mail do destinatário
            assunto: Assunto do e-mail
            corpo_html: Corpo do e-mail em HTML
            pdf_path: Caminho do PDF anexo (opcional)
            
        Returns:
            True se enviado com sucesso, False caso contrário
        """
        try:
            # Cria mensagem
            msg = MIMEMultipart('alternative')
            msg['From'] = self.sender_email if not self.use_mailtrap else "teste@exemplo.com"
            msg['To'] = destinatario
            msg['Subject'] = assunto
            
            # Adiciona corpo HTML
            html_part = MIMEText(corpo_html, 'html', 'utf-8')
            msg.attach(html_part)
            
            # Adiciona PDF se fornecido
            if pdf_path:
                try:
                    with open(pdf_path, 'rb') as f:
                        pdf_part = MIMEApplication(f.read(), _subtype='pdf')
                        pdf_part.add_header('Content-Disposition', 'attachment', 
                                           filename='relatorio_ncm.pdf')
                        msg.attach(pdf_part)
                except Exception as e:
                    st.warning(f"Não foi possível anexar PDF: {e}")
            
            # MODO MAILTRAP (para testes)
            if self.use_mailtrap:
                if not self.mailtrap_username or not self.mailtrap_password:
                    st.error("❌ Configure MAILTRAP_USERNAME e MAILTRAP_PASSWORD no .env")
                    st.info("💡 Veja o guia de configuração do Mailtrap")
                    return False
                
                with smtplib.SMTP(self.mailtrap_host, self.mailtrap_port) as server:
                    server.starttls()
                    server.login(self.mailtrap_username, self.mailtrap_password)
                    server.send_message(msg)
                
                st.success(f"✅ E-mail enviado para Mailtrap Inbox!")
                st.info(f"📧 Destinatário: {destinatario} (verifique na sua inbox do Mailtrap)")
                return True
            
            # MODO PRODUÇÃO (SMTP Real)
            else:
                app_password = os.getenv("EMAIL_APP_PASSWORD", "")
                
                if not app_password:
                    st.error("Configure EMAIL_APP_PASSWORD no .env")
                    return False
                
                with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                    server.starttls()
                    server.login(self.sender_email, app_password)
                    server.send_message(msg)
                
                return True
            
        except smtplib.SMTPAuthenticationError:
            st.error("❌ Erro de autenticação. Verifique username e password do Mailtrap.")
            st.info("💡 Copie as credenciais exatas da aba SMTP Settings do Mailtrap")
            return False
        except Exception as e:
            st.error(f"❌ Erro ao enviar e-mail: {str(e)}")
            return False
    
    def gerar_corpo_email_html(
        self, 
        total_produtos: int,
        ncms_problemas: int,
        percentual_conformidade: float,
        problemas_lista: str
    ) -> str:
        """Gera corpo HTML do e-mail de relatório"""
        
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    line-height: 1.6;
                    color: #333;
                }}
                .header {{
                    background-color: #4CAF50;
                    color: white;
                    padding: 20px;
                    text-align: center;
                }}
                .content {{
                    padding: 20px;
                }}
                .metrics {{
                    display: flex;
                    justify-content: space-around;
                    margin: 20px 0;
                }}
                .metric {{
                    text-align: center;
                    padding: 15px;
                    background-color: #f5f5f5;
                    border-radius: 5px;
                }}
                .metric-value {{
                    font-size: 24px;
                    font-weight: bold;
                    color: #4CAF50;
                }}
                .metric-label {{
                    font-size: 14px;
                    color: #666;
                }}
                .problems {{
                    margin-top: 20px;
                    padding: 15px;
                    background-color: #fff3cd;
                    border-left: 4px solid #ffc107;
                }}
                .footer {{
                    margin-top: 30px;
                    padding: 15px;
                    background-color: #f5f5f5;
                    text-align: center;
                    font-size: 12px;
                    color: #666;
                }}
                table {{
                    width: 100%;
                    border-collapse: collapse;
                    margin-top: 15px;
                }}
                th, td {{
                    padding: 10px;
                    text-align: left;
                    border-bottom: 1px solid #ddd;
                }}
                th {{
                    background-color: #4CAF50;
                    color: white;
                }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1>🐾 Relatório de Conformidade NCM - Setor Pet</h1>
            </div>
            
            <div class="content">
                <h2>Resumo da Validação</h2>
                
                <div class="metrics" style="display: block;">
                    <div class="metric" style="margin-bottom: 10px;">
                        <div class="metric-label">Total de Produtos</div>
                        <div class="metric-value">{total_produtos}</div>
                    </div>
                    
                    <div class="metric" style="margin-bottom: 10px;">
                        <div class="metric-label">Produtos com Problemas</div>
                        <div class="metric-value" style="color: #f44336;">{ncms_problemas}</div>
                    </div>
                    
                    <div class="metric" style="margin-bottom: 10px;">
                        <div class="metric-label">Conformidade</div>
                        <div class="metric-value" style="color: {'#4CAF50' if percentual_conformidade >= 80 else '#f44336'};">
                            {percentual_conformidade:.1f}%
                        </div>
                    </div>
                </div>
                
                {f'''
                <div class="problems">
                    <h3>⚠️ Problemas Encontrados</h3>
                    {problemas_lista}
                </div>
                ''' if ncms_problemas > 0 else '<p style="color: #4CAF50; font-weight: bold;">✅ Nenhum problema encontrado! Todas as notas fiscais estão em conformidade.</p>'}
                
                <p style="margin-top: 20px;">
                    <strong>Ações Recomendadas:</strong>
                </p>
                <ul>
                    <li>Revise os NCMs com problemas identificados</li>
                    <li>Corrija as notas fiscais antes de emitir novas</li>
                    <li>Consulte a tabela de referência para NCMs corretos</li>
                    <li>Entre em contato com seu contador se necessário</li>
                </ul>
            </div>
            
            <div class="footer">
                <p>Relatório gerado automaticamente pelo Sistema de Conformidade Fiscal NCM</p>
                <p>Data: {__import__('datetime').datetime.now().strftime('%d/%m/%Y %H:%M')}</p>
            </div>
        </body>
        </html>
        """
        
        return html


# Instância global
email_service = EmailService()
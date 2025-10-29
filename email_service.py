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
        self.mailtrap_username = st.secrets["smtp"]["username"] or os.getenv("MAILTRAP_USERNAME")
        self.mailtrap_password = st.secrets["smtp"]["password"] or os.getenv("MAILTRAP_PASSWORD")
        
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
        ncms_unicos: int,
        ncms_problemas: int,
        percentual_conformidade: float,
        problemas_lista: str
    ) -> str:
        """Gera corpo HTML do e-mail de relatório"""
        
        status_cor = '#4CAF50' if percentual_conformidade >= 80 else '#f44336'
        status_texto = '✅ BOM' if percentual_conformidade >= 80 else '⚠️ REQUER ATENÇÃO'
        
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    line-height: 1.6;
                    color: #333;
                    max-width: 800px;
                    margin: 0 auto;
                    padding: 20px;
                }}
                .header {{
                    background-color: #4CAF50;
                    color: white;
                    padding: 30px;
                    text-align: center;
                    border-radius: 10px 10px 0 0;
                }}
                .header h1 {{
                    margin: 0;
                    font-size: 24px;
                }}
                .header p {{
                    margin: 5px 0 0 0;
                    font-size: 14px;
                    opacity: 0.9;
                }}
                .content {{
                    padding: 30px;
                    background-color: #ffffff;
                    border: 1px solid #ddd;
                    border-top: none;
                }}
                .metrics {{
                    display: grid;
                    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                    gap: 15px;
                    margin: 20px 0;
                }}
                .metric {{
                    text-align: center;
                    padding: 20px;
                    background-color: #f5f5f5;
                    border-radius: 8px;
                    border-left: 4px solid #4CAF50;
                }}
                .metric-value {{
                    font-size: 32px;
                    font-weight: bold;
                    color: #2E7D32;
                    margin: 10px 0;
                }}
                .metric-label {{
                    font-size: 13px;
                    color: #666;
                    text-transform: uppercase;
                    letter-spacing: 0.5px;
                }}
                .status-box {{
                    padding: 20px;
                    background-color: {status_cor}15;
                    border-left: 4px solid {status_cor};
                    border-radius: 5px;
                    margin: 20px 0;
                }}
                .status-box h3 {{
                    margin: 0 0 10px 0;
                    color: {status_cor};
                }}
                .problems {{
                    margin-top: 20px;
                    padding: 20px;
                    background-color: #fff3cd;
                    border-left: 4px solid #ffc107;
                    border-radius: 5px;
                }}
                .problems h3 {{
                    margin: 0 0 15px 0;
                    color: #856404;
                }}
                table {{
                    width: 100%;
                    border-collapse: collapse;
                    margin-top: 15px;
                    font-size: 13px;
                }}
                th, td {{
                    padding: 12px;
                    text-align: left;
                    border-bottom: 1px solid #ddd;
                }}
                th {{
                    background-color: #4CAF50;
                    color: white;
                    font-weight: bold;
                }}
                tr:hover {{
                    background-color: #f5f5f5;
                }}
                .actions {{
                    margin-top: 25px;
                    padding: 20px;
                    background-color: #e3f2fd;
                    border-radius: 5px;
                }}
                .actions h3 {{
                    margin: 0 0 15px 0;
                    color: #1976d2;
                }}
                .actions ul {{
                    margin: 10px 0;
                    padding-left: 20px;
                }}
                .actions li {{
                    margin: 8px 0;
                }}
                .footer {{
                    margin-top: 30px;
                    padding: 20px;
                    background-color: #f5f5f5;
                    text-align: center;
                    font-size: 12px;
                    color: #666;
                    border-radius: 0 0 10px 10px;
                }}
                .attachment-note {{
                    margin-top: 20px;
                    padding: 15px;
                    background-color: #e8f5e9;
                    border-left: 4px solid #4CAF50;
                    border-radius: 5px;
                }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1>🐾 Relatório de Conformidade Fiscal NCM</h1>
                <p>Setor Pet - Validação de Notas Fiscais</p>
            </div>
            
            <div class="content">
                <h2 style="color: #2E7D32; border-bottom: 2px solid #4CAF50; padding-bottom: 10px;">
                    Resumo Executivo
                </h2>
                
                <div class="metrics">
                    <div class="metric">
                        <div class="metric-label">Total de Produtos</div>
                        <div class="metric-value">{total_produtos}</div>
                    </div>
                    
                    <div class="metric">
                        <div class="metric-label">NCMs Únicos</div>
                        <div class="metric-value" style="color: #1976d2;">{ncms_unicos}</div>
                    </div>
                    
                    <div class="metric" style="border-left-color: {'#4CAF50' if ncms_problemas == 0 else '#f44336'};">
                        <div class="metric-label">Produtos com Problemas</div>
                        <div class="metric-value" style="color: {'#4CAF50' if ncms_problemas == 0 else '#f44336'};">
                            {ncms_problemas}
                        </div>
                    </div>
                    
                    <div class="metric" style="border-left-color: {status_cor};">
                        <div class="metric-label">Conformidade</div>
                        <div class="metric-value" style="color: {status_cor};">
                            {percentual_conformidade:.1f}%
                        </div>
                    </div>
                </div>
                
                <div class="status-box">
                    <h3>Status Geral: {status_texto}</h3>
                    <p style="margin: 0;">
                        {
                            'Parabéns! Suas notas fiscais estão em conformidade.' if percentual_conformidade >= 95
                            else 'Boa conformidade geral. Algumas correções menores são recomendadas.' if percentual_conformidade >= 80
                            else 'Atenção necessária. Múltiplos problemas foram identificados e requerem correção.'
                        }
                    </p>
                </div>
                
                {f'''
                <div class="problems">
                    <h3>⚠️ Problemas Identificados</h3>
                    {problemas_lista}
                </div>
                ''' if ncms_problemas > 0 else '<p style="color: #4CAF50; font-weight: bold; text-align: center; padding: 20px; background-color: #e8f5e9; border-radius: 5px;">✅ Nenhum problema encontrado! Todas as notas fiscais estão em conformidade.</p>'}
                
                <div class="actions">
                    <h3>🎯 Ações Recomendadas</h3>
                    <ul>
                        <li><strong>Imediato:</strong> Revise os NCMs com problemas críticos identificados</li>
                        <li><strong>Curto Prazo (7 dias):</strong> Corrija as notas fiscais antes de emitir novas</li>
                        <li><strong>Médio Prazo (30 dias):</strong> Implemente processo de validação preventiva</li>
                        <li><strong>Consultoria:</strong> Entre em contato com seu contador para casos complexos</li>
                    </ul>
                </div>
                
                <div class="attachment-note">
                    <strong>📎 Relatório Completo em PDF</strong><br>
                    O relatório detalhado com todas as análises e recomendações está anexado a este e-mail.
                </div>
            </div>
            
            <div class="footer">
                <p><strong>Relatório gerado automaticamente</strong></p>
                <p>Sistema de Conformidade Fiscal NCM - Setor Pet</p>
                <p>Data: {__import__('datetime').datetime.now().strftime('%d/%m/%Y às %H:%M')}</p>
                <p style="margin-top: 10px; font-size: 11px;">
                    <em>Este é um relatório automático. Consulte um profissional contábil para orientações específicas.</em>
                </p>
            </div>
        </body>
        </html>
        """
        
        return html


# Instância global
email_service = EmailService()
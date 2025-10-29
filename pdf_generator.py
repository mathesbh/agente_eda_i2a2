"""
Gerador de relatórios em PDF usando ReportLab
"""
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.platypus import Image as RLImage
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from datetime import datetime
import pandas as pd
from typing import Dict, List

class PDFReportGenerator:
    """Gerador de relatórios PDF de conformidade NCM"""
    
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self._setup_custom_styles()
    
    def _setup_custom_styles(self):
        """Configura estilos customizados"""
        # Título principal
        self.styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#4CAF50'),
            spaceAfter=30,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        ))
        
        # Subtítulo
        self.styles.add(ParagraphStyle(
            name='CustomHeading',
            parent=self.styles['Heading2'],
            fontSize=16,
            textColor=colors.HexColor('#2E7D32'),
            spaceAfter=12,
            spaceBefore=12,
            fontName='Helvetica-Bold'
        ))
        
        # Texto normal
        self.styles.add(ParagraphStyle(
            name='CustomBody',
            parent=self.styles['Normal'],
            fontSize=11,
            spaceAfter=10,
            alignment=TA_JUSTIFY
        ))
    
    def gerar_relatorio_pdf(
        self,
        filename: str,
        total_produtos: int,
        ncms_unicos: int,
        ncms_problemas: int,
        percentual_conformidade: float,
        problemas_df: pd.DataFrame = None,
        observacoes: str = ""
    ) -> str:
        """
        Gera relatório PDF de conformidade
        
        Args:
            filename: Nome do arquivo PDF
            total_produtos: Total de produtos analisados
            ncms_unicos: Total de NCMs únicos
            ncms_problemas: Total de NCMs com problemas
            percentual_conformidade: Percentual de conformidade
            problemas_df: DataFrame com detalhes dos problemas
            observacoes: Observações adicionais
            
        Returns:
            Caminho do arquivo gerado
        """
        # Cria documento
        doc = SimpleDocTemplate(
            filename,
            pagesize=A4,
            rightMargin=72,
            leftMargin=72,
            topMargin=72,
            bottomMargin=72
        )
        
        # Container para elementos
        elements = []
        
        # Cabeçalho
        elements.append(Paragraph("🐾 Relatório de Conformidade Fiscal NCM", self.styles['CustomTitle']))
        elements.append(Paragraph("Setor Pet - Validação de Notas Fiscais", self.styles['CustomHeading']))
        elements.append(Spacer(1, 0.2*inch))
        
        # Data
        data_atual = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        elements.append(Paragraph(f"<b>Data de Geração:</b> {data_atual}", self.styles['CustomBody']))
        elements.append(Spacer(1, 0.3*inch))
        
        # Resumo Executivo
        elements.append(Paragraph("RESUMO EXECUTIVO", self.styles['CustomHeading']))
        
        # Tabela de métricas
        metricas_data = [
            ['Métrica', 'Valor'],
            ['Total de Produtos Analisados', str(total_produtos)],
            ['NCMs Únicos', str(ncms_unicos)],
            ['Produtos com Problemas', str(ncms_problemas)],
            ['Produtos em Conformidade', str(total_produtos - ncms_problemas)],
            ['Percentual de Conformidade', f"{percentual_conformidade:.1f}%"]
        ]
        
        metricas_table = Table(metricas_data, colWidths=[3.5*inch, 2*inch])
        metricas_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#4CAF50')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 10),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgrey]),
        ]))
        
        elements.append(metricas_table)
        elements.append(Spacer(1, 0.3*inch))
        
        # Status de Conformidade
        if percentual_conformidade >= 95:
            status = "✅ EXCELENTE"
            cor_status = colors.green
            msg_status = "As notas fiscais estão em excelente conformidade."
        elif percentual_conformidade >= 80:
            status = "⚠️ BOM"
            cor_status = colors.orange
            msg_status = "Algumas correções menores são necessárias."
        else:
            status = "❌ REQUER ATENÇÃO"
            cor_status = colors.red
            msg_status = "Múltiplos problemas foram identificados e requerem correção imediata."
        
        elements.append(Paragraph(f"<b>Status:</b> <font color='{cor_status}'>{status}</font>", 
                                 self.styles['CustomBody']))
        elements.append(Paragraph(msg_status, self.styles['CustomBody']))
        elements.append(Spacer(1, 0.3*inch))
        
        # Detalhes dos Problemas
        if problemas_df is not None and len(problemas_df) > 0:
            elements.append(PageBreak())
            elements.append(Paragraph("DETALHAMENTO DOS PROBLEMAS", self.styles['CustomHeading']))
            elements.append(Spacer(1, 0.2*inch))
            
            # Converte DataFrame para lista
            problemas_data = [problemas_df.columns.tolist()]
            for idx, row in problemas_df.iterrows():
                problemas_data.append([str(val)[:50] for val in row.tolist()])  # Limita tamanho
            
            # Cria tabela de problemas
            if len(problemas_data) > 1:
                problemas_table = Table(problemas_data, colWidths=[1.2*inch] * len(problemas_df.columns))
                problemas_table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#f44336')),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, 0), (-1, 0), 10),
                    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                    ('GRID', (0, 0), (-1, -1), 1, colors.black),
                    ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
                    ('FONTSIZE', (0, 1), (-1, -1), 8),
                    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgrey]),
                    ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                ]))
                
                elements.append(problemas_table)
        else:
            elements.append(Paragraph(
                "✅ <b>Nenhum problema encontrado!</b> Todas as notas fiscais estão em conformidade.",
                self.styles['CustomBody']
            ))
        
        elements.append(Spacer(1, 0.3*inch))
        
        # Ações Recomendadas
        elements.append(PageBreak())
        elements.append(Paragraph("AÇÕES RECOMENDADAS", self.styles['CustomHeading']))
        
        acoes = [
            "1. <b>Imediato:</b> Corrija os NCMs críticos antes de emitir novas notas fiscais.",
            "2. <b>Curto Prazo (7 dias):</b> Revise e corrija NCMs com problemas de alta severidade.",
            "3. <b>Médio Prazo (30 dias):</b> Implemente processo de validação preventiva.",
            "4. <b>Consultoria:</b> Entre em contato com contador para casos complexos.",
            "5. <b>Treinamento:</b> Capacite equipe sobre classificação fiscal de produtos pet.",
        ]
        
        for acao in acoes:
            elements.append(Paragraph(acao, self.styles['CustomBody']))
        
        elements.append(Spacer(1, 0.3*inch))
        
        # Observações
        if observacoes:
            elements.append(Paragraph("OBSERVAÇÕES ADICIONAIS", self.styles['CustomHeading']))
            elements.append(Paragraph(observacoes, self.styles['CustomBody']))
        
        # Rodapé
        elements.append(Spacer(1, 0.5*inch))
        elements.append(Paragraph(
            "<i>Este relatório foi gerado automaticamente pelo Sistema de Conformidade Fiscal NCM. "
            "Consulte um profissional contábil para orientações específicas.</i>",
            self.styles['CustomBody']
        ))
        
        # Gera PDF
        doc.build(elements)
        
        return filename


# Instância global
pdf_generator = PDFReportGenerator()
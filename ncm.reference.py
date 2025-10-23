"""
Módulo para carregar e consultar tabela de referência de NCMs do setor pet
"""
import pandas as pd
import os
from typing import Optional, List, Dict

class NCMReference:
    """Classe para gerenciar a tabela de referência de NCMs"""
    
    def __init__(self, csv_path: str = "ncm_petshop.csv"):
        self.csv_path = csv_path
        self.df_reference = None
        self.load_reference()
    
    def load_reference(self) -> bool:
        """Carrega o arquivo CSV de referência"""
        try:
            if not os.path.exists(self.csv_path):
                print(f"⚠️ Arquivo {self.csv_path} não encontrado. Usando lista padrão.")
                return False
            
            self.df_reference = pd.read_csv(self.csv_path)
            
            # Normaliza a coluna de NCM
            if 'Código NCM' in self.df_reference.columns:
                self.df_reference['NCM_normalizado'] = (
                    self.df_reference['Código NCM']
                    .astype(str)
                    .str.replace('.', '')
                    .str.replace('-', '')
                    .str.strip()
                )
            
            print(f"✅ Carregados {len(self.df_reference)} NCMs de referência")
            return True
            
        except Exception as e:
            print(f"❌ Erro ao carregar referência: {e}")
            return False
    
    def get_all_valid_ncms(self) -> List[str]:
        """Retorna lista de todos os NCMs válidos"""
        if self.df_reference is None:
            return []
        return self.df_reference['NCM_normalizado'].tolist()
    
    def get_ncm_info(self, ncm: str) -> Optional[Dict]:
        """Retorna informações sobre um NCM específico"""
        if self.df_reference is None:
            return None
        
        # Normaliza o NCM consultado
        ncm_norm = str(ncm).replace('.', '').replace('-', '').strip()
        
        # Busca no DataFrame
        result = self.df_reference[self.df_reference['NCM_normalizado'] == ncm_norm]
        
        if result.empty:
            return None
        
        row = result.iloc[0]
        return {
            'ncm': row.get('Código NCM', ncm_norm),
            'categoria': row.get('Categoria', 'N/A'),
            'descricao': row.get('Produto/Descrição Exemplo', 'N/A'),
            'observacoes': row.get('Observações', 'N/A')
        }
    
    def search_by_description(self, keyword: str) -> List[Dict]:
        """Busca NCMs pela descrição do produto"""
        if self.df_reference is None:
            return []
        
        keyword_lower = keyword.lower()
        results = self.df_reference[
            self.df_reference['Produto/Descrição Exemplo'].str.lower().str.contains(keyword_lower, na=False) |
            self.df_reference['Categoria'].str.lower().str.contains(keyword_lower, na=False)
        ]
        
        return [
            {
                'ncm': row['Código NCM'],
                'categoria': row['Categoria'],
                'descricao': row['Produto/Descrição Exemplo'],
                'observacoes': row.get('Observações', 'N/A')
            }
            for _, row in results.iterrows()
        ]
    
    def get_category_ncms(self, category: str) -> List[Dict]:
        """Retorna todos os NCMs de uma categoria específica"""
        if self.df_reference is None:
            return []
        
        results = self.df_reference[
            self.df_reference['Categoria'].str.lower() == category.lower()
        ]
        
        return [
            {
                'ncm': row['Código NCM'],
                'descricao': row['Produto/Descrição Exemplo'],
                'observacoes': row.get('Observações', 'N/A')
            }
            for _, row in results.iterrows()
        ]
    
    def get_reference_summary(self) -> str:
        """Retorna um resumo formatado da tabela de referência"""
        if self.df_reference is None:
            return "Tabela de referência não carregada."
        
        summary = "📋 TABELA DE REFERÊNCIA DE NCMs - SETOR PET\n\n"
        
        # Agrupa por categoria
        for categoria in self.df_reference['Categoria'].unique():
            summary += f"## {categoria}\n\n"
            categoria_df = self.df_reference[self.df_reference['Categoria'] == categoria]
            
            for _, row in categoria_df.iterrows():
                ncm = row['Código NCM']
                descricao = row['Produto/Descrição Exemplo']
                obs = row.get('Observações', '')
                
                summary += f"- **{ncm}**: {descricao}\n"
                if obs and obs != 'N/A':
                    summary += f"  _{obs}_\n"
            
            summary += "\n"
        
        return summary
    
    def validate_ncm(self, ncm: str) -> Dict:
        """Valida um NCM e retorna informações detalhadas"""
        ncm_norm = str(ncm).replace('.', '').replace('-', '').strip()
        
        # Verifica formato
        if len(ncm_norm) != 8 or not ncm_norm.isdigit():
            return {
                'valido': False,
                'motivo': 'Formato inválido - NCM deve ter 8 dígitos numéricos',
                'ncm': ncm
            }
        
        # Verifica se está na tabela de referência
        info = self.get_ncm_info(ncm_norm)
        
        if info:
            return {
                'valido': True,
                'ncm': info['ncm'],
                'categoria': info['categoria'],
                'descricao': info['descricao'],
                'observacoes': info['observacoes'],
                'motivo': 'NCM válido e adequado para o setor pet'
            }
        else:
            return {
                'valido': False,
                'ncm': ncm,
                'motivo': 'NCM não encontrado na tabela de referência do setor pet',
                'sugestao': 'Consulte a tabela de referência ou verifique se o NCM está correto'
            }


# Instância global para ser usada pelo agente
ncm_ref = NCMReference()


def get_valid_ncms_list() -> str:
    """Retorna lista formatada de NCMs válidos para usar no prompt"""
    if ncm_ref.df_reference is None:
        return "Tabela de referência não disponível"
    
    ncms = ncm_ref.df_reference['NCM_normalizado'].unique()
    return ", ".join(ncms)


def get_ncm_reference_for_prompt() -> str:
    """Retorna referência formatada para incluir no prompt do agente"""
    if ncm_ref.df_reference is None:
        return "Tabela de referência não carregada"
    
    prompt_text = "=== TABELA DE REFERÊNCIA DE NCMs VÁLIDOS PARA SETOR PET ===\n\n"
    
    for categoria in ncm_ref.df_reference['Categoria'].unique():
        prompt_text += f"{categoria.upper()}:\n"
        categoria_df = ncm_ref.df_reference[ncm_ref.df_reference['Categoria'] == categoria]
        
        for _, row in categoria_df.iterrows():
            ncm_norm = row['NCM_normalizado']
            ncm_format = row['Código NCM']
            descricao = row['Produto/Descrição Exemplo'][:60]  # Limita tamanho
            
            prompt_text += f"  - {ncm_norm} ({ncm_format}): {descricao}\n"
        
        prompt_text += "\n"
    
    return prompt_text
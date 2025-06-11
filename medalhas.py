import customtkinter as ctk
from tkinter import messagebox, ttk
import pandas as pd
import re
import random

import tkinter as tk
from difflib import SequenceMatcher

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class OlympicMedalsViewer:
    
    ############################################################################################################    cria a interface
    
    def __init__(self, root):
        self.root = root
        self.root.title("🏆 Visualizador de Medalhas Olímpicas - IA Dinâmica")
        self.root.geometry("1200x800")
        
        # Estados e dados
        self.tabela_visivel = False
        self.df = self.carregar_dados()
        self.anos_disponiveis = sorted(self.df['year'].unique()) if not self.df.empty else []
        self.paises_disponiveis = sorted(self.df['country'].unique()) if not self.df.empty else []
        self.placeholder_ativo = True

        self.todos_paises = {
            'afeganistão': 'Afghanistan', 'áfrica do sul': 'South Africa', 'albânia': 'Albania',
            'alemanha': 'Germany', 'andorra': 'Andorra', 'angola': 'Angola',
            'antígua e barbuda': 'Antigua and Barbuda', 'arábia saudita': 'Saudi Arabia',
            'argélia': 'Algeria', 'argentina': 'Argentina', 'armênia': 'Armenia',
            'aruba': 'Aruba', 'austrália': 'Australia', 'áustria': 'Austria',
            'azerbaijão': 'Azerbaijan', 'bahamas': 'Bahamas', 'bahrein': 'Bahrain',
            'bangladesh': 'Bangladesh', 'barbados': 'Barbados', 'belarus': 'Belarus',
            'bélgica': 'Belgium', 'belize': 'Belize', 'benin': 'Benin',
            'bermudas': 'Bermuda', 'butão': 'Bhutan', 'bolívia': 'Bolivia',
            'bósnia e herzegovina': 'Bosnia and Herzegovina', 'botsuana': 'Botswana',
            'brasil': 'Brazil', 'brunei': 'Brunei Darussalam', 'bulgária': 'Bulgaria',
            'burkina faso': 'Burkina Faso', 'burundi': 'Burundi', 'cabo verde': 'Cape Verde',
            'camarões': 'Cameroon', 'camboja': 'Cambodia', 'canadá': 'Canada',
            'catar': 'Qatar', 'cazaquistão': 'Kazakhstan', 'chade': 'Chad',
            'chile': 'Chile', 'china': 'China', 'chipre': 'Cyprus',
            'cingapura': 'Singapore', 'colômbia': 'Colombia', 'comores': 'Comoros',
            'congo': 'Congo', 'coreia do norte': 'North Korea', 'coreia do sul': 'South Korea',
            'costa do marfim': 'Ivory Coast', 'costa rica': 'Costa Rica', 'croácia': 'Croatia',
            'cuba': 'Cuba', 'dinamarca': 'Denmark', 'djibuti': 'Djibouti',
            'dominica': 'Dominica', 'egito': 'Egypt', 'el salvador': 'El Salvador',
            'emirados árabes unidos': 'United Arab Emirates', 'equador': 'Ecuador',
            'eritreia': 'Eritrea', 'eslováquia': 'Slovakia', 'eslovênia': 'Slovenia',
            'espanha': 'Spain', 'estados unidos': 'United States', 'estônia': 'Estonia',
            'essuatíni': 'Eswatini', 'etiópia': 'Ethiopia', 'fiji': 'Fiji',
            'filipinas': 'Philippines', 'finlândia': 'Finland', 'frança': 'France',
            'gabão': 'Gabon', 'gâmbia': 'Gambia', 'gana': 'Ghana',
            'geórgia': 'Georgia', 'granada': 'Grenada', 'grécia': 'Greece',
            'guatemala': 'Guatemala', 'guiana': 'Guyana', 'guiné': 'Guinea',
            'guiné-bissau': 'Guinea-Bissau', 'guiné equatorial': 'Equatorial Guinea',
            'haiti': 'Haiti', 'honduras': 'Honduras', 'hong kong': 'Hong Kong',
            'hungria': 'Hungary', 'iêmen': 'Yemen', 'ilhas cook': 'Cook Islands',
            'ilhas marshall': 'Marshall Islands', 'ilhas salomão': 'Solomon Islands',
            'índia': 'India', 'indonésia': 'Indonesia', 'irã': 'Iran',
            'iraque': 'Iraq', 'irlanda': 'Ireland', 'islândia': 'Iceland',
            'israel': 'Israel', 'itália': 'Italy', 'jamaica': 'Jamaica',
            'japão': 'Japan', 'jordânia': 'Jordan', 'kiribati': 'Kiribati',
            'kosovo': 'Kosovo', 'kuwait': 'Kuwait', 'laos': 'Laos',
            'lesoto': 'Lesotho', 'letônia': 'Latvia', 'líbano': 'Lebanon',
            'libéria': 'Liberia', 'líbia': 'Libya', 'liechtenstein': 'Liechtenstein',
            'lituânia': 'Lithuania', 'luxemburgo': 'Luxembourg', 'macedônia do norte': 'North Macedonia',
            'madagascar': 'Madagascar', 'malásia': 'Malaysia', 'maláui': 'Malawi',
            'maldivas': 'Maldives', 'mali': 'Mali', 'malta': 'Malta',
            'marrocos': 'Morocco', 'maurício': 'Mauritius', 'mauritânia': 'Mauritania',
            'méxico': 'Mexico', 'micronésia': 'Micronesia', 'mônaco': 'Monaco',
            'mongólia': 'Mongolia', 'montenegro': 'Montenegro', 'moçambique': 'Mozambique',
            'mianmar': 'Myanmar', 'namíbia': 'Namibia', 'nauru': 'Nauru',
            'nepal': 'Nepal', 'nicarágua': 'Nicaragua', 'níger': 'Niger',
            'nigéria': 'Nigeria', 'noruega': 'Norway', 'nova zelândia': 'New Zealand',
            'omã': 'Oman', 'países baixos': 'Netherlands', 'palau': 'Palau',
            'panamá': 'Panama', 'papua-nova guiné': 'Papua New Guinea', 'paquistão': 'Pakistan',
            'paraguai': 'Paraguay', 'peru': 'Peru', 'polônia': 'Poland',
            'portugal': 'Portugal', 'quênia': 'Kenya', 'quirguistão': 'Kyrgyzstan',
            'reino unido': 'Great Britain', 'república centro-africana': 'Central African Republic',
            'república dominicana': 'Dominican Republic', 'república tcheca': 'Czech Republic',
            'romênia': 'Romania', 'ruanda': 'Rwanda', 'rússia': 'Russia',
            'samoa': 'Samoa', 'san marino': 'San Marino', 'santa lúcia': 'Saint Lucia',
            'são cristóvão e nevis': 'Saint Kitts and Nevis', 'são tomé e príncipe': 'Sao Tome and Principe',
            'são vicente e granadinas': 'Saint Vincent and the Grenadines', 'senegal': 'Senegal',
            'serra leoa': 'Sierra Leone', 'sérvia': 'Serbia', 'seychelles': 'Seychelles',
            'síria': 'Syria', 'somália': 'Somalia', 'sri lanka': 'Sri Lanka',
            'sudão': 'Sudan', 'sudão do sul': 'South Sudan', 'suécia': 'Sweden',
            'suíça': 'Switzerland', 'suriname': 'Suriname', 'tailândia': 'Thailand',
            'taiwan': 'Chinese Taipei', 'tajiquistão': 'Tajikistan', 'tanzânia': 'Tanzania',
            'timor-leste': 'Timor-Leste', 'togo': 'Togo', 'tonga': 'Tonga',
            'trinidad e tobago': 'Trinidad and Tobago', 'tunísia': 'Tunisia',
            'turcomenistão': 'Turkmenistan', 'turquia': 'Turkey', 'tuvalu': 'Tuvalu',
            'ucrânia': 'Ukraine', 'uganda': 'Uganda', 'uruguai': 'Uruguay',
            'uzbequistão': 'Uzbekistan', 'vanuatu': 'Vanuatu', 'venezuela': 'Venezuela',
            'vietnã': 'Vietnam', 'zâmbia': 'Zambia', 'zimbábue': 'Zimbabwe',
            
            # Nomes alternativos e abreviações
            'eua': 'United States', 'usa': 'United States', 'america': 'United States',
            'uk': 'Great Britain', 'grã-bretanha': 'Great Britain', 'inglaterra': 'Great Britain',
            'coreia': 'South Korea', 'russia': 'Russia', 'urss': 'Russia',
            'holanda': 'Netherlands', 'birmânia': 'Myanmar', 'ceilão': 'Sri Lanka',
            'persia': 'Iran', 'sião': 'Thailand', 'rodésia': 'Zimbabwe',
            'zaire': 'Democratic Republic of the Congo', 'tchecoslováquia': 'Czech Republic',
            'iugoslávia': 'Serbia', 'alemanha oriental': 'Germany', 'alemanha ocidental': 'Germany'
        }
        
        # NOC de cada país
        self.nocs = {
            'AFG': 'Afghanistan', 'RSA': 'South Africa', 'ALB': 'Albania', 'GER': 'Germany',
            'AND': 'Andorra', 'ANG': 'Angola', 'ANT': 'Antigua and Barbuda', 'KSA': 'Saudi Arabia',
            'ALG': 'Algeria', 'ARG': 'Argentina', 'ARM': 'Armenia', 'ARU': 'Aruba',
            'AUS': 'Australia', 'AUT': 'Austria', 'AZE': 'Azerbaijan', 'BAH': 'Bahamas',
            'BRN': 'Bahrain', 'BAN': 'Bangladesh', 'BAR': 'Barbados', 'BLR': 'Belarus',
            'BEL': 'Belgium', 'BIZ': 'Belize', 'BEN': 'Benin', 'BER': 'Bermuda',
            'BHU': 'Bhutan', 'BOL': 'Bolivia', 'BIH': 'Bosnia and Herzegovina', 'BOT': 'Botswana',
            'BRA': 'Brazil', 'BRU': 'Brunei Darussalam', 'BUL': 'Bulgaria', 'BUR': 'Burkina Faso',
            'BDI': 'Burundi', 'CPV': 'Cape Verde', 'CMR': 'Cameroon', 'CAM': 'Cambodia',
            'CAN': 'Canada', 'QAT': 'Qatar', 'KAZ': 'Kazakhstan', 'CHA': 'Chad',
            'CHI': 'Chile', 'CHN': 'China', 'CYP': 'Cyprus', 'SGP': 'Singapore',
            'COL': 'Colombia', 'COM': 'Comoros', 'CGO': 'Congo', 'PRK': 'North Korea',
            'KOR': 'South Korea', 'CIV': 'Ivory Coast', 'CRC': 'Costa Rica', 'CRO': 'Croatia',
            'CUB': 'Cuba', 'DEN': 'Denmark', 'DJI': 'Djibouti', 'DMA': 'Dominica',
            'EGY': 'Egypt', 'ESA': 'El Salvador', 'UAE': 'United Arab Emirates', 'ECU': 'Ecuador',
            'ERI': 'Eritrea', 'SVK': 'Slovakia', 'SLO': 'Slovenia', 'ESP': 'Spain',
            'USA': 'United States', 'EST': 'Estonia', 'SWZ': 'Eswatini', 'ETH': 'Ethiopia',
            'FIJ': 'Fiji', 'PHI': 'Philippines', 'FIN': 'Finland', 'FRA': 'France',
            'GAB': 'Gabon', 'GAM': 'Gambia', 'GHA': 'Ghana', 'GEO': 'Georgia',
            'GRN': 'Grenada', 'GRE': 'Greece', 'GUA': 'Guatemala', 'GUY': 'Guyana',
            'GUI': 'Guinea', 'GBS': 'Guinea-Bissau', 'GEQ': 'Equatorial Guinea', 'HAI': 'Haiti',
            'HON': 'Honduras', 'HKG': 'Hong Kong', 'HUN': 'Hungary', 'YEM': 'Yemen',
            'COK': 'Cook Islands', 'MHL': 'Marshall Islands', 'SOL': 'Solomon Islands',
            'IND': 'India', 'INA': 'Indonesia', 'IRI': 'Iran', 'IRQ': 'Iraq',
            'IRL': 'Ireland', 'ISL': 'Iceland', 'ISR': 'Israel', 'ITA': 'Italy',
            'JAM': 'Jamaica', 'JPN': 'Japan', 'JOR': 'Jordan', 'KIR': 'Kiribati',
            'KOS': 'Kosovo', 'KUW': 'Kuwait', 'LAO': 'Laos', 'LES': 'Lesotho',
            'LAT': 'Latvia', 'LBN': 'Lebanon', 'LBR': 'Liberia', 'LBA': 'Libya',
            'LIE': 'Liechtenstein', 'LTU': 'Lithuania', 'LUX': 'Luxembourg', 'MKD': 'North Macedonia',
            'MAD': 'Madagascar', 'MAS': 'Malaysia', 'MAW': 'Malawi', 'MDV': 'Maldives',
            'MLI': 'Mali', 'MLT': 'Malta', 'MAR': 'Morocco', 'MRI': 'Mauritius',
            'MTN': 'Mauritania', 'MEX': 'Mexico', 'FSM': 'Micronesia', 'MON': 'Monaco',
            'MGL': 'Mongolia', 'MNE': 'Montenegro', 'MOZ': 'Mozambique', 'MYA': 'Myanmar',
            'NAM': 'Namibia', 'NRU': 'Nauru', 'NEP': 'Nepal', 'NCA': 'Nicaragua',
            'NIG': 'Niger', 'NGR': 'Nigeria', 'NOR': 'Norway', 'NZL': 'New Zealand',
            'OMA': 'Oman', 'NED': 'Netherlands', 'PLW': 'Palau', 'PAN': 'Panama',
            'PNG': 'Papua New Guinea', 'PAK': 'Pakistan', 'PAR': 'Paraguay', 'PER': 'Peru',
            'POL': 'Poland', 'POR': 'Portugal', 'KEN': 'Kenya', 'KGZ': 'Kyrgyzstan',
            'GBR': 'Great Britain', 'CAF': 'Central African Republic', 'DOM': 'Dominican Republic',
            'CZE': 'Czech Republic', 'ROU': 'Romania', 'RWA': 'Rwanda', 'RUS': 'Russia',
            'SAM': 'Samoa', 'SMR': 'San Marino', 'LCA': 'Saint Lucia', 'SKN': 'Saint Kitts and Nevis',
            'STP': 'Sao Tome and Principe', 'VIN': 'Saint Vincent and the Grenadines',
            'SEN': 'Senegal', 'SLE': 'Sierra Leone', 'SRB': 'Serbia', 'SEY': 'Seychelles',
            'SYR': 'Syria', 'SOM': 'Somalia', 'SRI': 'Sri Lanka', 'SUD': 'Sudan',
            'SSD': 'South Sudan', 'SWE': 'Sweden', 'SUI': 'Switzerland', 'SUR': 'Suriname',
            'THA': 'Thailand', 'TPE': 'Chinese Taipei', 'TJK': 'Tajikistan', 'TAN': 'Tanzania',
            'TLS': 'Timor-Leste', 'TOG': 'Togo', 'TGA': 'Tonga', 'TTO': 'Trinidad and Tobago',
            'TUN': 'Tunisia', 'TKM': 'Turkmenistan', 'TUR': 'Turkey', 'TUV': 'Tuvalu',
            'UKR': 'Ukraine', 'UGA': 'Uganda', 'URU': 'Uruguay', 'UZB': 'Uzbekistan',
            'VAN': 'Vanuatu', 'VEN': 'Venezuela', 'VIE': 'Vietnam', 'ZAM': 'Zambia',
            'ZIM': 'Zimbabwe'
        }
        
        # Configurações 
        self.config = {
            'palavras_chave': {
                'ano': {'ano', 'year', 'edicao', 'edição', 'quando', 'tempo', 'periodo', 'período'},
                'pais': {'pais', 'país', 'country', 'nacao', 'nação', 'nacionalidade', 'onde'},
                'medalha': {'medalha', 'medal', 'premio', 'prêmio', 'conquista', 'vitoria', 'vitória'},
                'ouro': {'ouro', 'gold', 'primeiro', '1º', 'campeao', 'campeão', 'dourada'},
                'prata': {'prata', 'silver', 'segundo', '2º', 'prateada'},
                'bronze': {'bronze', 'terceiro', '3º', 'bronzeada'},
                'total': {'total', 'soma', 'tudo', 'todos', 'todas', 'geral', 'completo'},
                'mais': {'mais', 'maior', 'maximo', 'máximo', 'top', 'melhor', 'superior'},
                'menos': {'menos', 'menor', 'minimo', 'mínimo', 'pior', 'inferior'},
                'ranking': {'ranking', 'classificacao', 'classificação', 'posicao', 'posição', 'lista'},
                'comparar': {'comparar', 'versus', 'vs', 'contra', 'diferença', 'comparação'},
                'sem': {'sem', 'nenhum', 'zero', 'não', 'nunca', 'ausencia', 'ausência'},
                'competitivo': {'competitivo', 'competição', 'disputa', 'concorrencia', 'concorrência'},
                'historico': {'historico', 'histórico', 'historia', 'história', 'evolucao', 'evolução'}
            },
            'cores': {
                'primaria': "#3b82f6", 'secundaria': "#00ff88", 'perigo': "#dc2626",
                'sucesso': "#16a34a", 'aviso': "#fbbf24", 'roxo': "#7c3aed", 'cinza': "#6b7280"
            },
            'textos': {
                'placeholder': "Digite sua pergunta aqui...",
                'aguardando': "💭 Aguardando pergunta...",
                'processando': "🔄 Processando pergunta...",
                'erro_pergunta': "❌ Digite uma pergunta primeiro!",
                'sem_resultado': "❌ Nenhum resultado encontrado",
                'crud_ativo': "🔧 Sistema CRUD ativo",
                'exemplo_carregado': "💡 Exemplo carregado! Clique em 'Processar Pergunta'"
            },
            'exemplos': [
                "Qual país ganhou mais medalhas de ouro em 2016?",
                "Top 5 países com mais medalhas total",
                "Mostre países sem medalha de ouro",
                "Histórico de medalhas do Brasil",
                "Países com menos medalhas de prata",
                "Ranking dos 15 melhores países em medalhas",
                "Quais países nunca ganharam bronze?",
                "Quais foram os países com a pior classificação em medalhas de ouro em 2004?",
                "Lista dos países com máximo de medalhas de bronze em 2012",
                "Histórico competitivo do Japão nas Olimpíadas",
                "Quem conquistou o maior número de medalhas em 2008?",
            ]
        }
        
        self.criar_interface()
    
    def criar_interface(self): # Scroll, Titulo, sistema de pesquisa e botao para mostrar a tabela 
        # Scroll
        self.main_frame = ctk.CTkScrollableFrame(self.root, fg_color="#0d1117")
        self.main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Título da página
        ctk.CTkLabel(self.main_frame, text="🏆 ANÁLISE DE MEDALHAS OLÍMPICAS", 
                    font=ctk.CTkFont(size=28, weight="bold"), text_color=self.config['cores']['primaria']).pack(pady=(0, 30))
        
        # Sistemas de pesquisa e gerenciamento do dataset
        self.criar_sistema_de_consulta()
        self.criar_sistema_crud()
        
        # Botão para mostrar e ocultar a tabela no final da interface
        self.botao_tabela = ctk.CTkButton(self.main_frame, text="📋 Mostrar Tabela Completa",
                                         command=self.alternar_tabela, width=200, height=45,
                                         fg_color="#1f538d", corner_radius=25)
        self.botao_tabela.pack(pady=30)
        
        self.criar_tabela()
    
    def criar_card(self, titulo, cor_borda, cor_titulo): # Cards com a interface de perguntas e gerenciamento do CRUD
        
        # Cards com a interface de perguntas e gerenciamento do CRUD
        card = ctk.CTkFrame(self.main_frame, fg_color="#161b22", border_color=cor_borda, 
                           border_width=2, corner_radius=15)
        card.pack(fill="x", pady=15, padx=10)
        
        ctk.CTkLabel(card, text=titulo, font=ctk.CTkFont(size=18, weight="bold"), 
                    text_color=cor_titulo).pack(anchor="w", padx=20, pady=(20, 10))
        
        content = ctk.CTkFrame(card, fg_color="transparent")
        content.pack(fill="x", padx=20, pady=(0, 20))
        return content
    
    def criar_sistema_de_consulta(self): # Campo de pesquisa, exemplos e botoes para a pesquisa 
        content = self.criar_card("🤖 CONSULTA INTELIGENTE", "#1f538d", self.config['cores']['secundaria'])
        
        # Campo de entrada da pergunta
        ctk.CTkLabel(content, text="💬 Digite sua pergunta sobre medalhas olímpicas:", 
                    font=ctk.CTkFont(size=14), text_color="#e6edf3").pack(anchor="w", pady=(0, 5))
        
        # Exemplos de perguntas 
        exemplos_text = "Exemplos: 'Qual país ganhou mais medalhas de ouro?' | 'Top 5 países com mais medalhas total' | 'Países sem medalha de ouro'"
        ctk.CTkLabel(content, text=exemplos_text, font=ctk.CTkFont(size=11), 
                    text_color=self.config['cores']['cinza'], wraplength=750).pack(anchor="w", pady=(0, 10))
        
        self.entry_pergunta = ctk.CTkTextbox(content, height=80, width=800)
        self.entry_pergunta.pack(fill="x", pady=(0, 15))
        self.entry_pergunta.insert("1.0", self.config['textos']['placeholder'])
        self.entry_pergunta.bind("<FocusIn>", self.limpar_placeholder)
        
        # Botões
        botoes_frame = ctk.CTkFrame(content, fg_color="transparent")
        botoes_frame.pack(fill="x", pady=10)
        
        botoes_config = [
            ("🔍 Processar Pergunta", self.processar_pergunta, self.config['cores']['secundaria'], 150),
            ("💡 Exemplos", self.mostrar_exemplos, self.config['cores']['aviso'], 120),
            ("🔄 Limpar", self.limpar_consulta, self.config['cores']['cinza'], 100)
        ]
        
        for texto, comando, cor, largura in botoes_config:
            btn = self.criar_botao(botoes_frame, texto, comando, cor, largura)
            if cor in [self.config['cores']['secundaria'], self.config['cores']['aviso']]:
                btn.configure(text_color="black")
            btn.pack(side="left", padx=10)
        
        # Status da consulta
        self.status_consulta = ctk.CTkLabel(content, text=self.config['textos']['aguardando'], 
                                          text_color="#7d8590", font=ctk.CTkFont(size=12))
        self.status_consulta.pack(anchor="w", pady=(10, 0))
    
    def criar_sistema_crud(self): # Botoes e gerenciamendo do CRUD
        content = self.criar_card("⚙ GERENCIAMENTO DE DADOS", 
                                 self.config['cores']['perigo'], self.config['cores']['perigo'])
        
        # Botões do CRUD
        crud_frame = ctk.CTkFrame(content, fg_color="transparent")
        crud_frame.pack(fill="x", pady=10)
        
        botoes_crud = [
            ("➕ Adicionar Registro", self.adicionar_registro, self.config['cores']['sucesso']),
            ("✏ Editar Registro", self.editar_registro, self.config['cores']['primaria']),
            ("🗑 Remover Registro", self.remover_registro, self.config['cores']['perigo']),
            ("📊 Estatísticas", self.mostrar_estatisticas, self.config['cores']['roxo']),
        ]
        
        for i, (texto, comando, cor) in enumerate(botoes_crud):
            if i % 3 == 0:
                linha_frame = ctk.CTkFrame(crud_frame, fg_color="transparent")
                linha_frame.pack(fill="x", pady=5)
            
            self.criar_botao(linha_frame, texto, comando, cor, 180, 35).pack(side="left", padx=10)
        
        # Status do CRUD
        self.status_crud = ctk.CTkLabel(content, text=self.config['textos']['crud_ativo'], 
                                      text_color="#7d8590", font=ctk.CTkFont(size=12))
        self.status_crud.pack(anchor="w", pady=(15, 0))
    
    def criar_botao(self, parent, texto, comando, cor, largura=150, altura=40):
        return ctk.CTkButton(parent, text=texto, command=comando, fg_color=cor,
                           width=largura, height=altura)

    def carregar_dados(self): # Carrega os dados do arquilo xlsx
        try:
            return pd.read_excel("world_olympedia_olympics_game_medal_tally.xlsx")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao abrir o Excel: {e}")
            return pd.DataFrame()

    ############################################################################################################    consultas e  perguntas
    
    def processar_pergunta(self): # pega o texto digitado pelo usuario, verifica os resultados
        # pega o texto digitado pelo usuario
        pergunta = self.entry_pergunta.get("1.0", "end").strip().lower()
        
        # verifica se esta vaxio ou é o placeholder
        if not pergunta or pergunta == self.config['textos']['placeholder'].lower():
            self.atualizar_status(self.status_consulta, self.config['textos']['erro_pergunta'])
            return
        
        self.atualizar_status(self.status_consulta, self.config['textos']['processando'])
        
        try:
            analise = self.analisar_pergunta(pergunta)
            resultado = self.executar_consulta_unica(analise)
            
            # Verifica se o resultado da pergunta nao esta vazio
            if resultado is not None and not resultado.empty:
                self.mostrar_tabela()
                self.atualizar_treeview(resultado)
                self.root.after(100, lambda: self.main_frame._parent_canvas.yview_moveto(0.8))
                self.atualizar_status(self.status_consulta, f"✅ {analise['descricao']}")
            else:
                self.atualizar_status(self.status_consulta, self.config['textos']['sem_resultado'])
                
        except Exception as e:
            self.atualizar_status(self.status_consulta, f"❌ Erro: {str(e)}")

    def verificar_palavra_chave(self, pergunta, categoria): # verfica se existe alguma palavra chave na pergunta

        if categoria not in self.config['palavras_chave']:
            return False
        
        palavras_pergunta = set(re.findall(r'\b\w+\b', pergunta.lower()))
        palavras_categoria = self.config['palavras_chave'][categoria]
        
        return bool(palavras_pergunta.intersection(palavras_categoria))
      
    def analisar_pergunta(self, pergunta): # verifica o tipo de pesquisa e filtra por tipo 
        numeros = re.findall(r'\b\d{4}\b|\b\d{1,2}\b', pergunta)
        
        analise = {
            'tipo': 'geral',
            'filtros': {},
            'ordenacao': 'desc',
            'limite': 10,
            'descricao': 'Consulta geral'
        }
        
        # Detecta o tipo de consulta
        tipos_consulta = {
            'ranking': 'ranking',
            'comparar': 'comparacao',
            'sem': 'sem_medalha',
            'historico': 'historico'
        }
        
        for palavra_chave, tipo in tipos_consulta.items():
            if self.verificar_palavra_chave(pergunta, palavra_chave):
                analise['tipo'] = tipo
                break
        
        # Detecta o filtro por medalha
        medalhas = {'ouro': 'gold', 'prata': 'silver', 'bronze': 'bronze', 'total': 'total'}
        for medalha_tipo, medalha_valor in medalhas.items():
            if self.verificar_palavra_chave(pergunta, medalha_tipo):
                analise['filtros']['medalha'] = medalha_valor
                break
        
        # Detecta o ano
        anos_validos = [int(n) for n in numeros if len(n) == 4 and 1896 <= int(n) <= 2024]
        if anos_validos:
            analise['filtros']['ano'] = anos_validos[0]
        
        # Detectar país
        pais_detectado = self.filtrar_paises(pergunta)
        if pais_detectado:
            analise['filtros']['pais'] = pais_detectado
        
        # Detecta o limite e ordenação
        limites = [int(n) for n in numeros if len(n) <= 2 and 1 <= int(n) <= 50]
        if limites:
            analise['limite'] = limites[0]
        
        if self.verificar_palavra_chave(pergunta, 'menos'):
            analise['ordenacao'] = 'asc'
        
        analise['descricao'] = self.gerar_descricao(analise)
        return analise
    
    def executar_consulta_unica(self, analise): # verifica o tipo de consulta de maneira unica
        df_trabalho = self.aplicar_filtros(self.df.copy(), analise['filtros'])
        
        #  Tipos de consulta
        consultas = {
            'ranking': lambda: self.pesquisar_ranking(df_trabalho, analise),
            'sem_medalha': lambda: self.pesquisar_sem_medalha(df_trabalho, analise),
            'historico': lambda: self.pesquisar_historico(df_trabalho, analise),
            'comparacao': lambda: self.pesquisar_comparacao(df_trabalho, analise),
            'geral': lambda: self.pesquisar_geral(df_trabalho, analise)
        }
        
        return consultas.get(analise['tipo'], consultas['geral'])()
    
    def limpar_placeholder(self, event=None): # limpa o campo de pesquisa 
        if self.placeholder_ativo:
            self.entry_pergunta.delete("1.0", "end")
            self.placeholder_ativo = False

    ############################################################################################################    tipos de consulta
    
    def pesquisar_ranking(self, df, analise):
        return self.resultado_ordenado(df, analise)
    
    def pesquisar_sem_medalha(self, df, analise):
        medalha = analise['filtros'].get('medalha', 'gold')
        resumo = self.agrupar_medalhas(df, ['country', 'country_noc'])
        return resumo[resumo[medalha] == 0].sort_values(by='total', ascending=False)
    
    def pesquisar_historico(self, df, analise):
        if 'pais' in analise['filtros']:
            return df[df['country'] == analise['filtros']['pais']].sort_values(by='year')
        else:
            return self.agrupar_medalhas(df, ['year']).sort_values(by='year')
    
    def pesquisar_comparacao(self, df, analise):
        resumo = self.agrupar_medalhas(df, ['country', 'country_noc'])
        medalha = analise['filtros'].get('medalha', 'total')
        return resumo.sort_values(by=medalha, ascending=False).head(20)
    
    def pesquisar_geral(self, df, analise):
        return self.resultado_ordenado(df, analise)
    
    def resultado_ordenado(self, df, analise):
        medalha = analise['filtros'].get('medalha', 'total')
        resumo = self.agrupar_medalhas(df, ['country', 'country_noc'])
        ascending = analise['ordenacao'] == 'asc'
        return resumo.sort_values(by=medalha, ascending=ascending).head(analise['limite'])
    
    def gerar_descricao(self, analise): # gera a decriçao de acordo com o filtro
        componentes = []
        
        if analise['tipo'] == 'ranking':
            componentes.append(f"Top {analise['limite']}")
        elif analise['tipo'] == 'sem_medalha':
            componentes.append("Países sem medalhas")
        
        if 'medalha' in analise['filtros']:
            medalha_nome = {'gold': 'ouro', 'silver': 'prata', 'bronze': 'bronze', 'total': 'total'}
            componentes.append(f"de {medalha_nome[analise['filtros']['medalha']]}")
        
        if 'ano' in analise['filtros']:
            componentes.append(f"em {analise['filtros']['ano']}")
        
        if 'pais' in analise['filtros']:
            componentes.append(f"do {analise['filtros']['pais']}")
        
        return " ".join(componentes) if componentes else "Consulta processada"
    
    def mostrar_exemplos(self): # Mostra os exemplo de pergunta no momento da pesquisa 
        exemplo_escolhido = random.choice(self.config['exemplos'])
        self.entry_pergunta.delete("1.0", "end")
        self.entry_pergunta.insert("1.0", exemplo_escolhido)
        self.placeholder_ativo = False
        self.atualizar_status(self.status_consulta, self.config['textos']['exemplo_carregado'])
    
    ############################################################################################################    opcoes do CRUD
  
    def adicionar_registro(self):
        self.abrir_formulario(modo='adicionar')

    def editar_registro(self): # selecionar o pais e ano para editar
        if self.df.empty:
            messagebox.showerror("Erro", "Nenhum dado carregado.")
            return

        # Janela
        janela = ctk.CTkToplevel(self.root)
        janela.title("✏ Selecionar Registro para Edição")
        janela.geometry("500x650")
        janela.grab_set()

        ctk.CTkLabel(janela, text="🌍 Escolha o País", font=ctk.CTkFont(size=18, weight="bold")).pack(pady=10)
        frame_paises = ctk.CTkScrollableFrame(janela, height=200)
        frame_paises.pack(fill="both", expand=True, padx=20)

        def selecionar_pais(pais): # seleciona o pais para editar
            anos = sorted(self.df[self.df['country'] == pais]['year'].unique())
            frame_paises.pack_forget()
            label_pais.pack_forget()
            ctk.CTkLabel(janela, text=f"📅 Anos de {pais}", font=ctk.CTkFont(size=16, weight="bold")).pack(pady=10)
            frame_anos = ctk.CTkScrollableFrame(janela, height=200)
            frame_anos.pack(fill="both", expand=True, padx=20)

            def selecionar_ano(ano): # seleciona o ano que deseja editar
                cond = (self.df['country'] == pais) & (self.df['year'] == ano)
                if not any(cond):
                    messagebox.showerror("Erro", "Registro não encontrado.")
                    janela.destroy()
                    return
                indice = self.df[cond].index[0]
                janela.destroy()
                self.abrir_formulario(modo='editar', indice=indice)

            for ano in anos:
                ctk.CTkButton(frame_anos, text=str(ano), command=lambda a=ano: selecionar_ano(a),
                            fg_color="#3b82f6", width=150, height=35).pack(pady=4)

        label_pais = ctk.CTkLabel(janela, text="Selecione um país para editar", font=ctk.CTkFont(size=14))
        label_pais.pack()

        paises_unicos = sorted(self.df['country'].unique())
        for pais in paises_unicos:
            ctk.CTkButton(frame_paises, text=pais, command=lambda p=pais: selecionar_pais(p),
                        fg_color="#16a34a", width=300, height=35).pack(pady=3)

    def remover_registro(self): # selecionar o pais e o ano para remover
        if self.df.empty:
            messagebox.showerror("Erro", "Nenhum dado carregado.")
            return

        # janela
        janela = ctk.CTkToplevel(self.root)
        janela.title("🗑 Selecionar Registro para Remoção")
        janela.geometry("500x650")
        janela.grab_set()

        ctk.CTkLabel(janela, text="🌍 Escolha o País", font=ctk.CTkFont(size=18, weight="bold")).pack(pady=10)
        frame_paises = ctk.CTkScrollableFrame(janela, height=200)
        frame_paises.pack(fill="both", expand=True, padx=20)

        def selecionar_pais(pais): # seleciona o pais e o ano para remover
            anos = sorted(self.df[self.df['country'] == pais]['year'].unique())
            frame_paises.pack_forget()
            label_pais.pack_forget()
            ctk.CTkLabel(janela, text=f"📅 Anos de {pais}", font=ctk.CTkFont(size=16, weight="bold")).pack(pady=10)
            frame_anos = ctk.CTkScrollableFrame(janela, height=200)
            frame_anos.pack(fill="both", expand=True, padx=20)

            def confirmar_remocao(ano): # confirmar a remoçao
                cond = (self.df['country'] == pais) & (self.df['year'] == ano)
                if not any(cond):
                    messagebox.showerror("Erro", "Registro não encontrado.")
                    janela.destroy()
                    return
                indice = self.df[cond].index[0]
                registro = self.df.loc[indice]
                confirmar = messagebox.askyesno("Confirmar Remoção", f"Deseja remover {pais} ({ano})?\n\n🥇 {registro['gold']}  🥈 {registro['silver']}  🥉 {registro['bronze']}")
                if confirmar:
                    self.df = self.df.drop(index=indice).reset_index(drop=True)
                    self._salvar_e_atualizar(f"✅ Registro removido: {pais} ({ano})")
                    messagebox.showinfo("Sucesso", "Registro removido com sucesso.")
                    janela.destroy()

            for ano in anos:
                ctk.CTkButton(frame_anos, text=str(ano), command=lambda a=ano: confirmar_remocao(a),
                            fg_color="#dc2626", width=150, height=35).pack(pady=4)

        label_pais = ctk.CTkLabel(janela, text="Selecione um país para remover", font=ctk.CTkFont(size=14))
        label_pais.pack()

        paises_unicos = sorted(self.df['country'].unique())
        for pais in paises_unicos:
            ctk.CTkButton(frame_paises, text=pais, command=lambda p=pais: selecionar_pais(p),
                        fg_color="#f59e0b", text_color="black", width=300, height=35).pack(pady=3)
  
    def validar_selecao(self): # pede para abrir a tabela ou selecionar algum dado para editar ou remover 
        if not self.tabela_visivel:
            messagebox.showwarning("Atenção", "Mostre a tabela primeiro para selecionar um registro.")
            return False
        if not self.tree.selection():
            messagebox.showwarning("Atenção", "Selecione um registro.")
            return False
        return True

    def abrir_formulario(self, modo='adicionar', indice=None):
        if self.df.empty:
            messagebox.showerror("Erro", "Nenhum dado carregado. Verifique o arquivo Excel.")
            return
        
        configs = {
            'adicionar': {'titulo': "➕ NOVO REGISTRO OLÍMPICO", 'cor': "#16a34a", 'botao': "💾 Salvar Registro"},
            'editar': {'titulo': "✏ EDITAR REGISTRO OLÍMPICO", 'cor': "#3b82f6", 'botao': "💾 Salvar Edição"}
        }
        config = configs[modo]
        
        registro_atual = self.df.iloc[indice].copy() if modo == 'editar' else None
        
        # Cria a janela
        janela = ctk.CTkToplevel(self.root)
        janela.title(f"{config['titulo'].split()[0]} Registro")
        janela.geometry("500x650" if modo == 'editar' else "500x600")
        janela.transient(self.root)
        janela.grab_set()
        
        # interface
        ctk.CTkLabel(janela, text=config['titulo'], font=ctk.CTkFont(size=20, weight="bold"),
                    text_color=config['cor']).pack(pady=20)
        
        # info do registro
        if modo == 'editar':
            info_frame = ctk.CTkFrame(janela, fg_color="#1a1a1a", corner_radius=10)
            info_frame.pack(pady=(0, 15), padx=25, fill="x")
            info_text = f"🎯 Editando: {registro_atual.get('country', 'N/A')} - {registro_atual.get('year', 'N/A')}"
            ctk.CTkLabel(info_frame, text=info_text, font=ctk.CTkFont(size=14, weight="bold"), 
                        text_color="#fbbf24").pack(pady=10)
        
        # scroll
        frame_scroll = ctk.CTkScrollableFrame(janela, width=450, height=350)
        frame_scroll.pack(pady=10, padx=25, fill="both", expand=True)
        
        # campos
        entries = {}
        placeholders = {'year': "Ex: 2024", 'country': "Ex: Brazil", 'country_noc': "Ex: BRA", 
                    'gold': "0", 'silver': "0", 'bronze': "0"}
        
        for coluna in self.df.columns:
            campo_frame = ctk.CTkFrame(frame_scroll, fg_color="transparent")
            campo_frame.pack(fill="x", pady=8)
            
            ctk.CTkLabel(campo_frame, text=f"{coluna.replace('_', ' ').title()}:", 
                        font=ctk.CTkFont(size=14, weight="bold")).pack(anchor="w")
            
            entry = ctk.CTkEntry(campo_frame, width=400, height=35)
            entry.pack(pady=(5, 0))
            entries[coluna] = entry
            
            # preencher campo
            if modo == 'editar':
                valor = str(registro_atual[coluna]) if pd.notna(registro_atual[coluna]) else ""
                entry.insert(0, valor)
                if coluna == 'total':
                    entry.configure(state="disabled")
            else:
                if coluna in placeholders:
                    entry.insert(0, placeholders[coluna])
                elif coluna == 'total':
                    entry.configure(state="disabled")
        
        # botoes
        frame_botoes = ctk.CTkFrame(janela, fg_color="transparent")
        frame_botoes.pack(pady=20)
        
        def validar_e_salvar():
            try:
                registro = {}
                
                # Valida os campos
                for coluna, entry in entries.items():
                    if coluna == 'total': continue
                    
                    valor = entry.get().strip()
                    if not valor:
                        messagebox.showerror("Erro", f"Campo '{coluna.replace('_', ' ').title()}' é obrigatório!")
                        entry.focus()
                        return
                    if coluna == 'year':
                        try:
                            ano = int(valor)
                            if not (1896 <= ano <= 2030):
                                raise ValueError()
                            registro[coluna] = ano
                        except ValueError:
                            messagebox.showerror("Erro", "Ano deve ser entre 1896 e 2030!")
                            entry.focus()
                            return
                    elif coluna in ['gold', 'silver', 'bronze']:
                        try:
                            medalhas = int(valor)
                            if medalhas < 0:
                                raise ValueError()
                            registro[coluna] = medalhas
                        except ValueError:
                            messagebox.showerror("Erro", f"'{coluna.title()}' deve ser um número não negativo!")
                            entry.focus()
                            return
                    else:
                        if len(valor) < 2:
                            messagebox.showerror("Erro", f"'{coluna.replace('_', ' ').title()}' deve ter pelo menos 2 caracteres!")
                            entry.focus()
                            return
                        registro[coluna] = valor
                
                # Calcula o total
                registro['total'] = registro['gold'] + registro['silver'] + registro['bronze']
                
                # Verifica se à duplicatas
                condicao_duplicata = (self.df['country'] == registro['country']) & (self.df['year'] == registro['year'])
                if modo == 'editar':
                    condicao_duplicata &= (self.df.index != indice)
                
                if not self.df[condicao_duplicata].empty:
                    if not messagebox.askyesno("Duplicata", f"Já existe registro para {registro['country']} em {registro['year']}. Continuar?"):
                        return
                
                # salva o registro
                if modo == 'adicionar':
                    novo_registro = pd.DataFrame([registro])
                    self.df = pd.concat([self.df, novo_registro], ignore_index=True)
                    status_msg = f"✅ Registro adicionado: {registro['country']} ({registro['year']})"
                    sucesso_msg = "Registro adicionado com sucesso!"
                else:
                    mudancas = [f"{col}: {registro_atual[col]} → {registro[col]}" 
                            for col in registro.keys() if str(registro[col]) != str(registro_atual[col])]
                    
                    if not mudancas:
                        messagebox.showinfo("Info", "Nenhuma alteração foi feita.")
                        return
                    
                    if not messagebox.askyesno("Confirmar", f"Confirmar alterações?\n\n" + "\n".join(mudancas)):
                        return
                    for coluna, valor in registro.items():
                        dtype_original = self.df[coluna].dtype
                        if pd.api.types.is_integer_dtype(dtype_original):
                            valor = int(valor)
                        elif pd.api.types.is_float_dtype(dtype_original):
                            valor = float(valor)
                        else:
                            valor = str(valor)
                        self.df.iloc[indice, self.df.columns.get_loc(coluna)] = valor
                    
                    status_msg = f"✅ Registro editado: {registro['country']} ({registro['year']})"
                    sucesso_msg = f"Registro editado com sucesso!\n\nAlterações: {len(mudancas)}"
                
                # salva e atualiza
                self._salvar_e_atualizar(status_msg)
                messagebox.showinfo("Sucesso", f"{sucesso_msg}\n\nPaís: {registro['country']}\nAno: {registro['year']}\nMedalhas: {registro['gold']}🥇 {registro['silver']}🥈 {registro['bronze']}🥉")
                janela.destroy()
                
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao processar dados:\n{str(e)}")
        
        def limpar_campos():
            for coluna, entry in entries.items():
                if coluna != 'total':
                    entry.delete(0, 'end')
                    if modo == 'adicionar' and coluna in placeholders:
                        entry.insert(0, placeholders[coluna])
            messagebox.showinfo("Limpo", "Campos limpos!" if modo == 'adicionar' else "Valores originais restaurados!")
        
        def restaurar_original():
            if modo == 'editar':
                for coluna, entry in entries.items():
                    if coluna != 'total':
                        entry.delete(0, 'end')
                        valor = str(registro_atual[coluna]) if pd.notna(registro_atual[coluna]) else ""
                        entry.insert(0, valor)
        
        # botoes
        ctk.CTkButton(frame_botoes, text=config['botao'], command=validar_e_salvar,
                    fg_color=config['cor'], width=140, height=45,
                    font=ctk.CTkFont(size=14, weight="bold")).pack(side="left", padx=10)
        
        ctk.CTkButton(frame_botoes, text="🔄 Restaurar" if modo == 'editar' else "🧹 Limpar", 
                    command=restaurar_original if modo == 'editar' else limpar_campos,
                    fg_color="#f59e0b", width=110, height=45, text_color="black").pack(side="left", padx=10)
        
        ctk.CTkButton(frame_botoes, text="❌ Cancelar", command=janela.destroy,
                    fg_color="#dc2626", width=100, height=45).pack(side="left", padx=10)
        
        # infrmaçao sobre o total
        info_frame = ctk.CTkFrame(janela, fg_color="#1a1a1a", corner_radius=10)
        info_frame.pack(pady=10, padx=25, fill="x")
        ctk.CTkLabel(info_frame, text="💡 Dica: O total de medalhas será calculado automaticamente",
                    font=ctk.CTkFont(size=12), text_color="#6b7280").pack(pady=8)

    def _salvar_e_atualizar(self, status_msg): # salva e atualiza os dados na interface
        try:
            self.df.to_excel("world_olympedia_olympics_game_medal_tally.xlsx", index=False)
            self.anos_disponiveis = sorted(self.df['year'].unique()) if not self.df.empty else []
            self.paises_disponiveis = sorted(self.df['country'].unique()) if not self.df.empty else []
            
            if self.tabela_visivel:
                self.atualizar_treeview(self.df)
            
            self.status_crud.configure(text=status_msg)
            
        except Exception as e:
            messagebox.showerror("Erro ao Salvar", f"Erro ao salvar no arquivo Excel:\n{str(e)}")

    ############################################################################################################    estatisticas da tabela
  
    def mostrar_estatisticas(self):
            if self.df.empty:
                messagebox.showinfo("Info", "Nenhum dado disponível.")
                return
            
            stats = {'Total de registros': len(self.df), 'Países únicos': len(self.df['country'].unique()),
                    'Anos únicos': len(self.df['year'].unique()), 'Total medalhas de ouro': self.df['gold'].sum(),
                    'Total medalhas de prata': self.df['silver'].sum(), 'Total medalhas de bronze': self.df['bronze'].sum(),
                    'Total geral de medalhas': self.df['total'].sum()}
            
            messagebox.showinfo("📊 Estatísticas", "\n".join([f"{k}: {v}" for k, v in stats.items()]))
            self.atualizar_status(self.status_crud, "📊 Estatísticas exibidas")

    def criar_tabela(self): # cria a interface da tabela
        self.frame_tabela = ctk.CTkFrame(self.main_frame, fg_color="#161b22", border_color="#1f538d",
                                        border_width=2, corner_radius=15)
        self.table_title = ctk.CTkLabel(self.frame_tabela, text="📊 RESULTADOS",
                                        font=ctk.CTkFont(size=18, weight="bold"), text_color="#3b82f6")
        tree_frame = ctk.CTkFrame(self.frame_tabela, fg_color="transparent")
        
        # configura estilo consolidado
        style = ttk.Style()
        style.theme_use("clam")
        configs = {"Custom.Treeview": {"background": "#161b22", "foreground": "#e6edf3", 
                                        "fieldbackground": "#161b22", "borderwidth": 0},
                    "Custom.Treeview.Heading": {"background": "#1f538d", "foreground": "white"}}
        [style.configure(nome, **config) for nome, config in configs.items()]
        style.map("Custom.Treeview", background=[('selected', '#3b82f6')])
        
        # criar os componentes
        self.colunas = list(self.df.columns) if not self.df.empty else []
        vsb, hsb = ttk.Scrollbar(tree_frame, orient="vertical"), ttk.Scrollbar(tree_frame, orient="horizontal")
        self.tree = ttk.Treeview(tree_frame, columns=self.colunas, show='headings', style="Custom.Treeview", 
                                yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        vsb.config(command=self.tree.yview)
        hsb.config(command=self.tree.xview)
        
        # configura a  colunas e o layout
        [self.tree.heading(col, text=col.capitalize()) or self.tree.column(col, width=120, anchor='center') 
            for col in self.colunas]
        
        components = [(vsb, {"side": "right", "fill": "y"}), (hsb, {"side": "bottom", "fill": "x"}), 
                        (self.tree, {"fill": "both", "expand": True})]
        [comp.pack(**kwargs) for comp, kwargs in components]
        self.tree_frame = tree_frame
        
        # trava o scroll dentro da tabela no fianl da interface
        def scroll_somente_na_tree(event):
            self.tree.yview_scroll(int(-1 * (event.delta / 120)), "units")
            return "break"

        self.tree.bind("<MouseWheel>", scroll_somente_na_tree)  # Windows/macOS
        self.tree.bind("<Button-4>", lambda e: self.tree.yview_scroll(-1, "units"))  # Linux scroll up
        self.tree.bind("<Button-5>", lambda e: self.tree.yview_scroll(1, "units"))   # Linux scroll down

    def atualizar_treeview(self, df_novo):
        [self.tree.delete(item) for item in self.tree.get_children()]
        
        if list(df_novo.columns) != self.colunas:
            self.tree["columns"] = list(df_novo.columns)
            [self.tree.heading(col, text=col.capitalize()) or self.tree.column(col, width=120, anchor='center') 
                for col in df_novo.columns]
            self.colunas = list(df_novo.columns)
        
        [self.tree.insert("", "end", values=list(row), tags=(str(idx),)) for idx, row in df_novo.iterrows()]

    def agrupar_medalhas(self, df, colunas_grupo):
        return df.groupby(colunas_grupo).agg({
            'gold': 'sum', 'silver': 'sum', 'bronze': 'sum', 'total': 'sum'
        }).reset_index()

    ############################################################################################################    comportamentos da tabela
  
    def alternar_tabela(self):
        if self.tabela_visivel:
            self.ocultar_tabela()
        else:
            self.mostrar_tabela()
            self.atualizar_treeview(self.df)
    
    def atualizar_status(self, label, texto, cor="#7d8590"):
        label.configure(text=texto, text_color=cor)

    def mostrar_tabela(self):
        if not self.tabela_visivel:
            actions = [(self.table_title, {"pady": (20, 10)}), 
                        (self.tree_frame, {"fill": "both", "expand": True, "padx": 20, "pady": (0, 20)}),
                        (self.frame_tabela, {"fill": "both", "expand": True, "pady": 20, "padx": 10})]
            [widget.pack(**kwargs) for widget, kwargs in actions]
            self.botao_tabela.configure(text="🗂 Ocultar Tabela")
            self.tabela_visivel = True

    def ocultar_tabela(self):
        if self.tabela_visivel:
            self.frame_tabela.pack_forget()
            self.botao_tabela.configure(text="📋 Mostrar Tabela Completa")
            self.tabela_visivel = False

    ############################################################################################################    filtros 
    
    def filtrar_paises(self, pergunta): # Filtro de nomes e NOCs de países 
        pergunta_para_busca = pergunta.lower().strip()
        
        # Busca pelo NOC do país
        nocs_encontrados = re.findall(r'\b[A-Z]{3}\b', pergunta.upper())
        for noc in nocs_encontrados:
            if noc in self.nocs:
                pais_noc = self.nocs[noc]
                # Verifica se o país existe nos dados
                if pais_noc in self.paises_disponiveis:
                    return pais_noc
        
        # Busca exata no mapeamento português -> inglês
        for nome_pt, nome_en in self.todos_paises.items():
            if nome_pt in pergunta_para_busca:
                if nome_en in self.paises_disponiveis:
                    return nome_en
        
        # Busca pelo nome do país
        palavras_pergunta = set(re.findall(r'\b\w+\b', pergunta_para_busca))
        
        for pais in self.paises_disponiveis:
            pais_palavras = set(re.findall(r'\b\w+\b', pais.lower()))
            
            if pais_palavras.intersection(palavras_pergunta):
                palavras_comuns = pais_palavras.intersection(palavras_pergunta)
                if len(palavras_comuns) / len(pais_palavras) >= 0.5:
                    return pais
        
        # Busca por similaridade 
        melhor_match = None
        melhor_score = 0
        
        # Busca os países que começam com as mesmas letras
        primeiras_letras = pergunta_para_busca[:3] if len(pergunta_para_busca) >= 3 else pergunta_para_busca
        candidatos = [p for p in self.paises_disponiveis if p.lower().startswith(primeiras_letras)]
        
        # Se não encontrar o país pelo NOC, mostra todos os países
        if not candidatos:
            candidatos = self.paises_disponiveis
        
        for pais in candidatos:
            score = SequenceMatcher(None, pais.lower(), pergunta_para_busca).ratio()
            
            # Dá preferêcia aos países que estão com o nome correto na pergunta
            palavras_pais = pais.lower().split()
            for palavra in palavras_pais:
                if palavra in pergunta_para_busca:
                    score += 0.3
            
            # Threshold mais alto para evitar falsos positivos
            if score > 0.8 and score > melhor_score:
                melhor_score = score
                melhor_match = pais
        
        return melhor_match

    def aplicar_filtros(self, df, filtros):
        if 'ano' in filtros:
            df = df[df['year'] == filtros['ano']]
        if 'pais' in filtros:
            df = df[df['country'] == filtros['pais']]
        return df

    def limpar_consulta(self):
        self.entry_pergunta.delete("1.0", "end")
        self.entry_pergunta.insert("1.0", self.config['textos']['placeholder'])
        self.placeholder_ativo = True
        self.atualizar_status(self.status_consulta, self.config['textos']['aguardando'])

if __name__ == "__main__":
    tk.Tk().withdraw()
    messagebox.showwarning("Acesso negado", "Por favor, inicie o programa através do login.")
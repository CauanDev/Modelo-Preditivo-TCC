import os
import psycopg2
from psycopg2 import sql
from datetime import datetime
from collections import defaultdict
import csv

conexao = psycopg2.connect(
    host="",          
    database="",  
    user="postgres",
    password="postgres",
    port=5432                 
)

cursor = conexao.cursor()

caminho_base = os.path.join(os.path.dirname(__file__), '..', 'arquivos')


sex_map = {
    "0": "Ignorado",
    "1": "Masculino",
    "2": "Feminino"
}

city_map = {
    '500020': 'Água Clara',
    '500025': 'Alcinópolis',
    '500060': 'Amambai',
    '500070': 'Anastácio',
    '500080': 'Anaurilândia',
    '500085': 'Angélica',
    '500090': 'Antônio João',
    '500100': 'Aparecida do Taboado',
    '500110': 'Aquidauana',
    '500124': 'Aral Moreira',
    '500150': 'Bandeirantes',
    '500190': 'Bataguassu',
    '500200': 'Batayporã',
    '500210': 'Bela Vista',
    '500215': 'Bodoquena',
    '500220': 'Bonito',
    '500230': 'Brasilândia',
    '500240': 'Caarapó',
    '500260': 'Camapuã',
    '500270': 'Campo Grande',
    '500280': 'Caracol',
    '500290': 'Cassilândia',
    '500295': 'Chapadão do Sul',
    '500310': 'Corguinho',
    '500315': 'Coronel Sapucaia',
    '500320': 'Corumbá',
    '500325': 'Costa Rica',
    '500330': 'Coxim',
    '500345': 'Deodápolis',
    '500348': 'Dois Irmãos do Buriti',
    '500350': 'Douradina',
    '500370': 'Dourados',
    '500375': 'Eldorado',
    '500380': 'Fátima do Sul',
    '500390': 'Figueirão',
    '500400': 'Glória de Dourados',
    '500410': 'Guia Lopes da Laguna',
    '500430': 'Iguatemi',
    '500440': 'Inocência',
    '500450': 'Itaporã',
    '500460': 'Itaquirai',
    '500470': 'Ivinhema',
    '500480': 'Japorã',
    '500490': 'Jaraguari',
    '500500': 'Jardim',
    '500510': 'Jateí',
    '500515': 'Juti',
    '500520': 'Ladário',
    '500525': 'Laguna Carapã',
    '500540': 'Maracaju',
    '500560': 'Miranda',
    '500568': 'Mundo Novo',
    '500570': 'Naviraí',
    '500580': 'Nioaque',
    '500600': 'Nova Alvorada do Sul',
    '500620': 'Nova Andradina',
    '500625': 'Novo Horizonte do Sul',
    '500630': 'Paranaíba',
    '500635': 'Paranhos',
    '500640': 'Pedro Gomes',
    '500660': 'Ponta Porã',
    '500690': 'Porto Murtinho',
    '500710': 'Ribas do Rio Pardo',
    '500720': 'Rio Brilhante',
    '500730': 'Rio Negro',
    '500740': 'Rio Verde de Mato Grosso',
    '500750': 'Rochedo',
    '500755': 'Santa Rita do Pardo',
    '500769': 'São Gabriel do Oeste',
    '500770': 'Sete Quedas',
    '500780': 'Selvíria',
    '500790': 'Sidrolândia',
    '500793': 'Sonora',
    '500795': 'Tacuru',
    '500797': 'Taquarussu',
    '500800': 'Terenos',
    '500830': 'Três Lagoas',
    '500840': 'Vicentina'
}

race_map = {
    '1' : 'Branca',
    '2' : 'Preta',
    '3' : 'Amarela',
    '4' : 'Parda',
    '5' : 'Indígena'
}

school_map = {
    '0' : 'Sem escolaridade',
    '1' : 'Fundamental I',
    '2' : 'Fundamental II',
    '3' : 'Médio',
    '4' : 'Superior Incompleto',
    '5' : 'Superior Completo',
    '9' : 'Ifnorado'
}


def ler_csv_para_dict(caminho_csv):
    mapa = {}
    with open(caminho_csv, newline='', encoding='latin-1') as csvfile:
        leitor = csv.DictReader(csvfile, delimiter=';')
        for linha in leitor:
            codigo = linha['CODIGO'].strip()
            titulo = linha['TITULO'].strip()
            mapa[codigo] = titulo
    return mapa


def eh_obito_infantil(idade: str):
    if not idade or len(idade) != 3:
        return False
    unidade = idade[0]
    valor = idade[1:]
    return (unidade in ['1', '2', '3']) or (unidade == '4' and valor == '00')

def idade_para_dias(idade: str) -> int:
            
    unidade = idade[0]
    valor = int(idade[1:3])
    if unidade == '1':  # minutos
        return max(1, valor // (60*24))
    elif unidade == '2':
        return max(1, valor // 24)
    elif unidade == '3':
        return valor * 30
    elif unidade == '4' or unidade == '0':
        return valor * 365
    elif unidade == '5' : 
        return 365 * 100
    return 0

def converter_data(dtnasc: str):
    try:
        return datetime.strptime(dtnasc, '%d%m%Y').date()
    except:
        return None
    
def inserir_dados(natural, data_dtnasc, sexo, idade, racacor, codmunocor, idademae, escmae, ocupmae, peso, table, cursor):
    query = f'''
        INSERT INTO {table}
        ("natural", "dtnasc", "sexo", "idade", "racacor", "codmunocor", "idademae", "escmae", "ocupmae", "peso")
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    '''
    cursor.execute(
        query,
        (
            natural,
            data_dtnasc,
            sexo,
            idade,
            racacor,
            codmunocor,
            idademae,
            escmae,
            ocupmae,
            peso
        )
    )
    
mapa_ocupacoes = ler_csv_para_dict('cbo2002.csv')
registros_lidos = 0
registros_validos = 0
registros_invalidos = 0
erros_por_campo = {
    "DTNASC": 0,
    "IDADE": 0,
    "NATURAL": 0,
    "SEXO": 0,
    "RACACOR": 0,
    "CODMUNOCOR": 0,
    "IDADEMAE": 0,
    "OCUPMAE": 0,
    "ESCMAE": 0,
    "PESO": 0
}

for nome_arquivo in os.listdir(caminho_base):
    if nome_arquivo.endswith('.csv'):
        caminho_arquivo = os.path.join(caminho_base, nome_arquivo)
        with open(caminho_arquivo, 'r', encoding='utf-8') as arquivo_csv:
            leitor_csv = csv.DictReader(arquivo_csv, delimiter=';')
            
            for linha in leitor_csv:
                registros_lidos += 1
                erros_linha = []
                try:
                
                    dt_nasc = linha.get('DTNASC')
                    idade_str = linha.get('IDADE')
                    natural = linha.get('NATURAL')
                    sexo = linha.get('SEXO')
                    raca = linha.get('RACACOR')
                    cod_municipio = linha.get('CODMUNOCOR')
                    idade_mae = idade_para_dias(linha.get('IDADEMAE'))
                    ocup_mae = linha.get('OCUPMAE')
                    esc_mae = linha.get('ESCMAE')
                    peso = linha.get('PESO')
                    data_nasc = converter_data(dt_nasc)
                    dias_idade = idade_para_dias(idade_str)
                        
                    if data_nasc is None:
                        erros_linha.append("DTNASC")
                    if dias_idade is None:
                        erros_linha.append("IDADE")
                    if not natural:
                        erros_linha.append("NATURAL")
                    if not sexo or sexo not in sex_map:
                        erros_linha.append("SEXO")
                    if not raca or raca not in race_map:
                        erros_linha.append("RACACOR")
                    if not cod_municipio or cod_municipio not in city_map:
                        erros_linha.append("CODMUNOCOR")
                    if not idade_mae:
                        erros_linha.append("IDADEMAE")
                    if not ocup_mae or ocup_mae not in mapa_ocupacoes:
                        erros_linha.append("OCUPMAE")
                    if not esc_mae or esc_mae not in school_map:
                        erros_linha.append("ESCMAE")
                    if not peso or not peso.isdigit():
                        erros_linha.append("PESO")

                    for campo in erros_linha:
                        erros_por_campo[campo] += 1
                    
                    if erros_linha:
                        registros_invalidos += 1
                        continue  #
                    

                    if(eh_obito_infantil(idade_str)):
                        tabela_destino = 'obitos_infantil'
                    else:
                        tabela_destino = 'sobreviventes'
                                            
                    inserir_dados(
                        natural=natural,
                        data_nascimento=data_nasc,
                        sexo=sex_map.get(sexo),
                        idade=dias_idade,
                        raca_cor=race_map.get(raca),
                        codigo_municipio=city_map.get(cod_municipio),
                        idade_mae=idade_mae,
                        escolaridade_mae=school_map.get(esc_mae),
                        ocupacao_mae=mapa_ocupacoes.get(ocup_mae),
                        peso=peso,
                        tabela=tabela_destino,
                        cursor=cursor
                    )

                    registros_validos += 1
                except Exception:
                    registros_invalidos += 1
                    continue

conexao.commit()
cursor.close()
conexao.close()

print(f'Total de registros lidos: {registros_lidos}')
print(f'Registros válidos inseridos: {registros_validos}')
print(f'Registros inválidos ignorados: {registros_invalidos}')
print("Erros por campo:", erros_por_campo)
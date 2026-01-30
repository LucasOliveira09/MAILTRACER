import os
from google import genai
from dotenv import load_dotenv

load_dotenv()

chave_api = os.getenv("GEMINI_API_KEY")

if not chave_api:
    raise ValueError("ERRO: A chave GEMINI_API_KEY não foi encontrada no arquivo .env")

client = genai.Client(api_key=chave_api)

def classificar_email(texto_do_email):
    prompt_sistema = """
    Você é um assistente de triagem de emails corporativos.
    
    Sua tarefa:
    1. Analisar o email abaixo.
    2. Classificar como "Produtivo" (requer ação, dúvidas, suporte, ou avisos) ou "Improdutivo" (spam, agradecimentos, mensagens sociais).
    3. Resumir o conteudo do email em poucas linhas, para que o usuario entenda do que se trata o email.
    4. Escrever uma sugestão de resposta profissional, sempre decorrendo da dependencia e assunto do email. Dependendo do email sugira nem responder, apenas ignorar.
    
    REGRA DE FORMATAÇÃO (Importante):
    Sua resposta deve seguir ESTRITAMENTE este formato (use duas barras verticais para separar):
    CATEGORIA || RESUMO DO EMAIL || RESPOSTA SUGERIDA
    
    Exemplos:
    Produtivo || O email está te enviando uma solicitação de oferta de marketing || Prezado, recebemos sua solicitação e estamos analisando.
    Improdutivo || O cliente está elogiando o produto || Agradecemos o contato. Tenha um ótimo dia.
    """

    try:
        mensagem_completa = f"{prompt_sistema}\n\nEMAIL PARA ANALISAR:\n{texto_do_email}"
        
        response = client.models.generate_content(
            model="gemini-2.5-flash", 
            contents=mensagem_completa
    )
        
        conteudo = response.text
        
        if "||" in conteudo:
            partes = conteudo.split("||")
            
            if len(partes) >= 3:
                categoria = partes[0].strip()
                resumo = partes[1].strip()
                resposta = partes[2].strip()
            else:
                categoria = partes[0].strip()
                resumo = "Resumo não gerado corretamente."
                resposta = partes[1].strip() if len(partes) > 1 else "Sem resposta."
        
            categoria = categoria.replace("**", "").replace('"', '')
            
            return categoria, resumo, resposta
        else:
            return "Indefinido", conteudo

    except Exception as e:
        print(f"Erro ao chamar o Gemini: {e}")
        return "Erro Técnico", "Não foi possível gerar uma resposta no momento."


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
    3. Escrever uma sugestão de resposta profissional, sempre decorrendo da dependencia e assunto do email. Dependendo do email sugira nem responder, apenas ignorar.
    
    REGRA DE FORMATAÇÃO (Importante):
    Sua resposta deve seguir ESTRITAMENTE este formato (use duas barras verticais para separar):
    CATEGORIA || RESPOSTA SUGERIDA
    
    Exemplos:
    Produtivo || Prezado, recebemos sua solicitação e estamos analisando.
    Improdutivo || Agradecemos o contato. Tenha um ótimo dia.
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
            categoria = partes[0].strip()
            resposta = partes[1].strip()
            
            categoria = categoria.replace("**", "").replace('"', '')
            
            return categoria, resposta
        else:
            return "Indefinido", conteudo

    except Exception as e:
        print(f"Erro ao chamar o Gemini: {e}")
        return "Erro Técnico", "Não foi possível gerar uma resposta no momento."

if __name__ == "__main__":
    print("--- Testando Cérebro (Nova SDK) ---")
    email_teste = "Gostaria de saber o preço da consultoria."
    
    cat, resp = classificar_email(email_teste)
    
    print(f"Email: {email_teste}")
    print(f"Categoria: {cat}")
    print(f"Resposta: {resp}")
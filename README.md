# 📬 MailTracer - Aplicação feita para classificar emails com uso de IA!

> **MailTracer** foi feito para classificar emails e traçar sua categoria conforme importancia, resumi-los e gerar uma resposta condizente ao email.

## ✅ Projeto em produção:

**O video demonstrando o funcionamento do projeto:**

[YouTube]([youtube.com](https://youtu.be/9m0wn8hMirg?si=qxeMocnwRXadwNaF))

**E abaixo segue o link do Projeto já em produção:**

[MailTracer](https://mailtracer.vercel.app)

## 🛠️ O que o MailTracer faz?

- **Extração de Texto Multi-Formato:** Lê emails diretamente de textos colados ou via upload de arquivos `.txt` e `.pdf`.
- **OCR:** Utiliza Tesseract.js para processar PDFs que contenham apenas imagens.
- **Classificação:** Identifica se o email é `Produtivo` ou `Improdutivo`.
- **Resumo:** Gera um resumo de uma linha para visualização rápida.
- **Sugestão de Resposta:** Redige automaticamente um rascunho de resposta profissional e contextualizado.

## 🏗️ Arquitetura do Projeto

O projeto segue uma arquitetura client-server:

Foi feito usando ``Python`` com o framework ``FastAPI`` no backend, a api/IA escolhida para o projeto foi a `gemini-2.5-flash` escolhida por conta de sua resposta rapida
alem de ser permitido o seu uso gratuito.

Já no front-end, optei por fazer de forma separada, usando ``html`` e ``TailwindCSS`` para fins de maior velocidade de desenvolvimento e mais familiaridade. No javascript usei o ``Teseract.js`` para ler arquivos que são somente imagens, assim culmina o erro responder que existem 0 caracteres no arquivo, também usei ``pdf.js`` para ler os pdfs normais.



1.  **Frontend:** Aplicação com front (/public) hospedada na **Vercel**.
2.  **Backend:** A API REST foi feita usando FastAPI em python e hospedada no **Render**.
3.  **IA:** Integração com **Google Gemini Pro 2.5-flash** para processar os emails, e para evitar gastos.

---

## ⚙️ Instalação Local

### Requisitos:
- Python 3.9+

### Passo a Passo:

1. **Clone o repositório:**
   ```bash
   git clone [https://github.com/LucasOliveira09/mailtracer.git](https://github.com/LucasOliveira09/mailtracer.git)

2. **Mude a linha 12 do arquivo app.py, para:**

    ```bash

    allow_origins=["*"], 

    ```

3. **Ative a pasta Venv:**

    ```bash
    .\venv\Scripts\activate
    ```

4. **Abra o terminal (Ctrl + ' no VS Code):**
    ```bash
    # Instale as dependencias usando o seguinte comando
    pip install -r requirements.txt
    # A .env já vem com minha chave configurada para fins demonstrativos, mas pode altera-lá caso necessaria, e não a compartilhe de forma alguma
    ```


5. **Inicie a aplicação**

    ``` bash
    python app.py
    ```

### Front-End:

**O backend estará rodando assim, mas ainda será necessario a configuração do FrontEnd!**

1. **Altere a rota do Url em:**
``./public/js/script.js``

```bash

# Altere a linha 8 para esse url, ou o url que estiver rodando seu BackEnd!
const URL_BACKEND = "http://127.0.0.1:8000/analisar";

```

2. **Então inicie o front end:**
```
 Usando a extenção CodeRunner do VsCode, inicie o arquivo: ``../public/index.html``
 ```


## 🛠️ Rotas

O projeto possui somente a rota /analisar no metodo POST, você deve enviar uma string e recebera um json assim:

        ```bash
        {
            "categoria": "",
            "resumo": "",
            "resposta": ""
        }
        ```








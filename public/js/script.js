// Configuração do PDF.js
pdfjsLib.GlobalWorkerOptions.workerSrc = 'https://cdnjs.cloudflare.com/ajax/libs/pdf.js/2.16.105/pdf.worker.min.js';

const fileInput = document.getElementById('inputFile');
const textArea = document.getElementById('inputTexto');
const resumeArea = document.getElementById('textoResumo');
const statusArquivo = document.getElementById('statusArquivo');

const URL_BACKEND = "https://mailtracer.onrender.com/analisar";

// --- LÓGICA DE TEMA ---
const themeToggle = document.getElementById('themeToggle');
const themeIcon = document.getElementById('themeIcon');
const html = document.documentElement;

if (localStorage.getItem('theme') === 'dark') {
    html.classList.add('dark');
    themeIcon.classList.replace('fa-moon', 'fa-sun');
}

themeToggle.addEventListener('click', () => {
    html.classList.toggle('dark');
    if (html.classList.contains('dark')) {
        themeIcon.classList.replace('fa-moon', 'fa-sun');
        localStorage.setItem('theme', 'dark');
    } else {
        themeIcon.classList.replace('fa-sun', 'fa-moon');
        localStorage.setItem('theme', 'light');
    }
});


// Design do modal

const modalOverlay = document.getElementById('modalOverlay');
const modalContent = document.getElementById('modalContent');

function abrirModal(categoria, resposta, resumo) {
    const badge = document.getElementById('badgeCategoria');
    const txtResposta = document.getElementById('textoResposta');

    badge.innerText = categoria;
    txtResposta.innerText = resposta;
    resumeArea.innerText = resumo;

    if (categoria.toLowerCase().includes('produtivo')) {
        badge.className = "px-6 py-2 rounded-full text-lg font-bold shadow-sm inline-block bg-red-100 text-red-600 dark:bg-red-900/30 dark:text-red-400 border border-red-200 dark:border-red-800";
        badge.innerHTML = '<i class="fas fa-exclamation-circle mr-2"></i>' + categoria;
    } else {
        badge.className = "px-6 py-2 rounded-full text-lg font-bold shadow-sm inline-block bg-green-100 text-green-600 dark:bg-green-900/30 dark:text-green-400 border border-green-200 dark:border-green-800";
        badge.innerHTML = '<i class="fas fa-check-circle mr-2"></i>' + categoria;
    }

    modalOverlay.classList.remove('hidden');
    setTimeout(() => {
        modalContent.classList.remove('scale-95', 'opacity-0');
        modalContent.classList.add('scale-100', 'opacity-100');
    }, 10);
}

function fecharModal() {
    modalContent.classList.remove('scale-100', 'opacity-100');
    modalContent.classList.add('scale-95', 'opacity-0');
    setTimeout(() => { modalOverlay.classList.add('hidden'); }, 300);
}

modalOverlay.addEventListener('click', (e) => { if (e.target === modalOverlay) fecharModal(); });
window.fecharModal = fecharModal;


// ocr para descrever imagens no pdf

async function realizarOCR(pdfDoc) {
    let textoOCR = "";
    const pagina = await pdfDoc.getPage(1);
    
    const viewport = pagina.getViewport({ scale: 2.0 }); 
    const canvas = document.createElement('canvas');
    const context = canvas.getContext('2d');
    canvas.height = viewport.height;
    canvas.width = viewport.width;

    await pagina.render({ canvasContext: context, viewport: viewport }).promise;

    const imagemData = canvas.toDataURL('image/png');

    statusArquivo.innerHTML = `<span class="text-indigo-600 dark:text-indigo-400 font-bold animate-pulse"><i class="fas fa-eye"></i> Aplicando OCR na imagem...</span>`;
    
    const worker = await Tesseract.createWorker('por'); 
    const { data: { text } } = await worker.recognize(imagemData);
    await worker.terminate();

    return text;
}

// adição de arquivos

fileInput.addEventListener('change', async function() {
    if (this.files && this.files.length > 0) {
        const arquivo = this.files[0];
        const nomeArquivo = arquivo.name.toLowerCase();

        statusArquivo.innerHTML = `<span class="text-indigo-600 dark:text-indigo-400 font-bold animate-pulse">Lendo: ${arquivo.name}...</span>`;
        textArea.disabled = true;
        textArea.value = "Analisando arquivo...";

        try {
            let textoExtraido = "";

            if (nomeArquivo.endsWith(".txt") || arquivo.type === "text/plain") {
                textoExtraido = await arquivo.text();
            } 
            else if (nomeArquivo.endsWith(".pdf") || arquivo.type === "application/pdf") {
                const buffer = await arquivo.arrayBuffer();
                const pdf = await pdfjsLib.getDocument(buffer).promise;
                
                const pagina = await pdf.getPage(1);
                const conteudo = await pagina.getTextContent();
                const strings = conteudo.items.map(item => item.str);
                let textoNormal = strings.join(' ').trim();

                if (textoNormal.length < 10) {
                    console.log("Texto vazio detectado. Iniciando OCR...");
                    textoExtraido = await realizarOCR(pdf);
                    textoExtraido = "[OCR] " + textoExtraido; 
                } else {
                    textoExtraido = textoNormal;
                    const maxPaginas = Math.min(pdf.numPages, 3);
                    for (let i = 2; i <= maxPaginas; i++) {
                        const p = await pdf.getPage(i);
                        const c = await p.getTextContent();
                        textoExtraido += '\n' + c.items.map(item => item.str).join(' ');
                    }
                }
            } else {
                throw new Error("Formato não suportado");
            }

            textArea.value = textoExtraido; 
            statusArquivo.innerHTML = `<i class="fas fa-check text-green-500"></i> ${arquivo.name}`;
            
        } catch (erro) {
            console.error(erro);
            mensagemErro("Erro ao ler arquivo. Tente uma imagem mais nítida.");
            statusArquivo.innerHTML = `<span class="text-red-500">Erro na leitura</span>`;
        } finally {
            textArea.disabled = false;
        }
    }
});

// input para limpar textInput

function limparInputs(){
  textArea.value = "";
}

document.getElementById('formAnalise').addEventListener('submit', async function(e) {
    e.preventDefault();
    let texto = textArea.value;
    if (!texto.trim()) { alert("Insira texto!"); return; }
    
    // Otimização
    let limpo = texto.replace(/\s+/g, ' ').trim();
    if (limpo.length > 3000) limpo = limpo.substring(0, 3000) + "...";

    const btn = document.getElementById('btnEnviar');
    const loading = document.getElementById('loading');
    
    btn.disabled = true;
    loading.classList.remove('hidden');

    try {
        const response = await fetch(URL_BACKEND, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ texto: limpo })
        });
        const data = await response.json();
        if (response.ok){
            abrirModal(data.categoria, data.resposta, data.resumo);
            limparInputs();
        } 
        else alert("Erro: " + data.erro);
    } catch (error) { alert("Erro de conexão."); }
    finally { btn.disabled = false; loading.classList.add('hidden'); }
});
window.fecharModal = fecharModal;

document.getElementById('btnCopiar').addEventListener('click', function() {
    const texto = document.getElementById('textoResposta').innerText;
    const btn = this;
    const originalContent = btn.innerHTML;

    navigator.clipboard.writeText(texto).then(() => {
        btn.innerHTML = '<i class="fas fa-check"></i> <span>Copiado!</span>';
        btn.classList.add('bg-green-50', 'text-green-600', 'border-green-200');
        
        setTimeout(() => {
            btn.innerHTML = originalContent;
            btn.classList.remove('bg-green-50', 'text-green-600', 'border-green-200');
        }, 2000);
    });
});
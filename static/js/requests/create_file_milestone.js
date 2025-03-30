let forms = document.querySelectorAll('.uploadForm')

forms.forEach(element => {
    element.addEventListener("submit", function(event) {
        event.preventDefault(); // Impede o envio tradicional do formulário
    
        const form = event.target; // O formulário
        const fileInput = form.querySelector("input[type='file']"); // Encontrar o campo de arquivo
        const file = fileInput.files[0]; // Obter o arquivo selecionado
    
        if (!file) return; // Se não houver arquivo, não faz nada
    
        const url = form.getAttribute('url'); // Obtém a URL do formulário
    
        const formData = new FormData();
        formData.append("file", file);
    
        // Obtém o CSRF token
        const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    
        fetch(url, {
            method: "POST",
            body: formData,
            headers: {
                'X-CSRFToken': csrfToken // Envia o CSRF token no cabeçalho
            }
        })
        .then(response => response.json())
        .then(data => {
            console.log("Sucesso:", data);
    
            // Verifica o tipo de arquivo retornado e chama a função para renderizar
            if (data.file && data.file.type) {
                renderFileElement(data.file);
            }
        })
        .catch(error => console.error("Erro:", error));
    });
});

document.getElementById("uploadForm")

// Função para criar o elemento baseado no tipo de arquivo
function renderFileElement(fileData) {
    const fileType = fileData.type;
    const fileUrl = fileData.url;
    const fileName = fileData.name
    const id = fileData.id
    let element;

    switch(fileType) {
        case 'image': // Imagens
            element = document.createElement('img');
            element.src = fileUrl;
            element.alt = 'Imagem enviada';
            element.classList.add('uploaded-image');

            document.getElementById('no_image').remove()
            break;
        case 'pdf': // PDF
            element = document.createElement('a');
            element.href = fileUrl;
            element.target = '_blank';
            element.textContent = 'Abrir PDF';
            element.classList.add('uploaded-pdf');
            break;
        case 'csv': // CSV
            element = document.createElement('a');
            element.href = fileUrl;
            element.target = '_blank';
            element.textContent = 'Abrir CSV';
            element.classList.add('uploaded-csv');
            break;
        case 'excel': // Excel
            element = document.createElement('a');
            element.href = fileUrl;
            element.target = '_blank';
            element.textContent = 'Abrir Excel';
            element.classList.add('uploaded-excel');
            break;
        case 'docx': // Word
            element = document.createElement('a');
            element.href = fileUrl;
            element.target = '_blank';
            element.textContent = 'Abrir Documento Word';
            element.classList.add('uploaded-docx');
            break;
        case 'txt': // Texto
            element = document.createElement('a');
            element.href = fileUrl;
            element.target = '_blank';
            element.textContent = 'Abrir Arquivo de Texto';
            element.classList.add('uploaded-txt');
            break;
        case 'pptx': // PowerPoint
            element = document.createElement('a');
            element.href = fileUrl;
            element.target = '_blank';
            element.textContent = 'Abrir Apresentação PowerPoint';
            element.classList.add('uploaded-pptx');
            break;
        case 'zip': // Arquivo ZIP
            element = document.createElement('a');
            element.href = fileUrl;
            element.target = '_blank';
            element.textContent = 'Baixar Arquivo ZIP';
            element.classList.add('uploaded-zip');
            break;
        default:
            element = document.createElement('p');
            element.textContent = 'Tipo de arquivo não suportado.';
            element.classList.add('unsupported-file');
    }

    // Adiciona o elemento criado ao DOM (por exemplo, dentro de um contêiner com id "uploaded-files")

    let container = null
    let newId = ''
    if (fileType == 'image') {
        newId = 'images'+id
        container = document.querySelector(`#${newId} .slider .slider-content`);
    }
    else {
        newId = 'geralDocs'+id
        container = document.querySelector(`#${newId} .docList`);
    }

    console.log(newId)

    if (container) {
        container.appendChild(element);
    } else {
        console.log("Container para arquivos não encontrado!");
    }
}

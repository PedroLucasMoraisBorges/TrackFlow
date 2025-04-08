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
    const fileName = fileData.name;
    const id = fileData.id;

    let a = document.createElement("a");
    a.href = fileUrl;
    a.target = "_blank";
    a.classList.add("docItem");

    // Cria o elemento img
    const img = document.createElement("img");
    img.src = "/static/imgs/folder.svg";
    img.alt = "image document";

    // Cria o elemento p
    const p = document.createElement("p");
    p.textContent = fileName;

    // Adiciona os elementos filhos corretamente
    a.appendChild(img);
    a.appendChild(p);

    // Adiciona o elemento ao DOM
    let newId = 'geralDocs' + id;
    let container = document.querySelector(`#${newId} .docList`);

    console.log(newId);

    if (container) {
        container.appendChild(a);
    } else {
        console.log("Container para arquivos não encontrado!");
    }
}

document.getElementById("stage_form").addEventListener("submit", async function(event) {
    event.preventDefault();  // Impede o recarregamento da página

    let formData = new FormData(this);  // Captura os dados do formulário

    // Obtém o CSRF token
    let csrftoken = document.querySelector("[name=csrfmiddlewaretoken]").value;

    let url = this.getAttribute('url')
    // Envia os dados do formulário para a API
    let response = await fetch(url, {
        method: "POST",
        body: formData,
        headers: {
            "X-CSRFToken": csrftoken
        }
    });

    

    // Verifica se a resposta foi bem-sucedida
    if (response.ok) {
        let data = await response.json();


        // Cria o componente para o stage com os dados da resposta
        let stageComponent = `
            <div class="stage-card" id="${data.stage.name}">
                <h3>${data.stage.name}</h3>
                <p>${data.stage.description}</p>
            </div>`
        ;

        console.log('jj')

        // Adiciona o componente na lista de stages ou em algum local específico
        document.getElementById("stage-list").innerHTML += stageComponent;
    } else {
        alert("Erro ao criar a etapa!");
    }
});
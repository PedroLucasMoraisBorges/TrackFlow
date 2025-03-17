document.getElementById("milestone-form").addEventListener("submit", async function(event) {
    event.preventDefault();  // Impede o recarregamento da página

    let formData = new FormData(this);  // Captura os dados do formulário

    // Obtém o CSRF token
    let csrftoken = document.querySelector("[name=csrfmiddlewaretoken]").value;

    let url = document.getElementById("milestone-form").getAttribute("url");

    let response = await fetch(url, {
        method: "POST",
        body: formData,
        headers: {
            "X-CSRFToken": csrftoken
        }
    });

    console.log(response.ok)


    if (response.ok) {
        let data = await response.json();

        // Esconde o formulário
        document.getElementById("form-container").style.display = "none";

        // Cria o componente do milestone
        let milestoneComponent = `
            <div class="milestone-card" id="${data.milestone.id}">
                <h3>${data.milestone.name}</h3>
                <p>${data.milestone.description}</p>
            </div>
        `;

        // Adiciona o componente na lista de milestones
        document.getElementById("milestone-list").innerHTML += milestoneComponent;
        document.getElementById("stage-list").style.display = "block"
        document.getElementById("stage_form").style.display = "block"

        console.log('teste')



        // Pega a URL atual da página
        let currentUrl = new URL(window.location.href);

        // Extrai a base da URL, até o final de 'registerMilestone/'
        let baseUrl = currentUrl.origin + '/project/' + currentUrl.pathname.split('/')[2] + '/registerMilestone/';

        // Cria a nova URL substituindo o 'milestone_id' no caminho
        let newUrl = baseUrl + data.milestone.id + '/';

        // Atualiza a URL no navegador sem recarregar a página
        window.history.pushState({}, '', newUrl);

    } else {
        alert("Erro ao criar milestone!");
    }
});
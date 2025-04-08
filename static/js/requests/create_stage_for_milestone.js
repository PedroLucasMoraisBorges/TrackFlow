let stage_form = document.getElementById("stage_form")

if (stage_form) {
    stage_form.addEventListener("submit", async function(event) {
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
            let stage = data.stage; 
            let imgUrl = "/static/imgs/bar-chart-steps.svg";
            let dropdownImgUrl = "/static/imgs/dropdown.svg";
            
            let stageCard = document.createElement("div");
            stageCard.classList.add("stage-card");
            stageCard.setAttribute("onclick", "toggleStageDropdown(this)");
            
            stageCard.innerHTML = `
                <div class="stage_name">
                    <img src="${imgUrl}" alt="">
                    <h3>${stage.name}</h3>
                </div>
                <img class="dropdown-icon" src="${dropdownImgUrl}" alt="">
            `;
    
            let dropdownContent = document.createElement("form");
            dropdownContent.id = stage.id
            dropdownContent.setAttribute("url", `/editStage/${stage.id}`);
            dropdownContent.classList.add("dropdown-content");
    
            dropdownContent.innerHTML = `<p>${stage.description}</p><div class="buttons"><button class="buttonEdit" onclick="enableEdit(this)"><img src="/static/imgs/edit.svg" alt=""></button></div>`
    
            let csrfInput = document.createElement("input");
            csrfInput.type = "hidden";
            csrfInput.name = "csrfmiddlewaretoken";
            csrfInput.value = csrftoken;
            dropdownContent.appendChild(csrfInput);
            
            document.querySelector(".stages").appendChild(stageCard);
            document.querySelector(".stages").appendChild(dropdownContent);
            
        } else {
            alert("Erro ao criar a etapa!");
        }
    });
}
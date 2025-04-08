function enableEdit(button) {
    let dropdownContent = button.closest(".dropdown-content");
    let stageCard = dropdownContent.previousElementSibling;
    
    let stageName = stageCard.querySelector("h3");
    let stageDesc = dropdownContent.querySelector("p:last-of-type");

    if (!stageName || !stageDesc) {
        console.error("Erro: Elemento não encontrado.");
        return;
    }

    let nameInput = document.createElement("input");
    nameInput.type = "text";
    nameInput.value = stageName.textContent.trim();
    nameInput.name = "name"
    nameInput.classList.add("edit-input");

    let descInput = document.createElement("textarea");
    descInput.value = stageDesc.textContent.trim();
    nameInput.name = "description"
    descInput.classList.add("edit-textarea");

    nameInput.setAttribute("data-original", stageName.textContent.trim());
    descInput.setAttribute("data-original", stageDesc.textContent.trim());

    stageDesc.remove();


    // Substitui o nome
    stageName.replaceWith(nameInput);

    // Insere o textarea antes dos botões
    let buttonContainer = button.parentElement;
    console.log(dropdownContent)
    dropdownContent.insertBefore(descInput, buttonContainer);

    button.remove();

    let saveButton = document.createElement("button");
    saveButton.classList.add("save-btn");
    saveButton.textContent = "Salvar";
    saveButton.onclick = function () { saveEdit(this); };

    let cancelButton = document.createElement("button");
    cancelButton.classList.add("cancel-btn");
    cancelButton.textContent = "Cancelar";
    cancelButton.onclick = function () { cancelEdit(this); };

    buttonContainer.appendChild(saveButton);
    buttonContainer.appendChild(cancelButton);
}

function restoreEditButton(buttonContainer) {
    buttonContainer.innerHTML = "";
    let editButton = document.createElement("button");
    editButton.classList.add("buttonEdit");
    editButton.onclick = function () { enableEdit(this); };

    let editImg = document.createElement("img");
    editImg.src = "/static/imgs/edit.svg";
    editImg.alt = "Editar";

    editButton.appendChild(editImg);
    buttonContainer.appendChild(editButton);
}


function saveEdit(button) {
    let dropdownContent = button.closest(".dropdown-content");
    let stageCard = dropdownContent.previousElementSibling;

    let nameInput = stageCard.querySelector("input");
    let descInput = dropdownContent.querySelector("textarea");

    let formData = new FormData();
    formData.append("name", nameInput.value);
    formData.append("description", descInput.value);

    // Obtém o CSRF token
    let csrftoken = document.querySelector("[name=csrfmiddlewaretoken]").value;

    let url = dropdownContent.getAttribute("url")
    // Envia os dados do formulário para a API
    let response = fetch(url, {
        method: "PUT",
        body: formData,
        headers: {
            "X-CSRFToken": csrftoken
        }
    });

    let stageName = document.createElement("h3");
    stageName.textContent = nameInput.value;

    let stageDesc = document.createElement("p");
    stageDesc.textContent = descInput.value;

    nameInput.replaceWith(stageName);
    descInput.replaceWith(stageDesc);

    // Restaurando o botão Editar
    restoreEditButton(button.parentElement)
}


function cancelEdit(button) {
    let dropdownContent = button.closest(".dropdown-content");
    let stageCard = dropdownContent.previousElementSibling;

    let nameInput = stageCard.querySelector("input");
    let descInput = dropdownContent.querySelector("textarea");

    let stageName = document.createElement("h3");
    stageName.textContent = nameInput.getAttribute("data-original");

    let stageDesc = document.createElement("p");
    stageDesc.textContent = descInput.getAttribute("data-original");

    nameInput.replaceWith(stageName);
    descInput.replaceWith(stageDesc);

    // Restaurando o botão Editar
    restoreEditButton(button.parentElement)
}
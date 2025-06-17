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



// Milestone

// Milestone

function enableEditMilestone(button) {
    let milestoneCard = button.closest(".milestone-card");
    let titleContainer = milestoneCard.querySelector(".title .info p");
    let descContainer = milestoneCard.querySelector(".description p:last-of-type");

    if (!titleContainer || !descContainer) {
        console.error("Erro: Elementos de nome ou descrição não encontrados.");
        return;
    }

    // Inputs
    let nameInput = document.createElement("input");
    nameInput.type = "text";
    nameInput.value = titleContainer.textContent.trim();
    nameInput.name = "name";
    nameInput.classList.add("edit-input");
    nameInput.setAttribute("data-original", titleContainer.textContent.trim());

    let descInput = document.createElement("textarea");
    descInput.value = descContainer.textContent.trim();
    descInput.name = "description";
    descInput.classList.add("edit-textarea");
    descInput.setAttribute("data-original", descContainer.textContent.trim());

    titleContainer.replaceWith(nameInput);
    descContainer.replaceWith(descInput);

    // Oculta o botão de editar (sem remover)
    button.style.display = "none";

    // Container de botões na seção .description
    let descriptionContainer = milestoneCard.querySelector(".description");

    let buttonGroup = document.createElement("div");
    buttonGroup.classList.add("edit-button-group");

    let saveButton = document.createElement("button");
    saveButton.classList.add("save-btn");
    saveButton.textContent = "Salvar";
    saveButton.onclick = function () { saveEditMilestone(this); };

    let cancelButton = document.createElement("button");
    cancelButton.classList.add("cancel-btn");
    cancelButton.textContent = "Cancelar";
    cancelButton.onclick = function () { cancelEditMilestone(this); };

    buttonGroup.appendChild(saveButton);
    buttonGroup.appendChild(cancelButton);
    descriptionContainer.appendChild(buttonGroup);
}


function saveEditMilestone(button) {
    let milestoneCard = button.closest(".milestone-card");
    let nameInput = milestoneCard.querySelector("input[name='name']");
    let descInput = milestoneCard.querySelector("textarea[name='description']");

    let formData = new FormData();
    formData.append("name", nameInput.value);
    formData.append("description", descInput.value);

    let csrftoken = document.querySelector("[name=csrfmiddlewaretoken]").value;
    let url = milestoneCard.getAttribute("url");

    fetch(url, {
        method: "PUT",
        body: formData,
        headers: {
            "X-CSRFToken": csrftoken
        }
    });

    let newTitle = document.createElement("p");
    newTitle.textContent = nameInput.value;

    let newDesc = document.createElement("p");
    newDesc.textContent = descInput.value;

    nameInput.replaceWith(newTitle);
    descInput.replaceWith(newDesc);

    restoreEditMilestoneButton(milestoneCard);
}


function cancelEditMilestone(button) {
    let milestoneCard = button.closest(".milestone-card");
    let nameInput = milestoneCard.querySelector("input[name='name']");
    let descInput = milestoneCard.querySelector("textarea[name='description']");

    let originalTitle = document.createElement("p");
    originalTitle.textContent = nameInput.getAttribute("data-original");

    let originalDesc = document.createElement("p");
    originalDesc.textContent = descInput.getAttribute("data-original");

    nameInput.replaceWith(originalTitle);
    descInput.replaceWith(originalDesc);

    restoreEditMilestoneButton(milestoneCard);
}


function restoreEditMilestoneButton(milestoneCard) {
    // Remove o grupo de botões se existir
    let buttonGroup = milestoneCard.querySelector(".edit-button-group");
    if (buttonGroup) buttonGroup.remove();

    // Mostra o botão de editar novamente
    let editButton = milestoneCard.querySelector(".buttonEdit");
    if (editButton) editButton.style.display = "";
}

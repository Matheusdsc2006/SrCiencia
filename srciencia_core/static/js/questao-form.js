document.addEventListener("DOMContentLoaded", function () {
    console.log("Arquivo JavaScript carregado.");
    // Seletores de campos de disciplina, conteúdo, tópico e outros elementos
    var disciplinaField = document.querySelector("#id_disciplina");
    var conteudoField = document.querySelector("#id_conteudo");
    var topicoField = document.querySelector("#id_topico");
    var selects = document.querySelectorAll("select");
    var form = document.querySelector("form");  
    var alternativas = document.querySelectorAll(".alternativa"); 

    // Atualizar os campos dinamicamente ao alterar Conteúdo
    conteudoField.addEventListener("change", function () {
        fetch(`/get_topicos/${this.value}/`)
            .then(response => response.json())
            .then(data => {
                topicoField.innerHTML = '<option value="">Selecione o tópico</option>';
                data.forEach(topico => {
                    topicoField.innerHTML += `<option value="${topico.id}">${topico.nome}</option>`;
                });
                topicoField.disabled = false;
            });
    });

    // Função para carregar conteúdos com base na disciplina selecionada
    function carregarConteudos(disciplinaId) {
        fetch(`/api/conteudos/${disciplinaId}`)
            .then((response) => response.json())
            .then((data) => {
                conteudoField.innerHTML = '<option value="">---------</option>';
                data.forEach((item) => {
                    var option = document.createElement("option");
                    option.value = item.id;
                    option.textContent = item.nome;
                    conteudoField.appendChild(option);
                });

                // Selecionar o valor atual se já existir
                if (conteudoField.dataset.selected) {
                    conteudoField.value = conteudoField.dataset.selected;
                }

                conteudoField.disabled = false;
            })
            .catch((error) => {
                console.error("Erro ao carregar conteúdos:", error);
            });
    }

    // Função para carregar tópicos com base no conteúdo selecionado
    function carregarTopicos(conteudoId) {
        // Verifica se o conteúdo ID é válido
        if (!conteudoId || conteudoId === "None") {
            console.error("Conteúdo ID inválido:", conteudoId);
            topicoField.innerHTML = '<option value="">---------</option>'; // Reseta o campo de tópicos
            topicoField.disabled = true; // Desabilita o select de tópicos
            return; // Interrompe a execução da função
        }
    
        // Faz a requisição para o endpoint de tópicos
        fetch(`/api/topicos/${conteudoId}/`)
            .then((response) => {
                if (!response.ok) {
                    throw new Error(`Erro ao carregar tópicos: ${response.statusText}`);
                }
                return response.json();
            })
            .then((data) => {
                topicoField.innerHTML = '<option value="">---------</option>';
                data.forEach((item) => {
                    var option = document.createElement("option");
                    option.value = item.id;
                    option.textContent = item.nome;
                    topicoField.appendChild(option);
                });
    
                topicoField.disabled = false;
    
                // Selecionar o valor atual se já existir
                if (topicoField.dataset.selected) {
                    topicoField.value = topicoField.dataset.selected;
                }
            })
            .catch((error) => {
                console.error("Erro ao carregar tópicos:", error);
            });
    }
    

    // Carregar valores iniciais ao editar
    if (disciplinaField.value) {
        carregarConteudos(disciplinaField.value);
        if (conteudoField.dataset.selected) {
            carregarTopicos(conteudoField.dataset.selected);
        }
    }

    // Eventos para atualizar os selects ao mudar valores
    disciplinaField.addEventListener("change", function () {
        fetch(`/get_conteudos/${this.value}/`)
            .then(response => response.json())
            .then(data => {
                conteudoField.innerHTML = '<option value="">Selecione o conteúdo</option>';
                data.forEach(conteudo => {
                    conteudoField.innerHTML += `<option value="${conteudo.id}">${conteudo.nome}</option>`;
                });
                conteudoField.disabled = false;
            });
    }); 

    // Configurar selects para mostrar opções no foco
    selects.forEach((select) => {
        select.addEventListener("focus", function () {
            this.setAttribute("size", 8);
        });

        select.addEventListener("blur", function () {
            this.removeAttribute("size");
        });

        select.addEventListener("change", function () {
            this.blur();
        });
    });


    // Adicionar evento de clique em cada botão de remoção
    document.addEventListener("click", function (event) {
        if (event.target.classList.contains("btn-remove-image")) {
            event.preventDefault();
    
            var index = event.target.dataset.index;
            console.log(`Botão de remoção clicado. Índice: ${index}`);
    
            var fileInput = document.getElementById(`id_form-${index}-imagem`);
            var uploadIcon = document.getElementById(`uploadIcon_${index}`);
            var viewIcon = document.getElementById(`viewImageIcon_${index}`);
            var imagePreview = document.getElementById(`imagePreviewImg_${index}`);
            var modal = document.getElementById(`modalImagePreview_${index}`);
    
            console.log("Verificando elementos:");
            console.log(`fileInput: ${fileInput?.outerHTML || "não encontrado"}`);
            console.log(`uploadIcon: ${uploadIcon?.outerHTML || "não encontrado"}`);
            console.log(`viewIcon: ${viewIcon?.outerHTML || "não encontrado"}`);
            console.log(`imagePreview: ${imagePreview?.outerHTML || "não encontrado"}`);
            console.log(`modal: ${modal?.outerHTML || "não encontrado"}`);
    
            if (!fileInput || !uploadIcon || !viewIcon || !imagePreview || !modal) {
                console.error("Um ou mais elementos não foram encontrados.");
                return;
            }
    
            fileInput.value = "";
            uploadIcon.style.display = "block";
            viewIcon.style.display = "none";
            imagePreview.src = "";
            imagePreview.style.display = "none";
            modal.style.display = "none";
    
            console.log("Imagem removida e modal fechado.");
            alert("Imagem excluída com sucesso!");
        }
    });
    


    // Atualizar pré-visualização ao carregar imagens
    document.querySelectorAll("input[type='file']").forEach((input) => {
        input.addEventListener("change", function (event) {
            var index = input.id.split("-")[1];
            var file = event.target.files[0];
            var imagePreview = document.getElementById(`imagePreviewImg_${index}`);

            if (!imagePreview) {
                console.error(`Elemento com ID imagePreviewImg_${index} não encontrado.`);
                return;
            }

            if (file) {
                var reader = new FileReader();
                reader.onload = function () {
                    imagePreview.src = reader.result;
                    imagePreview.style.display = "block";
                    console.log("Pré-visualização atualizada.");
                };
                reader.readAsDataURL(file);
            } else {
                imagePreview.src = "";
                imagePreview.style.display = "none";
                console.log("Pré-visualização removida.");
            }
        });
    });

    // Modais de visualização de imagem
    document.querySelectorAll(".view-image-icon").forEach((icon) => {
        icon.addEventListener("click", function () {
            var modalId = this.dataset.target;
            var modal = document.querySelector(modalId);
            if (modal) {
                modal.style.display = "block";
            }
        });
    });

    // Fechar modal ao clicar no botão de fechar
    document.querySelectorAll(".close-modal").forEach((closeButton) => {
        closeButton.addEventListener("click", function () {
            var modalId = this.dataset.target;
            var modal = document.querySelector(modalId);
            if (modal) {
                modal.style.display = "none";
            }
        });
    });

    // Fechar modal ao clicar fora do conteúdo
    document.querySelectorAll(".image-modal").forEach((modal) => {
        modal.addEventListener("click", function (event) {
            if (event.target === modal) {
                modal.style.display = "none";
            }
        });
    });
    form.addEventListener("submit", function (event) {
        let algumVazio = false;

        alternativas.forEach((alternativa) => {
            var descricao = alternativa.querySelector("input[name*='descricao']");
            var imagemUrl = alternativa.querySelector("input[name*='imagem_url']");
            var descricaoVazia = !descricao.value.trim();
            var imagemUrlVazia = !imagemUrl.value.trim();

            // Se descrição e imagem estiverem vazias
            if (descricaoVazia && imagemUrlVazia) {
                algumVazio = true;
                alternativa.classList.add("erro-alternativa"); // Adiciona uma classe de erro para destaque (opcional)
            } else {
                alternativa.classList.remove("erro-alternativa");
            }
        });

        if (algumVazio) {
            event.preventDefault(); // Impede o envio do formulário
            alert("Alguma alternativa ficou vazia! Adicione pelo menos a descrição.");
        }
    });
});


document.addEventListener("DOMContentLoaded", function () {
    console.log("Arquivo JavaScript carregado.");
    // Seletores de campos de disciplina, conteúdo, tópico e outros elementos
    var disciplinaField = document.querySelector("#id_disciplina");
    var conteudoField = document.querySelector("#id_conteudo");
    var topicoField = document.querySelector("#id_topico");
    var selects = document.querySelectorAll("select");
    var form = document.querySelector("form");  
    var alternativas = document.querySelectorAll(".alternativa"); 
    var conteudoSelect = document.getElementById("id_conteudo");
    var topicoSelect = document.getElementById("id_topico");
    var form = document.getElementById("questao-form");
    var disciplinaSelect = document.getElementById("id_disciplina");

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
        // Verifica se a disciplina é válida
        if (!disciplinaId) {
            console.error("Disciplina ID inválido:", disciplinaId);
            conteudoField.innerHTML = '<option value="">---------</option>';
            conteudoField.disabled = true;
            return;
        }

        // Faz a requisição ao endpoint de conteúdos
        fetch(`/api/conteudos/${disciplinaId}/`)
            .then((response) => {
                if (!response.ok) {
                    throw new Error(`Erro ao carregar conteúdos: ${response.statusText}`);
                }
                return response.json();
            })
            .then((data) => {
                // Atualiza o select de conteúdos
                conteudoField.innerHTML = '<option value="">---------</option>';
                data.forEach((item) => {
                    var option = document.createElement("option");
                    option.value = item.id;
                    option.textContent = item.nome;
                    conteudoField.appendChild(option);
                });

                conteudoField.disabled = false;

                // Seleciona o valor atual, se existir
                if (conteudoField.dataset.selected) {
                    conteudoField.value = conteudoField.dataset.selected;
                }
            })
            .catch((error) => {
                console.error("Erro ao carregar conteúdos:", error);
            });
    }

    // Função para carregar tópicos com base no conteúdo selecionado
    function carregarTopicos(conteudoId) {
        // Verifica se o conteúdo é válido
        if (!conteudoId || conteudoId === "None") {
            console.error("Conteúdo ID inválido:", conteudoId);
            topicoField.innerHTML = '<option value="">---------</option>';
            topicoField.disabled = true;
            return;
        }

        // Faz a requisição ao endpoint de tópicos
        fetch(`/api/topicos/${conteudoId}/`)
            .then((response) => {
                if (!response.ok) {
                    throw new Error(`Erro ao carregar tópicos: ${response.statusText}`);
                }
                return response.json();
            })
            .then((data) => {
                // Atualiza o select de tópicos
                topicoField.innerHTML = '<option value="">---------</option>';
                data.forEach((item) => {
                    var option = document.createElement("option");
                    option.value = item.id;
                    option.textContent = item.nome;
                    topicoField.appendChild(option);
                });

                topicoField.disabled = false;

                // Seleciona o valor atual, se existir
                if (topicoField.dataset.selected) {
                    topicoField.value = topicoField.dataset.selected;
                }
            })
            .catch((error) => {
                console.error("Erro ao carregar tópicos:", error);
            });
    }

    // Event Listener para carregar conteúdos ao alterar a disciplina
    disciplinaField.addEventListener("change", function () {
        var disciplinaId = this.value; // Obtém o ID da disciplina selecionada
        carregarConteudos(disciplinaId); // Chama a função para carregar conteúdos
        topicoField.innerHTML = '<option value="">---------</option>'; // Reseta os tópicos
        topicoField.disabled = true;
    });

    // Event Listener para carregar tópicos ao alterar o conteúdo
    conteudoField.addEventListener("change", function () {
        var conteudoId = this.value; // Obtém o ID do conteúdo selecionado
        carregarTopicos(conteudoId); // Chama a função para carregar tópicos
    });

    // Inicialização: carregar conteúdos e tópicos se houver valores pré-selecionados
    var disciplinaId = disciplinaField.value;
    if (disciplinaId) {
        carregarConteudos(disciplinaId);

        var conteudoId = conteudoField.dataset.selected;
        if (conteudoId) {
            carregarTopicos(conteudoId);
        }
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
    function atualizarTopicos(conteudoId) {
        // Limpar opções de tópicos
        topicoSelect.innerHTML = '<option value="">---------</option>';

        if (conteudoId) {
            // Fazer requisição para buscar tópicos relacionados
            fetch(`/app/u/0/api/topicos/${conteudoId}/`) // Certifique-se de usar o caminho correto
                .then((response) => response.json())
                .then((data) => {
                    if (data.length > 0) {
                        // Adicionar os tópicos ao select
                        data.forEach((topico) => {
                            var option = document.createElement("option");
                            option.value = topico.id;
                            option.textContent = topico.nome;
                            topicoSelect.appendChild(option);
                        });
                    } else {
                        console.log("Nenhum tópico encontrado para este conteúdo.");
                    }
                })
                .catch((error) => {
                    console.error("Erro ao carregar tópicos:", error);
                });
        }
    }

    // Evento para detectar mudanças no select de conteúdo
    conteudoSelect.addEventListener("change", () => {
        var conteudoId = conteudoSelect.value;
        atualizarTopicos(conteudoId); // Atualizar os tópicos dinamicamente
    });
    form.addEventListener("submit", (event) => {
        var conteudoValue = conteudoSelect.value;
        var topicoValue = topicoSelect.value;

        // Verificar se o conteúdo ou tópico estão vazios
        if (!conteudoValue || !topicoValue) {
            event.preventDefault(); // Impedir o envio do formulário
            alert("Você esqueceu de adicionar um conteúdo ou tópico!"); // Exibir alerta
        }
    });
    var loadConteudos = (disciplinaId) => {
        fetch(`/app/u/0/api/conteudos/${disciplinaId}/`)
            .then(response => {
                if (!response.ok) {
                    throw new Error('Erro ao buscar conteúdos');
                }
                return response.json();
            })
            .then(data => {
                var conteudoSelect = document.getElementById('id_conteudo');
                conteudoSelect.innerHTML = '<option value="">---------</option>';
                data.forEach(conteudo => {
                    var option = document.createElement('option');
                    option.value = conteudo.id;
                    option.textContent = conteudo.nome;
                    conteudoSelect.appendChild(option);
                });
            })
            .catch(error => console.error('Erro ao carregar conteúdos:', error));
    };
    
    var loadTopicos = (conteudoId) => {
        fetch(`/app/u/0/api/topicos/${conteudoId}/`)
            .then(response => {
                if (!response.ok) {
                    throw new Error('Erro ao buscar tópicos');
                }
                return response.json();
            })
            .then(data => {
                var topicoSelect = document.getElementById('id_topico');
                topicoSelect.innerHTML = '<option value="">---------</option>';
                data.forEach(topico => {
                    var option = document.createElement('option');
                    option.value = topico.id;
                    option.textContent = topico.nome;
                    topicoSelect.appendChild(option);
                });
            })
            .catch(error => console.error('Erro ao carregar tópicos:', error));
    };

    disciplinaSelect.addEventListener("change", () => {
        var disciplinaId = disciplinaSelect.value;
        loadConteudos(disciplinaId);
    });

    conteudoSelect.addEventListener("change", () => {
        var conteudoId = conteudoSelect.value;
        loadTopicos(conteudoId);
    });

    // Carregar Conteúdos e Tópicos no carregamento da página (apenas criação)
    var disciplinaId = disciplinaSelect.value;
    if (disciplinaId) {
        loadConteudos(disciplinaId);
    }

    var conteudoId = conteudoSelect.value;
    if (conteudoId) {
        loadTopicos(conteudoId);
    }
    form.addEventListener("submit", function (event) {
        // Obter todos os checkboxes de alternativas
        var checkboxes = document.querySelectorAll("input[type='checkbox'][name*='correta']");
        let atLeastOneChecked = false;

        // Verificar se pelo menos um checkbox está marcado
        checkboxes.forEach((checkbox) => {
            if (checkbox.checked) {
                atLeastOneChecked = true;
            }
        });

        // Se nenhuma alternativa estiver marcada, mostrar alerta e impedir o envio
        if (!atLeastOneChecked) {
            event.preventDefault(); // Impede o envio do formulário
            alert("Você esqueceu de indicar a(s) alternativa(s) correta(s).");
        }
    });
});


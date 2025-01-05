document.addEventListener('DOMContentLoaded', function () {

    // Inicializações relacionadas aos selects de disciplina, conteúdo e tópico
    const disciplinaSelect = document.querySelector('#id_disciplina');
    const conteudoSelect = document.querySelector('#id_conteudo');
    const topicoSelect = document.querySelector('#id_topico');

    // Carregar valores iniciais para os selects ao abrir a página de edição
    if (disciplinaSelect && disciplinaSelect.value) {
        updateConteudos(disciplinaSelect.value, conteudoSelect.dataset.selected);
    }

    if (conteudoSelect && conteudoSelect.dataset.selected) {
        updateTopicos(conteudoSelect.dataset.selected, topicoSelect.dataset.selected);
    }

    // Atualizar conteúdos ao alterar a disciplina
    if (disciplinaSelect) {
        disciplinaSelect.addEventListener('change', function () {
            const disciplinaId = this.value;
            updateConteudos(disciplinaId);
        });
    }

    // Atualizar tópicos ao alterar o conteúdo
    if (conteudoSelect) {
        conteudoSelect.addEventListener('change', function () {
            const conteudoId = this.value;
            updateTopicos(conteudoId);
        });
    }

    /**
     * Atualiza o select de conteúdos com base na disciplina selecionada
     * @param {Number} disciplinaId - ID da disciplina
     * @param {Number|null} selectedConteudo - ID do conteúdo pré-selecionado
     */
    function updateConteudos(disciplinaId, selectedConteudo = null) {
        fetch(`/api/conteudos/${disciplinaId}/`)
            .then(response => response.json())
            .then(data => {
                conteudoSelect.innerHTML = '<option value="">---------</option>';
                if (data.length > 0) {
                    data.forEach(conteudo => {
                        const option = new Option(conteudo.nome, conteudo.id);
                        conteudoSelect.add(option);
                    });
                    conteudoSelect.disabled = false;

                    // Preencher o valor selecionado, se houver
                    if (selectedConteudo) {
                        conteudoSelect.value = selectedConteudo;
                        updateTopicos(selectedConteudo, topicoSelect.dataset.selected);
                    }
                } else {
                    conteudoSelect.disabled = true;
                    conteudoSelect.innerHTML = '<option value="">---------</option>';
                    topicoSelect.disabled = true;
                    topicoSelect.innerHTML = '<option value="">---------</option>';
                }
            })
            .catch(error => console.error('Erro ao carregar conteúdos:', error));
    }

    /**
     * Atualiza o select de tópicos com base no conteúdo selecionado
     * @param {Number} conteudoId - ID do conteúdo
     * @param {Number|null} selectedTopico - ID do tópico pré-selecionado
     */
    function updateTopicos(conteudoId, selectedTopico = null) {
        fetch(`/api/topicos/${conteudoId}/`)
            .then(response => response.json())
            .then(data => {
                topicoSelect.innerHTML = '<option value="">---------</option>';
                if (data.length > 0) {
                    data.forEach(topico => {
                        const option = new Option(topico.nome, topico.id);
                        topicoSelect.add(option);
                    });
                    topicoSelect.disabled = false;

                    // Preencher o valor selecionado, se houver
                    if (selectedTopico) {
                        topicoSelect.value = selectedTopico;
                    }
                } else {
                    topicoSelect.disabled = true;
                    topicoSelect.innerHTML = '<option value="">---------</option>';
                }
            })
            .catch(error => console.error('Erro ao carregar tópicos:', error));
    }

    // Lógica para imagens e uploads
    document.querySelectorAll('.uploadIcon').forEach(function (icon) {
        const index = icon.id.split('_')[1];
        icon.addEventListener('click', function () {
            const fileInput = document.getElementById(`id_form-${index}-imagem`);
            if (fileInput) {
                fileInput.click();
            } else {
                console.error(`Input de arquivo não encontrado para o índice ${index}`);
            }
        });
    });    

    document.addEventListener("DOMContentLoaded", function () {
        input.addEventListener('change', function (event) {
            const index = input.id.split('-')[1]; // Extrai o índice do ID do input
            const file = event.target.files[0];
            const imagePreview = document.getElementById(`imagePreviewImg_${index}`);

            if (!imagePreview) {
                console.error(`Elemento com ID imagePreviewImg_${index} não encontrado.`);
                return;
            }

            if (file) {
                const reader = new FileReader();
                reader.onload = function () {
                    imagePreview.src = reader.result;
                    imagePreview.style.display = 'block';
                };
                reader.readAsDataURL(file);
            } else {
                imagePreview.src = '';
                imagePreview.style.display = 'none';
            }
        });
    });
});


    document.querySelectorAll('.btn-remove').forEach(function (button) {
        button.addEventListener('click', function () {
            const index = this.dataset.index;
            const imagePreview = document.getElementById(`imagePreviewImg_${index}`);
            const uploadIcon = document.getElementById(`uploadIcon_${index}`);
            const fileInput = document.getElementById(`id_form-${index}-imagem`);

            if (imagePreview) {
                imagePreview.src = '';
                imagePreview.style.display = 'none';
                uploadIcon.style.display = 'block';
                fileInput.value = ''; // Limpar o input de arquivo
            }
        });
    });

    function previewImage(event, index) {
        const file = event.target.files[0];
        const imagePreview = document.getElementById(`imagePreviewImg_${index}`);
    
        if (!imagePreview) {
            console.error(`Elemento com ID imagePreviewImg_${index} não encontrado.`);
            return; 
        }
    
        if (file) {
            const reader = new FileReader();
    
            reader.onload = function () {
                imagePreview.src = reader.result;
                imagePreview.style.display = 'block';
            };
    
            reader.readAsDataURL(file);
        } else {
            imagePreview.src = '';
            imagePreview.style.display = 'none';
        }
    }
    
    document.querySelectorAll('.view-image-icon').forEach((icon) => {
        icon.addEventListener('click', (event) => {
            const modalId = icon.dataset.target;
            const modal = document.querySelector(modalId);
            if (modal) {
                modal.style.display = 'block';
            }
        });
    });

    // Fechar o modal ao clicar no botão de fechar
    document.querySelectorAll('.close-modal').forEach((closeButton) => {
        closeButton.addEventListener('click', (event) => {
            const target = closeButton.dataset.target;
            const modal = document.querySelector(target);
            if (modal) {
                modal.style.display = 'none';
            }
        });
    });

    // Fechar o modal ao clicar fora do conteúdo
    document.querySelectorAll('.image-modal').forEach((modal) => {
        modal.addEventListener('click', (event) => {
            if (event.target === modal) {
                modal.style.display = 'none';
            }
        });
    });

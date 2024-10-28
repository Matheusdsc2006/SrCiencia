document.addEventListener('DOMContentLoaded', function() {
    

    const disciplinaSelect = document.querySelector('#id_disciplina');
    const conteudoSelect = document.querySelector('#id_conteudo');
    const topicoSelect = document.querySelector('#id_topico');

    disciplinaSelect.addEventListener('change', function () {
        const disciplinaId = this.value;
        updateConteudos(disciplinaId);
    });

    conteudoSelect.addEventListener('change', function () {
        const conteudoId = this.value;
        updateTopicos(conteudoId);
    });

    function updateConteudos(disciplinaId) {
        fetch(`/api/conteudos/${disciplinaId}/`)  
            .then(response => response.json())
            .then(data => {
                conteudoSelect.innerHTML = ''; 
                if (data.length > 0) {
                    data.forEach(conteudo => {
                        const option = new Option(conteudo.nome, conteudo.id);
                        conteudoSelect.add(option);
                    });
                    conteudoSelect.disabled = false; 
                } else {
                    conteudoSelect.disabled = true; 
                }
            });
    }

    function updateTopicos(conteudoId) {
        fetch(`/api/topicos/${conteudoId}/`)  
            .then(response => response.json())
            .then(data => {
                topicoSelect.innerHTML = '';
                if (data.length > 0) {
                    data.forEach(topico => {
                        const option = new Option(topico.nome, topico.id);
                        topicoSelect.add(option);
                    });
                    topicoSelect.disabled = false;
                } else {
                    topicoSelect.disabled = true; 
                }
            });
    }
});
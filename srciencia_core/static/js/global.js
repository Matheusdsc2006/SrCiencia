fetch('sr-ciencia.json')
            .then(response => response.json())
            .then(data => {
                const container = document.getElementById('icon-container');
                data.icons.forEach(icon => {
                    const img = document.createElement('img');
                    img.src = icon.url;  // Use a propriedade correta do seu JSON
                    img.alt = icon.name;
                    img.style.width = '50px'; // Defina um tamanho desejado
                    img.style.height = '50px';
                    container.appendChild(img);
                });
            })
            .catch(error => console.error('Erro ao carregar o JSON:', error));
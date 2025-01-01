fetch('sr-ciencia.json')
            .then(response => response.json())
            .then(data => {
                const container = document.getElementById('icon-container');
                data.icons.forEach(icon => {
                    const img = document.createElement('img');
                    img.src = icon.url;
                    img.alt = icon.name;
                    img.style.width = '50px';
                    img.style.height = '50px';
                    container.appendChild(img);
                });
            })
            .catch(error => console.error('Erro ao carregar o JSON:', error));
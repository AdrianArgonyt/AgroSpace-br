
document.addEventListener('DOMContentLoaded', () => {
    const apiBaseUrl = `${window.location.origin}/api`;
    let selectedCrop = null;
    let selectedEnvironment = null;

    const selectors = {
        cropList: document.getElementById('crop-list'),
        environmentList: document.getElementById('environment-list'),
        selectedCropCard: document.getElementById('selected-crop-card'),
        selectedEnvironmentCard: document.getElementById('selected-environment-card'),
        compareBtn: document.getElementById('compare-btn'),
        resultCard: document.getElementById('result-card'),
    };

    const apiFetch = async (endpoint) => {
        try {
            const response = await fetch(`${apiBaseUrl}${endpoint}`);
            if (!response.ok) {
                throw new Error(`Ocorreu um erro inesperado no servidor. Status: ${response.status}`);
            }
            return await response.json();
        } catch (error) {
            console.error(`Erro no fetch da API para o endpoint ${endpoint}:`, error);
            throw error;
        }
    };

    const createProgressBar = (value, min, max) => {
        const percentage = ((value - min) / (max - min)) * 100;
        return `<div class="w-full bg-gray-700 rounded-full h-2.5">
                    <div class="bg-blue-400 h-2.5 rounded-full" style="width: ${percentage}%"></div>
                </div>`;
    };
    
    const renderItemList = (element, items, type, clickHandler) => {
        element.innerHTML = '';
        items.forEach(item => {
            const li = document.createElement('li');
            li.className = 'flex items-center p-2 rounded-lg cursor-pointer hover:bg-slate-700 transition-colors duration-200';
            li.dataset.id = item.Id;
            
            // CORREÇÃO: Remove o prefixo 'web/' do caminho da imagem.
            // O servidor agora serve a pasta 'web' na raiz, então o caminho relativo correto é 'resources/...'
            const imagePath = item.ImagePath ? item.ImagePath.replace('web/', '') : 'resources/placeholder.png';

            li.innerHTML = `
                <img src="${imagePath}" alt="${type === 'crop' ? item.CommonName : item.Name}" class="w-8 h-8 rounded-full mr-3 object-cover">
                <span class="font-medium">${type === 'crop' ? item.CommonName : item.Name}</span>
            `;
            li.addEventListener('click', () => clickHandler(item, li));
            element.appendChild(li);
        });
    };

    const displaySelectedItem = (cardElement, item, type) => {
        cardElement.classList.remove('opacity-0');
        const isCrop = type === 'crop';

        // CORREÇÃO: Remove o prefixo 'web/' do caminho da imagem, similar à correção anterior.
        const imagePath = item.ImagePath ? item.ImagePath.replace('web/', '') : 'resources/placeholder.png';
        
        let detailsHtml = `
            <div class="flex flex-col items-center text-center">
                <img src="${imagePath}" alt="${isCrop ? item.CommonName : item.Name}" class="w-20 h-20 rounded-full mb-4 border-2 border-slate-500 object-cover">
                <h3 class="text-xl font-bold">${isCrop ? item.CommonName : item.Name}</h3>
                <p class="text-sm text-slate-400">${isCrop ? item.ScientificName || '' : item.Type || ''}</p>
            </div>
            <div class="space-y-4 mt-4 w-full">
        `;

        if (isCrop) {
            detailsHtml += `
                <div>
                    <div class="flex justify-between text-xs mb-1"><span>Temperatura</span> <span>${item.TempMinC}°C - ${item.TempMaxC}°C</span></div>
                    ${createProgressBar( (item.TempMinC + item.TempMaxC) / 2, -50, 50)}
                </div>
                <div>
                    <div class="flex justify-between text-xs mb-1"><span>pH do Solo</span> <span>${item.PhMin} - ${item.PhMax}</span></div>
                    ${createProgressBar( (item.PhMin + item.PhMax) / 2, 0, 14)}
                </div>
                <div>
                    <div class="flex justify-between text-xs mb-1"><span>Fotoperíodo</span> <span>${item.PhotoperiodMinH}h - ${item.PhotoperiodMaxH}h</span></div>
                    ${createProgressBar( (item.PhotoperiodMinH + item.PhotoperiodMaxH) / 2, 0, 24)}
                </div>
            `;
        } else { // Environment
            detailsHtml += `
                <div>
                    <div class="flex justify-between text-xs mb-1"><span>Temperatura</span> <span>${item.TempMinC}°C - ${item.TempMaxC}°C</span></div>
                    ${createProgressBar( (item.TempMinC + item.TempMaxC) / 2, -200, 500)}
                </div>
                <div>
                    <div class="flex justify-between text-xs mb-1"><span>Pressão</span> <span>${item.PressureKPa} kPa</span></div>
                    ${createProgressBar(item.PressureKPa, 0, 10000)}
                </div>
            `;
        }

        detailsHtml += '</div>';
        cardElement.innerHTML = detailsHtml;
    };
    
    const handleItemSelection = (listElement, item, clickedLi, type) => {
        // Remove a seleção de outros itens na mesma lista
        Array.from(listElement.children).forEach(child => child.classList.remove('bg-blue-800', 'font-bold'));
        // Adiciona a classe de selecionado ao item clicado
        clickedLi.classList.add('bg-blue-800', 'font-bold');

        if (type === 'crop') {
            selectedCrop = item;
            displaySelectedItem(selectors.selectedCropCard, item, 'crop');
        } else {
            selectedEnvironment = item;
            displaySelectedItem(selectors.selectedEnvironmentCard, item, 'environment');
        }

        // Habilita o botão de comparar apenas se ambos os itens estiverem selecionados
        selectors.compareBtn.disabled = !(selectedCrop && selectedEnvironment);
    };

    const handleCompare = async () => {
        if (!selectedCrop || !selectedEnvironment) return;
        
        selectors.compareBtn.disabled = true;
        selectors.compareBtn.textContent = 'Analisando...';
        
        try {
            const response = await fetch(`${apiBaseUrl}/match`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ cropId: selectedCrop.Id, environmentId: selectedEnvironment.Id }),
            });
            const result = await response.json();
            
            // Mostra o resultado
            selectors.resultCard.classList.remove('hidden');
            selectors.resultCard.innerHTML = `
                <div class="text-center">
                    <h3 class="text-lg font-semibold mb-2">Resultado da Análise</h3>
                    <div class="text-6xl font-bold my-4" style="color: hsl(${(result.score)}, 100%, 60%);">${result.score}%</div>
                    <p class="font-semibold text-slate-300">Compatibilidade</p>
                </div>
                <div class="mt-6">
                    <h4 class="font-semibold mb-2 text-slate-300">Fatores Limitantes:</h4>
                    <ul class="list-disc list-inside text-sm space-y-1 text-red-300">
                        ${result.limiting_factors.map(factor => `<li>${factor}</li>`).join('')}
                    </ul>
                </div>
                <div class="mt-4">
                    <h4 class="font-semibold mb-2 text-slate-300">Recomendações:</h4>
                    <ul class="list-disc list-inside text-sm space-y-1 text-sky-300">
                        ${result.rationale.map(r => `<li>${r}</li>`).join('')}
                    </ul>
                </div>
            `;
            
        } catch (error) {
            console.error('Erro ao comparar:', error);
            selectors.resultCard.classList.remove('hidden');
            selectors.resultCard.innerHTML = `<p class="text-red-400 text-center">Não foi possível realizar a análise. Tente novamente.</p>`;
        } finally {
            selectors.compareBtn.disabled = false;
            selectors.compareBtn.textContent = 'Combinar';
        }
    };

    const initialize = async () => {
        try {
            const [crops, environments] = await Promise.all([
                apiFetch('/crops'),
                apiFetch('/environments')
            ]);
            
            renderItemList(selectors.cropList, crops, 'crop', (item, li) => handleItemSelection(selectors.cropList, item, li, 'crop'));
            renderItemList(selectors.environmentList, environments, 'environment', (item, li) => handleItemSelection(selectors.environmentList, item, li, 'environment'));

            selectors.compareBtn.addEventListener('click', handleCompare);

        } catch (error) {
            selectors.cropList.innerHTML = `<li class="text-red-400 p-2">Erro ao carregar culturas.</li>`;
            selectors.environmentList.innerHTML = `<li class="text-red-400 p-2">Erro ao carregar ambientes.</li>`;
        }
    };

    initialize();
});


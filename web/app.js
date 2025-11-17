// URL base da API
const apiBaseUrl = `${window.location.origin}/api`;

// Estado global da aplicação
const state = {
    currentView: 'simulation', // 'simulation', 'login', 'register', 'admin', 'result'
    token: localStorage.getItem('token') || null,
    username: localStorage.getItem('username') || null,
    matchResult: null,
    // Cache simples para os dados das barras laterais
    crops: [],
    environments: []
};

// Referências aos elementos principais da DOM
const appRoot = document.getElementById('app-root');
const mainNav = document.getElementById('main-nav');

// ===================================================================
// FUNÇÕES DE REQUISIÇÃO À API
// ===================================================================

/**
 * Função utilitária para fazer requisições à API, tratando erros e cabeçalhos.
 */
const apiFetch = async (endpoint, options = {}) => {
    // Mensagem de depuração
    console.log(`[API Fetch] Iniciando requisição para: ${apiBaseUrl}${endpoint}`);
    
    const headers = {
        'Content-Type': 'application/json',
        ...options.headers,
    };
    
    if (state.token) {
        headers['Authorization'] = `Bearer ${state.token}`;
    }

    try {
        const response = await fetch(`${apiBaseUrl}${endpoint}`, { ...options, headers });
        
        if (!response.ok) {
            const errorData = await response.json();
            // Mensagem de depuração
            console.warn(`[API Fetch] Erro na resposta de ${endpoint} (Status: ${response.status}):`, errorData.error);
            if (response.status === 401) {
                handleLogout();
            }
            throw new Error(errorData.error || `Erro ${response.status} na API.`);
        }
        
        const responseData = response.status !== 204 ? await response.json() : null;
        // Mensagem de depuração
        console.log(`[API Fetch] Resposta recebida com sucesso de ${endpoint}:`, responseData);
        return responseData;
        
    } catch (error) {
        console.error(`[API Fetch] Erro crítico no fetch para ${endpoint}:`, error);
        throw error;
    }
};

// ===================================================================
// FUNÇÕES DE RENDERIZAÇÃO DE TELAS (VIEWS)
// ===================================================================

/**
 * Renderiza a barra de navegação principal com base no estado de login.
 */
const renderNav = () => {
    // Mensagem de depuração
    console.log(`[Render] Renderizando navegação. Logado: ${!!state.token}`);
    if (!mainNav) {
         console.warn("[Render] Elemento 'main-nav' não encontrado.");
         return;
    }
    // CORREÇÃO: Usamos data-target em vez de IDs para os botões de navegação
    mainNav.innerHTML = `
        <button data-target="simulation" class="font-orbitron text-sm font-bold ${state.currentView === 'simulation' ? 'text-primary-color' : 'text-text-dark'} hover:text-primary-color">Simulação</button>
        ${state.token 
            ? `<button data-target="admin" class="font-orbitron text-sm font-bold ${state.currentView === 'admin' ? 'text-primary-color' : 'text-text-dark'} hover:text-primary-color">Admin</button>
               <button data-target="logout" class="font-orbitron text-sm font-bold text-text-dark hover:text-primary-color">Sair (${state.username})</button>`
            : `<button data-target="login" class="font-orbitron text-sm font-bold ${state.currentView === 'login' ? 'text-primary-color' : 'text-text-dark'} hover:text-primary-color">Login Admin</button>`
        }
    `;
};

/**
 * Renderiza a tela principal (Simulação).
 */
const renderSimulationView = () => {
    // Mensagem de depuração
    console.log("[Render] Renderizando tela: Simulação");
    const template = document.getElementById('view-simulation');
    if (!appRoot || !template) {
        console.error("[Render] Falha ao renderizar Simulação: 'app-root' ou 'view-simulation' não encontrados.");
        return;
    }
    appRoot.innerHTML = template.innerHTML;
    
    // (DEBUG) Verifica se os elementos da barra lateral existem
    const cropsListEl = document.getElementById('crops-list');
    const environmentsListEl = document.getElementById('environments-list');
    if (!cropsListEl || !environmentsListEl) {
        console.error("[Render] Falha ao encontrar #crops-list ou #environments-list no DOM da simulação.");
        return;
    }
    
    const cropDetailsEl = document.getElementById('crop-details');
    const environmentDetailsEl = document.getElementById('environment-details');
    const combineButtonEl = document.getElementById('combine-button');
    
    let selectedCrop = null;
    let selectedEnvironment = null;

    const updateCombineButtonState = () => {
        if (combineButtonEl) {
            combineButtonEl.disabled = !(selectedCrop && selectedEnvironment);
        }
    };
    
    // Mensagem de depuração
    console.log("[Data] Carregando dados das barras laterais...");
    loadAndRenderSidebars(cropsListEl, environmentsListEl, (item, li, type) => {
        const listElement = type === 'crop' ? cropsListEl : environmentsListEl;
        Array.from(listElement.children).forEach(child => child.classList.remove('active'));
        li.classList.add('active');

        if (type === 'crop') {
            selectedCrop = item;
            displaySelectedItem(cropDetailsEl, item, 'crop');
        } else {
            selectedEnvironment = item;
            displaySelectedItem(environmentDetailsEl, item, 'environment');
        }
        updateCombineButtonState();
    });
    
    combineButtonEl?.addEventListener('click', async () => {
        if (!selectedCrop || !selectedEnvironment) return;

        combineButtonEl.textContent = 'ANALISANDO...';
        combineButtonEl.disabled = true;

        try {
            const result = await apiFetch('/match', {
                method: 'POST',
                body: JSON.stringify({
                    cropId: selectedCrop.Id,
                    environmentId: selectedEnvironment.Id,
                }),
            });
            state.matchResult = result;
            navigateTo('result');
        } catch (error) {
             alert(`Erro ao processar a análise: ${error.message}`);
        }
    });
};

/**
 * Renderiza a tela de Resultado da Análise.
 */
const renderResultView = () => {
    // Mensagem de depuração
    console.log("[Render] Renderizando tela: Resultado");
    const template = document.getElementById('view-result');
    if (!appRoot || !template) {
        console.error("[Render] Falha ao renderizar Resultado: 'app-root' ou 'view-result' não encontrados.");
        return;
    }
    appRoot.innerHTML = template.innerHTML;
    
    const result = state.matchResult;
    if (!result) {
        appRoot.innerHTML = `<p class="text-center text-red-400">Nenhum resultado para exibir. Por favor, volte à simulação.</p>`;
        return;
    }
    
    const resultCard = appRoot.querySelector('section');
    if (!resultCard) {
         console.error("[Render] Elemento 'section' do resultado não encontrado.");
         return;
    }
    
    const scoreColor = result.score > 70 ? 'text-green-400' : result.score > 40 ? 'text-yellow-400' : 'text-red-400';
    
    resultCard.innerHTML = `
        <h2 class="font-orbitron text-2xl font-bold text-center mb-4">Análise de Compatibilidade</h2>
        <div class="text-center mb-6">
            <p class="text-lg text-text-dark">Score Final</p>
            <p class="font-orbitron text-7xl font-bold ${scoreColor}">${result.score}</p>
        </div>
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
                <h3 class="font-bold text-lg mb-2 text-yellow-400">Fatores Limitantes</h3>
                <ul class="list-disc list-inside space-y-1 text-text-light">
                    ${result.limiting_factors.length > 0 ? result.limiting_factors.map(factor => `<li>${factor}</li>`).join('') : '<li>Nenhum fator limitante.</li>'}
                </ul>
            </div>
            <div>
                <h3 class="font-bold text-lg mb-2 text-green-400">Recomendações</h3>
                <ul class="list-disc list-inside space-y-1 text-text-light">
                    ${result.rationale.length > 0 ? result.rationale.map(rec => `<li>${rec}</li>`).join('') : '<li>Nenhuma recomendação específica.</li>'}
                </ul>
            </div>
        </div>
        <div class="text-center mt-8">
            <button id="back-to-sim" class="font-orbitron text-lg font-bold text-white py-3 px-8 rounded-lg btn-secondary">
                VOLTAR À SIMULAÇÃO
            </button>
        </div>
    `;
    
    // CORREÇÃO: Ativa a animação de entrada
    setTimeout(() => {
        resultCard.classList.add('card-enter-active');
    }, 10);
    
    document.getElementById('back-to-sim')?.addEventListener('click', () => navigateTo('simulation'));
};

/**
 * Renderiza a tela de Login.
 */
const renderLoginView = () => {
    // Mensagem de depuração
    console.log("[Render] Renderizando tela: Login");
    const template = document.getElementById('view-login');
    if (!appRoot || !template) {
         console.error("[Render] Falha ao renderizar Login: 'app-root' ou 'view-login' não encontrados.");
         return;
    }
    appRoot.innerHTML = template.innerHTML;
    
    // (DEBUG) Verifica se o conteúdo foi injetado
    console.log("[Render] Conteúdo de Login injetado no DOM.");
    
    // CORREÇÃO: Ativa a animação de entrada
    setTimeout(() => {
        const loginSection = appRoot.querySelector('section');
        if (loginSection) {
            loginSection.classList.add('card-enter-active');
            console.log("[Render] Animação de Login ativada.");
        } else {
            console.warn("[Render] <section> de Login não encontrada para animar.");
        }
    }, 10);
    
    const loginForm = document.getElementById('login-form');
    const errorMessageEl = document.getElementById('login-error');
    
    loginForm?.addEventListener('submit', async (e) => {
        e.preventDefault();
        errorMessageEl.textContent = '';
        const formData = new FormData(loginForm);
        const data = Object.fromEntries(formData.entries());
        
        try {
            const result = await apiFetch('/login', {
                method: 'POST',
                body: JSON.stringify(data),
            });
            
            state.token = result.token;
            state.username = result.user.username;
            localStorage.setItem('token', result.token);
            localStorage.setItem('username', result.user.username);
            
            navigateTo('admin');
            
        } catch (error) {
            errorMessageEl.textContent = error.message;
        }
    });
    
    // CORREÇÃO: Usar data-target para navegação
    document.getElementById('nav-to-register')?.addEventListener('click', (e) => {
        e.preventDefault();
        navigateTo('register');
    });
};

/**
 * Renderiza a tela de Registro.
 */
const renderRegisterView = () => {
    // Mensagem de depuração
    console.log("[Render] Renderizando tela: Registro");
    const template = document.getElementById('view-register');
    if (!appRoot || !template) {
         console.error("[Render] Falha ao renderizar Registro: 'app-root' ou 'view-register' não encontrados.");
         return;
    }
    appRoot.innerHTML = template.innerHTML;
    
    // (DEBUG) Verifica se o conteúdo foi injetado
    console.log("[Render] Conteúdo de Registro injetado no DOM.");
    
    // CORREÇÃO: Ativa a animação de entrada
    setTimeout(() => {
        const registerSection = appRoot.querySelector('section');
        if (registerSection) {
            registerSection.classList.add('card-enter-active');
            console.log("[Render] Animação de Registro ativada.");
        } else {
            console.warn("[Render] <section> de Registro não encontrada para animar.");
        }
    }, 10);
    
    const registerForm = document.getElementById('register-form');
    const messageEl = document.getElementById('register-message');
    
    registerForm?.addEventListener('submit', async (e) => {
        e.preventDefault();
        messageEl.textContent = '';
        messageEl.className = 'text-sm text-center';
        const formData = new FormData(registerForm);
        const data = Object.fromEntries(formData.entries());
        
        try {
            const result = await apiFetch('/register', {
                method: 'POST',
                body: JSON.stringify(data),
            });
            
            messageEl.textContent = result.message + " Pode fazer o login agora.";
            messageEl.classList.add('text-green-400');
            registerForm.reset();
            
        } catch (error) {
            messageEl.textContent = error.message;
            messageEl.classList.add('text-red-400');
        }
    });
    
    // CORREÇÃO: Usar data-target para navegação
    document.getElementById('nav-to-login')?.addEventListener('click', (e) => {
        e.preventDefault();
        navigateTo('login');
    });
};

/**
 * Renderiza a tela de Administração (com formulários de cadastro).
 */
const renderAdminView = () => {
    // Mensagem de depuração
    console.log("[Render] Renderizando tela: Admin");
    if (!state.token) {
        console.warn("[Auth] Acesso negado ao Admin. Redirecionando para login.");
        navigateTo('login');
        return;
    }
    
    const template = document.getElementById('view-admin');
    if (!appRoot || !template) {
         console.error("[Render] Falha ao renderizar Admin: 'app-root' ou 'view-admin' não encontrados.");
         return;
    }
    appRoot.innerHTML = template.innerHTML;
    
    // (DEBUG) Verifica se o conteúdo foi injetado
    console.log("[Render] Conteúdo de Admin injetado no DOM.");
    
    // CORREÇÃO: Ativa a animação de entrada
    setTimeout(() => {
        const adminSections = appRoot.querySelectorAll('section');
        if (adminSections.length > 0) {
            adminSections.forEach(el => el.classList.add('card-enter-active'));
            console.log("[Render] Animação de Admin ativada.");
        } else {
            console.warn("[Render] <section> de Admin não encontrada para animar.");
        }
    }, 10);
    
    const cropForm = document.getElementById('form-create-crop');
    const envForm = document.getElementById('form-create-env');
    const cropMsg = document.getElementById('crop-form-message');
    const envMsg = document.getElementById('env-form-message');

    cropForm?.addEventListener('submit', async (e) => {
        e.preventDefault();
        cropMsg.textContent = '';
        cropMsg.className = 'text-sm text-center';
        
        const formData = new FormData(cropForm);
        const data = Object.fromEntries(formData.entries());
        
        const numericFields = ['TempMinC', 'TempMaxC', 'PhMin', 'PhMax', 'PhotoperiodMinH', 'PhotoperiodMaxH'];
        numericFields.forEach(field => {
            if(data[field]) data[field] = parseFloat(data[field]);
        });
        
        try {
            const newCrop = await apiFetch('/crops', {
                method: 'POST',
                body: JSON.stringify(data),
            });
            cropMsg.textContent = `Cultura "${newCrop.CommonName}" salva com sucesso!`;
            cropMsg.classList.add('text-green-400');
            cropForm.reset();
            state.crops = []; // Limpa o cache
        } catch (error) {
            cropMsg.textContent = error.message;
            cropMsg.classList.add('text-red-400');
        }
    });
    
    envForm?.addEventListener('submit', async (e) => {
        e.preventDefault();
        envMsg.textContent = '';
        envMsg.className = 'text-sm text-center';

        const formData = new FormData(envForm);
        const data = Object.fromEntries(formData.entries());
        
        const numericFieldsEnv = ['TempMinC', 'TempMaxC', 'PressureKPa', 'SoilPh', 'PhotoperiodH'];
        numericFieldsEnv.forEach(field => {
            if(data[field]) data[field] = parseFloat(data[field]);
        });

        try {
            const newEnv = await apiFetch('/environments', {
                method: 'POST',
                body: JSON.stringify(data),
            });
            envMsg.textContent = `Ambiente "${newEnv.Name}" salvo com sucesso!`;
            envMsg.classList.add('text-green-400');
            envForm.reset();
            state.environments = []; // Limpa o cache
        } catch (error) {
            envMsg.textContent = error.message;
            envMsg.classList.add('text-red-400');
        }
    });
};

// ===================================================================
// FUNÇÕES AUXILIARES DA UI (Simulação)
// ===================================================================

/**
 * Renderiza a lista de itens (culturas ou ambientes) na barra lateral.
 */
const renderItemList = (element, items, type, clickHandler) => {
    if (!element) {
         console.warn(`[Render] Elemento da lista (${type}) não encontrado.`);
         return;
    }
    element.innerHTML = ''; 
    items.forEach(item => {
        const li = document.createElement('li');
        li.className = 'sidebar-item flex items-center p-2 rounded-lg cursor-pointer border-l-4 border-transparent';
        li.dataset.id = item.Id;
        
        const placeholderImg = 'https://placehold.co/100x100/334155/94a3b8?text=?';
        const imagePath = (item.ImagePath && (item.ImagePath.startsWith('http') || item.ImagePath.startsWith('/')))
            ? item.ImagePath
            : (item.ImagePath ? `/${item.ImagePath.replace('web/', '')}` : placeholderImg);

        li.innerHTML = `
            <img src="${imagePath}" alt="${type === 'crop' ? item.CommonName : item.Name}" class="w-10 h-10 rounded-full object-cover mr-3">
            <span class="font-bold">${type === 'crop' ? item.CommonName : item.Name}</span>
        `;
        li.addEventListener('click', () => clickHandler(item, li, type));
        element.appendChild(li);
    });
};

/**
 * Exibe os detalhes do item selecionado no cartão central.
 */
const displaySelectedItem = (cardElement, item, type) => {
    if (!cardElement) {
        console.warn(`[Render] Elemento de detalhes (${type}) não encontrado.`);
        return;
    }
    const isCrop = type === 'crop';
    
    const placeholderImg = 'https://placehold.co/100x100/334155/94a3b8?text=?';
    const imagePath = (item.ImagePath && (item.ImagePath.startsWith('http') || item.ImagePath.startsWith('/')))
        ? item.ImagePath
        : (item.ImagePath ? `/${item.ImagePath.replace('web/', '')}` : placeholderImg);

    let detailsHtml = `
        <img src="${imagePath}" alt="${isCrop ? item.CommonName : item.Name}" class="w-24 h-24 rounded-full object-cover mb-4 border-2 ${isCrop ? 'border-primary-color' : 'border-secondary-color'}">
        <h3 class="font-orbitron text-lg font-bold">${isCrop ? item.CommonName : item.Name}</h3>
        <p class="text-sm text-text-dark mb-4 italic">${isCrop ? (item.ScientificName || '') : (item.Type || '')}</p>
        <div class="w-full space-y-3 px-4">
    `;

    const createProgressBar = (label, text, value, min, max) => {
         const percentage = Math.max(5, Math.min(100, (Math.abs(value) / max) * 100));
         return `
            <div class="w-full text-left">
                <div class="flex justify-between items-center mb-1 text-sm">
                    <span class="font-bold">${label}</span>
                    <span class="text-text-dark">${text}</span>
                </div>
                <div class="w-full bg-border-color rounded-full h-2.5">
                    <div class="progress-bar-fill h-2.5 rounded-full" style="width: ${percentage}%"></div>
                </div>
            </div>
        `;
    };

    if (isCrop) {
        detailsHtml += createProgressBar('Temperatura', `${item.TempMinC} - ${item.TempMaxC} °C`, (item.TempMinC + item.TempMaxC) / 2, -50, 50);
        detailsHtml += createProgressBar('pH do Solo', `${item.PhMin} - ${item.PhMax}`, (item.PhMin + item.PhMax) / 2, 0, 14);
        detailsHtml += createProgressBar('Fotoperíodo', `${item.PhotoperiodMinH} - ${item.PhotoperiodMaxH} h/dia`, (item.PhotoperiodMinH + item.PhotoperiodMaxH) / 2, 0, 24);
    } else {
        detailsHtml += createProgressBar('Temperatura', `${item.TempMinC} - ${item.TempMaxC} °C`, (item.TempMinC + item.TempMaxC) / 2, -200, 500);
        detailsHtml += createProgressBar('pH do Solo', `${item.SoilPh || 'N/A'}`, item.SoilPh || 0, 0, 14);
        detailsHtml += createProgressBar('Pressão', `${item.PressureKPa || 'N/A'} kPa`, item.PressureKPa || 0, 0, 10000);
    }

    detailsHtml += '</div>';
    cardElement.innerHTML = detailsHtml;
};

/**
 * Carrega os dados das barras laterais (usando cache se disponível).
 */
const loadAndRenderSidebars = async (cropsListEl, environmentsListEl, clickHandler) => {
    try {
        if (state.crops.length === 0) {
            console.log("[Data] Cache de culturas vazio. Buscando na API...");
            state.crops = await apiFetch('/crops');
            console.log(`[Data] Culturas recebidas: ${state.crops.length} itens.`);
        }
        if (state.environments.length === 0) {
            console.log("[Data] Cache de ambientes vazio. Buscando na API...");
            state.environments = await apiFetch('/environments');
            console.log(`[Data] Ambientes recebidos: ${state.environments.length} itens.`);
        }
        
        console.log("[Render] Renderizando listas das barras laterais...");
        renderItemList(cropsListEl, state.crops, 'crop', clickHandler);
        renderItemList(environmentsListEl, state.environments, 'environment', clickHandler);
        console.log("[Render] Listas das barras laterais renderizadas.");

    } catch (error) {
        console.error("Erro CRÍTICO em loadAndRenderSidebars:", error);
        if (cropsListEl) cropsListEl.innerHTML = `<li class="text-center text-red-400">Erro ao carregar culturas.</li>`;
        if (environmentsListEl) environmentsListEl.innerHTML = `<li class="text-center text-red-400">Erro ao carregar ambientes.</li>`;
    }
};

// ===================================================================
// NAVEGAÇÃO E INICIALIZAÇÃO
// ===================================================================

/**
 * Lógica de Logout.
 */
const handleLogout = () => {
    console.log("[Auth] Usuário fazendo logout.");
    state.token = null;
    state.username = null;
    localStorage.removeItem('token');
    localStorage.removeItem('username');
    navigateTo('simulation');
};

/**
 * Função central de navegação que renderiza a tela correta.
 */
const navigateTo = (view) => {
    console.log(`[Navegação] Navegando para a tela: ${view}`);
    state.currentView = view;
    if (!appRoot) {
        console.error("[Navegação] Falha crítica: Elemento 'app-root' não encontrado.");
        return;
    }
    appRoot.innerHTML = ''; // Limpa a tela
    renderNav(); // Renderiza a navegação
    
    switch (view) {
        case 'simulation':
            renderSimulationView();
            break;
        case 'login':
            renderLoginView();
            break;
        case 'register':
            renderRegisterView();
            break;
        case 'admin':
            renderAdminView();
            break;
        case 'result':
            renderResultView();
            break;
        default:
            console.warn(`[Navegação] Tela desconhecida '${view}'. Voltando para 'simulation'.`);
            renderSimulationView();
    }
};

/**
 * (NOVA CORREÇÃO) Inicializa o ouvinte de eventos da navegação principal.
 * Isso usa "event delegation", que é mais robusto.
 */
const initializeApp = () => {
    if (!mainNav) {
        console.error("[Init] Falha fatal: Elemento 'main-nav' não encontrado no DOM.");
        return;
    }
    
    mainNav.addEventListener('click', (e) => {
        // Encontra o botão que foi clicado, mesmo que o clique seja no texto dentro dele
        const targetButton = e.target.closest('button');
        if (!targetButton) return; // Sai se o clique não foi em um botão
        
        const targetView = targetButton.dataset.target;
        if (!targetView) return; // Sai se o botão não tem um data-target

        // Trata o logout separadamente
        if (targetView === 'logout') {
            handleLogout();
        } else {
            navigateTo(targetView);
        }
    });

    // Carrega a tela inicial
    navigateTo(state.currentView);
};


// --- PONTO DE ENTRADA DA APLICAÇÃO ---
if (document.readyState === 'loading') {
    console.log("[Init] DOM ainda carregando. Aguardando DOMContentLoaded.");
    document.addEventListener('DOMContentLoaded', initializeApp);
} else {
    // Se o DOM já estiver pronto, executa imediatamente.
    console.log("[Init] DOM pronto. Iniciando a aplicação imediatamente.");
    initializeApp();
}
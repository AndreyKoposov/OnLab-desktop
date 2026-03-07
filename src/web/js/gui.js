async function initGUI() {
    // Элементы интерфейса
    const btn1 = document.getElementById('btn1');
    const btn2 = document.getElementById('btn2');
    const btn3 = document.getElementById('btn3');
    const btn4 = document.getElementById('btn4');
    const btn5 = document.getElementById('btn5');
    const btn6 = document.getElementById('btn6');
    
    const contentArea = document.getElementById('contentArea');

    // Массив всех кнопок для управления active-классом
    const allBtns = [btn1, btn2, btn3, btn4, btn5, btn6];

    // Функция сброса активного класса и установки нового
    function setActiveButton(activeBtn) {
        allBtns.forEach(btn => btn.classList.remove('active'));
        activeBtn.classList.add('active');
    }

    // Функция обновления контента
    function updateContent(btnNumber) {
        if (btnNumber == 1)
        contentArea.innerHTML = `
        <div class="chat-container">
            <!-- Заголовок чата - всегда сверху -->
            <div class="chat-header">
                <h3>💬 Ассистент по онтологическому анализу</h3>
            </div>

            <!-- Область сообщений - скроллится -->
            <div class="chat-messages" id="chatMessages">
                <!-- Приветственное сообщение -->
                <div class="message assistant">
                    <div class="message-bubble">
                        Здравствуйте! Я ваш ассистент по онтологическому анализу процессов. Чем могу помочь?
                        <div class="message-time">10:00</div>
                    </div>
                </div>
            </div>

            <!-- Область ввода - всегда снизу -->
            <div class="chat-input-area">
                <div class="input-wrapper">
                    <input type="text" class="chat-input" id="chatInput" placeholder="Введите сообщение..." autocomplete="off">
                    <button class="send-btn" id="sendMessageBtn" title="Отправить">➤</button>
                </div>

                <!-- Кнопки команд -->
                <div class="command-buttons" id="commandButtons">
                    <button class="command-btn" data-command="/help">/help</button>
                    <button class="command-btn" data-command="/analyze">/analyze</button>
                    <button class="command-btn" data-command="/ontology">/ontology</button>
                    <button class="command-btn" data-command="/processes">/processes</button>
                    <button class="command-btn" data-command="/clear">/clear</button>
                    <button class="command-btn" data-command="/export">/export</button>
                </div>
            </div>
        </div>
        `;
    }

    // ========== УПРАВЛЕНИЕ ПРОЦЕССАМИ ==========
    
    // Начальные данные процессов
    let processes = []
    infos = await eel.get_processes_list()()
    for (let i = 0; i < infos.length; i++) {
        pr_id = infos[i]["id"]
        pr_name = infos[i]["name"]
        pr_avatar = infos[i]["avatar"]
        pr_created = infos[i]["created"]

        processes.push({ id: pr_id, name: pr_name, avatar: pr_avatar, badge: '24 элемента', meta: pr_created })
    }

    // DOM элементы
    const processItems = document.getElementById('processItems');
    const processCount = document.getElementById('processCount');
    const addProcessBtn = document.getElementById('addProcessBtn');

    // Модальное окно
    const modalOverlay = document.createElement('div');
    modalOverlay.className = 'modal-overlay';
    modalOverlay.innerHTML = `
        <div class="modal">
            <h3 id="modalTitle">Новый процесс</h3>
            <input type="text" class="modal-input" id="processNameInput" placeholder="Введите название процесса">
            <div class="modal-buttons">
                <button class="modal-btn cancel" id="modalCancel">Отмена</button>
                <button class="modal-btn save" id="modalSave">Сохранить</button>
            </div>
        </div>
    `;
    document.body.appendChild(modalOverlay);

    const modalTitle = document.getElementById('modalTitle');
    const processNameInput = document.getElementById('processNameInput');
    const modalCancel = document.getElementById('modalCancel');
    const modalSave = document.getElementById('modalSave');

    // Состояние модального окна
    let currentEditId = null;

    // Функция обновления счетчика процессов
    function updateProcessCount() {
        processCount.textContent = `${processes.length} активных`;
    }

    // ID выбранного процесса (по умолчанию первый)
    let selectedProcessId = 1;

    function selectProcess(id) {
        selectedProcessId = id;
        
        // Обновляем классы у всех элементов
        document.querySelectorAll('.process-item').forEach(item => {
            const itemId = parseInt(item.data_id);
            if (itemId === id) {
                item.classList.add('selected');
            } else {
                item.classList.remove('selected');
            }
        });

        // Здесь можно добавить логику загрузки данных выбранного процесса
        eel.select_process(id)()
        console.log('Выбран процесс:', processes.find(p => p.id === id).name);
    }

    // Функция отрисовки списка процессов
    function renderProcesses() {
        processItems.innerHTML = '';
        
        processes.forEach(process => {
            const processElement = document.createElement('div');
            processElement.className = 'process-item';
            processElement.data_id = process.id
            processElement.innerHTML = `
                <div class="process-avatar">${process.avatar}</div>
                <div class="process-info">
                    <div class="process-name-container">
                        <span class="process-name" title="${process.name}">${process.name}</span>
                        <button class="edit-process-btn" data-id="${process.id}" title="Редактировать процесс">✎</button>
                    </div>
                    <div class="process-meta">
                        <span>${process.meta}</span>
                        <span class="badge">${process.badge}</span>
                    </div>
                </div>
            `;
            
            processItems.appendChild(processElement);
        });

        // Добавляем обработчики на клик по процессу (для выделения)
        document.querySelectorAll('.process-item').forEach(item => {
            item.addEventListener('click', (e) => {
                // Не выделяем, если кликнули на кнопку редактирования
                if (e.target.classList.contains('edit-process-btn')) {
                    return;
                }
                const id = parseInt(item.data_id);
                selectProcess(id);
            });
        });

        // Добавляем обработчики на кнопки редактирования
        document.querySelectorAll('.edit-process-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                e.stopPropagation();
                const id = parseInt(btn.dataset.id);
                openEditModal(id);
            });
        });

        updateProcessCount();
    }

    // Функция открытия модального окна для создания
    function openCreateModal() {
        currentEditId = null;
        modalTitle.textContent = 'Новый процесс';
        processNameInput.value = '';
        modalOverlay.classList.add('active');
        processNameInput.focus();
    }

    // Функция открытия модального окна для редактирования
    function openEditModal(id) {
        const process = processes.find(p => p.id === id);
        if (process) {
            console.log("Edit process with id " + process.id)
            currentEditId = id;
            modalTitle.textContent = 'Редактировать процесс';
            processNameInput.value = process.name;
            modalOverlay.classList.add('active');
            processNameInput.focus();
        }
    }

    // Функция закрытия модального окна
    function closeModal() {
        modalOverlay.classList.remove('active');
        processNameInput.value = '';
        currentEditId = null;
    }

    // Функция сохранения процесса
    async function saveProcess() {
        const name = processNameInput.value.trim();
        
        if (!name) {
            alert('Введите название процесса');
            return;
        }

        if (currentEditId != undefined) {
            // Редактирование существующего
            const process = processes.find(p => p.id === currentEditId);
            if (process) {
                new_proc = await eel.rename_process(process.id, name)();
                process.name = new_proc["name"];
                process.avatar = new_proc["avatar"];
            }
        } else {
            // Создание нового
            //const newId = Math.max(...processes.map(p => p.id), 0) + 1;
            //const avatar = name.split(' ').map(word => word[0]).join('').substring(0, 2).toUpperCase() || 'П';
            new_proc = await eel.create_new_process(name)();
            processes.push({
                id: new_proc["id"],
                name: new_proc["name"],
                avatar: new_proc["avatar"],
                badge: '0 элементов',
                meta: new_proc["created"]
            });

            // Автоматически выделяем новый процесс
            selectedProcessId = new_proc["id"];
        }

        renderProcesses();
        closeModal();
    }

    // Инициализация
    renderProcesses();

    // Обработчики для модального окна
    addProcessBtn.addEventListener('click', openCreateModal);
    
    modalCancel.addEventListener('click', closeModal);
    
    modalSave.addEventListener('click', saveProcess);

    // Закрытие по клику на оверлей
    modalOverlay.addEventListener('click', (e) => {
        if (e.target === modalOverlay) {
            closeModal();
        }
    });

    // Закрытие по Escape
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape' && modalOverlay.classList.contains('active')) {
            closeModal();
        }
    });

    // Обработчики для кнопок правой панели
    btn1.addEventListener('click', function(e) {
        setActiveButton(btn1);
        updateContent(1);
        startChat()
    });

    btn2.addEventListener('click', function(e) {
        setActiveButton(btn2);
        updateContent(2);
    });

    btn3.addEventListener('click', function(e) {
        setActiveButton(btn3);
        updateContent(3);
    });

    btn4.addEventListener('click', function(e) {
        setActiveButton(btn4);
        updateContent(4);
    });

    btn5.addEventListener('click', function(e) {
        setActiveButton(btn5);
        updateContent(5);
    });

    btn6.addEventListener('click', function(e) {
        setActiveButton(btn6);
        updateContent(6);
    });

    // Инициализация контента
    btn1.click()
    //setActiveButton(btn1);
    //updateContent(1);
}
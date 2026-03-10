async function initGUI() {
    // Элементы интерфейса
    const btn1 = document.getElementById('btn1');
    const btn2 = document.getElementById('btn2');
    const btn3 = document.getElementById('btn3');
    const btn4 = document.getElementById('btn4');
    const btn5 = document.getElementById('btn5');
    const btn6 = document.getElementById('btn6');

    // Область оснвного контента
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
        if (btnNumber == 2)
            contentArea.innerHTML = `
        <!-- XML редактор (вставьте это внутрь .content-area) -->
<div class="xml-container" id="xmlContainer">
    <!-- Заголовок -->
    <div class="xml-header">
        <h3>
            📄 XML документ
        </h3>
        <div class="xml-unsaved-badge" id="xmlUnsavedBadge">✎ Несохранённые изменения</div>
    </div>
    
    <!-- Область редактирования -->
    <div class="xml-editor-area">
        <!-- Индикатор загрузки -->
        <div class="xml-loading" id="xmlLoading" style="display: none;">
            <div class="xml-loading-spinner"></div>
        </div>
        
        <!-- Редактор с нумерацией строк -->
        <div class="xml-editor-wrapper">
            <textarea 
                class="xml-textarea" 
                id="xmlTextarea"
                spellcheck="false"
                wrap="off"
                placeholder="Загрузка XML документа..."
            ></textarea>
        </div>
    </div>
    
    <!-- Панель инструментов -->
    <div class="xml-toolbar">
        <div class="xml-toolbar-left">
            <button class="xml-btn" id="xmlSaveBtn" title="Сохранить изменения">
                💾 Сохранить
            </button>
            <button class="xml-btn" id="xmlCopyBtn" title="Копировать в буфер обмена">
                📋 Копировать
            </button>
            <button class="xml-btn" id="xmlDownloadBtn" title="Скачать XML файл">
                ⬇️ Скачать
            </button>
        </div>
       
    </div>
    
    <!-- Статусбар -->
    <div class="xml-statusbar">
        <div class="xml-status">
            <div class="xml-status-item">
                <span class="xml-status-dot valid" id="xmlValidationDot"></span>
                <span id="xmlValidationStatus">XML валиден</span>
            </div>
            <div class="xml-status-item">
                <span id="xmlLineCount">Строк: 0</span>
            </div>
            <div class="xml-status-item">
                <span id="xmlCharCount">Символов: 0</span>
            </div>
        </div>
        <div class="xml-encoding">
            UTF-8
        </div>
    </div>
</div>
        `;
        if (btnNumber == 3)
            contentArea.innerHTML = `
        `;
        if (btnNumber == 4)
            contentArea.innerHTML = `
        <!-- Таблица для просмотра данных (вставьте это внутрь .content-area) -->
<div class="table-container" id="tableContainer">
    <!-- Заголовок -->
    <div class="table-header">
        <h3>
            📊 Таблица данных
        </h3>
        <div class="table-count-badge" id="tableRowCount">0 записей</div>
    </div>
    
    <!-- Область таблицы -->
    <div class="table-wrapper" id="tableWrapper">
        <!-- Индикатор загрузки -->
        <div class="table-loading" id="tableLoading" style="display: none;">
            <div class="table-loading-spinner"></div>
        </div>
        
        <!-- Таблица -->
        <table class="data-table" id="dataTable">
            <thead>
                <tr>
                    <th>Параметр</th>
                    <th>Признак модели</th>
                    <th>Трансформация</th>
                </tr>
            </thead>
            <tbody id="tableBody">
                <!-- Данные будут вставлены через JavaScript -->
            </tbody>
        </table>
        
        <!-- Пустое состояние -->
        <div class="table-empty" id="tableEmpty" style="display: none;">
            <div class="table-empty-icon">📭</div>
            <div>Нет данных для отображения</div>
            <div style="font-size: 13px; color: #cbd5e1;">Загрузите данные через Python</div>
        </div>
    </div>
    
    <!-- Панель инструментов -->
    <div class="table-toolbar">
        
        
        <div class="table-toolbar-left">
            <button class="table-btn" id="tableExportBtn" title="Скачать в Excel формате">
                📥 Скачать Excel
            </button>
            <button class="table-btn" id="tableRefreshBtn" title="Обновить данные">
                🔄 Обновить
            </button>
        </div>
    </div>
</div>
        `;
        if (btnNumber == 5)
            contentArea.innerHTML = `
        `;
        if (btnNumber == 6)
            contentArea.innerHTML = `
        `;
    }

    // ========== УПРАВЛЕНИЕ ПРОЦЕССАМИ ==========
    let processes = []

    // Получение процессов с сервера 
    async function fetch_processes() {
        // Очистка списка процессов
        processes = []
        // Запрос процессов от python eel
        infos = await eel.fetch_processes()()
        // Добавляем процессы в список
        for (let i = 0; i < infos.length; i++) {
            pr_id = infos[i]["id"]
            pr_name = infos[i]["name"]
            pr_avatar = infos[i]["avatar"]
            pr_created = infos[i]["created"]
            pr_option = infos[i]["option"]

            processes.push({ id: pr_id, name: pr_name, avatar: pr_avatar, badge: '24 элемента', meta: pr_created, option: pr_option })
        }
    }
    // Функция обновления счетчика процессов
    function updateProcessCount() {
        processCount.textContent = `${processes.length} активных`;
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

    // Элементы модального окна
    const modalTitle = document.getElementById('modalTitle');
    const processNameInput = document.getElementById('processNameInput');
    const modalCancel = document.getElementById('modalCancel');
    const modalSave = document.getElementById('modalSave');

    // Состояние модального окна
    let currentEditId = null;
    let deleteMode = false;

    // ID выбранного процесса (по умолчанию первый)
    let selectedProcessId = undefined;

    // Обработка нажатия на процесс
    function selectProcess(id) {
        selectedProcessId = id;
        // Визуальная подсветка
        highlightProcess(id)
        // Здесь можно добавить логику загрузки данных выбранного процесса
        eel.select_process(id)()
        const process = processes.find(p => p.id === id)
        const option = process["option"];
        console.log('Выбран процесс:', process.name);
        console.log('Текущая опция:', option);

        if (option === 1) btn1.click();
        if (option === 2) btn2.click();
        if (option === 3) btn3.click();
        if (option === 4) btn4.click();
        if (option === 5) btn5.click();
        if (option === 6) btn6.click();
    }
    function highlightProcess(id) {
        // Обновляем классы у всех элементов
        document.querySelectorAll('.process-item').forEach(item => {
            const itemId = parseInt(item.data_id);
            if (itemId === id) {
                item.classList.add('selected');
            } else {
                item.classList.remove('selected');
            }
        });
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
                        <button class="edit-process-btn" data-id="${process.id}" data-type="edit" title="Редактировать процесс">✎</button>
                        <button class="edit-process-btn" data-id="${process.id}" data-type="delete" title="Удалить процесс">❌</button>
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
                // Не выделяем, если кликнули на кнопку редактирования или удаления
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
                const type = btn.dataset.type;
                if (type === "delete")
                    openDeleteModal(id);
                else
                    openEditModal(id);
            });
        });

        highlightProcess(selectedProcessId)
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
            currentEditId = id;
            modalTitle.textContent = 'Редактировать процесс';
            processNameInput.value = process.name;
            modalOverlay.classList.add('active');
            processNameInput.focus();
        }
        else {
            console.log("Cant find process with id " + process.id)
        }
    }
    // Функция открытия модального окна для удаления
    function openDeleteModal(id) {
        deleteMode = true;
        const process = processes.find(p => p.id === id);
        if (process) {
            currentEditId = id;
            modalTitle.textContent = 'Удаление процесса! Введите "' + process.name + '"';
            processNameInput.value = '';
            modalOverlay.classList.add('active');
            processNameInput.focus();
        }
        else {
            console.log("Cant find process with id " + process.id)
        }
    }
    // Функция закрытия модального окна
    function closeModal() {
        modalOverlay.classList.remove('active');
        processNameInput.value = '';
        currentEditId = null;
        deleteMode = false;
    }
    // Функция сохранения процесса
    async function saveProcess() {
        const name = processNameInput.value.trim();
        
        if (!name) {
            alert('Введите название процесса');
            return;
        }

        if (currentEditId != undefined) {
            // Редактирование/удаление существующего
            const process = processes.find(p => p.id === currentEditId);
            if (process) {
                if (deleteMode) {
                    if (name === process.name)
                        await eel.delete_process(process.id)();
                    else {
                        alert('Неверно введено название!');
                        return;
                    }
                }
                else
                    await eel.edit_process(process.id, name)();

                await fetch_processes()
            }
        } else {
            // Создание нового
            await eel.create_process(name)();
            await fetch_processes()
        }

        renderProcesses();
        closeModal();
    }

    // Инициализация
    await fetch_processes()
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
    // Сохранение выбранной опции и обновление значения в списке процессов
    function set_option(option) {
        eel.set_option(option)();
        const process = processes.find(p => p.id === selectedProcessId);
        process.option = option;
    }

    // Обработчики для кнопок правой панели
    btn1.addEventListener('click', function(e) {
        if (selectedProcessId == undefined)
            return;

        set_option(1);
        setActiveButton(btn1);
        updateContent(1);
        startChat()
    });

    btn2.addEventListener('click', function(e) {
        if (selectedProcessId == undefined)
            return;

        set_option(2);
        setActiveButton(btn2);
        updateContent(2);
        initXMLviewer()
    });

    btn3.addEventListener('click', function(e) {
        if (selectedProcessId == undefined)
            return;

        set_option(3);
        setActiveButton(btn3);
        updateContent(3);
    });

    btn4.addEventListener('click', function(e) {
        if (selectedProcessId == undefined)
            return;

        set_option(4);
        setActiveButton(btn4);
        updateContent(4);
        startTable()
    });

    btn5.addEventListener('click', function(e) {
        if (selectedProcessId == undefined)
            return;

        set_option(5);
        setActiveButton(btn5);
        updateContent(5);
    });

    btn6.addEventListener('click', function(e) {
        if (selectedProcessId == undefined)
            return;

        set_option(6);
        setActiveButton(btn6);
        updateContent(6);
    });

    // Сразу нажимаем на чат
    //btn1.click()
}
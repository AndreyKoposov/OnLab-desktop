function startChecker() {
    var url = "http://90.156.155.241/ping"
    // Создание проверщика
    const connectionChecker = getConnectionChecker(url, 20000);
    // Устанавливаем обработчики событий
    connectionChecker.onConnectionLost(() => {
        setConnectionStatus(false) // При потере соединения
    });
    connectionChecker.onConnectionRestored(() => {
        setConnectionStatus(true) // При подключении
    });
    connectionChecker.onStatusChange((isConnected, statusCode, error) => {
        setConnectionStatus(isConnected)
        console.log(`Статус соединения: ${isConnected ? 'Подключено' : 'Отключено'}`, 
                    statusCode ? `Код: ${statusCode}` : '',
                    error ? `Ошибка: ${error.message}` : ''); // Если состояние подключения изменилось
    });
    // Запускаем проверку
    connectionChecker.start();
}

function setConnectionStatus(isOnline) {
    const indicator = document.getElementById('statusIndicator');
    const statusText = document.getElementById('statusText');
    
    if (isOnline) {
        indicator.classList.remove('offline');
        indicator.classList.add('online');
        statusText.textContent = 'Соединение установлено';
    } else {
        indicator.classList.remove('online');
        indicator.classList.add('offline');
        statusText.textContent = 'Нет соединения';
    }
}

function getConnectionChecker(url, timeout) {
    // Переменная для хранения интервала
    let intervalId = null;
    
    // Флаг для отслеживания состояния соединения
    let isConnected = true;
    
    // Функция для выполнения проверки соединения
    async function checkConnection() {
        try {
            const controller = new AbortController(); // Для прерывание запроса по истечению timeout
            const timeoutId = setTimeout(() => controller.abort(), timeout); // Запускаем таймер timeout
            
            const response = await fetch(url, {
                method: 'HEAD', // Используем HEAD запрос для минимальной нагрузки
                cache: 'no-cache',
                signal: controller.signal // Привязываем сигнал котнроллера
            });
            
            clearTimeout(timeoutId); 
            
            const newStatus = response.ok;
            
            // Если статус изменился, вызываем соответствующий колбэк
            if (newStatus !== isConnected) {
                if (newStatus) {
                    onConnectionRestored?.();
                } else {
                    onConnectionLost?.();
                }
                isConnected = newStatus;
            }

            // Если нет - вызываем колбэк с результатом проверки
            onStatusChange?.(newStatus, response.status);
            
        } catch (error) {
            // Если произошла ошибка (сеть недоступна, таймаут и т.д.)
            if (error.name === 'AbortError') {
                console.log('Request timeout - connection may be slow or unavailable');
            }
            
            if (isConnected) {
                onConnectionLost?.();
                isConnected = false;
            }
            
            onStatusChange?.(false, null, error);
        }
    }
    
    // Колбэки для различных событий
    let onConnectionLost = null;
    let onConnectionRestored = null;
    let onStatusChange = null;
    
    // Запуск проверки
    function start() {
        if (intervalId === null) {
            // Сразу выполняем первую проверку
            checkConnection();
            // Затем запускаем интервал на секунду
            intervalId = setInterval(checkConnection, 1000);
            console.log('Connection checking started');
        }
    }
    
    // Остановка проверки
    function stop() {
        if (intervalId !== null) {
            clearInterval(intervalId);
            intervalId = null;
            console.log('Connection checking stopped');
        }
    }
    
    // Методы для установки колбэков
    return {
        start,
        stop,
        onConnectionLost: (callback) => { onConnectionLost = callback; },
        onConnectionRestored: (callback) => { onConnectionRestored = callback; },
        onStatusChange: (callback) => { onStatusChange = callback; },
        isRunning: () => intervalId !== null,
        getCurrentStatus: () => isConnected
    };
}
/**
 * Чат с ИИ - модуль для интеграции в основное приложение
 */
function startChat() {
    // Состояние чата
    const chatState = {
        messages: [],
        isTyping: false,
        userId: 'user',
        assistantId: 'assistant'
    };

    // DOM элементы
    const chatMessages = document.getElementById('chatMessages');
    const chatInput = document.getElementById('chatInput');
    const sendBtn = document.getElementById('sendMessageBtn');
    const commandButtons = document.getElementById('commandButtons');

    // Инициализация чата
    function initChat() {
        if (!chatMessages || !chatInput || !sendBtn) {
            console.warn('Элементы чата не найдены');
            return;
        }

        // Загружаем сохраненные сообщения (если есть)
        loadMessages();
        
        // Добавляем обработчики событий
        sendBtn.addEventListener('click', sendMessage);
        chatInput.addEventListener('keypress', handleKeyPress);
        
        // Обработчики для командных кнопок
        if (commandButtons) {
            commandButtons.querySelectorAll('.command-btn').forEach(btn => {
                btn.addEventListener('click', () => {
                    chatInput.value = btn.dataset.command + ' ';
                    chatInput.focus();
                });
            });
        }

        // Скроллим вниз
        scrollToBottom();
    }

    // Загрузка сообщений из localStorage (для демо)
    function loadMessages() {
        const saved = localStorage.getItem('chatMessages');
        if (saved) {
            try {
                chatState.messages = JSON.parse(saved);
                renderMessages();
            } catch (e) {
                console.error('Ошибка загрузки сообщений', e);
            }
        }
    }

    // Сохранение сообщений
    function saveMessages() {
        localStorage.setItem('chatMessages', JSON.stringify(chatState.messages));
    }

    // Отправка сообщения
    function sendMessage() {
        const text = chatInput.value.trim();
        if (!text) return;

        // Добавляем сообщение пользователя
        addMessage(text, 'user');
        chatInput.value = '';

        // Показываем индикатор печатания
        showTypingIndicator();

        // Имитируем ответ ассистента (в реальном приложении здесь будет API вызов)
        setTimeout(() => {
            hideTypingIndicator();
            
            // Генерируем ответ в зависимости от команды
            let response = generateResponse(text);
            addMessage(response, 'assistant');
        }, 1000 + Math.random() * 1000);
    }

    // Генерация ответа (демо-режим)
    function generateResponse(userMessage) {
        const lowerMsg = userMessage.toLowerCase();
        
        if (lowerMsg.includes('/help')) {
            return "Доступные команды:\n/analyze - анализ текущего процесса\n/ontology - показать онтологию\n/processes - список процессов\n/clear - очистить чат\n/export - экспортировать данные";
        }
        else if (lowerMsg.includes('/analyze')) {
            return "🔍 Анализ процесса... Обнаружено 15 сущностей и 23 связи. Рекомендую проверить консистентность онтологии.";
        }
        else if (lowerMsg.includes('/ontology')) {
            return "📊 Текущая онтология содержит 8 классов, 24 свойства и 56 аксиом. Основные классы: Процесс, Ресурс, Роль, Событие.";
        }
        else if (lowerMsg.includes('/processes')) {
            return "📋 Список процессов:\n• Закупка сырья\n• Производство\n• Контроль качества\n• Логистика\n• HR-подбор\n• Финансовый аудит";
        }
        else if (lowerMsg.includes('/clear')) {
            clearChat();
            return "";
        }
        else if (lowerMsg.includes('/export')) {
            return "📎 Экспорт данных в формате OWL завершен. Файл сохранен.";
        }
        else if (lowerMsg.includes('привет') || lowerMsg.includes('здравствуй')) {
            return "Здравствуйте! Чем могу помочь в онтологическом анализе?";
        }
        else if (lowerMsg.includes('спасибо')) {
            return "Пожалуйста! Обращайтесь ещё 😊";
        }
        else {
            const responses = [
                "Интересный вопрос. Дайте подумать...",
                "В контексте онтологического анализа это можно интерпретировать как...",
                "Согласно текущей онтологии, это относится к классу...",
                "Я бы рекомендовал рассмотреть это с точки зрения...",
                "Для более точного анализа мне нужно больше информации о..."
            ];
            return responses[Math.floor(Math.random() * responses.length)];
        }
    }

    // Добавление сообщения
    function addMessage(text, sender) {
        const message = {
            id: Date.now() + Math.random(),
            text: text,
            sender: sender,
            time: new Date().toLocaleTimeString('ru-RU', { hour: '2-digit', minute: '2-digit' })
        };

        chatState.messages.push(message);
        
        // Если это не системная команда очистки, рендерим
        if (!(text === '/clear' && sender === 'user')) {
            renderMessage(message);
        }
        
        saveMessages();
        scrollToBottom();
    }

    // Отрисовка одного сообщения
    function renderMessage(message) {
        if (!chatMessages) return;

        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${message.sender}`;
        messageDiv.dataset.id = message.id;
        
        messageDiv.innerHTML = `
            <div class="message-bubble">
                ${message.text.replace(/\n/g, '<br>')}
                <div class="message-time">${message.time}</div>
            </div>
        `;
        
        chatMessages.appendChild(messageDiv);
    }

    // Отрисовка всех сообщений
    function renderMessages() {
        if (!chatMessages) return;
        
        chatMessages.innerHTML = '';
        chatState.messages.forEach(msg => renderMessage(msg));
        scrollToBottom();
    }

    // Показать индикатор печатания
    function showTypingIndicator() {
        if (chatState.isTyping) return;
        
        chatState.isTyping = true;
        
        const typingDiv = document.createElement('div');
        typingDiv.className = 'message assistant';
        typingDiv.id = 'typingIndicator';
        typingDiv.innerHTML = `
            <div class="typing-indicator">
                <span></span>
                <span></span>
                <span></span>
            </div>
        `;
        
        chatMessages.appendChild(typingDiv);
        scrollToBottom();
    }

    // Скрыть индикатор печатания
    function hideTypingIndicator() {
        const indicator = document.getElementById('typingIndicator');
        if (indicator) {
            indicator.remove();
        }
        chatState.isTyping = false;
    }

    // Очистка чата
    function clearChat() {
        chatState.messages = [];
        chatMessages.innerHTML = '';
        saveMessages();
        
        // Добавляем приветственное сообщение
        addMessage('Чат очищен. Чем могу помочь?', 'assistant');
    }

    // Скролл вниз
    function scrollToBottom() {
        if (chatMessages) {
            chatMessages.scrollTop = chatMessages.scrollHeight;
        }
    }

    // Обработка нажатия Enter
    function handleKeyPress(e) {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            sendMessage();
        }
    }

    // Публичные методы (для вызова из основного приложения)
    window.ChatModule = {
        init: initChat,
        sendMessage: sendMessage,
        clearChat: clearChat,
        addMessage: addMessage
    };

    // Автоматическая инициализация при загрузке DOM
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initChat);
    } else {
        initChat();
    }
}
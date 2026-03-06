function initGUI() {
    // Элементы интерфейса
    const btn1 = document.getElementById('btn1');
    const btn2 = document.getElementById('btn2');
    const btn3 = document.getElementById('btn3');
    const btn4 = document.getElementById('btn4');
    const btn5 = document.getElementById('btn5');
    const btn6 = document.getElementById('btn6');
    
    const contentTitle = document.getElementById('contentTitle');
    const contentBody = document.getElementById('contentBody');
    const contentCard = document.getElementById('contentCard');

    // Массив всех кнопок для управления active-классом
    const allBtns = [btn1, btn2, btn3, btn4, btn5, btn6];

    // Функция сброса активного класса и установки нового
    function setActiveButton(activeBtn) {
        allBtns.forEach(btn => btn.classList.remove('active'));
        activeBtn.classList.add('active');
    }

    // Функция обновления контента
    function updateContent(btnNumber) {
        // Меняем заголовок
        contentTitle.innerHTML = `🧬 Панель ${btnNumber} <span>онтология</span>`;

        // Меняем основной текст в зависимости от кнопки
        let mainText = '';
        let tags = [];

        switch (btnNumber) {
            case 1:
                mainText = 'Здесь будет контент для кнопки 1. Онтологический слой процессов: классификация сущностей, отношения и аксиомы. Отображаются базовые метаданные выбранного процесса.';
                tags = ['сущность: activity', 'сущность: роль', 'отношение: participates_in', 'аксиома: временные рамки'];
                break;
            case 2:
                mainText = 'Контент второй кнопки. Анализ таксономии процессов, иерархия классов и подклассов. Модель онтологии верхнего уровня.';
                tags = ['класс: процесс', 'подкласс: производственный', 'свойство: имеет_вход', 'свойство: имеет_выход'];
                break;
            case 3:
                mainText = 'Содержимое для кнопки 3. Атрибутивный анализ: объектные свойства и атрибуты данных. Отображение доменов и диапазонов.';
                tags = ['datatype: string', 'datatype: integer', 'objectProperty: выполняет', 'функциональное свойство'];
                break;
            case 4:
                mainText = 'Вы нажали кнопку 4. Связи между процессами и временные паттерны. Алгебра процессов и онтология событий.';
                tags = ['событие: старт', 'событие: финиш', 'отношение: последовательность', 'отношение: параллельность'];
                break;
            case 5:
                mainText = 'Кнопка 5. Семантическая разметка и вывод новых знаний. Правила вывода на основе онтологии (SWRL-подобные конструкции).';
                tags = ['правило: modus_ponens', 'правило: наследование', 'аксиома: транзитивность', 'аксиома: симметричность'];
                break;
            case 6:
                mainText = 'Интерфейс для кнопки 6. Визуализация графа онтологии, метрики и статистика. Здесь будет диаграмма (заглушка).';
                tags = ['граф: 124 узла', 'граф: 287 ребер', 'плотность 0.04', 'компоненты связности: 2'];
                break;
            default:
                mainText = 'Выберите кнопку';
                tags = [];
        }

        contentBody.textContent = mainText;

        // Обновляем блок с тегами
        const oldTagsContainer = contentCard.querySelector('.tags-container');
        if (oldTagsContainer) {
            const newTagsContainer = document.createElement('div');
            newTagsContainer.className = 'tags-container';
            
            tags.forEach(tagText => {
                const span = document.createElement('span');
                span.className = 'ontology-tag';
                span.textContent = tagText;
                newTagsContainer.appendChild(span);
            });

            oldTagsContainer.parentNode.replaceChild(newTagsContainer, oldTagsContainer);
        }
    }

    // Назначаем обработчики кликов
    btn1.addEventListener('click', function(e) {
        setActiveButton(btn1);
        updateContent(1);

        prompt_test = `Процесс:
                Фотолитография — метод получения рисунка на поверхности материала.
                На подложку наносится фоторезист, который засвечивается через фотошаблон,
                проявляется, а затем используется для травления или напыления. Фотолитография
                начинается с нанесения фоторезиста на подложку. Затем происходит засвечивание
                через фотошаблон, проявление и использование для травления или напыления.
                
                ## Задание
                Выдели основные сущности описанного процесса и верни их в виде JSON строго по шаблону:
                {
                    entities: [
                        "entity_name_1",
                        "entity_name_2",
                    ]
                }
                `
        // fetch(`http://localhost:8000/api/entities`, 
        //     {
        //         method: "POST",
        //         headers: {
        //           "Content-Type": "application/json",
        //         },
        //         body: JSON.stringify({ prompt: prompt_test }),
        //     }
        // )
        // .then(response => response.json())
        // .then(data => alert(data["content"]))
        // .catch(error => console.error('Error:', error));
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

    // Инициализация
    setActiveButton(btn1);
    updateContent(1);
}
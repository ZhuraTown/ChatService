// Функция для сохранения токена
const saveToken = (token) => {
    localStorage.setItem('AccessToken', token);
};

// Функция для получения токена
const getToken = () => {
    return localStorage.getItem('AccessToken');
};

// Обработка кликов по вкладкам
document.querySelectorAll('.tab').forEach(tab => {
    tab.addEventListener('click', () => showTab(tab.dataset.tab));
});

// Функция отображения выбранной вкладки
function showTab(tabName) {
    document.querySelectorAll('.tab').forEach(tab => tab.classList.remove('active'));
    document.querySelectorAll('.form').forEach(form => form.classList.remove('active'));

    document.querySelector(`.tab[data-tab="${tabName}"]`).classList.add('active');
    document.getElementById(`${tabName}Form`).classList.add('active');
}

// Функция для валидации данных формы
const validateForm = fields => fields.every(field => field.trim() !== '');

// Функция для отправки запросов
const sendRequest = async (url, data) => {
    try {
        const response = await fetch(url, {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify(data)
        });

        const result = await response.json();

        if (response.ok) {
            alert(result.message || 'Операция выполнена успешно!');
            return result;
        } else {
            alert(result.message || 'Ошибка выполнения запроса!');
            return null;
        }
    } catch (error) {
        console.error("Ошибка:", error);
        alert('Произошла ошибка на сервере');
    }
};

// Функция для обработки формы
const handleFormSubmit = async (formType, url, fields) => {
    if (!validateForm(fields)) {
        alert('Пожалуйста, заполните все поля.');
        return;
    }

    const data = await sendRequest(url, formType === 'login'
        ? {email: fields[0], password: fields[1]}
        : {email: fields[0], name: fields[1], password: fields[2], password_check: fields[3]});

    if (data && data.access_token) {
        saveToken(data.access_token)
    }
    if (data && formType === 'login' && data.ok && data.access_token) {
        window.location.href = '/chat';
    }
    return data
};


// Обработка формы входа
document.getElementById('loginButton').addEventListener('click', async (event) => {
    event.preventDefault();

    const email = document.querySelector('#loginForm input[type="email"]').value;
    const password = document.querySelector('#loginForm input[type="password"]').value;

    const response = await handleFormSubmit('login', 'api/users/login', [email, password]);

    if (response && response.access_token) {
        saveToken(response.access_token); // Сохраняем токен
        getChatPageWithToken();
    }
});


const getChatPageWithToken = async () => {
    const token = getToken(); // Получаем токен из localStorage

    if (!token) {
        alert('Ошибка: токен не найден.');
        return;
    }

    try {
        const response = await fetch('/chat', {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${token}`, // Передаём токен
                'Accept': 'text/html' // Ожидаем HTML-ответ
            }
        });

        if (!response.ok) {
            throw new Error('Ошибка загрузки страницы чата');
        }

        const html = await response.text(); // Получаем HTML как текст

        // Заменяем содержимое текущей страницы
        document.open(); // Открываем поток
        document.write(html); // Записываем новый HTML
        document.close(); // Закрываем поток
    } catch (error) {
        console.error('Ошибка:', error);
        alert('Не удалось загрузить страницу чата');
    }
};

// Обработка формы регистрации
document.getElementById('registerButton').addEventListener('click', async (event) => {
    event.preventDefault();

    const email = document.querySelector('#registerForm input[type="email"]').value;
    const name = document.querySelector('#registerForm input[type="text"]').value;
    const password = document.querySelectorAll('#registerForm input[type="password"]')[0].value;
    const password_check = document.querySelectorAll('#registerForm input[type="password"]')[1].value;

    if (password !== password_check) {
        alert('Пароли не совпадают.');
        return;
    }

    await handleFormSubmit('register', 'api/users/register', [email, name, password, password_check]);
});
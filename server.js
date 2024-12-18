const express = require('express');
const sqlite3 = require('sqlite3').verbose();
const cors = require('cors');

const app = express();
const port = 3000;

// Подключение к базе данных SQLite
const db = new sqlite3.Database(':memory:');

// Включаем CORS для возможности работать с клиентом
app.use(cors());

// Разрешаем использование JSON в запросах
app.use(express.json());

// Инициализация базы данных с пробными ID
db.serialize(() => {
  db.run('CREATE TABLE users (id TEXT, name TEXT)');
  const stmt = db.prepare('INSERT INTO users (id, name) VALUES (?, ?)');
  stmt.run('666666', 'Пользователь 666666');
  stmt.run('777777', 'Пользователь 777777');
  stmt.finalize();
});

// Маршрут для проверки существования пользователя
app.post('/check-user', (req, res) => {
  const { id } = req.body;
  db.get('SELECT * FROM users WHERE id = ?', [id], (err, row) => {
    if (err) {
      res.status(500).json({ message: 'Ошибка базы данных' });
    } else if (row) {
      res.json({ message: `Пользователь ${row.name} найден.` });
    } else {
      res.json({ message: 'Пользователь не найден.' });
    }
  });
});

// Запуск сервера
app.listen(port, () => {
  console.log(`Сервер запущен на http://localhost:${port}`);
});
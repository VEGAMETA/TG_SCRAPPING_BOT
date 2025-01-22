# Парсер чатов по ключевым словам

## Использование

### Linux

```bash
pyhton3 -m venv venv
./venv/bin/activate
pip install -r reqirements.txt
```

### Windows

```cmd
pyhton -m venv venv
.\venv\Scripts\activate
pip install -r reqirements.txt
```

### Запуск

```bash
python main.py
```

---

### Настройка

#### Для использования бота необходимо добавить переменные среды или прописать в файл `bot.env` необходимые значения (Доступные при создании приложения по адресу <https://my.telegram.org/apps>)

---

Добавляйте (Каждый элемент с новой сторки):

- Чаты которые нужно проанализировать в `res/chats.list` в формате username (напр `@vegameta` или `vegameta`)
- Ключевые слова в `res/keywords.list` (в т.ч. словосочетания)

---

### TODO

- [ ] TDatas
- [ ] > 1 bot
- [ ] Docker
- [ ] API

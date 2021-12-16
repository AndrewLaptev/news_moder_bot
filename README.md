# news-moder-bot
Moderation news via telegram bot


Plan:
- [x] Разобраться с изначальным кодом получения новостей с каналов
- [x] Разобраться с Telegram API, создать бота и тестовые чаты
- [x] Написать скрипт для бота
- [x] Переписать скрипт для получения новостей
- [x] Распарсить новости в JSON и разобраться с разметкой
- [x] Приделать заголовок канала + ссылку к отправляемой новости (костыльно)
- [x] Приделать к пересыламой новости в бот инлайн кнопки
- [x] Настроить обработчик кнопок
- [x] Сохранять новости в JSON
- [ ] Грамотно распарсить JSON новостей, структуризировать, решить проблему с кодировкой
- [ ] Исправить пересылку сообщений с медиа
- [ ] Исправить некорректную верстку Маркдауна
- [ ] Задеплоить Redis для кэша непроверенных новостей
- [ ] Написать скрипт проверки новостей по словарю перед отправкой в бот
- [ ] Задеплоить MongoDB и настроить отправку проверенных новостей в нее
- [ ] Упаковать все в Docker Compose

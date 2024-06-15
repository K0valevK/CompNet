# Скрипт для тестирования MTU в канале

## Запуск

Сборка docker файла

```
docker build -t mtu-search .
```

Запуск

```
docker run -d -t mtu-search HOSTNAME
```

Где `HOSTNAME` - ip адресс или имя хоста для проверки MTU.

В конце своей работы скрипт выводит значение MTU.

# вторая часть задания
По итогам первой части было создано два репозитория:
* [simplest_grabber](https://github.com/sdlm/simplest_grabber) для получения данных
* [marshmallow_orm_drivers](https://github.com/sdlm/marshmallow_orm_drivers) для сериализации и записи в БД 

### установка пакетов
```
pip install -U -r ./requirements.txt

git submodule update --remote
cd grabber/
pip install .
cd ../marshmallow_orm_drivers/
pip install .
```

Пример вывода ```pip freeze```:   
```
Django==2.0.6
feedparser==5.2.1
marshmallow==2.15.3
...
grabber==0.1
marshmallow_orm_drivers==0.1
```

### Features
* проходят тесты
* пакеты из первой части устанавливаются как pip пакеты

### P.S.
Так же можно посмотреть пробные реализации в других ветках этого репозитория.
* marshmallow
* DRF
* drf-writable-nested

Так же был создан примитивный аналог marshmallow [simplest_serializer](https://github.com/sdlm/simplest_serializer), с тестами.
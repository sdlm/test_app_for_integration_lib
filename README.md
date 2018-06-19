# установка пакетов
```
pip install -U -r ./required.txt

git submodule update --remote
cd lib/grabber/
pip install .
cd ../serializer/
pip install .
```

Пример работы ```pip freeze```:   
```
Django==2.0.6
feedparser==5.2.1
grabber==0.1
serializer==0.1
```

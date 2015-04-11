1. Введение
======================

Почему так важна скорость загрузки и отображения веб ресурсов?
--------------------------------------------------------------
	http://www.searchenginejournal.com/seo-101-important-site-speed-2014/111924/
	http://www.searchenginejournal.com/seo-101-important-site-speed-2014/111924/
	http://www.slate.com/articles/business/operations/2012/06/queueing_theory_what_people_hate_most_about_waiting_in_line_.html
	http://iomelt.com/capacitricks/file/2011/11/7923431-10.1.1.19.3667.pdf
	https://blog.kissmetrics.com/loading-time/
	https://www.thinkwithgoogle.com/articles/the-google-gospel-of-speed-urs-hoelzle.html

Устаревший подход к отображению веб ресурсов
--------------------------------------------

	1. Браузер делает запрос.
	2. Сервер генерирует HTML и отдает его.
	3. Браузер парсит HTML и загружает доп контент (css, js, images)
	4. После загрузки всех критичных ресурсов, браузер рисует страницу

### Минусы:
	
    1. Каждый запрос к серверу полностью пересовывает веб страницу, даже если произошли небольшие изменения.
    2. Каждый раз сервер отдает веб страницу целиком. Страницу никак не кэшируется.
    3. Браузеру необходимо дождаться пока сервер сгенерирует для него страницу и заново запросить дополнительные ресурсы (css, js), даже 	если они закэшированы.

### Что можно улучшить: 

    1. Перенести создание веб страницы с сервера на клиент.	Таким образом не нужно скачивать страницу целиком при каждом запросе.
    2. Уменьшаем количество запросов на сервер, путем сохранени доп ресурсов веб страницы в специальном хранилище брауера.
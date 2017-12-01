# SCRAPY en producción

Demo del Meetup de Python Madrid:

## DevOps y Scraping en el ecosistema Python
https://www.meetup.com/python-madrid/events/244901807/

Para ejecutar el proyecto:

```
pip install -r requirements.txt
scrapy crawl idealista
```

## Parámetros del spider

**neighborhoods:** Barrio o lista de barrios separados por comas que 
se quieren analizar. 

## Pipelines

#### clean.CleanItems

Para cada item, añade:
1. Country Code
2. El precio en float
3. Numero de habitaciones en Float
4. Currency (USD o EUR)

#### prices.AddUSDToItems
Añade el precio en USD

#### stats.AddItemStats
Cachea información para generar las estadísticas.

## Middlewares

#### useragent.RotateUserAgentMiddleware
Añade a la request un user agent de manera random con la posibilidad
de elegir entre una lista de Desktop y Mobile. 


#### customheader.AddCustomHeaderMiddleware
Añade otro header a la request.

## Extensions

#### statistics.StatsExtension

Cuando el spider termina, se genera una señal "spider_closed".

En ese momento, se generan 4 estadísticas:
1. Media de habitaciones
2. Media de precio
3. Media de metros cuadrados
4. Precio medio por metro cuadrado 


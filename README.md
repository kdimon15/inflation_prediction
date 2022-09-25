# Прогнозирование инфляции
> Решение команды Chill_Garage чемпионата Цифровой Прорыв на хакатоне Центрального федерального округа кейса "ИИ прогнозирует инфляцию".


![Python](https://img.shields.io/badge/Python-FFD43B?style=for-the-badge&logo=python&logoColor=blue)
![Jupyter](https://img.shields.io/badge/Jupyter-F37626.svg?&style=for-the-badge&logo=Jupyter&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-2C2D72?style=for-the-badge&logo=pandas&logoColor=white)
![numpy](https://img.shields.io/badge/Numpy-777BB4?style=for-the-badge&logo=numpy&logoColor=white)
![plotly](https://img.shields.io/badge/Plotly-239120?style=for-the-badge&logo=plotly&logoColor=white)


## Данные

Preprocessing.ipynb - Предобработка датасета, для уменьшения потребления ОЗУ

train.ipynb - Файл тренировки моделей

Inference.ipynb - Запуск решения на тестовом датасете

Предказания на тестовой выборке лежат в inference_data/submits


## Описание нашего решения
Решение состоит из 2 частей:
-  Делаем фичи по изменению цен на каждый товар, на этих фичах строим KMeans кластеризацию
-  Для каждого полученного класса строим индекс среднего изменения цен на товары, относительно предыдущего месяца и обучаем линейную регрессию

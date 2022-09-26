import matplotlib

matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.preprocessing import LabelEncoder
import numpy as np
from tqdm import tqdm

import pickle
import pmdarima as pm


async def inference():
    with open(r'D:\Code\bot_for_cfo\utils\models\main_model.pkl', 'rb') as f:
        main_model = pickle.load(f)

    with open(r'D:\Code\bot_for_cfo\utils\models\cluster_model.pkl', 'rb') as f:
        cluster_model, cluster_classes = pickle.load(f)

    path = r'D:\Code\bot_for_cfo\utils\submits\test9.csv'
    test_df = pd.read_csv(path, sep='\t')
    test_df['StockStatus'] = test_df['StockStatus'].str.lower().replace({'instock': 1, 'outofstock': 0}).astype(np.int8)

    test_df['DateObserve'] = pd.to_datetime(test_df['DateObserve'])
    a = LabelEncoder().fit(test_df['WebPriceId'])
    test_df['WebPriceId'] = a.transform(test_df['WebPriceId'])

    test_df['month'] = test_df['DateObserve'].dt.month
    test_df['year'] = test_df['DateObserve'].dt.year
    test_df['day'] = test_df['DateObserve'].dt.day

    test_df['year'] -= test_df['year'].min()
    test_df['num_month'] = test_df['year'] * 12 + test_df['month']
    test_df['num_day'] = test_df['year'] * 366 + test_df['month'] * 31 + test_df['day']
    test_df = test_df.drop(['DateObserve', 'month', 'year'], axis=1)

    tmp_df = test_df[test_df['StockStatus'] == 1][['WebPriceId', 'num_month']].drop_duplicates().groupby(
        'WebPriceId').count()
    goods = tmp_df[tmp_df['num_month'] >= 2].index
    test_df = test_df[test_df['WebPriceId'].isin(goods)]

    test_df = test_df.sort_values('day').reset_index(drop=True)

    all_features = []
    all_target = []
    for month in tqdm(range(test_df['num_month'].min() + 4, test_df['num_month'].max() + 1)):

        cur_features = []
        cur_main_df = test_df[((test_df['num_month'] <= month) & (test_df['num_month'] >= month - 3))]

        goods = cur_main_df[cur_main_df['num_month'] >= 2].index

        # Строим сводную таблицу по товару и месяцам, берем последнюю цену
        grouped = cur_main_df[cur_main_df['WebPriceId'].isin(goods)].groupby(['num_month', 'WebPriceId']).agg(
            {'CurrentPrice': 'last'}).unstack()
        grouped = grouped.fillna(method='ffill').fillna(method='bfill')
        grouped.columns = grouped.columns.droplevel(0)

        # Для каждого товара смотрим на процентное изменение цены, отностельно предыдущего месяца
        month_change = np.exp(np.log((grouped.pct_change() + 1)))
        month_change = month_change[month_change.index != month - 3]

        values = month_change.values.transpose(1, 0)
        main = [values[x] for x in range(len(month_change.columns)) if
                np.array(values[x]).max() < 2.5 and np.array(values[x]).min() > 0.4]
        for j in range(len(main)):
            new_val = [x for x in main[j] if x != 1]
            main[j] = new_val
        cluster_features = [[np.mean(y), np.median(y), np.std(y), len(y)] for y in main if len(y) > 0]

        # Предсказываем типа графика, исходя из предсказания KMeans
        preds = cluster_model.predict(cluster_features)
        c = month_change.columns.tolist()
        for j in cluster_classes:
            good_cols = [c[x] for x in range(len(preds)) if preds[x] == j]
            cur_df = cur_main_df[cur_main_df['WebPriceId'].isin(good_cols)]

            # Берем товары, которые продавались 2 месяца за последние 4 месяца
            tmp_df = cur_df[['WebPriceId', 'num_month']].drop_duplicates().groupby('WebPriceId').count()
            goods = tmp_df[tmp_df['num_month'] >= 2].index
            cur_df = cur_df[cur_df['WebPriceId'].isin(goods)]

            # Берем товары, которые продавались в текущем месяце
            cur_df = cur_df[cur_df['WebPriceId'].isin(cur_df[cur_df['num_month'] == month]['WebPriceId'].unique())]

            # Строим сводную таблицу по товару и месяцам, берем последнюю цену
            grouped = cur_df.groupby(['num_month', 'WebPriceId']).agg({'CurrentPrice': 'last'}).unstack()
            grouped = grouped.fillna(method='ffill').fillna(method='bfill')
            grouped.columns = grouped.columns.droplevel(0)
            # Для каждого товара смотрим на процентное изменение цены, отностельно предыдущего месяца
            month_change = np.exp(np.log((grouped.pct_change() + 1)))
            month_change = month_change[month_change.index == month]

            values = month_change.dropna(axis=1).values[0]
            sort_values = [x for x in values if 0.4 < x < 2.5]

            cur_features.append([np.average(sort_values, weights=[0.2 if x > 1.6 else 1 for x in sort_values]) - 1])
            cur_features.append([np.average(sort_values) - 1])

        all_features.append(np.concatenate(cur_features))
        fig, ax = matplotlib.pyplot.subplots(nrows=1, ncols=1)
        for x in range(len(all_features[0])):
            ax.plot(np.array(all_features)[:, x])
        matplotlib.pyplot.savefig(r"D:\Code\bot_for_cfo\data\photo\graph.png")
        matplotlib.pyplot.close(fig)

        try:
            ARIMA_model = pm.auto_arima(
                pd.Series(np.array(all_features)[:, 0].tolist()).replace(np.inf, np.nan).fillna(method='ffill').fillna(
                    method='bfill').reset_index(drop=True),
                # Первым аргументом передаётся временной ряд, по которому и делается график
                start_p=2,
                start_q=2,
                test='adf',  # use adftest to find optimal 'd'
                max_p=3, max_q=3,  # maximum p and q
                m=1,  # frequency of series (if m==1, seasonal is set to FALSE automatically)
                d=None,  # let model determine 'd'
                seasonal=True,  # No Seasonality for standard ARIMA
                trace=True,  # logs
                error_action='warn',  # shows errors ('ignore' silences these)
                suppress_warnings=True,
                stepwise=True)

            # ARIMA_model.summary()
            ARIMA_model.plot_diagnostics(figsize=(15, 12))
            matplotlib.pyplot.savefig(r"D:\Code\bot_for_cfo\data\photo\graph2.png")
            matplotlib.pyplot.close()
        except ValueError:
            pass
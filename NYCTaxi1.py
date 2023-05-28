import pandas as pd
from pyproj import Transformer

transformer = Transformer.from_crs('epsg:4326', 'epsg:2263')

# CSVファイルを読み込む
df = pd.read_csv('data/NYCTaxi0.csv')

# pickupとdropが同じ座標である行の数をカウントする
same_coord_count = df[(df['pickup_longitude'] == df['dropoff_longitude']) & (df['pickup_latitude'] == df['dropoff_latitude'])].shape[0]
print(f"Same pickup and dropoff coordinates: {same_coord_count}")

# それらの行を除く
df = df[(df['pickup_longitude'] != df['dropoff_longitude']) | (df['pickup_latitude'] != df['dropoff_latitude'])]

# tpep_pickup_datetimeとtpep_dropoff_datetimeをdatetime型に変換する
df['tpep_pickup_datetime'] = pd.to_datetime(df['tpep_pickup_datetime'])
df['tpep_dropoff_datetime'] = pd.to_datetime(df['tpep_dropoff_datetime'])

# 差分が1分未満である行の数をカウントする
less_than_minute_count = df[(df['tpep_dropoff_datetime'] - df['tpep_pickup_datetime']) < pd.Timedelta(minutes=1)].shape[0]
print(f"Less than a minute between pickup and dropoff: {less_than_minute_count}")

# それらの行を除く
df = df[(df['tpep_dropoff_datetime'] - df['tpep_pickup_datetime']) >= pd.Timedelta(minutes=1)]


# 2013-05-08T00:00:00を基準にしたtpep_pickup_datetimeの秒数を生成する
reference_time = pd.Timestamp('2013-05-08T00:00:00')
df['tpep_pickup_seconds'] = (df['tpep_pickup_datetime'] - reference_time).dt.total_seconds()

# tpep_pickup_secondsの昇順にデータを並べ替える
df = df.sort_values(by='tpep_pickup_seconds')

# インデックスをリセット（0から始まる新しい行番号を生成）
df = df.reset_index(drop=True)

x, y = transformer.transform(df['pickup_latitude'].values, df['pickup_longitude'].values)
df['pickup_longitude2'] = x
df['pickup_latitude2'] = y

x, y = transformer.transform(df['dropoff_latitude'].values, df['dropoff_longitude'].values)
df['dropoff_longitude2'] = x
df['dropoff_latitude2'] = y

# 新しいデータフレームを作成する
new_df = pd.DataFrame({
    'Row_Number': df.index,
    'tpep_pickup_seconds': df['tpep_pickup_seconds'],
    'pickup_longitude': df['pickup_longitude2'],
    'pickup_latitude': df['pickup_latitude2'],
    'dropoff_longitude': df['dropoff_longitude2'],
    'dropoff_latitude': df['dropoff_latitude2']
})

# データフレームをCSVファイルとして出力する
df.to_csv('data/NYCTaxi1_sub.csv', encoding='utf-8', index=False)

# データフレームをCSVファイルとして出力する
new_df.to_csv('data/NYCTaxi1_'+str(len(new_df))+'.csv', encoding='utf-8', index=False)
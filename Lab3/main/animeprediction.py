import pandas as pd


# tmp_predictions_df31.xlsx
# C:/Vita/РУДН/СППР/Лабы/2/anime.csv

def predict_anime(index):
    predictions = pd.read_excel('D:/Vita/pythondjango/Animenew/main/tmp_predictions_df31.xlsx')
    results = predictions.loc[index, 0:5]
    results = results.dropna()
    list_pred = []
    for index in range(len(results)):
        tmp = results.iloc[index]
        tmp = tmp.replace('(', '')
        tmp = tmp.replace(')', '')
        tmp = tmp.replace(', ', ' ')
        a = tmp.split(' ')
        b = []
        for i in a:
            b.append(float(i))
        list_pred.append(b)
    recommended_anime_ids=[]
    for x in range(0, len(list_pred)):
        recommended_anime_ids.append(int(list_pred[x][0]))
    anime_df = pd.read_csv("D:/Vita/pythondjango/Animenew/main/anime.csv")
    recommended_anime = anime_df[anime_df['anime_id'].isin(recommended_anime_ids)]
    anime_list = recommended_anime["name"].tolist()
    return anime_list



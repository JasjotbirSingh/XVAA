from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import playground.models
import pandas as pd
import json


@csrf_exempt
def recommender(request):
    if request.method == 'GET':
        params = {}
        for tup in request.GET.items():
            params.update({tup[0]: int(tup[1])})

        dist = playground.models.Distance(params)
        table_top10 = dist.get_distances()
        print(table_top10)

        json_records = table_top10.reset_index().to_json(orient='records')
        data = []
        data = json.loads(json_records)

        return render(request, 'recommendations.html', {'data': data})
    return render(request, 'recommendations.html')


def get_json_of_df(df):
    return json.loads(df.reset_index().to_json(orient='records'))


def contains_question(columns, ques_id):
    for col in columns:
        if col.endswith(ques_id):
            return True
    return False


def get_df_of_tweets(df_questions, df_user):
    df = pd.DataFrame(columns=['ID_question', 'tweet', 'weights', 'sentiment'])

    for index_ques, row_ques in df_questions.iterrows():
        if contains_question(df_user.columns, str(row_ques['ID_question'])):
            for index_tweet, row_tweet in df_user.iterrows():
                col_weights = 'absa_token_weights_' + str(row_ques['ID_question'])
                col_sentiment = 'absa_sentiment_' + str(row_ques['ID_question'])
                if type(row_tweet[col_weights]) == str:
                    df = df.append({'ID_question': row_ques['ID_question'], 'tweet': row_tweet['tweet'],
                                    'weights': row_tweet[col_weights], 'sentiment': row_tweet[col_sentiment]},
                                   ignore_index=True)
    return df


def get_names(df, username):
    df = df[df['username'] == username]
    cols = ['firstname', 'lastname']
    df = df[cols]
    return df


def get_answers(df, username):
    df = df[df['username'] == username]
    cols_to_drop = ['ID_candidate', 'firstname', 'lastname', 'n_answers', 'username']
    df = df.drop(columns=cols_to_drop)
    return df


def del_index_from_json(data):
    data = data[0]
    try:
        del data['index']
    except KeyError:
        pass
    return data


def detail(request):
    if request.method == 'GET':
        for tup in request.GET.items():
            username = tup[1]

        dict_username = {'username': username}
        df_questions = pd.read_csv('../data/questions.csv')
        df_user = pd.read_csv('../data/tweets/' + username + '.csv')
        df_cands = pd.read_csv('../data/cand_answers.csv')

        cand_answers = get_answers(df_cands, username)

        df_names = get_names(df_cands, username)
        df_ques_tweets = get_df_of_tweets(df_questions, df_user)

        data_names = get_json_of_df(df_names)
        data_questions = get_json_of_df(df_questions)
        data_ques_tweets = get_json_of_df(df_ques_tweets)
        data_cand_answers = get_json_of_df(cand_answers)

        data_cand_answers = del_index_from_json(data_cand_answers)

        range_slider = range(8)
        range_standard = range(4)
        range_budget = range(5)

        context = {'dict_username': dict_username,
                   'data_names': data_names,
                   'data_questions': data_questions,
                   'data_ques_tweets': data_ques_tweets,
                   'data_cand_answers': data_cand_answers,
                   'range_slider': range_slider,
                   'range_standard': range_standard,
                   'range_budget': range_budget
                   }
        return render(request, 'detail.html', context)

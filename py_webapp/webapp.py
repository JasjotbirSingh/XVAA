import streamlit as st
import pandas as pd
import math
import webbrowser
import requests
from urllib.parse import urlencode

st.set_page_config(page_title='Voting Advice Application')
st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)
horizontal_line = '''
---
'''
st.title('Voting Advice Application')

JA = 'ja'
EHER_JA = "eher ja"
EHER_NEIN = "eher nein"
NEIN = 'nein'

DEUTLICH_WENIGER = 'deutlich weniger'
WENIGER = 'weniger'
GLEICHVIEL = 'gleichviel'
MEHR = 'mehr'
DEUTLICH_MEHR = 'deutlich mehr'

df_questions = pd.read_csv('./data/questions.csv')
df_answers_candidates = pd.read_csv('./data/cand_answers.csv')


def calculate_distances(dict_ans):
    df_distances = pd.DataFrame(columns=['firstname', 'total_distance'])
    for index, row in df_answers_candidates.iterrows():
        distance_cumulated = 0

        for question_id, value in dict_ans.items():
            val_cand = row['answer_' + str(question_id)]
            distance_val = pow((val_cand - value), 2)
            distance_cumulated += distance_val

        total_distance = math.sqrt(distance_cumulated)
        df_distances = df_distances.append({'firstname': row['firstname'], 'total_distance': total_distance},
                                           ignore_index=True)

    st.dataframe(df_distances.head(10))


def convert_dict(dict_ans):
    for question_id, value in dict_ans.items():
        if value == 1:
            dict_ans[question_id] = 17
        if value == 2:
            dict_ans[question_id] = 33
        if value == 3:
            dict_ans[question_id] = 50
        if value == 4:
            dict_ans[question_id] = 67
        if value == 5:
            dict_ans[question_id] = 83
        if value == 6:
            dict_ans[question_id] = 100

        if value == NEIN:
            dict_ans[question_id] = 0
        if value == EHER_NEIN:
            dict_ans[question_id] = 25
        if value == EHER_JA:
            dict_ans[question_id] = 75
        if value == JA:
            dict_ans[question_id] = 100

        if value == DEUTLICH_WENIGER:
            dict_ans[question_id] = 0
        if value == WENIGER:
            dict_ans[question_id] = 25
        if value == GLEICHVIEL:
            dict_ans[question_id] = 50
        if value == MEHR:
            dict_ans[question_id] = 75
        if value == DEUTLICH_MEHR:
            dict_ans[question_id] = 100
    return dict_ans


with st.form('form_questions'):
    dict_answers = {}

    for index, row in df_questions.iterrows():
        if row['type'] == 'Slider-7':
            dict_answers[row['ID_question']] = st.slider(row['question'], min_value=0, max_value=7,
                                                         key=row['ID_question'])
        elif row['type'] == 'Standard-4':
            dict_answers[row['ID_question']] = st.radio(row['question'], [JA, EHER_JA, EHER_NEIN, NEIN],
                                                        key=row['ID_question'])
        elif row['type'] == 'Budget-5':
            dict_answers[row['ID_question']] = st.radio(row['question'],
                                                        [DEUTLICH_WENIGER, WENIGER, GLEICHVIEL, MEHR,
                                                         DEUTLICH_MEHR], key=row['ID_question'])

        st.markdown(horizontal_line)

    submit_button = st.form_submit_button('Submit')

if submit_button:
    dict_answers = convert_dict(dict_answers)

    url = 'http://127.0.0.1:8000/playground/recommender'
    query = '?' + urlencode(dict_answers)

    url_get = url + query
    webbrowser.open(url_get)

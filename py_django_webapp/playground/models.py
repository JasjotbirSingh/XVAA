from django.db import models
import pandas as pd
import math


class Distance:
    def calculate_distance(self, dict_ans_user):
        df_answers_candidates = pd.read_csv('../data/cand_answers.csv')
        df_distances = pd.DataFrame(
            columns=['firstname', 'lastname', 'username', 'total_distance'])  # should be user_id

        for index, row in df_answers_candidates.iterrows():
            distance_cumulated = 0

            for question_id, value in dict_ans_user.items():
                val_cand = row['answer_' + question_id]
                distance_val = pow((val_cand - value), 2)
                distance_cumulated += distance_val

            total_distance = math.sqrt(distance_cumulated)
            df_distances = df_distances.append(
                {'firstname': row['firstname'], 'lastname': row['lastname'], 'username': row['username'],
                 'total_distance': total_distance
                 },
                ignore_index=True)

            df_distances.sort_values(by=['total_distance'], inplace=True)
            df_distances.reset_index(inplace=True, drop=True)

        return df_distances

    def __init__(self, dict_and_user):
        self.dict_ans = dict_and_user
        self.df_distances = self.calculate_distance(dict_and_user)

    def get_distances(self, n: int = 10):
        return self.df_distances.head(n)

import pandas as pd

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel


class Model:
    def __init__(self):
        self.input_data = pd.read_csv(
            '/home/ramsha/Documents/ramsha-blog/backend/blog_api/tmdb_5000_movies.csv')
        self.C = self.input_data['vote_average'].mean()
        self.m = self.input_data['vote_count'].quantile(0.9)
        self.q_movies = self.input_data.copy(
        ).loc[self.input_data['vote_count'] >= self.m]

    def weighted_rating(self, x):
        v = x['vote_count']
        R = x['vote_average']
        return (v / (v + self.m) * R) + (self.m / (self.m + v) * self.C)

    def preprocessing(self):
        self.q_movies['score'] = self.q_movies.apply(
            self.weighted_rating, axis=1)
        self.q_movies = self.q_movies.sort_values('score', ascending=False)
        self.pop = self.input_data.sort_values('popularity', ascending=False)
        self.tdif = TfidfVectorizer(stop_words='english')
        self.input_data['overview'] = self.input_data['overview'].fillna('')
        self.tdif_matrix = self.tdif.fit_transform(self.input_data['overview'])
        self.cosine_sim = linear_kernel(self.tdif_matrix, self.tdif_matrix)
        self.indices = pd.Series(
            self.input_data.index, index=self.input_data['title']).drop_duplicates()
        return self.input_data

    def predict(self, title):
        if title not in self.indices:
            return {"status": "Error", "message": "This is not a valid movie name."}
        idx = self.indices[title]
        sim_scores = list(enumerate(self.cosine_sim[idx]))
        sim_scores = sorted(
            sim_scores, key=lambda X: X[1], reverse=True)
        sim_scores = sim_scores[1:11]
        movie_indices = [i[0] for i in sim_scores]
        return self.input_data['title'].iloc[movie_indices]

    def compute_prediction(self, title):
        try:
            self.preprocessing()
            prediction = self.predict(title)
        except Exception as e:
            return {"status": "Error", "message": str(e)}

        return prediction


# model = Model()
# title_to_predict = "Avatar"
# prediction = model.compute_prediction(title_to_predict)
# print(prediction)

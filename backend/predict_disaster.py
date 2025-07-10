import joblib


class DisasterPredictor():
    def __init__(self):
        self.vectorizer = joblib.load('tfidf_vectorizer.pkl')
        self.model = joblib.load('lightgbm_model.pkl')
        self.label_encoder = joblib.load('label_encoder.pkl')

    def predict_disasters_on_list(self, posts):
        print('Adding disaster types to posts')
        for post in posts:
            self.add_disaster_type(post)    ##
        return posts



    def add_disaster_type(self, post):
        input_vector = self.vectorizer.transform([post.text])
        prediction = self.model.predict(input_vector).argmax(axis=1)[0]
        post.disaster_type = self.label_encoder.inverse_transform([prediction])[0]

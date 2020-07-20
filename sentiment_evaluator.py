from textblob import TextBlob


class SentimentEvaluator:
    def __init__(self):
        pass

    @staticmethod
    def score_sentiment(text):
        sentiment_score = 0
        sentence_count = 0
        for sentence in [x for x in TextBlob(text).sentences]:
            sentiment_score += sentence.sentiment.polarity
            sentence_count += 1
        return sentiment_score / sentence_count


if __name__ == '__main__':
    se = SentimentEvaluator()
    print(se.score_sentiment('''I hate dogs. Best best best best.'''))

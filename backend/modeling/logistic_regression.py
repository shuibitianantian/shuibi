
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split


def fit_logistic_regression(x, y, dump_performance=False, save_model=False):
    """
    train the model and save the performance
    :param save_model:
    :param dump_performance:
    :param x: features
    :param y: labels
    :return: model, float
    """
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.33, random_state=18)
    clf = LogisticRegression(random_state=18, max_iter=1000)
    clf.fit(x_train, y_train)
    accuracy = clf.score(x_test, y_test)
    print(f'LG Accuracy: {accuracy * 100 :10.4f}%')
    return clf, accuracy

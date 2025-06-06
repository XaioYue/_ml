import ml

x_train,x_test,y_train,y_test=ml.load_csv('bc_dump.csv', 'target')
from sklearn.ensemble import RandomForestClassifier

def learn_classifier(x_train, y_train):
    model = RandomForestClassifier(n_estimators=10)
    model.fit(x_train, y_train)
    return model



classifier = learn_classifier(x_train, y_train)
print('=========== train report ==========')
ml.report(classifier, x_train, y_train)
print('=========== test report ==========')
ml.report(classifier, x_test, y_test)

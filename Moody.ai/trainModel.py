import pandas
from pandas.plotting import scatter_matrix
import matplotlib.pyplot as plt
from sklearn import model_selection
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC
from sklearn.linear_model import LogisticRegression
import pickle


'''
Splits out dataset into 80% training data and 20% validation dataset. 
Returns a tuple of numpy arrays X_train, X_validation, Y_train, Y_validation
as numpy arrays. It uses a random_state start seed of 100. 
'''
def splitDataset(dataset, seed, scoring):
	array = dataset.values
	X = array[:,1:5]
	Y = array[:,5]
	validation_size = 0.80
	X_train, X_validation, Y_train, Y_validation = model_selection.train_test_split(X, Y,
												   test_size=validation_size,
												   random_state=seed)
	return X_train, X_validation, Y_train, Y_validation

'''
Tries different classifiers and see which one performs the best. Tries
Linear Discriminant Analysis, K Neighbors, Decision Tree, Logistic Regression,
Support Vector Machine, and Gaussian Native Bayes. It uses a cross validation score
to rate the classifiers. It will print out the mean and standard deviation of the 
result scores. It will also create a graph that shows the difference in the algorithm
 performance. This function is intended to be used to pick the best classifier to use. 
'''
def tryClassifiers(X_train, Y_train, seed, scoring):
	models = []
	models.append(('Linear Discriminant Analysis', LinearDiscriminantAnalysis()))
	models.append(('K Neighbors', KNeighborsClassifier()))
	models.append(('Decision Tree', DecisionTreeClassifier()))
	models.append(('Logistic Regression', LogisticRegression(solver='liblinear',
															 multi_class='ovr')))
	models.append(('Support Vector Machine', SVC(gamma='auto')))
	models.append(('Gaussian Naive Bayes', GaussianNB()))

	#Try each model and print out the results of the scores of each one
	results = []
	names = []
	for name, model in models:
		kfold = model_selection.KFold(n_splits=10, random_state=None)
		cv_results = model_selection.cross_val_score(model, X_train, Y_train, cv=kfold, scoring=scoring)
		results.append(cv_results)
		names.append(name)
		mean = cv_results.mean()
		stdDev = cv_results.std()
		msg = "%s: %f (%f)" % (name, mean, stdDev)
		print(msg)

	#Create graph that will show differences in algorithm performance
	figure = plt.figure()
	figure.suptitle('Differences in Algorithm Performance')
	ax = figure.add_subplot(111)
	plt.boxplot(results)
	ax.set_xticklabels(names)
	plt.show()

'''
Fits model to 80% training data.
Check how well model performs on the 20% data that we set aside as
the validation training set. This function will print an accuracy score,
confusion matrix, and classification report for the passed in model. 
It will return the trained model. 
'''
def checkModel(model, X_train, Y_train, X_validation, Y_validation):
	model.fit(X_train, Y_train)
	predictions = model.predict(X_validation)
	print(accuracy_score(Y_validation, predictions))
	print(confusion_matrix(Y_validation, predictions))
	print(classification_report(Y_validation, predictions))
	return model

'''
Returns model that has been trained on the training dataset. The classifier
being used is a decision tree. 
'''
if __name__ == '__main__':
	# Load dataset
	dataset = pandas.read_csv("trainingSet.csv",
	 						  names=['id','danceability', 'energy', 
	 						  		 'valence', 'loudness', 'mood'])
	seed = 100
	scoring = 'accuracy'
	#split dataset into training and validation data
	X_train, X_validation, Y_train, Y_validation = splitDataset(dataset, seed, scoring)
	print(X_train)
	#try multiple classifiers and print data on how well they perform
	tryClassifiers(X_train, Y_train, seed, scoring)
	#chose model based on results
	chosenModel =  LogisticRegression(solver='liblinear',
									  multi_class='ovr')
	model = checkModel(chosenModel, X_train, Y_train,
					   X_validation, Y_validation)
	print(model)
	pickle.dump(model, open("model.sav", 'wb'))
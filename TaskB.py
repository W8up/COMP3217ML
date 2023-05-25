import numpy as np
import pandas as pd
from sklearn import datasets, neighbors, linear_model, svm, metrics
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay, f1_score, r2_score, mean_squared_error
import matplotlib.pyplot as plt
from sklearn.inspection import DecisionBoundaryDisplay
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.decomposition import PCA
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler


pca = PCA()
scaler = StandardScaler()

data_train = pd.read_csv("./TrainingDataMulti.csv",header=None)
data_test = pd.read_csv("./TestingDataMulti.csv")

x_data = data_train.drop(128, axis=1)
y_data = data_train[128]

x_train, x_test, y_train, y_test = train_test_split(x_data, y_data, test_size=0.2)

logistic = linear_model.LogisticRegression(C=0.01, max_iter=10000, tol=0.1)
pipe = Pipeline(steps=[("scaler", scaler), ("pca", pca), ("logistic", logistic)])

log = logistic.fit(x_train, y_train).score(x_test, y_test)
print(log)
predictions = logistic.predict(x_test)
print(predictions)
print (f1_score(y_test, predictions, average='macro'))

#Create a svm Classifier
clf = svm.SVC(kernel='linear') # Linear Kernel

#Train the model using the training sets
clf.fit(x_train, y_train)

#Predict the response for test dataset
y_pred = clf.predict(x_test)

print("Accuracy:",metrics.accuracy_score(y_test, y_pred))
print("Mean root error:", mean_squared_error(y_test, y_pred))
print("Coefficient of determination:", r2_score(y_test, y_pred))

#Get confusion matrix
cm = confusion_matrix(y_test, y_pred, labels=logistic.classes_)
disp = ConfusionMatrixDisplay(confusion_matrix=cm,                           display_labels=logistic.classes_)
disp.plot()
plt.show()



# # Parameters of pipelines can be set using '__' separated parameter names:
# param_grid = {
#     "pca__n_components": [75,80,85,90,95,100,105,110,115,120,128],
#     "logistic__C": np.logspace(-1, 1, 1),
# }
# search = GridSearchCV(pipe, param_grid, n_jobs=2,cv=5)
# search.fit(x_data, y_data)
# print("Best parameter (CV score=%0.3f):" % search.best_score_)
# print(search.best_params_)

# Plot the PCA spectrum
# pca.fit(x_data)

# fig, (ax0, ax1) = plt.subplots(nrows=2, sharex=True, figsize=(6, 6))
# ax0.plot(
#     np.arange(1, pca.n_components_ + 1), pca.explained_variance_ratio_, "+", linewidth=2
# )
# ax0.set_ylabel("PCA explained variance ratio")

# ax0.axvline(
#     search.best_estimator_.named_steps["pca"].n_components,
#     linestyle=":",
#     label="n_components chosen",
# )
# ax0.legend(prop=dict(size=12))

# # For each number of components, find the best classifier results
# results = pd.DataFrame(search.cv_results_)
# print (results)
# components_col = "param_pca__n_components"
# best_clfs = results.groupby(components_col).apply(
#     lambda g: g.nlargest(1, "mean_test_score")
# )

# best_clfs.plot(
#     x=components_col, y="mean_test_score", yerr="std_test_score", legend=False, ax=ax1
# )
# ax1.set_ylabel("Classification accuracy (val)")
# ax1.set_xlabel("n_components")

# plt.xlim(-1, 128)

# plt.tight_layout()
# plt.show()

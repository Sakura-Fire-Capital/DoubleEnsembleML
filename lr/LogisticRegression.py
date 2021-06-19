import numpy as np
from sklearn import datasets
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import normalize


def sigmoid(x):
    return 1 / (1 + np.exp(-x))


class LogisticRegression():
    def __init__(self, learning_rate=.1, n_iterations=4000):
        self.learning_rate = learning_rate
        self.n_iterations = n_iterations

    def initialize_weights(self, n_features):
        limit = np.sqrt(1 / n_features)
        w = np.random.uniform(-limit, limit, (n_features, 1))
        #把偏置加到w的矩阵中
        b = 0
        self.w = np.insert(w, 0, b, axis=0)

    def fit(self, X, y):
        n_samples, n_features = X.shape
        self.initialize_weights(n_features)
        #x要加多1列才能保持输出shape不变
        X = np.insert(X, 0, 1, axis=1)
        y = np.reshape(y, (n_samples, 1))

        for i in range(self.n_iterations):
            h = X.dot(self.w)
            y_pred = sigmoid(h)
            #公式推倒后的J(w)的梯度,推倒结果和线性回归很像.
            #若果是y - y_pred 的话后面 self.w = self.w + self.learning_rate * w_grad
            w_grad = X.T.dot(y_pred - y)
            self.w = self.w - self.learning_rate * w_grad
            #w_grad = X.T.dot(y -  y_pred )
            #self.w = self.w + self.learning_rate * w_grad

        def compute_sample_weight(class_weight, y, *, indices=None):
            y = np.atleast_1d(y)
            if y.ndim == 1:
                y = np.reshape(y, (-1, 1))
            n_outputs = y.shape[1]

            if isinstance(class_weight, str):
                if class_weight not in ["balanced"]:
                    raise ValueError(
                        "The only valid preset for class_weight is "
                        '"balanced". Given "%s".' % class_weight)
            elif indices is not None and not isinstance(class_weight, str):
                raise ValueError(
                    "The only valid class_weight for subsampling is "
                    '"balanced". Given "%s".' % class_weight)
            elif n_outputs > 1:
                if not hasattr(class_weight, "__iter__") or isinstance(
                        class_weight, dict):
                    raise ValueError(
                        "For multi-output, class_weight should be a "
                        "list of dicts, or a valid string.")
                if len(class_weight) != n_outputs:
                    raise ValueError(
                        "For multi-output, number of elements in "
                        "class_weight should match number of outputs.")

            expanded_class_weight = []
            for k in range(n_outputs):

                y_full = y[:, k]
                classes_full = np.unique(y_full)
                classes_missing = None

                if class_weight == "balanced" or n_outputs == 1:
                    class_weight_k = class_weight
                else:
                    class_weight_k = class_weight[k]

                if indices is not None:
                    # Get class weights for the subsample, covering all classes in
                    # case some labels that were present in the original data are
                    # missing from the sample.
                    y_subsample = y[indices, k]
                    classes_subsample = np.unique(y_subsample)

                    weight_k = np.take(
                        compute_class_weight(class_weight_k,
                                             classes=classes_subsample,
                                             y=y_subsample),
                        np.searchsorted(classes_subsample, classes_full),
                        mode="clip",
                    )

                    classes_missing = set(classes_full) - set(
                        classes_subsample)
                else:
                    weight_k = compute_class_weight(class_weight_k,
                                                    classes=classes_full,
                                                    y=y_full)

                weight_k = weight_k[np.searchsorted(classes_full, y_full)]

                if classes_missing:
                    # Make missing classes' weight zero
                    weight_k[np.in1d(y_full, list(classes_missing))] = 0.0

                expanded_class_weight.append(weight_k)

            expanded_class_weight = np.prod(expanded_class_weight,
                                            axis=0,
                                            dtype=np.float64)

            return expanded_class_weight

    def predict(self, X):
        X = np.insert(X, 0, 1, axis=1)
        #np.round四舍五入,小于0.5等于0,大于0.5等于1
        y_pred = np.round(sigmoid(X.dot(self.w)))
        return y_pred.astype(int)


if __name__ == '__main__':
    data = datasets.load_iris()
    X = normalize(data.data[data.target != 0])
    y = data.target[data.target != 0]
    y[y == 1] = 0
    y[y == 2] = 1

    X_train, X_test, y_train, y_test = train_test_split(X,
                                                        y,
                                                        test_size=0.33,
                                                        random_state=1)

    clf = LogisticRegression()
    clf.fit(X_train, y_train)
    y_pred = clf.predict(X_test)
    y_pred = np.reshape(y_pred, y_test.shape)

    accuracy = accuracy_score(y_test, y_pred)
    print("Accuracy:", accuracy)

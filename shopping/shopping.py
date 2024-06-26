import csv
import sys

from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

TEST_SIZE = 0.4


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python shopping.py data")

    load_data(sys.argv[1])

    # Load data from spreadsheet and split into train and test sets
    evidence, labels = load_data(sys.argv[1])
    X_train, X_test, y_train, y_test = train_test_split(
        evidence, labels, test_size=TEST_SIZE
    )

    # Train model and make predictions
    model = train_model(X_train, y_train)
    predictions = model.predict(X_test)
    sensitivity, specificity = evaluate(y_test, predictions)

    # Print results
    print(f"Correct: {(y_test == predictions).sum()}")
    print(f"Incorrect: {(y_test != predictions).sum()}")
    print(f"True Positive Rate: {100 * sensitivity:.2f}%")
    print(f"True Negative Rate: {100 * specificity:.2f}%")


def load_data(filename):
    """
    Load shopping data from a CSV file `filename` and convert into a list of
    evidence lists and a list of labels. Return a tuple (evidence, labels).


    evidence should be a list of lists, where each list contains the
    following values, in order:
        - Administrative, an integer
        - Administrative_Duration, a floating point number
        - Informational, an integer
        - Informational_Duration, a floating point number
        - ProductRelated, an integer
        - ProductRelated_Duration, a floating point number
        - BounceRates, a floating point number
        - ExitRates, a floating point number
        - PageValues, a floating point number
        - SpecialDay, a floating point number
        - Month, an index from 0 (January) to 11 (December)
        - OperatingSystems, an integer
        - Browser, an integer
        - Region, an integer
        - TrafficType, an integer
        - VisitorType, an integer 0 (not returning) or 1 (returning)
        - Weekend, an integer 0 (if false) or 1 (if true)

    labels should be the corresponding list of labels, where each label
    is 1 if Revenue is true, and 0 otherwise.
    """
    with open(filename) as shopping_file:
        csvFile = csv.reader(shopping_file, delimiter=",")
        column_name = next(csvFile)
        evidence = []
        labels = []
        month = {'Jan': 0, 'Feb': 1, 'Mar': 2, 'Apr': 3, 'May': 4, 'June': 5,
                 'Jul': 6, 'Aug': 7, 'Sep': 8, 'Oct': 9, 'Nov': 10, 'Dec': 11}
        for row in csvFile:
            list_indi = []
            for item in row[:17]:
                if row.index(item) in (0, 2, 4, 11, 12, 13, 14):
                    list_indi.append(int(item))
                elif row.index(item) in (1, 3, 5, 6, 7, 8, 9):
                    list_indi.append(float(item))
                elif item == 'TRUE':
                    list_indi.append(1)
                elif item == 'FALSE':
                    list_indi.append(0)
                elif item == 'Returning_Visitor':
                    list_indi.append(1)
                elif item == 'New_Visitor' or 'Other':
                    list_indi.append(0)
                else:
                    list_indi.append(month[item])
            evidence.append(list_indi)

            for item in row[17:]:
                if item == 'TRUE':
                    labels.append(1)
                else:
                    labels.append(0)

    return (evidence, labels)



def train_model(evidence, labels):
    """
    Given a list of evidence lists and a list of labels, return a
    fitted k-nearest neighbor model (k=1) trained on the data.
    """
    knn = KNeighborsClassifier(n_neighbors=1)

    # Fit the classifier on the training data
    knn.fit(evidence, labels)

    # Return the fitted classifier
    return knn


def evaluate(labels, predictions):
    """
    Given a list of actual labels and a list of predicted labels,
    return a tuple (sensitivity, specificity).

    Assume each label is either a 1 (positive) or 0 (negative).

    `sensitivity` should be a floating-point value from 0 to 1
    representing the "true positive rate": the proportion of
    actual positive labels that were accurately identified.

    `specificity` should be a floating-point value from 0 to 1
    representing the "true negative rate": the proportion of
    actual negative labels that were accurately identified.
    """
    true_positives: int = 0
    true_negatives: int = 0
    for i in labels:
        if i == 1:
            true_positives += 1
        else:
            true_negatives += 1

    sensitivity = 0
    specificity = 0
    for label, prediction in zip(labels, predictions):
        if label == 1 and prediction == 1:
            sensitivity += 1
        elif label == 0 and prediction == 0:
            specificity += 1

    sensitivity = sensitivity/true_positives
    specificity = specificity/true_negatives
    return sensitivity, specificity






if __name__ == "__main__":
    main()

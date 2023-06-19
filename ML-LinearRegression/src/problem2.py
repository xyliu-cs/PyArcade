
import numpy as np 
import pandas as pd
from sklearn.model_selection import train_test_split


def insert_ones_front(X_raw_arg):
    return np.insert(X_raw_arg, 0, np.ones(np.shape(X_raw_arg)[0]), axis=1)

def poly_matrix(mx):
    mx_poly = mx
    # tricky: old matrix cols num doesn't change
    cols = np.shape(mx)[1]
    for i in range(cols):
        for j in range(i+1, cols):
            res1 = mx_poly[:,i].reshape(-1,1)
            res2 = mx_poly[:,j].reshape(-1,1)
            # element-wise multiplication
            tmp = res1 * res2
            mx_poly = np.append(mx_poly, tmp, axis=1)
    for i in range(cols):
        tmp1 = mx[:,i].reshape(-1,1)
        tmp2 = tmp1 * tmp1
        mx_poly = np.append(mx_poly, tmp2, axis=1)
    # print("mx shape is: ", np.shape(mx_poly))
    return insert_ones_front(mx_poly)

def one_hot_3(mx):
    if (np.shape(mx)[1] != 1):
        print("shape mismatch, shape is ", np.shape(mx))
    rows = np.shape(mx)[0]
    ret = np.empty([rows, 3])
    for i in range(rows):
        if mx[i] == 1:
            ret[i] = [1,0,0]
        elif mx[i] == 2:
            ret[i] = [0,1,0]
        elif mx[i] == 3:
            ret[i] = [0,0,1]
        else:
            print("unrecogniziable class: ", mx[i])
    # print("shape is ", np.shape(ret))
    # print(ret)
    return ret

def poly_regression(X, w):
    X_poly = poly_matrix(X)
    y_raw = np.matmul(X_poly, w)
    tmp = np.argmax(y_raw, axis=1)
    # add 1 for index {0, 1, 2} to class {1, 2, 3}
    y = np.transpose(tmp).reshape(-1,1) + 1
    return y



def calc_error(y_pred, y_fact):
    count = 0
    y_rows = np.shape(y_pred)[0]
    for j in range(y_rows):
        if (y_pred[j] != y_fact[j]):
            count += 1
    rate = count / y_rows
    perc = "{:.2%}".format(rate)
    return perc



def main():
    df = pd.read_excel("./Classification iris.xlsx", header=None)

    df.dropna(axis=0, how='any', inplace=True)

    df[4].replace('Iris-setosa', 1, inplace=True)
    df[4].replace('Iris-versicolor', 2, inplace=True)
    df[4].replace('Iris-virginica', 3, inplace=True)

    # print(df)
    data = df.to_numpy()

    i = 0
    while(i < 10):
        print("\nTest ", i+1)
        data_train, data_test = train_test_split(data, train_size=0.8)
        # drop last col for prediction
        X_RAW = np.delete(data_train, [-1], axis=1)
        X_RAW_TEST = np.delete(data_test, [-1], axis=1)

        y_RAW = data_train[:,-1].reshape(-1,1)
        y_RAW_TEST = data_test[:,-1].reshape(-1,1)
        # print(np.shape(X_RAW))

        P = poly_matrix(X_RAW)
        P_T = np.transpose(P)
        P_P_T = np.matmul(P, P_T)
        # print(np.shape(P_P_T))

        k = 0
        cols = np.shape(P_P_T)[0]
        id = np.identity(cols)
        # if uninvertible
        while (np.linalg.det(P_P_T) == 0):
            if (k > 10):
                print("failed")
                break
            k += 0.00001
            P_P_T = P_P_T + (id * k)

        # change name for clarity
        P_P_T_I = P_P_T
        P_P_T_I_inv = np.linalg.inv(P_P_T_I)
        tmp = np.matmul(P_T, P_P_T_I_inv)
        y_hot = one_hot_3(y_RAW)

        # finished calc w
        w_hat = np.matmul(tmp, y_hot)


        # calc for prediction
        y_predict_train = poly_regression(X_RAW, w_hat)
        y_predict_test = poly_regression(X_RAW_TEST, w_hat)

        train_err = calc_error(y_predict_train, y_RAW)
        test_err = calc_error(y_predict_test, y_RAW_TEST)

        # calc for error
        print("training error: ", train_err)
        print("testing error: ", test_err)

        i = i+1
        

if __name__ == "__main__":
    main()

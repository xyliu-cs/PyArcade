
import numpy as np 
import pandas as pd
import math
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error


# axis = 1 --> col; axis = 0 --> row

def linear_reg_func(w_hat_arg, X_new_arg):
    return np.matmul(X_new_arg, w_hat_arg)

def insert_ones_front(X_raw_arg):
    return np.insert(X_raw_arg, 0, np.ones(np.shape(X_raw_arg)[0]), axis=1)

def my_calc_rmse(y_predict_arg, y_fact_arg):
    if (np.shape(y_predict_arg) != np.shape(y_fact_arg)):
        print("matrix shape mismatch !")
        print("y_predict shape: ", np.shape(y_predict_arg))
        print("y_fact shape: ", np.shape(y_fact_arg))
        return
    matrix_diff = y_predict_arg - y_fact_arg
    cols = np.shape(y_predict_arg)[1]
    # print(cols)
    rmse_vec = []
    for i in range(cols):
        mse_tmp = np.average(np.square(matrix_diff[:, i]))
        # print(mse_tmp)
        rmse_tmp = math.sqrt(mse_tmp)
        rmse_vec.append(rmse_tmp)
    return np.array(rmse_vec)
        
def sklearn_rmse_result(X_train, y_train, X_test, y_test):
    model = LinearRegression()
    model.fit(X_train, y_train)
    y_predict = model.predict(X_test)
    rmse = mean_squared_error(y_true=y_test, y_pred=y_predict, squared=False, multioutput='raw_values')
    return rmse



def main():
    df = pd.read_csv("./Regression.csv")

    # data clean
    df.drop(df.columns[[0,1]], axis=1, inplace=True)
    df.dropna(axis=0, how='any', inplace=True)


    # pandas DataFrame to nparray
    data = df.to_numpy()

    i = 0
    safety = 0
    while (i < 10) :
        if (safety > 500):
            print("something is wrong!")
            break

        print("\nTest ", i+1)
        data_train, data_test = train_test_split(data, train_size=0.8)

        # drop the last two cols for prediction
        X_raw = np.delete(data_train, [21,22], axis=1)
        X_new_raw = np.delete(data_test, [21,22], axis=1)
        X = insert_ones_front(X_raw)
        X_new = insert_ones_front(X_new_raw)


        y = data_train[:, 21:]
        y_fact = data_test[:, 21:]

        X_T = np.transpose(X) 
        X_T_X = np.matmul(X_T, X)

        # XTX is invertiable
        if (np.linalg.det(X_T_X) != 0):
            X_T_X_inv = np.linalg.inv(X_T_X)
            tmp = np.matmul(X_T_X_inv, X_T)
            w_hat = np.matmul(tmp, y)

            y_test_predict = linear_reg_func(w_hat, X_new)
            y_train_predict = linear_reg_func(w_hat, X)

            my_train_rmse = my_calc_rmse(y_train_predict, y)
            my_test_rmse = my_calc_rmse(y_test_predict, y_fact)
            sk_test_rmse = sklearn_rmse_result(X_raw, y, X_new_raw, y_fact)

            print("My Training RMSE      (under uniform-average): ", np.average(my_train_rmse))
            print("My Testing RMSE       (under uniform-average): ", np.average(my_test_rmse))
            # print("Sklearn Testing RMSE  (under uniform-average): ", np.average(sk_test_rmse))
            i += 1
        else:
            safety += 1
        


if __name__ == "__main__":
    main()

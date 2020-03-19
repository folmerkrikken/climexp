
from sklearn.linear_model import Lasso


def lasso_regr(y_train,x_train,x_test,alpha=0.1):
    lassoReg = Lasso(alpha=alpha, normalize=True)
    lassoReg.fit(x_train.T,y_train)
    pred = lassoReg.predict(x_test.T)
    
    fit_train = lassoReg.predict(x_train.T))
    fit_test = lassoReg.predict(x_test.T))
    beta = lassoReg.coef_
    return fit_train,fit_test,beta
    
    
    

    # calculating mse

    #mse = np.mean((pred_cv - y_cv)**2)

    
    #lassoReg.score(x_cv,y_cv)

    

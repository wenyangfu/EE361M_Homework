You can use the glmnet package (https://cran.r-project.org/web/packages/glmnet/glmnet.pdf)

Data can be loaded as follows.
data = read.csv('prostate.csv')

You can use the ridge and lasso regression to fit a model as follows.
 model <- glmnet(train.x, train.y, alpha=alpha.value); # here train.x is the x matrix and train.y is the response variable. Set alpha = 0 for ridge regression and alpha=1 for lasso.

For cross validation, you can use the cv.glmnet function:

model.cv <- cv.glmnet(train.x, train.y, alpha=alpha.value, nfold=5, lambda=<sequence of regularized parameters>);

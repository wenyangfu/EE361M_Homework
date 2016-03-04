library(caret)
library(Metrics)
library(glmnet)

prostate.data = read.csv('prostate.csv')

set.seed(42)
trainIndex <- createDataPartition(prostate.data$lcavol, p = .66667, list=FALSE, times = 1)

prostate.train <- prostate.data[trainIndex,]
prostate.test <- prostate.data[-trainIndex,]

prostate.train.features <- prostate.train[-c(1)]
prostate.train.response <- prostate.train[c(1)]

prostate.test.features <- prostate.test[-c(1)]
prostate.test.response <- prostate.test[c(1)]

prostate.train.features.matrix <- as.matrix(prostate.train.features)
prostate.train.response.matrix <- as.matrix(prostate.train.response)

prostate.test.features.matrix <- as.matrix(prostate.test.features)
prostate.test.response.matrix <- as.matrix(prostate.test.response)

ridge.cv <- cv.glmnet(
  prostate.train.features.matrix,
  prostate.train.response.matrix,
  alpha=0,
  nfold=5,
  lambda=c(0.00001, 0.0001,0.001, 0.005, 0.01, 0.05, 0.1, 1, 5, 10, 100) # 0.05 is best
)
plot(ridge.cv)

lasso.cv <- cv.glmnet(
  prostate.train.features.matrix,
  prostate.train.response.matrix,
  alpha=1,
  nfold=5,
  lambda=c(0.0001, 0.0005, 0.001, 0.005, 0.01, 0.05, 0.1, 0.2, 0.3, 0.4, 0.5) # 0.1 is best
)
plot(lasso.cv)

ridge <- glmnet(prostate.train.features.matrix, prostate.train.response.matrix, alpha=0)
lasso <- glmnet(prostate.train.features.matrix, prostate.train.response.matrix, alpha=1)

plot(ridge,xvar="lambda")
plot(lasso,xvar="lambda")

leastsquares.all <- lm(lcavol ~ lweight + age + lbph + svi + lcp + gleason + pgg45 + lpsa, data=prostate.train)
print("Least Squares Regression")
print(mean(se(prostate.test.response, predict(leastsquares.all, prostate.test))))

print("Ridge Regression")
print(mean(se(prostate.test.response, predict(ridge.cv, prostate.test.features.matrix))))

print("Lasso Regression")
print(mean(se(prostate.test.response, predict(lasso.cv, prostate.test.features.matrix))))
print(coef(lasso.cv))

leastsquares.remaining <- lm(lcavol ~ lcp + lpsa, data=prostate.train)
print("Least Squares Regression with Non-Zero Lasso")
print(mean(se(prostate.test.response, predict(leastsquares.remaining, prostate.test))))
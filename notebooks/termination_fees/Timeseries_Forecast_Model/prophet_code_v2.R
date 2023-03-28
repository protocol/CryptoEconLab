install.packages("prophet")
library(prophet)
library(tidyverse)
library(hrbrthemes)
library(viridis)

## documentation and model details (assumptions, limitations and mathematical implementation): https://peerj.com/preprints/3190/


#######################

df <- read.csv('terminations_df.csv')
df = subset(df, select = -c(X) )
str(df)

df$ds <- as.POSIXct(df$ds, format = "%Y-%m-%d %H:%M:%S")
is.na(df$ds)
m <- prophet(df, yearly.seasonality = FALSE, weekly.seasonality = FALSE, daily.seasonality = FALSE)

future <- make_future_dataframe(m, periods = 365)
tail(future)

forecast <- predict(m, future)
tail(forecast[c('ds', 'yhat', 'yhat_lower', 'yhat_upper')])

plot(m, forecast)

###---------------------------------------------------###

df <- read.csv('terminationn_per_rbp_df.csv')
df = subset(df, select = -c(X) )
str(df)

df$ds <- as.POSIXct(df$ds, format = "%Y-%m-%d %H:%M:%S")
is.na(df$ds)
df$y <- log(df$y)


m <- prophet(df, yearly.seasonality = FALSE, weekly.seasonality = FALSE, daily.seasonality = FALSE)
future <- make_future_dataframe(m, periods = 700)
tail(future)

forecast <- predict(m, future)
m$history$y <- exp(m$history$y)
forecast$trend <- exp(forecast$trend)
forecast$yhat <- exp(forecast$yhat)
forecast$trend_lower <- exp(forecast$trend_lower)
forecast$trend_upper <- exp(forecast$trend_upper)
forecast$yhat_lower <- exp(forecast$yhat_lower)
forecast$yhat_upper <- exp(forecast$yhat_upper)


write.csv(forecast, 'plot.csv')

plot(m, forecast, x_label = "Date", y_label = "Daily Terminating Fraction")
prophet_plot_components(m, forecast)

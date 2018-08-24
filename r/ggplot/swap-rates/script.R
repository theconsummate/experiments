setwd("/home/dhruv/code/upwork/swap-rates")
library(ggplot2)
library(dplyr)

swap = read.csv("swap_rates.csv")
skew = read.csv("skew_5x10_20180807.csv")
trsy = read.csv("trsy_rates.csv")

# converting to numeric
trsy$X10.yr = as.numeric(levels(trsy$X10.yr))[trsy$X10.yr]
trsy$Date = as.Date(trsy$Date, format='%m/%d/%Y')
# categorical variable

trsy$X10.yr_grcut <- cut(trsy$X10.yr, 
breaks = c(0, 1.5, 2.5, 3.5, 4.5, 5.5, 6.5, 7.5, 8.5, 9.5, 10.5, 11.5, 12.5, 13.5, 14.5, Inf), 
# labels = c("0-5 mnths", "6-11 mnths", "12-23 mnths", "24-59 mnths", "5-14 yrs", "adult"), 
                       right = FALSE)

trsy$date_grcut <- cut(trsy$Date, 
breaks = as.Date(c("01/01/1990", "01/01/1995", "01/01/2000", "01/01/2005",
                   "01/01/2010", "01/01/2015", "01/01/2020"), format="%m/%d/%Y"),)

# labels = c("0-5 mnths", "6-11 mnths", "12-23 mnths", "24-59 mnths", "5-14 yrs", "adult"), )

g1 = ggplot(trsy, aes(x=X10.yr_grcut, fill=date_grcut)) + geom_bar()


# increments
rmse_my <- function(x) {sqrt(mean(x^2)*252) }
# na.omit(trsy)
error = mutate(na.omit(trsy), inc = (X10.yr - lag(X10.yr))*100 ) %>% group_by(X10.yr_grcut) %>% summarise(err = rmse_my(inc))

error = na.omit(error)
# line plot
g2 = ggplot(error, aes(x=X10.yr_grcut, y = err, group = 1)) + geom_point() + geom_line()

# combine datasets
full = full_join(trsy, error, by = "X10.yr_grcut")

ggplot(full, aes(x=X10.yr_grcut)) + geom_bar(aes(fill=date_grcut)) +
  geom_point(aes(y=err, group=1)) + geom_line(aes(y=err, group=1)) + 
  scale_y_continuous(sec.axis = sec_axis(~.*1, name = "Error"))
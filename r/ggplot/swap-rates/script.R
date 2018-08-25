setwd("~/code/utils/r/ggplot/swap-rates")
library(ggplot2)
library(dplyr)
library(reshape)
library(RColorBrewer)

swap = read.csv("swap_rates.csv")
skew = read.csv("skew_5x10_20180807_modified.csv")
trsy = read.csv("trsy_rates.csv")

# Treasury
# converting to numeric
trsy$X10.yr = as.numeric(levels(trsy$X10.yr))[trsy$X10.yr]
trsy$Date = as.Date(trsy$Date, format='%m/%d/%Y')
# categorical variable

trsy$X10.yr_grcut <- cut(trsy$X10.yr,
breaks = c(0, 1.5, 2.5, 3.5, 4.5, 5.5, 6.5, 7.5, 8.5, 9.5, 10.5, 11.5, 12.5, 13.5, 14.5, Inf), right = FALSE)

trsy$date_grcut <- cut(trsy$Date,
breaks = as.Date(c("01/01/1990", "01/01/1995", "01/01/2000", "01/01/2005",
                   "01/01/2010", "01/01/2015", "01/01/2020"), format="%m/%d/%Y"),)

trsy = na.omit(trsy)

# g1 = ggplot(trsy, aes(x=X10.yr_grcut, fill=date_grcut)) + geom_bar()


# increments
rmse_my <- function(x) {sqrt(mean(x^2)*252) }
# na.omit(trsy)
error = mutate(trsy, inc = (X10.yr - lag(X10.yr))*100 ) %>% group_by(X10.yr_grcut) %>% summarise(err = rmse_my(inc))

error = na.omit(error)
# line plot
# g2 = ggplot(error, aes(x=X10.yr_grcut, y = err, group = 1)) + geom_point() + geom_line()

# combine datasets
full = full_join(trsy, error, by = "X10.yr_grcut")

ggplot(full, aes(x=X10.yr_grcut)) + geom_bar(aes(fill=date_grcut)) +
  geom_point(aes(y=err, group=1)) + geom_line(aes(y=err, group=1)) +
  scale_y_continuous(sec.axis = sec_axis(~.*1, name = "Annualized deviations (bp)")) +
  ggtitle("Daily Volatility versus Level for 10 Year Treasury Rate") +
  xlab("rate level, %") + ylab("Observations") +
  guides(fill=guide_legend(title=NULL)) + scale_fill_brewer(palette = "Pastel1")
# + scale_fill_grey() + theme_classic()

# skew plot
atm = 305.0950
sigmaF = filter(skew, strike == 0)$volatility
skew = skew %>% mutate(cev.0 = ((atm/(atm + strike))^((1-0)/2)) * sigmaF )

# skew = skew %>% mutate(cev.0.23 = ((atm/(atm + strike))^((1-0.23)/2)) * sigmaF )
skew = skew %>% mutate(cev.0.5 = ((atm/(atm + strike))^((1-0.5)/2)) * sigmaF )
skew = skew %>% mutate(cev.1 = ((atm/(atm + strike))^((1-1)/2)) * sigmaF )

# drop volatality column
skew = subset(skew, select=-c(volatility))

# ggplot(skew, aes(x=strike)) +
#   geom_point(aes(y=volatility)) +
#   geom_point(aes(y=cev.0)) +
#   geom_point(aes(y=cev.0.5)) +
#   geom_point(aes(y=cev.1)) +
#   geom_point(aes(y=cev.0.23))


skk = melt(skew, id=c("strike"))

ggplot(skk, aes(x=strike)) +
  geom_point(aes(y=value, shape=factor(variable))) +
  theme(legend.title=element_blank()) +
  ggtitle("Implied Volatility Skew on 5-Year-into-10-Year Swap") +
  xlab("strike") + ylab("Volatility Skew")

# swap plot
swap$Date = as.Date(swap$Date, format='%m/%d/%Y')
# categorical variable

swap$PX_LAST_grcut <- cut(swap$PX_LAST,
breaks = c(0, 1.5, 2.5, 3.5, 4.5, 5.5, 6.5, 7.5, 8.5, 9.5, 10.5, 11.5, 12.5, 13.5, 14.5, Inf), right = FALSE)

swap$date_grcut <- cut(swap$Date,
breaks = as.Date(c("01/01/1990", "01/01/1995", "01/01/2000", "01/01/2005",
                   "01/01/2010", "01/01/2015", "01/01/2020"), format="%m/%d/%Y"),)

swap = na.omit(swap)

# g1 = ggplot(swap, aes(x=PX_LAST_grcut, fill=date_grcut)) + geom_bar()


# increments
rmse_my <- function(x) {sqrt(mean(x^2)*252) }
# na.omit(swap)
error.swap = mutate(swap, inc = (PX_LAST - lag(PX_LAST))*100 ) %>% group_by(PX_LAST_grcut) %>% summarise(err = rmse_my(inc))

error.swap = na.omit(error.swap)
# line plot
# g2 = ggplot(error.swap, aes(x=PX_LAST_grcut, y = err, group = 1)) + geom_point() + geom_line()

# combine datasets
full.swap = full_join(swap, error.swap, by = "PX_LAST_grcut")

ggplot(full.swap, aes(x=PX_LAST_grcut)) + geom_bar(aes(fill=date_grcut)) +
  geom_point(aes(y=err*5, group=1)) + geom_line(aes(y=err*5, group=1)) +
  scale_y_continuous(sec.axis = sec_axis(~./5, name = "Annualized deviations (bp)")) +
  ggtitle("Daily Volatility versus Level for 10 Year Swap Rate") +
  xlab("rate level, %") + ylab("Observations") +
  guides(fill=guide_legend(title=NULL)) + scale_fill_brewer(palette = "Pastel1")
# scale_fill_grey() + theme_classic()

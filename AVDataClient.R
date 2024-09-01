# Steps for cloning project into fresh directory:
# https://stackoverflow.com/questions/41427500/creating-a-virtualenv-with-preinstalled-packages-as-in-requirements-txt
# library(renv) # https://posit.co/blog/renv-project-environments-for-r/ Quick start guide for 'renv'

library(httr)
library(readr)
library(reticulate)

use_virtualenv('/Users/alanjackson/Environments/alphaVantageAPI/myEnv')
path = "/Users/alanjackson/Environments/alphaVantageAPI/"
setwd(path)

source("AVcredentials.R")
source_python(paste0(path, "AVDataClient.py"))
# Run the following function from RobinhoodAPI script to get my latest RH portfolio data:
# source_python(paste0(path, "RobinhoodAPI.py"))
# export_dict_to_csv(my_stocks, '/Users/alanjackson/Environments/alphaVantageAPI/RobinhoodPortfolio.csv')

filename <- "RobinhoodPortfolio.csv"

fundamentals <- getLatestFundamentalsData(filename, PREMIUM_API_KEY)
weekly_data <- getLatestWeeklyPrices(filename, PREMIUM_API_KEY)
weekly_data$pk <- paste0(weekly_data$date, weekly_data$symbol, weekly_data$volume)

weekly_data <- getLatestWeeklyPrices(filename, PREMIUM_API_KEY)

eps_data <- getEPSdata(filename, PREMIUM_API_KEY)
vwap <- getVWAP(filename, PREMIUM_API_KEY)
# sma <- getSMA(filename, PREMIUM_API_KEY)



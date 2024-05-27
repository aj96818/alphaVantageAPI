# Steps for cloning project into fresh directory:
# https://stackoverflow.com/questions/41427500/creating-a-virtualenv-with-preinstalled-packages-as-in-requirements-txt
#library(renv) # https://posit.co/blog/renv-project-environments-for-r/ Quick start guide for 'renv'
library(httr)
library(readr)
library(reticulate)

use_virtualenv('/Users/alanjackson/Environments/alphaVantageAPI/myEnv')
path = "/Users/alanjackson/Environments/alphaVantageAPI/"
setwd(path)
source("AVcredentials.R")
# Source 'myEnv' Python "AVDataClient" Script 
source_python(paste0(path, "AVDataClient.py"))

tickers <- getLatestTickerSymbols(PREMIUM_API_KEY)

# Fundamentals Data for all stocks last downloaded on 5/12/24 "av_fundamentals_all_tickers.csv"
# fun_data <- getLatestFundamentalsData(paste0(path, "allActiveTickers.csv"), PREMIUM_API_KEY)
# daily_data <- getHistoricalDailyPrices(paste0(path, "allActiveTickers.csv"), PREMIUM_API_KEY)

filename <- "allTickersAsOf_2024-05-27.csv"
fundamentals <- getLatestFundamentalsData(filename, PREMIUM_API_KEY)
weekly_data <- getHistoricalWeeklyPrices(filename, PREMIUM_API_KEY)
eps_data <- getEPSdata(filename, PREMIUM_API_KEY)
crypto_data <- getLatestCryptoPrices(PREMIUM_API_KEY)

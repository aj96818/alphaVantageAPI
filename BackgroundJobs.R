library(httr)
library(readr)
#library(renv) # https://posit.co/blog/renv-project-environments-for-r/ Quick start guide for 'renv'
#install.packages("reticulate")
library(reticulate)
use_virtualenv('/Users/alanjackson/Environments/alphaVantageAPI/myEnv')

source("~/Environments/alphaVantageAPI/AVcredentials.R")
path = "/Users/alanjackson/Environments/alphaVantageAPI/"
setwd(path)

getLatestTickerSymbols = function(API_KEY){
  url <- paste0("https://www.alphavantage.co/query?function=LISTING_STATUS&apikey=", API_KEY)
  response <- GET(url)
  
  # Input data as a single character vector
  parsed_data <- (rawToChar(response$content))
  
  # Splitting data into lines
  lines <- strsplit(parsed_data, "\r\n")[[1]]
  
  # Initialize empty vectors to store parsed data
  symbol <- character()
  name <- character()
  exchange <- character()
  assetType <- character()
  ipoDate <- character()
  delistingDate <- character()
  status <- character()
  
  # Loop through each line and extract fields
  for (line in lines) {
    if (line != "") {  # Skip empty lines
      fields <- strsplit(line, ",")[[1]]
      symbol <- c(symbol, fields[1])
      name <- c(name, fields[2])
      exchange <- c(exchange, fields[3])
      assetType <- c(assetType, fields[4])
      ipoDate <- c(ipoDate, fields[5])
      delistingDate <- c(delistingDate, fields[6])
      status <- c(status, fields[7])
    }
  }
  
  # Create dataframe from extracted data
  df <- data.frame(
    symbol = symbol,
    name = name,
    exchange = exchange,
    assetType = assetType,
    ipoDate = as.Date(ipoDate, format = '%Y-%m-%d'),  # Convert ipoDate to Date type
    delistingDate = as.Date(delistingDate, format = '%Y-%m-%d'),  # Convert delistingDate to Date type
    status = status,
    stringsAsFactors = FALSE  # Avoid conversion to factors
  )
  
  df <- df[-1, ]
  stocks <- df[df$assetType == 'Stock', ]
  return(stocks)
}
stocks = getLatestTickerSymbols(PREMIUM_API_KEY)
write_csv(stocks, paste0('allActiveTickers_', Sys.Date(), '.csv'))

# Source 'myEnv' Python "AVDataClient" Script 
source_python(paste0(path, "AVDataClient.py"))

# Fundamentals Data for all stocks last downloaded on 5/12/24 "av_fundamentals_all_tickers.csv"
# fun_data <- getLatestFundamentalsData(paste0(path, "allActiveTickers.csv"), PREMIUM_API_KEY)
# daily_data <- getHistoricalDailyPrices(paste0(path, "allActiveTickers.csv"), PREMIUM_API_KEY)

filename <- "allActiveTickers_2024-05-24.csv"
fundamentals <- getLatestFundamentalsData(filename, PREMIUM_API_KEY)
weekly_data <- getHistoricalWeeklyPrices(filename, PREMIUM_API_KEY)
eps_data <- getEPSdata(filename, PREMIUM_API_KEY)
crypto_data <- getLatestCryptoPrices(PREMIUM_API_KEY)

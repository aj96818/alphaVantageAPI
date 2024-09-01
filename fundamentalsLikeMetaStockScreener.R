# # Stock screener 1:
# Let's try to find a stock like META that is undervalued.
# We'll use Meta's KPI's (EPS, PERatio, etc.) to find other stocks like it.
# 
# We'll use the following filters to try find stocks like Meta:
# 
# Market Cap > $1B
# PERatio > 25
# EPS >= 10
# RevenuePerShareTTM > $20
# ProfitMargin > 0.3
# QuarterlyEarningsGrowthYOY > 1.1
# QuarterlyRevenueGrowthYoY > 0.2
# ReturnOnEquityTTM > 0.2

# import latest fundamentals CSV after joining it to all the stocks.

funLikeMeta <- fundamentals[(fundamentals$PERatio >= 25
                             & fundamentals$EPS >= 10
                             & fundamentals$RevenuePerShareTTM > 20
                             & fundamentals$ProfitMargin > 0.3
                             & fundamentals$QuarterlyEarningsGrowthYOY > 1.1
                             & fundamentals$QuarterlyRevenueGrowthYOY > 0.2
                             & fundamentals$ReturnOnEquityTTM > 0.2), ]


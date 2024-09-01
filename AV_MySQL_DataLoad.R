
# If error occurs writing data to MySQL DB, refer to the following thread:
# https://stackoverflow.com/questions/50745431/trying-to-use-r-with-mysql-the-used-command-is-not-allowed-with-this-mysql-vers?rq=1

# Install and load the necessary packages
install.packages("RMySQL")
install.packages("readr")

library(RMySQL)
library(readr)

# Define the MySQL database connection parameters
db_host <- "localhost"
db_user <- "root"
db_password <- "mysqlrootpw"
db_name <- "av"


# Connect to the MySQL database
con <- dbConnect(MySQL(), 
                 user = db_user, 
                 password = db_password, 
                 host = db_host, 
                 dbname = db_name)

# Write the data returned by the AV API calls to the following MySQL database ("av") tables:

# weekly prices data
dbWriteTable(con, "weekly_prices", weekly_data, overwrite = TRUE, row.names = FALSE)

# fundamentals data
dbWriteTable(con, "fundamentals", fundamentals, overwrite = TRUE, row.names = FALSE)

# EPS data
dbWriteTable(con, "eps", eps_data, overwrite = TRUE, row.names = FALSE)

# Close the connection
dbDisconnect(con)

use av;

drop table weekly_prices;

-- weekly_prices table

CREATE TABLE weekly_prices (
    id INT AUTO_INCREMENT PRIMARY KEY
    , `date` date
    , open decimal(10,4)
    , high DECIMAL(10, 4)
    , low DECIMAL(10, 4)
    , close DECIMAL(10, 4)
    , volume INT
    , dividend DECIMAL(8, 4)
    , symbol VARCHAR(25)
    , pk VARCHAR(255)
);

select * from weekly_prices;

-- fundamentals table

CREATE TABLE fundamentals (
    Symbol VARCHAR(10),
    AssetType VARCHAR(50),
    Name VARCHAR(255),
    Description TEXT,
    CIK INT,
    Exchange VARCHAR(10),
    Currency VARCHAR(5),
    Country VARCHAR(50),
    Sector VARCHAR(100),
    Industry VARCHAR(100),
    Address VARCHAR(255),
    OfficialSite VARCHAR(255),
    FiscalYearEnd VARCHAR(20),
    LatestQuarter DATE,
    MarketCapitalization BIGINT,
    EBITDA BIGINT,
    PERatio DECIMAL(10, 2),
    PEGRatio DECIMAL(10, 3),
    BookValue DECIMAL(10, 3),
    DividendPerShare DECIMAL(10, 3),
    DividendYield DECIMAL(10, 5),
    EPS DECIMAL(10, 2),
    RevenuePerShareTTM DECIMAL(10, 2),
    ProfitMargin DECIMAL(10, 3),
    OperatingMarginTTM DECIMAL(10, 3),
    ReturnOnAssetsTTM DECIMAL(10, 3),
    ReturnOnEquityTTM DECIMAL(10, 3),
    RevenueTTM BIGINT,
    GrossProfitTTM BIGINT,
    DilutedEPSTTM DECIMAL(10, 2),
    QuarterlyEarningsGrowthYOY DECIMAL(10, 3),
    QuarterlyRevenueGrowthYOY DECIMAL(10, 3),
    AnalystTargetPrice DECIMAL(10, 2),
    AnalystRatingStrongBuy INT,
    AnalystRatingBuy INT,
    AnalystRatingHold INT,
    AnalystRatingSell INT,
    AnalystRatingStrongSell INT,
    TrailingPE DECIMAL(10, 2),
    ForwardPE DECIMAL(10, 2),
    PriceToSalesRatioTTM DECIMAL(10, 3),
    PriceToBookRatio DECIMAL(10, 2),
    EVToRevenue DECIMAL(10, 2),
    EVToEBITDA DECIMAL(10, 2),
    Beta DECIMAL(10, 3),
    52WeekHigh DECIMAL(10, 2),
    52WeekLow DECIMAL(10, 2),
    50DayMovingAverage DECIMAL(10, 2),
    200DayMovingAverage DECIMAL(10, 2),
    SharesOutstanding BIGINT,
    DividendDate DATE,
    ExDividendDate DATE
);

-- EPS data table

CREATE TABLE eps (
    fiscalDateEnding DATE,
    reportedDate DATE,
    reportedEPS DECIMAL(10, 2),
    estimatedEPS DECIMAL(10, 2),
    surprise DECIMAL(10, 2),
    surprisePercentage DECIMAL(10, 4),
    reportTime VARCHAR(20),
    symbol VARCHAR(10)
);

select * from eps

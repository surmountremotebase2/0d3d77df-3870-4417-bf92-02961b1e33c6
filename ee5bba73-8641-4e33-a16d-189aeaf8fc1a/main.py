from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import RSI, SMA
from surmount.data import Ratios, Asset

class NikeDipBuyingStrategy(Strategy):

    def __init__(self):
        self.ticker = "NKE"
        self.rsi_lower_threshold = 30
        self.dip_percentage = 0.07 # buy when the price falls 7% below moving average
        self.data_list = [
            Ratios(self.ticker),
            Asset(self.ticker) # to collect price history
        ]

    @property
    def interval(self):
        return "1day"

    @property
    def assets(self):
        return [self.ticker]

    @property
    def data(self):
        return self.data_list

    def run(self, data):
        allocation = 0
        ohlcv = data.get("ohlcv")
        if not ohlcv or len(ohlcv) < 50:  # Ensure sufficient data
            return TargetAllocation({})

        # Calculate RSI
        rsi_values = RSI(self.ticker, ohlcv, 14)
        
        if rsi_values:
            current_rsi = rsi_values[-1]
            # Calculate 50-day SMA
            sma_50 = SMA(self.ticker, ohlcv, 50)

            current_price = ohlcv[-1][self.ticker]['close']
            
            if current_rsi < self.rsi_lower_threshold:
                #check for a price 7% below moving average
                if sma_50 is not None and current_price < sma_50[-1] * (1-self.dip_percentage):
                  allocation = 0.7 # Allocate 70% if RSI and MA conditions are met 
                else:
                    allocation = 0.4 # Allocate 40% if only RSI condition is met
            
            #Fundamental Analysis Check (Simplified Example)
            ratios = data.get(("ratios", self.ticker))
            if ratios:
                # Example: Check if current P/E is significantly below historical average
                # (This is a simplified example and needs more robust historical data)
                current_pe = ratios[-1].get("peRatio")
                if current_pe and current_pe < 25:  # Assuming a historical average around 30
                    allocation = min(allocation + 0.3, 1.0)  # Increase allocation if P/E is favorable
        
        return TargetAllocation({self.ticker: allocation})
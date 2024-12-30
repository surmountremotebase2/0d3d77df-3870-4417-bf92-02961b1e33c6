from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import RSI
from surmount.logging import log

class TradingStrategy(Strategy):
    def __init__(self):
        # Define the ticker for Nike
        self.ticker = "NKE"
        # Define an RSI threshold for buying (typical oversold condition)
        self.oversold_rsi_threshold = 30

    @property
    def assets(self):
        # Only trade Nike
        return [self.ticker]

    @property
    def interval(self):
        # Use daily data for this strategy
        return "1day"

    def run(self, data):
        # Initialize allocation to zero
        allocation_dict = {self.ticker: 0}
        
        # Calculate the RSI for Nike
        rsi_values = RSI(self.ticker, data["ohlcv"], length=14)  # Using 14 periods for RSI calculation
        
        if rsi_values is not None and len(rsi_values) > 0:
            current_rsi = rsi_values[-1]
            log(f"Current RSI for {self.ticker}: {current_rsi}")
            
            # Check if the RSI is under the oversold threshold
            if current_rsi < self.oversold_rsi_threshold:
                log(f"{self.ticker} is oversold, buying signal.")
                allocation_dict[self.ticker] = 1  # Set full allocation to buy
                
        else:
            log(f"RSI data unavailable for {self.ticker}.")
        
        # Return the target allocation
        return TargetAllocation(allocation_dict)
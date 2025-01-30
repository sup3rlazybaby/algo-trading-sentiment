from utils import setup_logging, fetch_data
from technical import TechnicalAnalyser
from fundamental import FundamentalAnalyser
from sentiment import SentimentAnalyser
import logging

class Strategy:
    def __init__(self, symbols: list):
        self.symbols = symbols
    
    def analyse_stock(self, symbol: str) -> dict:
        try:
            data = fetch_data(symbol)
            
            tech = TechnicalAnalyser(data)
            tech_score = tech.analyse()
            
            fund = FundamentalAnalyser(symbol)
            fund_score = fund.analyse()
            
            sent = SentimentAnalyser(symbol)
            sent_score = sent.analyse()
            
            total_score = (
                tech_score * 0.4 +          # Technical weight
                fund_score * 0.4 +          # Fundamental weight
                sent_score * 0.2            # Sentiment weight
            )
            
            return {
                'symbol': symbol,
                'score': total_score,
                'technical': tech_score,
                'fundamental': fund_score,
                'sentiment': sent_score
            }
        except Exception as e:
            logging.error(f"Error analyzing {symbol}: {e}")
            return None
        
if __name__ == '__main__':
    # setup_logging()
    strategy = Strategy(['AAPL', 'MSFT', 'GOOGL'])
    for symbol in strategy.symbols:
        result = strategy.analyse_stock(symbol)
        print(f'Score for {symbol}: \
                \n\tTechnical: {result['technical']}\
                \n\tFundamental: {result['fundamental']}\
                \n\tSentiment: {result['sentiment']}\
                \n\tTotal: {result['score']}')
        
        # if result:
        #     logging.info(f"Analysis for {symbol}: {result}")
import logger
import strategyTester as st
import dataManipulator as dm
from multiprocessing import Pool
import pandas as pd

findBest = True

def runBacktestProcess(symbol, strategy):
    bestStrategy = strategy

    if findBest:
        bestSharpe = 0
        strategies = ['dailyRange', 'buyAndHold']

        for strategy in strategies:
            result = st.runBacktest(symbol, strategy)

            if result is None:
                return None
            
            if result['Sharpe Ratio'] > bestSharpe:
                bestSharpe = result['Sharpe Ratio']
                bestStrategy = strategy

    else:
        result = st.runBacktest(symbol, strategy)
    
    if result is None:
        return None
    
    # Convert result to a dictionary or other simple format
    simplifiedResult = {
        'symbol': symbol,
        'maxDrawdown': result['Max. Drawdown [%]'],
        'return': result['Return [%]'],
        'equity_curve': result['_equity_curve'],
        'strategy': bestStrategy
    }
    
    logger.logSimple(simplifiedResult)  # Log the simplified result
    return simplifiedResult

if __name__ == "__main__":
    # symbols = pd.read_html('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')[0]['Symbol'].tolist()
    # print(symbols)
    symbols = ['AMD', 'NVDA', 'CAT', 'AAPL', 'MSFT', 'GOOG', 'AMZN', 'CSCO', 'QCOM', 'IBM', 'NFLX', 'T']
    # symbols = ['AMD', 'NVDA', 'CAT']
    # symbols = ['ES=F', 'GC=F', 'YM=F', 'NQ=F', 'RTY=F', 'SIL=F']
    # strategy = 'dailyRange'
    strategy = 'buyAndHold'

    # Use Pool to parallelize the backtest process
    with Pool() as pool:
        # Run backtest in parallel and get the results
        results = pool.starmap(runBacktestProcess, [(symbol, strategy) for symbol in symbols])

    # After all backtests are done, log the aggregated results
    logger.logAggregatedResults(results)
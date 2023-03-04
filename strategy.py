from datetime import date
from dateutil.relativedelta import relativedelta

def get_historical_data(instrument_token, from_date=str(date.today() + relativedelta(months=-2)), to_date=str(date.today()), interval='minute'):
    try:
        return kite.historical_data(instrument_token, from_date, to_date, interval)
    except Exception:
        pass
    
train_test_records = get_historical_data(instrument_token=738561, from_date=str(date.today() + relativedelta(days=-30)), to_date=str(date.today() + relativedelta(days=-7)))
validation_records = get_historical_data(instrument_token=738561, from_date=str(date.today() + relativedelta(days=-7)), to_date=str(date.today()))

#converting to pandas dataframe
import pandas as pd
df = pd.DataFrame(train_test_records)

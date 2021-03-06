# Moving Average
def mavg(df, term, symbol='close'):
    df_mavg = df[symbol].copy().to_frame().rolling(window=term).mean().join(df['timestamp'])
    return df_mavg


# Bollinger Band
def bband_upper(df, term, symbol='close'):
    df_mavg = df[symbol].copy().to_frame().rolling(window=term).mean()
    df_sigma = df[symbol].copy().to_frame().rolling(window=term).std()
    df_bband_upper = df_mavg + 2 * df_sigma
    df_bband_upper['timestamp'] = df['timestamp']
    return df_bband_upper


def bband_lower(df, term, symbol='close'):
    df_mavg = df[symbol].copy().to_frame().rolling(window=term).mean()
    df_sigma = df[symbol].copy().to_frame().rolling(window=term).std()
    df_bband_lower = df_mavg - 2 * df_sigma
    df_bband_lower['timestamp'] = df['timestamp']
    return df_bband_lower


def bband(df, term, symbol='close'):
    df_mavg = df[symbol].copy().to_frame().rolling(window=term).mean()
    df_sigma = df[symbol].copy().to_frame().rolling(window=term).std()
    df_bband = df.copy()
    df_bband['upper'] = df_mavg + 2 * df_sigma
    df_bband['lower'] = df_mavg - 2 * df_sigma
    return df_bband


# Exponential Moving Average(term=12, 26 for MACD)
def ema(df, term=12, symbol='close'):
    df_ema_cp = df[symbol].copy().to_frame()
    df_ema = df_ema_cp.ewm(span=term).mean()
    df_ema['timestamp'] = df['timestamp']
    return df_ema


class TechnicalIndicator:

    def __init__(self, df=None, name=None, color=None, alpha=None):
        self.df = df
        self.name = name
        self.color = color
        self.alpha = alpha


class MavgIndicator(TechnicalIndicator):

    def __init__(self, df, term=26, color=None, alpha=None):
        self.df = mavg(df=df, term=term)
        self.name = 'Moving Average: term=' + str(term)
        self.color = color
        self.alpha = alpha


class BBandUpperIndicator(TechnicalIndicator):

    def __init__(self, df, term=26, color=None, alpha=None):
        self.df = bband_upper(df=df, term=term)
        self.name = 'Bollinger Band Upper: term=' + str(term)
        self.color = color
        self.alpha = alpha


class BBandLowerIndicator(TechnicalIndicator):

    def __init__(self, df, term=26, color=None, alpha=None):
        self.df = bband_lower(df=df, term=term)
        self.name = 'Bollinger Band Lower: term=' + str(term)
        self.color = color
        self.alpha = alpha


class BBandIndicator(TechnicalIndicator):

    def __init__(self, df, term=26, color=None, alpha=None):
        self.df = bband(df=df, term=term)
        self.name = 'Bollinger Band: term=' + str(term)
        self.color = color
        self.alpha = alpha
        if self.alpha:
            self.subalpha = self.alpha / 2
        else:
            self.subalpha = None


class EMAIndicator(TechnicalIndicator):

    def __init__(self, df, term=26, color=None, alpha=None):
        self.df = ema(df=df, term=term)
        self.name = 'Exponential Moving Average: term=' + str(term)
        self.color = color
        self.alpha = alpha

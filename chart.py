import datetime

import pandas as pd

import technical as tec


def plot_and_save_chart(save_filename, list_indicators, fdate=None, tdate=None):
    from matplotlib import pyplot as plt
    plt.style.use('ggplot')
    plt.figure(figsize=(9.6, 5.4))
    for indicator in list_indicators:
        if fdate:
            indicator.df = indicator.df[indicator.df['timestamp'] > fdate]
        if tdate:
            indicator.df = indicator.df[indicator.df['timestamp'] < tdate]
        if isinstance(indicator, tec.BBandIndicator):
            plt.plot(
                indicator.df['timestamp'],
                indicator.df['upper'],
                label=indicator.name,
                color=indicator.color,
                alpha=indicator.alpha)
            plt.plot(
                indicator.df['timestamp'],
                indicator.df['lower'],
                label=None,
                color=indicator.color,
                alpha=indicator.alpha)
            plt.plot(
                [indicator.df['timestamp'], indicator.df['timestamp']],
                [indicator.df['lower'], indicator.df['upper']],
                label=None,
                color=indicator.color,
                alpha=indicator.subalpha)
        else:
            plt.plot(indicator.df['timestamp'], indicator.df['close'], label=indicator.name, color=indicator.color)
    plt.xlabel('Date')
    plt.ylabel('USD/BTC')
    plt.legend()
    plt.savefig(save_filename, dpi=350)


def caliculate_and_plot_data(btc_data_filename, from_date: str, to_date: str):

    list_indicators = []
    if from_date:
        from_date = datetime.datetime.strptime(from_date, '%Y-%m-%d')
    else:
        from_date = None
    if to_date:
        to_date = datetime.datetime.strptime(to_date, '%Y-%m-%d')
    else:
        to_date = None

    df_usd2btc = pd.read_csv(btc_data_filename)
    df_usd2btc['timestamp'] = df_usd2btc['time'].apply(lambda x: datetime.datetime.fromtimestamp(x))

    raw_indicator = tec.TechnicalIndicator(df=df_usd2btc[['close', 'timestamp']], name='Raw Data(USD/BTC)')
    mavg_indicator = tec.MavgIndicator(df=raw_indicator.df)
    bband_indicator = tec.BBandIndicator(df=raw_indicator.df, color='c', alpha=0.4)
    ema_short_indicator = tec.EMAIndicator(df=raw_indicator.df, term=12, color='y')
    ema_long_indicator = tec.EMAIndicator(df=raw_indicator.df, term=26, color='g')

    list_indicators.append(bband_indicator)
    list_indicators.append(mavg_indicator)
    list_indicators.append(ema_short_indicator)
    list_indicators.append(ema_long_indicator)
    list_indicators.append(raw_indicator)

    plot_and_save_chart(list_indicators=list_indicators, fdate=from_date, tdate=to_date)

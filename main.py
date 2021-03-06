# Crypto Currency Automated Trading System
import datetime
import os
import pytz

import pandas

from chart import caliculate_and_plot_data
from get_data import get_data
from mastodon import publish_status_with_media


if __name__ == "__main__":

    btc_datafile = "btc2usd.csv"
    img_file = "btc_analysis.png"
    # Please set the access_token of mastodon in environment variables
    # In AWS EC2 instance: Amazon Linux 2 AMI, cannot use os.environ
    # So, for now, directly set access_token in EC2 instance
    token_env = "MASTODON_CLOUD_TOKEN"

    print("="*80)
    print(datetime.datetime.now())

    # generate or update btc data csv file
    get_data(*btc_datafile.split("."))
    print(f"[Finished fetching bitcoin data] -> {btc_datafile}")

    date_today = str(datetime.datetime.now(tz=pytz.utc).date())
    date_90days_ago = str((datetime.datetime.now(tz=pytz.utc) - datetime.timedelta(days=90)).date())

    # generate png file of btc data
    caliculate_and_plot_data(btc_data_filename=btc_datafile,
                             save_filename=img_file,
                             from_date=date_90days_ago,
                             to_date=date_today)
    print(f"[Finished generating png] -> {img_file}")

    df_btc = pandas.read_csv(btc_datafile)
    btc_price_today = df_btc["close"].tail(1).item()

    # publish the image to mastodon
    status = f"[bot] Bitcoin Chart Today\nTIMESTAMP: {datetime.datetime.now()}\nBTCPRICE: {btc_price_today} USD/BTC\n\n(=^･ω･^=)<Have a good one!\n"
    publish_status_with_media(access_token=os.environ[token_env], status=status, filename=img_file)
    print("[Finished publising the image to Mastodon]")

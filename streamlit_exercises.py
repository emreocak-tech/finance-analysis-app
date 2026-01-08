###python -m streamlit run streamlit_exercises.py
import streamlit as st
import matplotlib.pyplot as plt
import yfinance as yf
from datetime import datetime
from prophet import Prophet
import json
from dotenv import load_dotenv
from urllib3 import HTTPSConnectionPool
from urllib3.exceptions import SSLError
load_dotenv()
import os
import requests
api_key=os.getenv("api_key")
decision=os.getenv("decision")
base_url=os.getenv("base_url")
coins=os.getenv("coins")
st.title("Kullanıcı Sözleşmesi")
st.write("UYARI: **Lütfen Okuyunuz !** Bu uygulama yalnızca bilgilendirme amaçlıdır ve yatırım tavsiyesi içermez.- Finansal piyasalarda işlem yapmak yüksek risk içerir ve sermaye kaybına yol açabilir.- Sağlanan tahminler ve analizler kesin sonuç vermez, yanılabilir.- Alacağınız tüm yatırım kararlarının sorumluluğu tamamen size aittir.- Uygulama geliştiricisi, kullanımdan kaynaklanan herhangi bir zarardan sorumlu değildir.- Yatırım kararı vermeden önce profesyonel bir finansal danışmana başvurmanız önerilir.")
check_box = st.checkbox("Yukarıdaki kullanıcı sözleşmesini okudum, anladım ve finansal kararlarımın sorumluluğunun bana ait olduğunu kabul ediyorum.")
if check_box:
    end_date = datetime(year=2025, month=10, day=22)
    start_date = datetime(year=2023, month=9, day=21)
    st.title("ECONOMY WEBSİTE")
    st.header("**Welcome!**")
    st.header("**Anlık Hisse Fiyat Değeri**")
    decision = ["AAPL", "NVDA", "ASELS.IS", "TSLA", "ORCL", "INTC", "EREGL.IS", "MSFT", "AMD", "GM", "LMT", "BABA","QNBTR.IS"]
    stock_market_now=st.selectbox("Hisse Seç",options=decision)
    try:
        def determine():
            ticker = yf.Ticker(stock_market_now)
            price = ticker.fast_info['last_price']
            return  price
    except ValueError as value_er:
        st.warning(f"DataType Hatası! , Hata Kodu : {value_er}")
    except Exception as ec:
        st.warning(f"Hata! , Hata Kodu: {ec}")
    except ConnectionError as connect_er:
        st.warning("API servisiyle bağlantı kurulamadı!")
    if st.button("Determine instantenous price"):
        price=determine()
        st.write(f"Seçtiğiniz hissenin anlık fiyatı: {str(price)[0:6]} 💲")
    st.header("**Son 30 Günlük Fiyat Ortalaması**")
    stock_code = st.selectbox("Choose a company", options=decision, help="Select any company")
    def calculate():
        try:
            df = yf.download(tickers=stock_code, start=start_date, end=end_date, interval="1d")
            price = df["Close"].iloc[0:30].mean()
            return price
        except Exception as er:
            st.warning(f"Hata! Hata Kodu : {er}")
        except ConnectionError as connection_error_one:
            st.warning(f"Bağlantı Hatası! , Hata Kodu:{connection_error_one}")
        except TypeError as t_error:
            st.warning(f"Yanlış Değer Döndürüldü! , Hata Kodu : {t_error}")
    if st.button("Calculate"):
        origin_price=calculate()
        st.write("Seçtiğiniz hissenin son 30 günlük fiyat değeri :" + " " + str(float(origin_price))[0:5] + " " + "💲")
        st.success("İşlem Başarılı")
    st.balloons()
    st.header("HİSSE KARŞILAŞTIRICI")
    choosen = st.multiselect("Hisse Seçin:", options=decision,help="Birden çok hisse seçebilirsiniz")
    if len(choosen)==3:
        try:
            def calculate():
                df2 = yf.download(tickers=choosen, interval="1d", start=start_date, end=end_date)
                st.warning("3 hisse kodu girmeniz lazım!")
                prices1 = df2["Close"][choosen[0]].iloc[0:30].mean()
                prices2 = df2["Close"][choosen[1]].iloc[0:30].mean()
                prices3 = df2["Close"][choosen[2]].iloc[0:30].mean()
                return [prices1,prices2,prices3]
            if st.button("Calculate that"):
                price=calculate()
                st.write(f"{choosen[0]} hissesinin son 30 günlük kapanış ortalaması:" + " " + str(float(price[0]))[0:7] + " " + "💲")
                st.write(f"{choosen[1]} hissesinin son 30 günlük kapanış ortalaması:" + " " + str(float(price[1]))[0:7] + " " + "💲")
                st.write(f"{choosen[2]} hissesinin son 30 günlük kapanış ortalaması:" + " " + str(float(price[2]))[0:7] + " " + "💲")
                st.success("İşlem Başarılı!")
        except ConnectionError as connection_error:
            st.warning(f"Bağlantı Hatası! , Hata Kodu:{connection_error}")
        except ValueError as value_error:
            st.warning(f"Datatype Hatası! , Hata Kodu : {value_error}")
    else:
        st.warning("3 hisse seçebilirsiniz!")
    st.header("GRAPHİCAL ANALYSIS")
    company = st.selectbox("Select a company", options=decision, help="Give a value")
    try:
        df3 = yf.download(tickers=company, start=start_date, end=end_date, interval="1d")
        value = df3["Close"].iloc[0:30]
        fig1, ax1 = plt.subplots(figsize=(10, 6))
        bar_values = value.iloc[0:25].values.flatten().astype(float)
        bar_indices = range(len(bar_values))
        ax1.plot(bar_indices, bar_values,color="Red")
        ax1.set_xlabel("Gün")
        ax1.set_ylabel("Fiyat ($)")
        ax1.set_title(f"{company} Kapanış Fiyatları")
        ax1.grid()
        st.pyplot(fig1)
    except ConnectionError as connection_error:
        st.warning(f"Bağlantı Hatası! , Hata Kodu:{connection_error}")
    except TypeError as type_er:
        st.warning(f"Yanlış Değer Döndürüldü! , Hata Kodu : {type_er}")
    st.header("**Hisse Tahmin Etme**")
    select=st.selectbox("**Şirket Seç**",options=decision)
    interval=st.slider("Kaç Gün Sonrasını Tahmin Etmek İstiyorsunuz:",min_value=0,max_value=100,help="Kaydırsana!")
    try:
        def calculate():
            df4 = yf.download(tickers=select, start=start_date, end=end_date, interval="1d")
            df4 = df4[['Close']].reset_index()
            df4.columns = ['ds', 'y']
            df4 = df4.dropna()
            model = Prophet()
            model.fit(df4)
            future = model.make_future_dataframe(periods=360)
            predict = model.predict(future)
            tahmin_degeri = predict.iloc[-interval]['yhat']
            return [tahmin_degeri,predict,model]
    except Exception as e:
        st.warning(f"Hata! Hata Kodu : {e}")
    except ConnectionError as connection_error_two:
        st.warning(f"Bağlantı Hatası! Hata Kodu:{connection_error_two}")
    except None:
        st.warning("Yanlış Değer Döndürüldü!")
    if st.button("Determine"):
        tahmin_degeri = calculate()
        st.write(f"{select} hissesinin {interval} gün sonraki tahmini fiyat değeri:" + " " + str(tahmin_degeri[0])[0:5] + " " + "💲")
    try:
        values=calculate()
        if st.button("Predict Graphic"):
            fig2 = values[2].plot(values[1])
            plt.title(f"{select} Hisse Tahmini - {interval} Gün")
            st.pyplot(fig2)
    except TypeError as type_error:
        st.warning("Yanlış Değer Döndürüldü!")
    except Exception as e:
        st.warning(f"Hata! Hata Kodu : {e}")
    except ConnectionError as connection_error_two:
        st.warning(f"Bağlantı Hatası! Hata Kodu:{connection_error_two}")
    st.info("💡 **Not:** Bu tahmin Prophet modeline dayanmaktadır. Gerçek piyasa koşulları daha karmaşıktır.")
    st.header("ANLIK DÖVİZ DEĞERLERİ")
    currency=st.selectbox("İstediğiniz Para Birimini Giriniz",options=["USD","EUR", "GBP" , "JPY" , "CNY","AED","IRR","CAD","RUB","SAR","GEL"])
    try:
        def calculate_currency():
            url = f'https://v6.exchangerate-api.com/v6/{api_key}/latest/{currency}'
            response = requests.get(url)
            data = response.json()
            return data
        data=calculate_currency()
        if st.button("Calculate Currency"):
            st.write(f"**1 {currency} = {str(data['conversion_rates']['TRY'])} TL'dir**")
    except ValueError as v_error:
        st.warning("API yanıtı düzgün değil!")
    except Exception as e:
        st.warning("Hata! , Lütfen Daha Sonra Tekrar Deneyin!")
    except ConnectionError as connection_err:
        st.warning("API bağlantı hatası!")
    st.header("**Bitcoin**")
    ticker=st.selectbox("Bir Coin Seç",options=["BERAUSDT","BTCUSDT","ETH","SOL","DOGE","AVAX","SHIB","APT","PI","TRUMP","XRP","TRX"])
    try:
        def btc_price():
           url = "https://api.binance.com/api/v3/ticker/price"
           response=requests.get(url,params={"symbol":ticker},verify=False,timeout=10)
           cevap=response.json()
           if response.status_code==200:
               return cevap
        if st.button("BTC Price Button"):
            response = btc_price()
            st.write(f"{ticker} değeri anlık olarak :" + " " + str(response.json()['price']))
        else:
            st.warning("API hizmetiyle bağlantı kurulamadı!")
    except ConnectionError as connection_error_three:
        st.warning("Binance API servislerine Ulaşılamadı!")
    except requests.exceptions.SSLError as ssl_error:
        st.warning("SSL hatası , AWS hizmetlerine erişilemiyor!")
    except HTTPSConnectionPool as error_html:
        st.warning(f"HTML hatası! , Hata Kodu : {error_html}")
else:
    st.info("Kullanıcı Sözleşmesini Kabul Edin!")




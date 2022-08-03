### Console bit.ly client

Script can shorten the link via bit.ly service
and also provides clicks statistic for bit.link

**installation:**

```
pip install -r requirements.txt
```

**setup:**

u need to add `BITLY_TOKEN` to env variables

**usage:**

enter long url to shorten, or short url to check clicks

```
python main.py https://long-url.kek
> Bitlink: https://bit.ly/3bs1lyo
```

```
python main.py https://bit.ly/3bs1lyo
> clicks: 5
```
from prometheus_client import Counter

zipcode_metric = Counter('zipcode', 'zipcode used for forecast', ['zipcode'])




# AWS Cloudwatch Server Monitor

# Set up

```
$ python3.6 -m venv .env
$ source .env/bin/activate
$ pip install -r requirements.txt
```

# To run a docker image

```
$ docker build -t metrics .
$ docker run -p 80:7000 metrics
```

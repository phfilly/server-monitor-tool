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
# What you can expect

![Nodes](https://github.com/phfilly/server-monitor-tool/blob/master/Screen%20Shot%202018-02-16%20at%201.47.09%20PM.png)

# Follow this link in order to setup and read AWS instance memory metrics

https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/mon-scripts.html
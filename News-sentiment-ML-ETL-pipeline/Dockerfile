# the lower base image must be a linux operating system
FROM python:3.10
EXPOSE 5000
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
CMD sh -c 'sleep 15s; python3 app.py'
# CMD sh -c 'sleep 10s ; python3 ./news_api.py ; sleep 4s; python3 ./app.py'
# command to give the mapping of the host and container ports -- 5000:5000 (first one is host and second one is container)
# so using the host port we try to access the container port on which docker image is running
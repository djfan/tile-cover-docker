FROM node:lts

# To install tzdata assuming UTC
# See https://stackoverflow.com/questions/44331836/apt-get-install-tzdata-noninteractive
ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y python-pip python3-pip python-tk
COPY requirements.txt /app/
RUN pip install -r /app/requirements.txt
RUN pip3 install -r /app/requirements.txt

RUN apt-get install -y jq

RUN npm install commander
RUN npm install @mapbox/tile-cover

COPY tile_cover.py /app/
COPY tile_cover.js /app/
COPY tile_cover.sh /app/

ENTRYPOINT ["bash", "/app/tile_cover.sh"]

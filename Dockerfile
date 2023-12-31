
# To Run: 
#  docker volume create cs2
#  docker volume create steamcmd_login_volume
#  docker volume create steamcmd_volume
#  docker build . -t cs2-manager
#  docker run -it -p 27015:27015 -p 5000:5000 -e STEAM_USERNAME=YOUR_USERNAME -e STEAM_PASSWORD="YOUR_PASSWORD" \ 
#      -v "cs2:/cs2" -v "steamcmd_login_volume:/home/steam/Steam" -v "steamcmd_volume:/home/steam/steamcmd" cs2-manager
#
#

FROM cm2network/steamcmd:root

RUN apt update 

RUN apt install -y wget build-essential libncursesw5-dev libssl-dev \
     libsqlite3-dev tk-dev libgdbm-dev libc6-dev libbz2-dev libffi-dev zlib1g-dev

WORKDIR /build
RUN wget https://www.python.org/ftp/python/3.11.3/Python-3.11.3.tgz 
RUN tar xzf Python-3.11.3.tgz
WORKDIR /build/Python-3.11.3
RUN ./configure --enable-optimizations
RUN make altinstall 
WORKDIR / 
RUN rm -rf /build

RUN pip3.11 install uvicorn pydantic fastapi

COPY . /app
WORKDIR /app

ENV CS_PORT=27015
ENV API_PORT=5000
ENV STEAM_USERNAME=anonymous
ENV STEAM_PASSWORD=anonymous

RUN mkdir /cs2
VOLUME /cs2

RUN chmod -R 777 /app
USER ${USER}

CMD python3.11 -m cs2_server_management_service.service --cs_server_port $CS_PORT \
  --api_port $API_PORT --steam_username $STEAM_USERNAME --steam_password $STEAM_PASSWORD --server_install_directory /cs2 --steamcmd /home/steam/steamcmd/steamcmd.sh

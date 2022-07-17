FROM mojl/pyconbb

RUN apt-get clean all
RUN apt-get update
RUN apt-get -y install --no-install-recommends default-jdk
RUN apt-get -y install --no-install-recommends default-jre
COPY ./app /home/




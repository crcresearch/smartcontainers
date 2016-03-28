FROM ubuntu:14.04
MAINTAINER Nicolas Reed <Nicolas.Reed.102 at nd dot edu>
RUN apt-get --yes update && apt-get --yes upgrade
RUN apt-get install -y curl unzip g++ git cmake libgsl0-dev libboost-all-dev libxerces-c-dev xsdcxx
RUN git clone https://github.com/SwissTPH/openmalaria
RUN cd openmalaria \
  && git checkout schema-32 \
  && git pull
RUN cd openmalaria && mkdir build \
  && cd build \
  && cmake -DCMAKE_CXX_COMPILER=/usr/bin/g++ -DCMAKE_BUILD_TYPE=Release .. \
  && make -j4
WORKDIR /om
RUN cp /openmalaria/build/openMalaria /om/
RUN curl -L -O https://github.com/SwissTPH/openmalaria/releases/download/binary-archive/Schema.32.zip
RUN unzip Schema.32.zip
RUN cp Schema\ 32/densities.csv Schema\ 32/autoRegressionParameters.csv Schema\ 32/scenario_32.xsd /om
VOLUME /om/scenarios
ENTRYPOINT ["./openMalaria"]
CMD ["-h"]

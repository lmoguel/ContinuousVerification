FROM mojl/pyconbb

COPY install-packages.sh /home/
RUN chmod +x install-packages.sh
RUN ./install-packages.sh

COPY ./requirements.txt /home/
RUN pip install -r requirements.txt 

COPY ./app /home/

FROM selenium/standalone-chrome 
RUN sudo apt update && sudo apt install -y \
    python3 \
    python3-pip
RUN pip3 install Flask selenium
ADD ./clicker-service.py /clicker/
CMD [ "python3", "/clicker/clicker-service.py" ]

FROM ubuntu:20.04
RUN apt update
RUN apt install python3 -y; apt install pip -y
RUN python3 -m pip install requests
CMD python3 /botTG/checkmail.py
FROM ubuntu:20.04
RUN apt update
RUN apt install python3 -y; apt install pip -y
RUN python3 -m pip install requests
RUN apt install cron -y; apt install nano -y
RUN crontab -l | { cat; echo "*/2 * * * * /botTG/checkmail.py"; } | crontab -
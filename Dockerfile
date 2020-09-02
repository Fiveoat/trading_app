FROM python:3.7

RUN useradd -ms /bin/bash default_user
USER default_user
WORKDIR /home/default_user/opt
ENV PATH="/home/default_user/.local/bin:${PATH}"
ENV PYTHONPATH $PYTHONPATH: /home/default_user
COPY --chown=default_user:default_user requirements.txt requirements.txt
RUN pip3 install --user -r requirements.txt
EXPOSE 5000
COPY --chown=default_user:default_user . .

ENTRYPOINT ["/bin/bash", "entrypoint.sh"]


#CMD [ "python", "app.py" ]

# FROM alpine:latest
# RUN apk add --no-cahche python3-dev && pip3 install --upgrade pip

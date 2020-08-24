FROM python:3.7

RUN useradd -ms /bin/bash default_user
USER default_user
WORKDIR /home/default_user/opt
ENV PATH="/home/default_user/.local/bin:${PATH}"
ENV PYTHONPATH $PYTHONPATH: /home/default_user
COPY --chown=default_user:default_user requirements.txt requirements.txt
RUN pip install --user -r requirements.txt
EXPOSE 5000
COPY --chown=default_user:default_user . .

ENTRYPOINT ["/bin/bash", "entrypoint.sh"]

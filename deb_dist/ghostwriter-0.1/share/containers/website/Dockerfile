FROM debian

MAINTAINER hiro <hiro@torproject.org>

RUN \
    apt-get update && \
    apt-get install -y tor nginx &&\
    apt-get clean && rm -rf /var/lib/apt/lists/* &&\
    rm -rf /usr/share/doc/ && rm -rf /usr/share/man &&\
    rm -rf /usr/share/locale

COPY tor/torrc /etc/tor

COPY default /etc/nginx/sites-available/default
COPY onion-entrypoint.sh /onion-entrypoint.sh

# Define mountable directories.
VOLUME ["/etc/nginx/sites-enabled", "/etc/nginx/certs", "/etc/nginx/conf.d", "/var/log/nginx"]

# Define working directory.
WORKDIR /etc/nginx

# Add user

RUN useradd -ms /bin/bash peer
RUN mkdir -p 700 /home/peer/

EXPOSE 80

# Start up
ENTRYPOINT ["/onion-entrypoint.sh"]

CMD ["cat /home/peer/hidden_service/hostname"]

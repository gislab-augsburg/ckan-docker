#FROM ckan/ckan-base:ckan-2.10.0
#FROM ckan/ckan-base:dev-v2.10
FROM martymcfly333/ckan-docker-edit-ini:latest

# Set up environment variables
ENV APP_DIR=/srv/app
ENV TZ=UTC
RUN echo ${TZ} > /etc/timezone

# Make sure both files are not exactly the same
RUN if ! [ /usr/share/zoneinfo/${TZ} -ef /etc/localtime ]; then \
        cp /usr/share/zoneinfo/${TZ} /etc/localtime ;\
    fi ;

FROM ckan/ckan-base:2.10.0
#FROM ckan/ckan-base:2.9.9

# Set up environment variables
ENV TZ=UTC
RUN echo ${TZ} > /etc/timezone

# Make sure both files are not exactly the same
RUN if ! [ /usr/share/zoneinfo/${TZ} -ef /etc/localtime ]; then \
        cp /usr/share/zoneinfo/${TZ} /etc/localtime ;\
    fi ;

USER 1002890000
ENV APP_DIR=/srv/app

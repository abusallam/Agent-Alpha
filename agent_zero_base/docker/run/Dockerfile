FROM frdel/agent-zero-base:latest

ARG BRANCH
RUN if [ -z "$BRANCH" ]; then echo "ERROR: BRANCH is not set!" >&2; exit 1; fi
ENV BRANCH=$BRANCH

COPY docker/run/fs/ /

RUN bash /ins/pre_install.sh $BRANCH

RUN bash /ins/install_A0.sh $BRANCH

RUN bash /ins/install_additional.sh $BRANCH

ARG CACHE_DATE=none
RUN echo "cache buster $CACHE_DATE" && bash /ins/install_A02.sh $BRANCH

RUN bash /ins/post_install.sh $BRANCH

EXPOSE 22 80 9000-9009

RUN chmod +x /exe/initialize.sh /exe/run_A0.sh /exe/run_searxng.sh /exe/run_tunnel_api.sh

CMD ["/exe/initialize.sh", "$BRANCH"]

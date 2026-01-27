FROM alpine:3.19

RUN apk add --no-cache curl ca-certificates

COPY scripts/init-templates.sh /init-templates.sh

RUN chmod +x /init-templates.sh

ENTRYPOINT ["/bin/sh", "/init-templates.sh"]

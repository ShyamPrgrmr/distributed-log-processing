FROM logstash:9.1.9

#Testing
COPY /test/test.log /tmp/test.log

COPY /config/logstash.yml /usr/share/logstash/config/logstash.yml

COPY /pipeline/logstash.conf /usr/share/logstash/pipeline/logstash.conf

EXPOSE 5044






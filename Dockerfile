FROM ubuntu:20.04
WORKDIR /linux-performance
EXPOSE 8080
RUN apt-get update && apt-get install -y bash && apt install curl -y
COPY ./linuxhealth.sh /linux-performance
RUN chmod +x /linux-performance/linuxhealth.sh
CMD ["./linuxhealth.sh"]

FROM debian:testing
MAINTAINER Johan Hidding <j.hidding@esciencecenter.nl>

RUN apt-get update && \
    apt-get install -y --no-install-recommends git python3.5 python3-numpy \
    python3-scipy ca-certificates python3-setuptools openssh-server \
    openssh-sftp-server slurmd slurm-client slurm-wlm

RUN cd /tmp && \
    git clone https://github.com/NLeSC/noodles.git && \
    cd noodles && \
    git checkout devel && \
    python3.5 setup.py install

EXPOSE 22

RUN mkdir /var/run/sshd

RUN useradd -ms /bin/bash -p $(openssl passwd sixpack) joe

USER joe
RUN mkdir /home/joe/.ssh
ADD id_rsa.pub /home/joe/.ssh/authorized_keys

USER root

ADD slurm.conf /etc/slurm-llnl
RUN mkdir /var/run/slurm-llnl

ADD welcome.txt /etc/motd
ADD start.sh /usr/bin
RUN chmod +x /usr/bin/start.sh

CMD ["/usr/bin/start.sh"]

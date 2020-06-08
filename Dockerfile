FROM daocloud.io/centos:7

# Install Python 3.6 在进行安装时，使用&&连接多行的原因时：减少镜像层数量，压缩镜像体积
RUN yum -y install https://centos7.iuscommunity.org/ius-release.rpm \
    && yum -y install python36u \
    && yum -y install python36u-pip \
    && yum -y install python36u-devel \
    # clean up cache
    && yum -y clean all \
    && mkdir -p /app/log

#定义时区参数
ENV TZ=Asia/Shanghai
#设置时区
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo '$TZ' > /etc/timezone
#设置编码
ENV LANG en_US.UTF-8

# App home
WORKDIR /app
ADD main.py /app/
ADD requirements.txt /app/
RUN pip3 install --user -r requirements.txt -i http://mirrors.aliyun.com/pypi/simple/ --trusted-host mirrors.aliyun.com
CMD ["python3", "/app/main.py"]

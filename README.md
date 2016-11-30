#金山云oss上传工具 Python版


##安装

安装python2.7.12

对于windows，假定安装在C:/Python27 (windows的python2.7自带了pip)

安装金山云的sdk

    git clone https://github.com/ks3sdk/ks3-python-sdk.git
    cd ks3-python-sdk
    C:\Python27\python.exe setup.py install

安装six(ks3-python-sdk的依赖包)

    C:\Python27\Scripts\pip.exe install six



##配置
执行该脚本时需要设置如下环境变量:

    KS3_ACCESS_KEY            金山云的access_key
    KS3_ACCESS_SECRET         金山云的access_secret
    KS3_REGION                对应region的域名
    
    关于region域名，详见文档: https://ks3.ksyun.com/doc/api/index.html
    比如： 上海外网 ks3-cn-shanghai.ksyun.com， 内网 ks3-cn-shanghai-internal.ksyun.com


##执行

    C:\Python27\python.exe ks3_oss.py <你要上传的文件或目录> <上传的目标bucket>
    
    如果是目录，该脚本会自动遍历目录下的文件，按照从该目录的basename开始的相对路径在oss上创建对应的目录结构
    
    比如 上传  E:\workspace\mytest\upload 这个目录， 在oss上就会创建 upload这个目录
    
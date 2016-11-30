# coding=utf8
import os
import sys
import hashlib
from ks3.connection import Connection


class OSS(object):
    def __init__(self, ak, sk, region):
        self.c = Connection(ak, sk, host=region)
        self.buckets = self.c.get_all_buckets()

    def print_all_buckets(self):
        for b in self.buckets:
            print(b.name)


    def print_key_name(self, bucket_name):
        b = self.c.get_bucket(bucket_name)
        for k in b.list():
            print(k.name)

    def create_bucket(self):
        raise NotImplementedError

    def get_md5(self, filename):
        with open(filename, 'rb') as f:
            md5 = hashlib.md5()
            md5.update(f.read())
        #return (md5.digest(), md5.digest().encode('base64')[:-1])
        return md5

    def upload(self, pathname, bucket_name, policy="public-read"):
        """upload file or dir to specified bucket"""
        b = self.c.get_bucket(bucket_name)
        if os.path.isfile(pathname):
            key_name = os.path.basename(pathname)
            k = b.new_key(key_name)
            md5 = self.get_md5(pathname)
            print(pathname)
            print(key_name)
            k.set_contents_from_filename(pathname, policy=policy,
                                         md5=(md5.digest(), md5.digest().encode('base64')[:-1]))
        elif os.path.isdir(pathname):
            basename = os.path.basename(pathname)
            print(basename)
            for root, dirs, files in os.walk(pathname):
                for f in files:
                    filename = os.path.join(root, f)
                    key_name = "%s/%s" % (basename, filename.replace(pathname, "").replace(os.path.sep, '/').lstrip('/'))

                    k = b.new_key(key_name)
                    md5 = self.get_md5(filename)
                    print(filename)
                    print(key_name)
                    k.set_contents_from_filename(filename, policy=policy,  md5=(md5.digest(), md5.digest().encode('base64')[:-1]))

def usage():
    print("""usage: python ks3_oss.py <path_to_be_uploaded> <bucket>""")

if __name__ == "__main__":
    ak = os.getenv('KS3_ACCESS_KEY', "")
    sk = os.getenv('KS3_ACCESS_SECRET', "")
    region = os.getenv('KS3_REGION', "")

    if not ak or not sk:
        print('KS3_ACCESS_KEY or KS3_ACCESS_SECRET empty, please set them in environment')
        sys.exit(1)
    if not region:
        print('region empty, please set them in environment, see detail in https://ks3.ksyun.com/doc/api/index.html')
        sys.exit(1)

    if len(sys.argv) < 3:
        usage()
        sys.exit(1)

    target_path = sys.argv[1]
    bucket = sys.argv[2]

    if not os.path.exists(target_path):
        print("%s not exists" % target_path)
        sys.exit(1)

    oss = OSS(ak, sk, region)
    oss.upload(target_path, bucket)
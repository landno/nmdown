#!/usr/bin/env python
# -*- coding: utf-8 -*-

from hashlib import md5
from base64 import b64encode


def make_hash(dfsid):
    '''
    计算下载地址的 hash 部分

    代码精简优化版
    '''

    key = '3go8&$8*3*3h0k(2)2'
    key_codes = map(ord, list(key))
    fid_codes = map(ord, list(str(dfsid)))

    hash_codes = []
    for i in xrange(len(fid_codes)):
        hash_code = (fid_codes[i] ^ key_codes[i % len(key)]) & 0xFF
        hash_codes.append(hash_code)

    string = ''.join(map(chr, hash_codes))
    md5_digest = md5(string).digest()
    base64_encoded = b64encode(md5_digest)
    unescape_symbol = base64_encoded.replace('+', '-').replace('/', '_')
    return unescape_symbol


def make_hash_details(dfsid):
    '''
    计算下载地址的 hash 部分
    根据 smali 字节码直接翻译版，详细版

    破解自 apk 版本 CloudMusic_official_1.4.0_3.apk
    此文件 md5 为 dc3d698721c296ca82845d2cce75db3c 使用 apktool 反汇编
    关键代码在 /smali/com/netease/cloudmusic/utils/ak.smali 第 4249 行的函数
    .method public static final b(Ljava/lang/String;)Ljava/lang/String;
    '''

    # 4249 .method public static final b(Ljava/lang/String;)Ljava/lang/String;
    # 4250     .locals 7
    # 4251
    # 寄存器 p0 就是函数实参，即文件名部分
    p0 = str(dfsid)

    # 4252     const/4 v0, 0x0
    # 4253
    v0 = 0

    # 4254     const-string v2, "3go8&$8*3*3h0k(2)2"
    # 4255
    # 这似乎就是一个密钥
    v2 = '3go8&$8*3*3h0k(2)2'

    # 4256     :try_start_0
    # 4257     const-string v1, "ISO_8859_1"
    # 4258
    # 4259     invoke-virtual {v2, v1}, Ljava/lang/String;->getBytes(Ljava/lang/String;)[B
    # 4260
    # 4261     move-result-object v3
    # 4262
    # 取得密钥以 ISO_8859_1 字符集表示的 byte 数组
    v3 = map(ord, list(v2))

    # 4263     const-string v1, "ISO_8859_1"
    # 4264
    # 4265     invoke-virtual {p0, v1}, Ljava/lang/String;->getBytes(Ljava/lang/String;)[B
    # 4266
    # 4267     move-result-object v4
    # 4268
    # 同上，不过使用的是文件名
    v4 = map(ord, list(p0))

    # 4269     move v1, v0
    # 4270
    v1 = v0

    while True:

        # 4271     :goto_0
        # 4272     array-length v5, v4
        # 4273
        v5 = len(v4)

        # 4274     if-ge v1, v5, :cond_0
        # 4275
        if v1 >= v5:
            break

        # 4276     aget-byte v5, v4, v1
        # 4277
        v5 = v4[v1]

        # 4278     invoke-virtual {v2}, Ljava/lang/String;->length()I
        # 4279
        # 4280     move-result v6
        # 4281
        v6 = len(v2)

        # 4282     rem-int v6, v1, v6
        # 4283
        v6 = v1 % v6

        # 4284     aget-byte v6, v3, v6
        # 4285
        v6 = v3[v6]

        # 4286     xor-int/2addr v5, v6
        # 4287
        v5 = v5 ^ v6

        # 4288     int-to-byte v5, v5
        # 4289
        v5 = v5 & 0xFF

        # 4290     aput-byte v5, v4, v1
        # 4291
        v4[v1] = v5

        # 4292     add-int/lit8 v1, v1, 0x1
        # 4293
        v1 = v1 + 0x1

        # 4294     goto :goto_0
        # 4295
        # 对应此次 while 语句

    # 4296     :cond_0
    # 对应上面的 while 的 break 语句

    # 余下代码，目测是计算 v4 的 md5，然后再用 base64 编码
    string = ''.join(map(chr, v4))
    md5_digest = md5(string).digest()
    base64_encoded = b64encode(md5_digest)

    # 一些符号要转义
    unescape_symbol = base64_encoded.replace('+', '-').replace('/', '_')

    # 最终结果
    return unescape_symbol

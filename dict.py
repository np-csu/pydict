#!/usr/bin/env python
#encoding=utf-8

import urllib2
import sys, getopt
import json

from termcolor import colored

URL = "http://fanyi.youdao.com/openapi.do?keyfrom=sasfasdfasf&key=1177596287&type=data&doctype=json&version=1.1&q="

def showResult(result):
    if "basic" not in result.keys():
        print colored("未找到您查询的单词:" , 'yellow'),
        print colored(result["query"], 'red')
        print
        return
    else:
        print
        print colored('\t\t\t' + result["query"], 'green')
        print
        if "us-phonetic" in result["basic"] and "uk-phonetic" in result["basic"]:
            print '\t', "美音音标:", "[" + result["basic"]["us-phonetic"] + "]", "\t英音音标:", "[" + result["basic"]["uk-phonetic"] + "]"
            print
        print '\t', "基本释义:"
        for explain in result["basic"]["explains"]:
            print '\t\t' + explain
        print
        print '\t', "网络释义:"
        for webExp in result["web"]:
            print '\t\t%-20s' %  webExp["key"],
            #if len(webExp["key"]) == len(result["query"]):
            #       print '\t',
            for value in webExp["value"]:
                print value + ';',
            print
        print

def getResult(word):
    try:
        return urllib2.urlopen(URL + word)
    except urllib2.URLError as e:
        print "错误: 向服务器发送查询请求未成功，请检查网络"
        print
        sys.exit()

def parseJson(resp):
    return json.loads(resp.read())

def usage():
    print '''
使用说明: 
    dict [需要查询的单词]
    使用dict -h获得帮助
    '''

def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "h")
        for op, value in opts:
            if op == "-h":
                usage()
                sys.exit()
        if len(args) == 0:
            usage()
            sys.exit()
    except getopt.GetoptError as e:
        print "错误: 使用了无效的参数-%s" % e.opt
        usage()
        sys.exit()
    resp = getResult(" ".join(args).lower())
    result = parseJson(resp)
    showResult(result)

if __name__ == '__main__':
    main()

#!/usr/bin/env python

import os
import re
import subprocess
import sys

"""
1. parse basic YAML grammars
2. fail if there are space/tab lines
3. fail if spaces in any Key
"""

yamlList = []
grammarGood = True
spaceLine = True
spaceKey = True

def findYAMLs(yamlPath):
    global yamlList
    if not os.path.exists(yamlPath):
        print "yaml file path %s is not existing." % yamlPath
        return 1

    tmpFiles = os.listdir(yamlPath)
    for file in tmpFiles:
        if file.split('.')[-1] == "yaml":
            yamlList.append(file)
    if len(yamlList)==0:
        print "no yaml files found under dir %s." % yamlPath
        return 1

    return 0

def parseYAML(pList):
    global grammarGood
    for file in pList:
        f = open(sys.argv[1] + file, "r")
        try:
            yaml.load(f)
        except Exception as e:
            print e
            print file + " yaml grammar illegal."
            grammarGood = False
        else:
            print file + " grammar is OK."
        finally:
            f.close()

def parseSpaceTabLine(pList):
    global spaceLine
    for file in pList:
        f = open(sys.argv[1] + file, "r")
        line = True
        i = 0
        while line:
            i += 1
            line = f.readline()
            tmp = line.strip("\r").strip("\n")
            # line starts with [ \t\f\v] and ends with [ \t\f\v], do not care \r\n because they are legal
            if re.match('^[ \t\f\v]*[ \t\f\v]$', tmp):
                print "There is space/tab line in file %s at line %d, please remove it." % (file, i)
                spaceLine = False
        f.close()

    if spaceLine:
        print "There is no space/tab line in YAML files, --OK"

def unwindDict(file, pDict):
    global spaceKey
    if not isinstance(pDict, dict):
        return
    for k,v in pDict.iteritems():
        if re.search('\s', k):
            print "There are space characters in %s YAML key, please check this: %s" % (file, k)
            spaceKey = False
        unwindDict(file, v)

def parseKeys(pList):
    global spaceKey
    for file in pList:
        f = open(sys.argv[1] + file, "r")
        try:
            dict = yaml.load(f)
            unwindDict(file, dict)
        except Exception as e:
            print e
            spaceKey= False
        else:
            pass
        finally:
            f.close()

    if spaceKey:
        print "There is no space/tab in YAML keys, --OK"

def main():
    global grammarGood, spaceLine, spaceKey
    if findYAMLs(sys.argv[1])!=0:
        return 1
    parseYAML(yamlList)
    parseSpaceTabLine(yamlList)
    parseKeys(yamlList)
    if grammarGood and spaceLine and spaceKey:
        return 0
    else:
        return 1

if __name__ == "__main__":
    sys.exit( main( ) )

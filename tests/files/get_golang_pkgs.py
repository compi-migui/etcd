#!/usr/bin/python
import logging
import re
import yum
from optparse import OptionParser


def get_pkg_name(req_line, rpm_list):
    kws = re.split("[() /]", req_line.strip())[2:5]
    kws.reverse()
    compare_str = "devel"
    tmp_list = rpm_list
    for kw in kws:
        tmp_list = [_ for _ in tmp_list if re.findall("%s" % compare_str, _)]
        if len(tmp_list) > 1:
            compare_str = "%s-%s" % (kw, compare_str)
        else:
            break

    if not tmp_list:
        if kws[-1] == "github.com":
            compare_str = "github-.*-%s-devel" % kws[0]
            tmp_list = [_ for _ in rpm_list if re.findall("%s" % compare_str, _)]
        if kws[-1] == "golang.org":
            compare_str = "golangorg-%s-devel" % kws[0]
            tmp_list = [_ for _ in rpm_list if re.findall("%s" % compare_str, _)]
        if kws[-1] == "google.golang.org":
            compare_str = "-%s-.*-devel" % kws[1]
            tmp_list = [_ for _ in rpm_list if re.findall("%s" % compare_str, _)]


    return tmp_list


if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option("-f", "--spec_file", dest="sfile",
                       default="")
    
    (options, args) = parser.parse_args()
    sfile = options.sfile

    yb = yum.YumBase()
    yum_list = yb.doPackageLists()
    alist = sorted(yum_list.available)
    source_rpms = [_.name for _ in alist if re.match("golang", _.name)]

    install_pkgs = []
    with open(sfile) as f:
        for line in f:
            install_pkgs += get_pkg_name(line, source_rpms)
    for pkg in set(install_pkgs):
        print pkg

#!/usr/bin/python
# -*- coding: utf-8 -*-
import json
import csv

if __name__ == "__main__":

    with open('output/output.json', 'r') as f:
        f_obj = json.load(f)

    keys = sorted([int(i) for i in f_obj])
    lst_childrens_all = []

    for key in keys:
        # key - регион
        # lst_x - список всех детей по региону
        lst_x = f_obj.get(str(key))

        if len(lst_x) < 2:
            continue
        else:
            for children in lst_x:
                lst_childrens_all.append(children)

    lst_clear = []

    for item in lst_childrens_all:
        for k, v in item.items():
            lst_clear.append([*item, *v.values()])

    with open('output/output.csv', "w", newline='') as csv_file:
        writer = csv.writer(csv_file, delimiter=',')

        for line in lst_clear:
            writer.writerow(line)

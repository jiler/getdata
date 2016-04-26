#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'lenovo'



def keywords_judge(search_engine_title,keywords):
    related_flag = 1
    must_key_flag = 1
    #循环每个必要的关键字
    try:
        for must_key in keywords:
            if must_key_flag == 0:
                break
            must_key_flag = 0
            #切分必要的关键字
            same_mean_keys = must_key.split()
            #循环切分好的关键字
            for key in same_mean_keys:
                if search_engine_title.find(key) != -1:
                    must_key_flag = 1
                    break


        if must_key_flag == 0:
            related_flag = 0
    except Exception,e:
        print e

    return related_flag
#!/usr/bin/env python3
"""pymongo function"""
import pymongo


def list_all(mongo_collection):
    """ list all collection """
    if mongo_collection == None:
        return []
    return list(mongo_collection.find())

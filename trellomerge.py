#!/usr/bin/env python
# -*- coding: utf-8 -*-

# import json
import sys
# from collections import OrderedDict
import argparse
import os
from dao.trellodao import TrelloBoardDAO

conf = {}


def listexists(listname, lists):
    res = None
    for l in lists:
        if l['name'] == listname:
            res = l
            break
    return res


def cardexists(card, cardlist, prefix):
    res = None
    for c in cardlist:
        if c['name'] == ''.join([prefix, card['name']]):
            res = c
            break
    return res


def main():

    slavedao = TrelloBoardDAO(conf['appkey'], conf['token'], conf['slaveboard'])
    masterdao = TrelloBoardDAO(conf['appkey'], conf['token'], conf['masterboard'])
    prefix = '[kr]'

    # get master lists
    masterlists = masterdao.getLists()

    # create (or reopen) list in slave if not exists
    slavelists = slavedao.getLists()

    # cards that have been synced while computing masterlist
    syncslavecards = []

    # for each master list
    for ml in masterlists:
        print "\n---------------------------------------"
        print "compute master list:", ml['name']
        print "---------------------------------------"

        # if list exists in slave ?
        slavelist = listexists(ml['name'], slavelists)
        if slavelist is not None:
            print "* ", ml['name'], " exists in slaveboard"

            # if it's not open
            if slavelist['closed']:
                print "* ", ml['name'], " is closed in slaveboard"
                # open it
                slavedao.openList(slavelist['id'])
                print "* ", ml['name'], " is now open in slaveboard"
        else:
            print "* ", ml['name'], " does not exists in slaveboard"
            # else create it
            slavelist = slavedao.createList(ml['name'])
            print "* ", ml['name'], " is now created in slaveboard"

        # for each open card in master list
        mastercards = masterdao.getOpenCards(ml['id'])
        slavecards = slavedao.getOpenCards(slavelist['id'])
        for mc in mastercards:
            print "** compute master card:", mc['name'], "**"

            # if not exists in slave
            sc = cardexists(mc, slavecards, prefix)
            if sc is None:
                print "** ", mc['name'], "does not exist in slave board"

                # create it
                sc = slavedao.copyCardToList(mc['id'], slavelist['id'], prefix)
                print "** ", mc['name'], "is now created in slave board"
            # if exists in slave
            else:
                print "** ", mc['name'], "exists in slave board"
                # compare last modification date
                # if master fresher than slave
                if mc['dateLastActivity'] > sc['dateLastActivity']:
                    print "** ", mc['name'], "needs to be refresh from master"

                    # delete slave card
                    slavedao.deleteCard(sc['id'])
                    print "** ", mc['name'], "has been deleted"
                    # recreate it
                    sc = slavedao.copyCardToList(mc['id'], slavelist['id'], prefix)
                    print "** ", mc['name'], "has been recreated"

            syncslavecards.append(sc['id'])

    print "******** sync ok: ", str(syncslavecards)

    # For each slave list remove master synced close cards
    slavelists = slavedao.getLists()
    for sl in slavelists:
        print "\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
        print "compute slave list:", sl['name']
        print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
        slavecards = slavedao.getOpenCards(sl['id'])
        for sc in slavecards:
            if sc['name'].startswith(prefix):
                print "* created from master:", sc['name']
                if sc['id'] not in syncslavecards:
                    print "* no longer exists in master:", sc['name'], sc['id']
                    slavedao.deleteCard(sc['id'])
                    print "* ", sc['name'], "has been deleted"

        # reordrer cards
        print "* reorder cards:", sl['name']
        priority = ['green', 'yellow', 'orange', 'red']
        ignorelist = []
        toreorder = [sc for sc in slavecards if sc['labels'] != []]
        for p in priority:
            for sc in toreorder:
                colors = sc['labels']
                colorpresence = None
                colorpresence = [label for label in colors if label['color'] == p]
                if colorpresence != []:
                    print "** ", sc['name'], " has a label ", p
                    if sc['id'] not in ignorelist:
                        slavedao.moveCard(sc['id'], 'top')
                        print "** ", sc['name'], " moved to top ", p
                        ignorelist.append(sc['id'])


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=("synchronize 2 trello boards "))
    parser.add_argument('conf', help='configuration file', type=str)
    args = parser.parse_args()
    shouldquit = False

    if not os.path.exists(args.conf):
        shouldquit = True
        print "configuration file  does not exist:" + args.conf

    if shouldquit:
        sys.exit(1)

    execfile(args.conf, conf)
    main()

# -*- coding: utf-8 -*-


class TrelloUtils(object):

    _dao = None

    def __init__(self, trello_dao):
        self._dao = trello_dao

    def reorderListByPriority(self, listid, labels_order_by_priority_asc):

        cards = self._dao.getOpenCards(listid)
        ignorelist = []
        toreorder = [sc for sc in cards if sc['labels'] != []]
        for p in labels_order_by_priority_asc:
            for sc in toreorder:
                colors = sc['labels']
                colorpresence = None
                colorpresence = [label for label in colors if label['color'] == p]
                if colorpresence != []:
                    print "** ", sc['name'], " has a label ", p
                    if sc['id'] not in ignorelist:
                        self._dao.moveCard(sc['id'], 'top')
                        print "** ", sc['name'], " moved to top ", p
                        ignorelist.append(sc['id'])

    def reorderListByDueDate(self, listid):
        cards = self._dao.getOpenCards(listid)
        toreorder = [sc for sc in cards if sc['due'] != 'null']
        neworder = sorted(toreorder, key=lambda x: x['due'], reverse=True)
        for c in neworder:
            print "** ", c['name'], " has a due date ", c['due']
            self._dao.moveCard(c['id'], 'top')
            print "** ", c['name'], " moved to top "

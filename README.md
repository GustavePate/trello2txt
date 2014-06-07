TOC
=========

* [Trellomerge: synchronize your trello boards](#Trellomerge) "Trello merge synchronize boards")
* [Trello2txt: dump your boards to text](#Trello2txt) "Trello merge synchronize boards")



Trello2txt
==========

Fetch trello cards from a board and output their text in stdout. Notable use case: use it with conky !

## Context

While improving my workflow, I was searching to have my trello tasks quickly accessible.
Then I lokk at my conky dashboard ;)
All I needed was a trello2txt tool. Here it is !

## Requirements

trello2txt use standard libray python module and the request module

On debian/ubuntu:

    sudo apt-get install python-requests

or

    [sudo] pip install requests

## Installation

First

    git clone https://github.com/GustavePate/trello2txt

Then

    vim /path/to/trello2txt/conf.py

Change the configuration, you will need:
- a trello api developper key [here](https://trello.com/docs/).
- a trello api developper token [here](https://trello.com/docs/).
- your board id (see the url in your webbrowser when you're connected to trello)
- the name of the lists you wan't to dump to text

Adjust the filters to your needs (by default only cards with orange and red labels will be display)

Then just run:

    python /path/to/trello2txt/trello2txt.py /path/to/trello2txt/conf.py -s

or to create a local file:

    python /path/to/trello2txt/trello2txt.py /path/to/trello2txt/conf.py -s -d /tmp/trello.txt

Enjoy !

## Use it with conky

First make sure you completed the installation section !

There is a conky template to display your trello list on your desktop.
Edit it first, you'll have to change the path to the trello2txt.py, conf.py and to the stored todolist file.

>I'm currently not happy with it's line by line implementation. I'll be glad if you send me an improvement !

Then:

    conky -d -c /path/to/trello2txt/trelloconkyrc

Wait up to 10 minutes to ensure the list is updated.

Tada !

A screenshot of my desktop with trello2txt/conky:

![screenshot of conky and trello2txt](https://raw.github.com/GustavePate/trello2txt/master/pics/trello+conky.png "Conky + Trello screenshot")


Trellomerge
===========

Trellomerge allows you to define a master and a slave board.
The slave board will be updated with the master cards and lists while keeping its own cards and lists.
Cards coming from the master board are prefixed in the slave board.

Use crontab to keep your trello boards synchronized.

*usage:*

    python /path/to/trello2txt/trellomerge.py /path/to/trello2txt/conf.py

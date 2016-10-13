============
Installation
============

Since there is no stable release yet, the only option is to install the project
from the source.

Development version from the source
-----------------------------------

Installation of latest dev version from the source code::

    $ git clone https://github.com/Tendrl/bridge_common.git
    $ cd bridge_common
    $ mkvirtualenv bridge_common
    $ pip install .

Note that we use virtualenvwrapper_ here to create and activate `python virtual
enviroment`_, where we install the *bridge common* via pip.

.. _virtualenvwrapper: https://virtualenvwrapper.readthedocs.io/en/latest/
.. _`python virtual enviroment`: https://virtualenv.pypa.io/en/stable/

And finally, create and edit config file as required::

    $ cp etc/tendrl/tendrl.conf.sample /etc/tendrl/tendrl.conf

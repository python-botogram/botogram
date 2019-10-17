.. Copyright (c) 2015-2019 The Botogram Authors (see AUTHORS)
   Documentation released under the MIT license (see LICENSE)

.. _install:

========================
Installazione di botogram
========================

botogram è disponibile `nell'indice dei pacchetti di Python`_, quindi puoi
installarlo facilmente con il comando `pip`. Prima di installarlo, assicurati
di avere Python_ 3.4 (o una versione più nuova), pip_, virtualenv_ e setuptools_
installati sul tuo sistema. Poi, esegui il seguente comando::

   $ python3 -m pip install botogram2

perfetto, botogram è ora installato! Ora, puoi seguire il
":ref:`tutorial`" per creare un bot ora!

.. _install-edge:

Vivi sul filo del rasoio
==================

Se non ti crea problemi avere instabilità o bugs, e vuoi le ultime funzionalità
non ancora rilasciate, puoi clonare la `repo git di botogram`_, installare
`virtualenv`_, `invoke`_ ed eseguire l'installazione da codice sorgente::

   $ git clone https://github.com/python-botogram/botogram.git
   $ cd botogram
   $ invoke install

Ricorda che ci possono essere cambiamenti e rimozioni senza nessun avviso,
fin quando la funzionalità sarà rilasciata, quindi non usare una versione
non rilasciata in ambiente di produzione.

.. _install-venvs:

Riguardo agli ambienti virtuali
==========================

Installare pacchetti Python globalmente non è una buona idea. Una gran parte
della community di Pythonn risolve questo problema con un tool chiamato virtualenv_,
che crea una piccola ed isolata installazione di Python per ogni progetto.
Ciò consente di sperimentare in un progetto senza interferire con altri. 

Per creare un ambiente virtuale, prima di tutto hai bisogno di `installare virtualenv`_.
Poi, puoi eseguire il seguente comando per creare un ambiente virtuale in ``env/``::

   $ virtualenv -p python3 env

Quindi, ora hai un ambiente virtuale con Python 3 installato. Per attivarlo
puoi eseguire il comando ``source`` dal terminale::  

   $ source env/bin/activate

Ora, tutto ciò che installerai tramite pip verrà confinato in quell'ambiente.
Ciò significa che devi etnrare nell'ambiente virtuale ogni volta che vuoi
eseguire lo script. Quando hai finito di lavorare in questo ambiente, puoi
uscire usando il comando ``deactivate``::

   $ deactivate

.. _install-troubleshooting:

Risoluzione dei problemi
===============

Potresti incontrare dei problemi mentre installi botogram. Ecco spiegato come
sistemare i più frequenti:

Permessi insufficienti - Insufficient permissions
------------------------

In alcuni sistemi linux, spesso non hai abbastanza privilegi per installare
qualcosa globalmente. In questo caso puoi chiedere al tuo amministratore
di sistema di eseguire il comando sopra, oppure puoi precedere il comando
con sudo, se sei autorizzato a farlo::

   $ sudo python3 -m pip install botogram2

Se hai deciso di installare tramite codice sorgente, devi utilizzare questo
comando al posto del precedente::

   $ sudo invoke install

.. _nell'indice dei pacchetti di Python: https://pypi.python.org/pypi/botogram
.. _pip: https://pip.pypa.io
.. _Python: https://www.python.org
.. _setuptools: https://setuptools.pypa.io
.. _repo git di botogram: https://github.com/pietroalbini/botogram
.. _virtualenv: https://virtualenv.pypa.io
.. _invoke: https://www.pyinvoke.org
.. _installare virtualenv: https://virtualenv.pypa.io/en/latest/installation.html

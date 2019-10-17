.. Copyright (c) 2015-2019 The Botogram Authors (see AUTHORS)
   Documentation released under the MIT license (see LICENSE)

.. _unavailable-chats:

==============================
Gestione delle chat non disponibili
==============================

Il tuo bot non può inviare messaggi a tutti, perchè vi sono alcune restrizioni
imposte da Telegram: non puoi inviare messaggi a persone che non hanno mai avviato
il tuo bot prima, persone che hanno bloccato il tuo bot e alcuni altri casi.

Quando provi a farlo, botogram termina la gestione dell'evento, e ti permette
di reagire: per esempio, se stai inviando un messaggio di massa agli utenti
e uno di loro ha bloccato il tuo bot, puoi rimuoverlo dalla lista dei destinatari.

.. versionadded:: 0.3

.. _unavailable-chats-reasons:

Possibili motivi per i quali una chat non è disponibile
============================================

Qui una lista dei motivi per il quale una chat può non essere disponibile
Here there is a list of the current reasons why a chat isn't available:

* **blocked**: l'utente ha bloccato il tuo bot, probabilmente perchè non
  vuole più interagirvi.

* **account_deleted**: l'utente ha eliminato il suo account, e quindi non
  potrai più scrivergli messaggi.

* **chat_moved**: la chat ha cambiato ID. Questo avviene quando un gruppo
  viene convertito a supergruppo

* **not_found**: la chat con l'ID che stai tentando di contattare non esiste!

* **kicked**: il tuo bot è stato espulso dal gruppo a cui stai tentando di scrivere. 


.. _unavailable-chats-react:

Intervieni quando una chat non è disponibile
=======================================

Fare qualcosa quando una chat non è disponibile è molto semplice in
botogram: devi solo decorare la funzione che entrerà in azione con il
decoratore :py:meth:`~botogram.Bot.chat_unavailable`:

.. code-block:: python

   @bot.chat_unavailable
   def rimuovi_utente(chat_id, reason):
       # Rimuovi l'utente dal database
       db_connection.query("DELETE FROM users WHERE id = ?", chat_id)

Ricorda che la funzione verrà chiamata anche se il messaggio è stato inviato
da un altro componente, quindi controlla se stai tenendo traccia di quell'ID
prima di eliminarlo. La funzione verrà passata con due argomenti:

* **chat_id**: l'ID della chat che non puoi contattare.

* **reason**: il motivo per il quale non puoi contattare la chat, in stringa.
  Puoi vedere la lista di tutti i possibili motivi nella  :ref:`sezione sopra
  <unavailable-chats-reasons>`.

Se stai scrivendo un componente, puoi invece chiamare il metodo 
:py:meth:`~botogram.Component.add_chat_unavailable_hook` del tuo componente:

.. code-block:: python

   class RemoveUserComponent(botogram.Component):
       component_name = "remove-user"

       def __init__(self, db):
           self.db = db
           self.add_chat_unavailable_hook(self.remove_user)

       def remove_user(self, chat_id, reason):
           """Rimuovi l'utente dal database"""
           self.db.query("DELETE FROM users WHERE id = ?", chat_id)

.. _unavailable-chats-catch:

Intercetta l'eccezione mentre si processa l'update
========================================================

Il decoratore globale :py:meth:`~botogram.Bot.chat_unavailable` è utile perchè
non devi sempre gestire chat non disponibili ogni volta che invii un messaggio.
La cosa negativa è che annulla il processo dell'update, quindi non è utilizzabile
nel caso tu stia tentando di inviare messaggi di massa a utenti multipli. 

In questi casi, puoi intercettare direttamente l'eccezione generata da botogram,
in modo da gestirla senza annullare il processo dell'update:

.. code-block:: python

   @bot.command("send")
   def invia(bot, chat, message, args):
       """Invia un messaggio ad una lista di utenti"""
       message = " ".join(args)
       users = [12345, 67890, 54321]

       for user in users:
           try:
               bot.chat(user).send(message)
           except botogram.ChatUnavailableError as e:
               print("Non posso inviare messaggi a %s (motivo: %s)" %
                     (e.chat_id, e.reason))
               users.remove(user)

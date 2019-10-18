.. Copyright (c) 2015-2019 The Botogram Authors (see AUTHORS)
   Documentation released under the MIT license (see LICENSE)

.. _bot-creation:

=========================
Creazione di un nuovo bot Telegram
=========================

Prima di iniziare a scrivere codice, dovresti creare un bot su Telegram.
In mesto modo viene riservato un username per il tuo bot, e ti verrà
restituita l'API key che serve per controllare il tuo bot. Questa pagina
ti spiegherà come fare. 

.. _bot-creation-naming:

Scelta di un buon username per il tuo bot
===================================

L'username del tuo bot è molto importante: gli utenti lo useranno per parlare
ai loro amici del tuo bot ed apparirà nei link telegram.me. Inoltre, non puoi
cambiare username senza eliminare il tuo bot, e quindi senza perdere utenti.

Gli username dei bot devono avere queste caratteristiche:

* L'username deve essere lungo almeno cinque caratteri
* L'username può contenere solo lettere, numeri e trattini bassi
* L' username deve finire con ``bot``

Per esempio, tutti gli username seguenti sono validi: ``il_mio_bot``,
``SpamBot``, ``test123bot``.

.. _bot-creation-botfather:

Creazione del bot con @botfather
==============================

Al momento, puoi solo creare un bot... con un altro bot. Con il tuo client
Telegram apero, contatta `@botfather`_, avvialo ed esegui il comando ``/newbot``.
Ti verranno fatte alcune domande sul tuo bot.

Successivamente ti verrà fornita un API key univoca, che puoi utilizzare per
comunicare con il tuo bot. **Assicurati di tenerla segreta!** Tutti coloro
con la tua API key possono prendere il pieno controllo del tuo bot, e non è
una cosa divertente.

.. _bot-creation-customization:

Personalizzazione del tuo bot
==================

Oltre a consentirti di crearlo, `@botfather`_ ti permette anche di
personalizzare il tuo bot. Per esempio, puoi cambiare la foto profilo
del tuo bot, il suo nome o la sua descrizione. Per vedere cosa puoi fare,
uilizza il comando ``/help`` su @botfather. Poi esegui il comando relativo
a cosa vuoi personalizzare.

Se vuoi usare il tuo bot per gestire un canale, probabilmente non hai bisogno
di farlo.

.. _@botfather: https://telegram.me/botfather

.. Copyright (c) 2015-2019 The Botogram Authors (see AUTHORS)
   Documentation released under the MIT license (see LICENSE)

.. _api-inline:

==========
Inline API
==========

This page contains the documentation for the APIs related to the
inline mode. See the :ref:`narrative chapter about them <inline>`
for more informations about it.


.. py:class:: botogram.InlineQuery

   This class allows you to build inline responses that are used
   to answers  inline queries.

   .. py:method:: switch_pm(text, parameter)

      Adds a button with the specified *text* above the inline results
      redirecting the user to the bot's private chat and appending the specified
      *parameter* to the /start command.

      :param str text: The text to be shown on top of the inline results.
      :param str parameter: The parameter passed to the /start command when
      the *text* is clicked.

   .. py:method:: article(title, content, [description=None, url=None, hide_url=None, thumb_url=None, hide_url=None, thumb_url=None, thumb_width=None, thumb_height=None, attach=None])

      Renders an inline article result. An inline article represents a
      generic text, a link to an article or to a web page.

      whatever is inside the *content* parameter will be sent when the user
      clicks on the result.

      The *attach* parameter allows you to attach extra things like
      :ref:`buttons <buttons>` to the message.

      :param str title: The title of the inline result.
      :param object content: The content of the message to be sent.
      :param str description: A short description of the inline result.
      :param str url: The URL of the result.
      :param bool hide_url: Pass `True`, if you don't want the URL to be shown in the inline result.
      :param str thumb_url: The URL of the thumbnail for the inline result.
      :param int thumb_width: The thumbnail width *(in pixels)*.
      :param int thumb_height: The thumbnail height *(in pixels)*.
      :param object attach: An extra thing to attach to the message.

   .. py:method:: photo([file_id=None, url=None, width=None, height=None, title=None, content=None, thumb_url=None, description=None, caption=None, syntax=None, attach=None])

      Renders an inline photo result. By default, the photo will be sent by
      the user with an optional caption. Alternatively, you can fill
      the *content* parameter to send a message with the specified content
      instead of the photo.

      You can specify the photo by passing its *file_id* or its *url*.

      The *attach* parameter allows you to attach extra things like
      :ref:`buttons <buttons>` to the message.

      :param str file_id: The Telegram *file_id* of the photo.
      :param str url: The URL of the photo.
      :param int width: The width of the photo *(in pixels)*.
      :param int height: The height of the photo *(in pixels)*.
      :param str title: The title of the inline result.
      :param object content: The content of the message to be sent *(instead of the photo)*.
      :param str thumb_url: The URL of the thumbnail for the photo.
      :param str description: A short description of the inline result.
      :param str caption: The caption of the photo to be sent, 0-1024 characters
      :param str syntax: The name of the syntax used for the caption.
      :param object attach: An extra thing to attach to the message.

   .. py:method:: audio([file_id=None, url=None, title=None,  performer=None, duration=None, content=None, caption=None, syntax=None, attach=None])

      Renders an inline audio result. By default, the audio will be sent by
      the user with the an optional caption. Alternatively, you can fill
      the *content* parameter to send a message with the specified content
      instead of the audio.

      You can specify the audio by passing its *file_id* or its *url*.
      You may optionally specify the *duration*, the *performer*
      and the *title* of the audio track.

      The *attach* parameter allows you to attach extra things like
      :ref:`buttons <buttons>` to the message.

      :param str file_id: The Telegram *file_id* of the audio.
      :param str url: The URL of the audio.
      :param str title: The title of the audio track.
      :param str performer: The name of the performer.
      :param int duration: The track duration, in seconds.
      :param object content: The content of the message to be sent *(instead of the audio)*.
      :param str caption: The caption of the audio track to be sent, 0-1024 characters
      :param str syntax: The name of the syntax used for the caption.
      :param object attach: An extra thing to attach to the message.

   .. py:method:: voice([file_id=None, url=None, title=None,  performer=None, duration=None, content=None, caption=None, syntax=None, attach=None])

      Renders an inline voice result. By default, the voice will be sent by
      the user with the an optional caption. Alternatively, you can fill
      the *content* parameter to send a message with the specified content
      instead of the voice.

      You can specify the audio by passing its *file_id* or its *url*.
      You may optionally specify the *duration*, the *performer*
      and the *title* of the audio track.

      The *attach* parameter allows you to attach extra things like
      :ref:`buttons <buttons>` to the message.

      :param str file_id: The Telegram *file_id* of the audio.
      :param str url: The URL of the audio.
      :param str title: The title of the audio track.
      :param str performer: The name of the performer.
      :param int duration: The track duration, in seconds.
      :param object content: The content of the message to be sent *(instead of the audio)*.
      :param str caption: The caption of the audio track to be sent, 0-1024 characters
      :param str syntax: The name of the syntax used for the caption.
      :param object attach: An extra thing to attach to the message.


   .. py:method:: video([file_id=None, url=None, title=None, content=None, thumb_url=None, description=None, mime_type=None, width=None, height=None, duration=None, caption=None, syntax=None, attach=None])

      Renders an inline video result. By default, the video will be sent by
      the user with an optional caption. Alternatively, you can fill
      the *content* parameter to send a message with the specified content
      instead of the video.

      You can specify the video by passing its *file_id* or an *url* pointing
      to the video file or an embedded video player (e.g. YouTube, ...).
      You **must** fill the *mime_type* parameter if you specify an *url*, and
      if *url* is an embedded video player you **must** specify the
      *content* parameter.

      The *attach* parameter allows you to attach extra things like
      :ref:`buttons <buttons>` to the message.

      :param str file_id: The Telegram *file_id* of the video.
      :param str url: The direct URL of the video or an embedded video player URL.
      :param str title: The title of the video.
      :param object content: The content of the message to be sent *(instead of the video)*.
      :param str thumb_url: The URL of the thumbnail for the video.
      :param str description: A short description of the result.
      :param str mime_type: The mime type of the content of video url, like *text/html* or *video/mp4*.
      :param str width: The video width.
      :param str height: The video height.
      :param int duration: The video duration, in seconds.
      :param str caption: The caption of the video to be sent, 0-1024 characters.
      :param str syntax: The name of the syntax used for the caption.
      :param object attach: An extra thing to attach to the message.

   .. py:method:: file([file_id=None, url=None, title=None, content=None, thumb_url=None, thumb_width=None, thumb_height=None, description=None, mime_type=None, caption=None, syntax=None, attach=None])

      Renders an inline document result. By default, the document will be
      sent by the user with an optional caption. Alternatively, you can fill
      the *content* parameter to send a message with the specified content
      instead of the file.

      You can specify the document by passing its *file_id* or its *url*.
      You **must** fill the *mime_type* parameter if you specify an *url*.
      Currently, only *.PDF* and *.ZIP* files can be sent with the *url*
      parameter.

      The *attach* parameter allows you to attach extra things like
      :ref:`buttons <buttons>` to the message.

      :param str file_id: The Telegram *file_id* of the file.
      :param str url: The URL to the file *(only for .PDF and .ZIP files)*
      :param str title: The title of the result.
      :param object content: The content of the message to be sent *(instead of the file)*.
      :param str thumb_url: The URL of the thumbnail for the file.
      :param int thumb_width: The thumbnail width *(in pixels)*.
      :param int thumb_height: The thumbnail height *(in pixels)*.
      :param str description: A short description of the result.
      :param str mime_type: The mime type of the content of the file url, either *application/pdf* or *application/zip*.
      :param int caption: The caption of the file to be sent, 0-1024 characters.
      :param str syntax: The name of the syntax used for the caption.
      :param object attach: An extra thing ot attach to the message.

   .. py:method:: location(latitude, longitude, title, [live_period=None, content=None, thumb_url=None, thumb_width=None, thumb_height=None, attach=None])

      Renders an inline location result. By default, the location will be sent
      by the user. Alternatively, you can fill the *content* parameter to send
      a message with the specified content instead of the location.

      The *live_period* parameter is for defining if this location must be a
      live location and needs to be updated over time. Leave to `None`
      if it is not or set it as a number between 60 and 86400 (seconds) if it is.

      The *attach* parameter allows you to attach extra things like
      :ref:`buttons <buttons>` to the message.

      :param float latitude: The latitude of the location.
      :param float longitude: The longitude of the location.
      :param str title: The title of the location.
      :param int live_period: The duration of the live location *(in seconds)*.
      :param object content: The content of the message to be sent *(instead of the location)*.
      :param str thumb_url: The URL of the thumbnail for the location.
      :param int thumb_width: The thumbnail width *(in pixels)*.
      :param int thumb_height: The thumbnail height *(in pixels)*.
      :param object attach: An extra thing ot attach to the message.

   .. py:method:: venue(latitude, longitude, title, address, [foursquare_id=None, foursquare_type=None, content=None, thumb_url=None, thumb_width=None, thumb_height=None, attach=None])

      Renders an inline venue result. By default, the venue will be sent
      by the user. Alternatively, you can fill the *content* parameter to send
      a message with the specified content instead of the venue.

      The *attach* parameter allows you to attach extra things like
      :ref:`buttons <buttons>` to the message.

      :param float latitude: The latitude of the location.
      :param float longitude: The longitude of the location.
      :param str title: The title of the venue.
      :param str address: The address of the venue.
      :param str foursquare_id: The foursquare ID of the venue.
      :param str foursquare_type: The foursquare type of the venue, if known.
      :param object content: The content of the message to be sent *(instead of the venue)*.
      :param str thumb_url: The URL of the thumbnail for the venue.
      :param int thumb_width: The thumbnail width *(in pixels)*.
      :param int thumb_height: The thumbnail height *(in pixels)*.
      :param object attach: An extra thing ot attach to the message.

   .. py:method:: sticker(file_id, [content=None, attach=None])

      Renders an inline sticker result. By default, the sticker will be sent
      by the user. Alternatively, you can fill the *content* parameter to send
      a message with the specified content instead of the sticker.

      The *attach* parameter allows you to attach extra things like
      :ref:`buttons <buttons>` to the message.

      :param str file_id: The Telegram *file_id* of the sticker.
      :param object content: The content of the message to be sent *(instead of the sticker)*.
      :param object attach: An extra thing ot attach to the message.

   .. py:method:: contact(phone, first_name, [last_name=None, vcard=None, content=None, thumb_url=None, thumb_width=None, thumb_height=None, attach=None])

      Renders an inline contact result. By default, the contact will be sent
      by the user. Alternatively, you can fill the *content* parameter to send
      a message with the specified content instead of the contact.

      The *attach* parameter allows you to attach extra things like
      :ref:`buttons <buttons>` to the message.

      :param str phone: The phone number of the contact.
      :param str first_name: The first name of the contact.
      :param str last_name: The last name of the contact.
      :param str vcard: Additional data about the contact in the form of a vCard.
      :param object content: The content of the message to be sent *(instead of the venue)*.
      :param str thumb_url: The URL of the thumbnail for the contact.
      :param int thumb_width: The thumbnail width *(in pixels)*.
      :param int thumb_height: The thumbnail height *(in pixels)*.
      :param object attach: An extra thing ot attach to the message.

   .. py:method:: gif([file_id=None, url=None, title=None, content=None, thumb_url=None, width=None, height=None, duration=None, caption=None, syntax=None, attach=None])

      Renders an inline GIF result. By default, the GIF will be sent
      by the user. Alternatively, you can fill the *content* parameter to send
      a message with the specified content instead of the GIF.

      The *attach* parameter allows you to attach extra things like
      :ref:`buttons <buttons>` to the message.

      :param str file_id: The Telegram *file_id* of the GIF.
      :param str url: The URL to the GIF.
      :param str title: The title of the result.
      :param object content: The content of the message to be sent *(instead of the GIF)*.
      :param str thumb_url: The URL of the thumbnail for the GIF.
      :param str width: The GIF width.
      :param str height: The GIF height.
      :param int duration: The GIF duration, in seconds.
      :param str caption: The caption of the GIF to be sent, 0-1024 characters.
      :param str syntax: The name of the syntax used for the caption.
      :param object attach: An extra thing to attach to the message.

   .. py:method:: mpeg4_gif([file_id=None, url=None, title=None, content=None, thumb_url=None, width=None, height=None, duration=None, caption=None, syntax=None, attach=None])

      Renders an inline video animation (H.264/MPEG-4 AVC video without sound) result.
      By default, the video animation will be sent by the user.
      Alternatively, you can fill the *content* parameter to send
      a message with the specified content instead of the animation.

      The *attach* parameter allows you to attach extra things like
      :ref:`buttons <buttons>` to the message.

      :param str file_id: The Telegram *file_id* of the animation.
      :param str url: The URL to the animation.
      :param str title: The title of the result.
      :param object content: The content of the message to be sent *(instead of the animation)*.
      :param str thumb_url: The URL of the thumbnail for the animation.
      :param str width: The animation width.
      :param str height: The animation height.
      :param int duration: The animation duration, in seconds.
      :param str caption: The caption of the animation to be sent, 0-1024 characters.
      :param str syntax: The name of the syntax used for the caption.
      :param object attach: An extra thing to attach to the message.

   .. versionadded:: 0.7


.. py:class:: botogram.InlineInputMessage

   This class allows you to build content from
   inline responses that contains a message.

   .. code-block:: python

      content = botogram.InlineInputMessage(
         text = 'This is the text of the message to be sent',
         syntax='html',
         preview = False,
      )
      yield inline.article(
         title='My inline result',
         content,
      )


   .. py:method:: __init___(text, [syntax=None, preview=None])

      Creates a instance of this class.

      :param str text: The textual messsage to be sent.
      :param str syntax: The name of the syntax used for the message.
      :param bool preview: Whether to show link previews.

   .. versionadded:: 0.7


.. py:class:: botogram.InlineInputLocation

   This class allows you to build content from
   inline responses that contains a location.

   .. code-block:: python

      content = botogram.InlineInputLocation(
         latitude=0.0,
         longitude=0.0,
      )
      yield inline.article(
         title='My inline result',
         content,
      )

   .. py:method:: __init__(latitude, longitude, [live_period=None])

      Creates an instance of this class.

      :param float latitude: The latitude of the location.
      :param float longitude: The longitude of the location.
      :param int live_period: Period in seconds for which the location can be
      updated, should be between 60 and 86400.

   .. versionadded:: 0.7


.. py:class:: botogram.InlineInputVenue

   This class allows you to build content from
   inline responses that contains a venue.

   .. code-block:: python

      content = botogram.InlineInputVenue(
         latitude=0.0,
         longitude=0.0,
         title='The Abyss',
         address='Atlantic Ocean',
      )
      yield inline.article(
         title='My inline result',
         content,
      )

   .. py:method:: __init__(latitude, longitude, title, address, [foursquare_id=None, foursquare_type=None])

      Creates an instance of this class.

      :param float latitude: The latitude of the venue.
      :param float longitude: The longitude of the venue.
      :param str title: The name of the venue.
      :param str address: The address of the venue.
      :param str foursquare_id: The Foursquare ID of the venue
      :param str foursquare_type: The Foursquare type of the venue, if known.

   .. versionadded:: 0.7


.. py:class:: botogram.InlineInputContact

   This class allows you to build content from
   inline responses that contains a contact.

   .. code-block:: python

      content = botogram.InlineInputContact(
         phone='390124567890',
         first_name='Support',
      )
      yield inline.article(
         title='My inline result',
         content,
      )

   .. py:method:: __init__(phone, first_name, [last_name=None, vcard=None])

      Creates an instance of this class.

      :param str phone: The phone number of the contact.
      :param str first_name: The first name of the contact.
      :param str last_name: The last name of the contact.
      :param str vcard: Additional data about the contact in the form of a vCard.

   .. versionadded:: 0.7

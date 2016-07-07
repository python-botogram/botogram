"""
    botogram.utils.startup
    Utilities for starting up botogram

    Copyright (c) 2015-2016 Pietro Albini <pietro@pietroalbini.io>
    Released under the MIT license
"""

import os
import sys
import gettext

import pkg_resources
import logbook


# This small piece of global state will track if logbook was configured
_logger_configured = False


def get_language(lang):
    """Get the GNUTranslations instance of a specific language"""
    path = pkg_resources.resource_filename("botogram", "i18n/%s.mo" % lang)
    if not os.path.exists(path):
        raise ValueError('Language "%s" is not supported by botogram' % lang)

    with open(path, "rb") as f:
        gt = gettext.GNUTranslations(f)

    return gt


def configure_logger():
    """Configure a logger object"""
    global _logger_configured

    # Don't configure the logger multiple times
    if _logger_configured:
        return

    # The StreamHandler will log everything to stdout
    min_level = 'DEBUG' if 'BOTOGRAM_DEBUG' in os.environ else 'INFO'
    handler = logbook.StreamHandler(sys.stdout, level=min_level)
    handler.format_string = '{record.time.hour:0>2}:{record.time.minute:0>2}' \
                            '.{record.time.second:0>2} - ' \
                            '{record.level_name:^9} - {record.message}'
    handler.push_application()

    # Don't reconfigure the logger, thanks
    _logger_configured = True

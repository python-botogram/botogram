# Copyright (c) 2015-2017 The Botogram Authors (see AUTHORS)
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
#   The above copyright notice and this permission notice shall be included in
#   all copies or substantial portions of the Software.
#
#   THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#   IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#   FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#   AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#   LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
#   FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
#   DEALINGS IN THE SOFTWARE.

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

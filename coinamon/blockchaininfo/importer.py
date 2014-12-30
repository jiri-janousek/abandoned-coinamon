# coding: utf-8

# Copyright 2014 Jiří Janoušek <janousek.jiri@gmail.com>
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice, this
#    list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR
# ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import json

from coinamon.core.importer import BadDataError
from coinamon.core.importer import Importer


class BlockchaininfoImporter(Importer):
    name = "blockchaininfo"
    label = "Blockchain.info Wallet"
    capabilities = (Importer.IMPORTS_CONTACTS, )

    def import_contacts(self, data, errors):
        try:
            data = json.loads(data)["address_book"]
        except (TypeError, ValueError, LookupError) as e:
            raise BadDataError(*e.args)

        try:
            for item in data:
                try:
                    addr = item["addr"]
                    label = item.get("label", addr)
                    yield {"addr": addr, "label": label}
                except (LookupError, TypeError) as e:
                    errors.append(BadDataError(
                        "{} {}, data: {}".format(e.__class__.__name__, e, item)))
        except TypeError as e:
            raise BadDataError(*e.args)

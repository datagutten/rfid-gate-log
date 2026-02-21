import re

import requests
from Sip2.sip2 import Sip2


class SipHTTP(Sip2):
    url: str
    session: requests.Session
    username: str
    password: str

    def connect(self):
        # Initialize logger on first connect
        if self.log is None:
            self._init_logger()
        self.session = requests.Session()
        self.session.headers['User-Agent'] = 'Mozilla/4.0 (compatible; Synapse)'
        self.session.headers['Content-Type'] = 'application/xml'

    def get_response(self, request):
        xml = '''<?xml version="1.0" encoding="UTF-8" ?>
<ns1:sip login="%s" password="%s" xsi:schemaLocation="http://axiell.com/Schema/sip.xsd sip.xsd" xmlns:ns1="http://axiell.com/Schema/sip.xsd" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" >
<request>%s</request>
</ns1:sip>''' % (self.username, self.password, request)

        response = self.session.post(self.url, data=xml)
        response.raise_for_status()
        matches = re.search(r'<response>(.+)</response>', response.text)
        return matches.group(1)

    def sip_login_request(self, loginUserId, loginPassword):
        """ Generate login (code 93) request messages in sip2 format
        @param  string loginUserId     login value for the CN field
        @param  string loginPassword   password value for the CO field
        @return string                 SIP2 request message

        @note SIP2 Protocol definition document:
        This message can be used to login to an ACS server program. The ACS
        should respond with the Login Response message. Whether to use this
        message or to use some other mechanism to login to the ACS is
        configurable on the SC. When this message is used, it will be the first
        message sent to the ACS.
            93<UID algorithm><PWD algorithm><login user id><login password><location code>
        """
        self._request_new('93')
        self._request_addOpt_fixed(self.UIDalgorithm, 1)
        self._request_addOpt_fixed(self.PWDalgorithm, 1)
        self._request_addOpt_var('CN', loginUserId)
        self._request_addOpt_var('CO', loginPassword)
        # self._request_addOpt_var('CP', self.scLocation, True)

        self.username = loginUserId
        self.password = loginPassword

        return self._request_return(False, False)

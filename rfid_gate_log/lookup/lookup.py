import requests

from sip import SipHTTP


class LMSLookup:

    def __init__(self, url: str):
        self.session = requests.Session()
        self.sip = SipHTTP()
        self.sip.url = url
        self.sip.hostPort = 443
        self.sip.scLocation = None

    def sip_connect(self, username, password):
        # connect to server
        self.sip.connect()

        # Now login you SC device
        msg = self.sip.sip_login_request(username, password)
        response = self.sip.sip_login_response(self.sip.get_response(msg))

    def query(self, tag):
        msg = self.sip.sip_item_information_request(tag)
        response = self.sip.sip_item_information_response(self.sip.get_response(msg))
        return response['variable']['AJ'][0]

# -*- coding: utf-8 -*-
import base64
import json
import logging

logger = logging.getLogger("parseOntData")

class ParseOntData(object):
    """
    解析ont数据.
    """
    def __init__(self, data):
        self.data = data
        self.retDict = {}
        self.retDict['ont_kyc_data'] = data

    def parse_data(self):
        """
        """
        logger.info("ParseOntData.parse_data / begin..., data={}".format(self.data))
        jsonData = json.loads(self.data)

        self.retDict['ont_OntPassOntId'] = jsonData.get('OntPassOntId')
        self.retDict['ont_Claims'] = jsonData.get('Claims')
        self.retDict['ont_Signature'] = jsonData.get('Signature')
        self.retDict['ont_UserOntId'] = jsonData.get('UserOntId')
        logger.info("ParseOntData.parse_data/parse data..., ont_OntPassOntId={}".format(self.retDict['ont_OntPassOntId']))
        logger.info("ParseOntData.parse_data/parse data..., ont_Claims={}".format(self.retDict['ont_Claims']))
        logger.info("ParseOntData.parse_data/parse data..., ont_Signature={}".format(self.retDict['ont_Signature']))
        logger.info("ParseOntData.parse_data/parse data..., ont_UserOntId={}".format(self.retDict['ont_UserOntId']))

        self.parse_claims()
        return self.retDict


    def parse_claims(self):
        """
        """
        claims = self.retDict['ont_Claims']
        if claims is None:
            logger.error("ParseOntData.parse_claims Error / Claims is null error ! ")
            return None

        logger.info("ParseOntData.parse_claims / claims..., type={},length={}, data={}".
                format(type(claims), len(claims), claims))

        if isinstance(claims, list):
            for i, v in enumerate(claims):
                logger.info("ParseOntData.parse_claims / claim items..., i={}, v={}".format(i, v))

                claim_list = claims[i].split(".")

                # claim_list = claims[0].split(".")
                # logger.info("ParseOntData.parse_claims/claim_list..., length={}".format(len(claim_list)))
                # for i, v in enumerate(claim_list):
                #     logger.info("ParseOntData.parse_claims/claim_list_item...{}, data={}".format(i, v))
                #     logger.info("ParseOntData.parse_claims/claim_list_item...{}, base64_encode={}".format(i, base64.b64decode(v)))

                head = None
                payload = None
                signature = None
                merkleproof = None
                if len(claim_list) >= 1:
                    head = base64.b64decode(claim_list[0])
                if len(claim_list) >= 2:
                    payload = base64.b64decode(claim_list[1])
                if len(claim_list) >= 3:
                    signature = base64.b64decode(claim_list[2])
                if len(claim_list) >= 4:
                    merkleproof = base64.b64decode(claim_list[3])
                logger.info("ParseOntData.parse_claims/parse data..., payload={}".format(payload))
                logger.info("ParseOntData.parse_claims/parse data..., head={}".format(head))
                logger.info("ParseOntData.parse_claims/parse data..., signature={}".format(signature))
                logger.info("ParseOntData.parse_claims/parse data..., merkleproof={}".format(merkleproof))

                if payload:
                    self.retDict['ont_payload'] = payload

                    jsonData = json.loads(payload)
                    if jsonData['clm']:
                        if not self.retDict.get('ont_Claims_clm_IssuerName', None):
                            self.retDict['ont_Claims_clm_IssuerName'] = jsonData.get('clm').get('IssuerName')

                        if not self.retDict.get('ont_Claims_clm_Email', None):
                            self.retDict['ont_Claims_clm_Email'] = jsonData.get('clm').get('Email')

                        if not self.retDict.get('ont_Claims_clm_Country', None):
                            self.retDict['ont_Claims_clm_Country'] = jsonData.get('clm').get('Nationality')
                            if not self.retDict['ont_Claims_clm_Country']:
                                self.retDict['ont_Claims_clm_Country'] = jsonData.get('clm').get('Country')

                        if not self.retDict.get('ont_Claims_clm_PhoneNumber', None):
                            self.retDict['ont_Claims_clm_PhoneNumber'] = jsonData.get('clm').get('PhoneNumber')
                            if not self.retDict.get('ont_Claims_clm_PhoneNumber', None):
                                self.retDict['ont_Claims_clm_PhoneNumber'] = jsonData.get('clm').get('Phone')

                        if not self.retDict.get('ont_Claims_clm_DocumentType', None):
                            self.retDict['ont_Claims_clm_DocumentType'] = jsonData.get('clm').get('DocumentType')

                        if not self.retDict.get('ont_Claims_clm_Name', None):
                            self.retDict['ont_Claims_clm_Name'] = jsonData.get('clm').get('Name')

                        # add 907，身份证.
                        if not self.retDict.get('id_name', None):
                            self.retDict['id_name'] = jsonData.get('clm').get(u'姓名')
                        if not self.retDict.get('id_no', None):
                            self.retDict['id_no'] = jsonData.get('clm').get(u'身份证号')

                    if jsonData['sub']:
                        self.retDict['ont_Claims_sub'] = jsonData.get('sub')
                    if jsonData[r'@context']:
                        self.retDict['ont_Claims_context'] = jsonData.get('@context')
                    if jsonData['iat']:
                        self.retDict['ont_Claims_iat'] = jsonData.get('iat')
                    if jsonData['exp']:
                        self.retDict['ont_Claims_exp'] = jsonData.get('exp')

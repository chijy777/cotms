# -*- coding: utf-8 -*-
import base64
import json
import logging

logger = logging.getLogger("parseOntData")

class ParseOntData(object):
    """
    //可信声明
    String claim = "eyJraWQiOiJkaWQ6b250OkFScjZBcEsyNEVVN251Zk5ENHMxU1dwd1VMSEJlcnRwSmIja2V5cy0xIiwidHlwIjoiSldULVgiLCJhbGciOiJPTlQtRVMyNTYifQ==.eyJjbG0tcmV2Ijp7InR5cCI6IkF0dGVzdENvbnRyYWN0IiwiYWRkciI6IjM2YmI1YzA1M2I2YjgzOWM4ZjZiOTIzZmU4NTJmOTEyMzliOWZjY2MifSwic3ViIjoiZGlkOm9udDpBYTdCeXdDUWV6TDNHTERyTXJxMnFQNmJMZjVWV2gzYWRWIiwidmVyIjoidjEuMCIsImNsbSI6eyJJc3N1ZXJOYW1lIjoiSWRlbnRpdHlNaW5kIiwiRW1haWwiOiJubHB4X2RjQGhvdG1haWwuY29tIiwiQ291bnRyeSI6IkNOIiwiUGhvbmVOdW1iZXIiOiIrODYgMTM3OTU0MDg3NzMiLCJEb2N1bWVudFR5cGUiOiJQUCIsIk5hbWUiOiJ6aG91cWlhbmcifSwiaXNzIjoiZGlkOm9udDpBUnI2QXBLMjRFVTdudWZORDRzMVNXcHdVTEhCZXJ0cEpiIiwiZXhwIjoxNTY1NDk0Njc4LCJpYXQiOjE1MzM5NTg2NzksIkBjb250ZXh0IjoiY2xhaW06aWRtX3Bhc3Nwb3J0X2F1dGhlbnRpY2F0aW9uIiwianRpIjoiOTA5YmEwOTU5NzE1MGQyYjI3NzgzZWZkYjczY2Y0NDJlYzRjYzY4M2ViNmI5MTcxNTRmMGQ4MmZiOTdkN2ZiMCJ9.AXmwbnXmuzTIJvm1SZF4Gq5BcY2wG+2Mi+jaBYc04avt9bb7ZGSAKIf7sx8MwYXET4VGvZvDkxUnp+7bh8qNp+Q=\\\\.eyJQcm9vZiI6eyJUeXBlIjoiTWVya2xlUHJvb2YiLCJNZXJrbGVSb290IjoiMDM3MmViOGRjZGYxMzdiOTFjNTFhOTA2YjQzZDVhYWRiYzM1ZWY1Y2RhODlmYmM4YWViZTc5OTgwNjhjYmI2MSIsIlR4bkhhc2giOiIzNWQ4ZWQ0OTNiM2VkMWVmM2U2NTIzNTlkZDA1NjdiN2ZlNTg0ODljYzk5ODY1NjRkMDc0NTc4NzA2MTQ0M2M5IiwiQmxvY2tIZWlnaHQiOjEyNzgxMywiTm9kZXMiOlt7IlRhcmdldEhhc2giOiIwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwIiwiRGlyZWN0aW9uIjoiTGVmdCJ9LHsiVGFyZ2V0SGFzaCI6ImUxNDE3MmM4YTZlMTkzOTQzNDY1NjQ4ZTFjNTg2YTkxODZhMzc4NGVlN2VlMjlkYjllZGJmNmFmZTA0ZjUzOTAiLCJEaXJlY3Rpb24iOiJMZWZ0In0seyJUYXJnZXRIYXNoIjoiZGNmYWI0ZDg5YjFiMzk4ZDQ4ZjZlNDQ3MDBlMjE4MzEzZWNjOWIwOTMzMjAyZGI1MjEzOGJkMjk4ZmE5NTE5NCIsIkRpcmVjdGlvbiI6IkxlZnQifSx7IlRhcmdldEhhc2giOiJiNzg0NWEyYjFkZDBlNGFlZWU1NzdlODVjNTdiNmRlNTVmYWU5NjI5ZjkwYzM5MzBjZDYxMjRmNDJjNmFiNjY0IiwiRGlyZWN0aW9uIjoiTGVmdCJ9LHsiVGFyZ2V0SGFzaCI6IjMyMjY1NTBmOGIzZDlkNzAyZGViYjllNGZmYjczMDNhMmU5NjY5NDQwZjVmY2JlMTVhZWU2OWRlYWFjYTkwOTUiLCJEaXJlY3Rpb24iOiJMZWZ0In0seyJUYXJnZXRIYXNoIjoiNjk5YTY5N2E1MDFkNTJlNTFkOTJlNjNmZDMwOWU5MzExY2JhZDYzOWRjZjIwZGM1YzQxMGE1MmE5OGUyN2E1MiIsIkRpcmVjdGlvbiI6IkxlZnQifSx7IlRhcmdldEhhc2giOiJlNTc5ZGU4MzgxMjFlNTQ5NzcxMmQzZmM3ZGZiMTJiMWJjMDA0MWM0YjhhZWU3NWI1Zjc4NjUwN2UyMGE2YmU1IiwiRGlyZWN0aW9uIjoiTGVmdCJ9LHsiVGFyZ2V0SGFzaCI6ImM4ZmE0ZWU2MGE4NThmOTZmNzljMmQ0OGY2NGY2MTMwYzA3ZDVlNjkxZjBjZDJjYjI2ZTc2Njc1OTBjNmQ2NjkiLCJEaXJlY3Rpb24iOiJMZWZ0In0seyJUYXJnZXRIYXNoIjoiZTc3NWYxZDEzYzVhMDlkNGQyZjkxZTYwZTllYTNmMzhjMTQyNmExZDlhMWM3YWZkNTYxMzUxYjE0NGI2YTY1NCIsIkRpcmVjdGlvbiI6IkxlZnQifSx7IlRhcmdldEhhc2giOiI5YWMxZmVkZTZmNzZjYTFiMjA2NmM5MjFjNmZhMTMwOTFlN2QyMTA5MDIxYmIyYjA2MTdlYWFkODcxZWE3ZDU0IiwiRGlyZWN0aW9uIjoiTGVmdCJ9XSwiQ29udHJhY3RBZGRyIjoiMzZiYjVjMDUzYjZiODM5YzhmNmI5MjNmZTg1MmY5MTIzOWI5ZmNjYyJ9fQ==";
    String[] aa = claim.split("\\.");
    System.out.println("length:" + aa.length);
    String head = new String(Base64.getDecoder().decode(aa[0]));
    String payload = new String(Base64.getDecoder().decode(aa[1]));
    String signature = aa[2];
    String merkleproof = new String(Base64.getDecoder().decode(aa[3]));
    System.out.println("head:" + head);
    System.out.println("payload:" + payload);
    System.out.println("signature:"+signature);
    System.out.println("merkleproof:" + merkleproof);
    """
    def __init__(self, data):
        self.data = data

    def parse_data(self):
        logger.info("ParseOntData.parse_data/begin..., data={}".format(self.data))
        jsonData = json.loads(self.data)

        OntPassOntId = jsonData.get('OntPassOntId')
        Claims = jsonData.get('Claims')
        Signature = jsonData.get('Signature')
        UserOntId = jsonData.get('UserOntId')
        logger.info("ParseOntData.parse_data/parse data..., OntPassOntId={}".format(OntPassOntId))
        logger.info("ParseOntData.parse_data/parse data..., Claims={}".format(Claims))
        logger.info("ParseOntData.parse_data/parse data..., Signature={}".format(Signature))
        logger.info("ParseOntData.parse_data/parse data..., UserOntId={}".format(UserOntId))

        self.parse_claims(Claims)


    def parse_claims(self, claims):
        if claims is None:
            logger.error("ParseOntData.parse_claims Error/claim is null error ! ")
            return None

        logger.info("ParseOntData.parse_claims/claims..., type={}, data={}".format(type(claims), claims))

        if isinstance(claims, list):
            logger.info("ParseOntData.parse_claims/claims..., length={}".format(len(claims)))
            claims = claims[0]

        claim_list = claims.split("\\.")
        logger.info("ParseOntData.parse_claims/claim_list..., length={}".format(len(claim_list)))

        for i, v in enumerate(claim_list):
            print("ParseOntData.parse_claims/claim items..., i={}, v={}".format(i, v))

        head = None
        payload = None
        signature = None
        merkleproof = None
        if len(claim_list) >= 1 :
            head = base64.b64decode(claim_list[0])
        if len(claim_list) >= 2:
            payload = base64.b64decode(claim_list[1])
        if len(claim_list) >= 3:
            signature = base64.b64decode(claim_list[2])
        if len(claim_list) >= 4:
            merkleproof = base64.b64decode(claim_list[3])
        logger.info("ParseOntData.parse_claims/parse data..., head={}".format(head))
        logger.info("ParseOntData.parse_claims/parse data..., payload={}".format(payload))
        logger.info("ParseOntData.parse_claims/parse data..., signature={}".format(signature))
        logger.info("ParseOntData.parse_claims/parse data..., merkleproof={}".format(merkleproof))




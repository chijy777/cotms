import json
import logging
import tornado
import tornado.web
import tornado.httpserver
import tornado.ioloop
import tornado.options
from handler.kycItem import KycItem
from handler.parseOntData import ParseOntData
from model.ontKycLog import OntKycLog
from tornado.options import define, options

logger = logging.getLogger("kyc_server")

class IndexHandler(tornado.web.RequestHandler):
    """Use to test."""
    def get(self):
        self.write("Hello, ONT&COT KYC!")


class NotifyHandler(tornado.web.RequestHandler):
    """
    回调函数，接收证书信息.
    """
    error = {
        '101': 'Receive ont_kyc_data null!',
        '102': 'PhoneNumber is null error!'
    }
    kycItem = {}

    def post(self):
        logger.info(
            "kyc_server.notify/begin..., client_ip={}, arguments={}, body={}".
                format(self.request.remote_ip, self.request.arguments, self.request.body)
        )

        ont_data = self.request.body

        # 接收数据异常
        if ont_data is None or len(ont_data)==0:
            logger.error(
                "kyc_server.notify Error./get data is null error ! data={}".format(ont_data)
            )
            respond = {
                'Action': 'AuthConfirm', "Error": 101, "Desc": self.error['101'], "Result": 'false',
            }
            return self.write(  tornado.escape.json_encode(respond) )

        # 数据解析
        parser = ParseOntData(ont_data)
        self.kycItem = parser.parse_data()
        logger.info(
            "kyc_server.notify/parse kyc_item..., kycItem={}".format(self.kycItem)
        )

        # 数据检查.
        ret, respond = self.check_data()
        if ret != 0: # 异常.
            return self.write(tornado.escape.json_encode(respond))

        # 插入DB.
        OntKycLog.insert(
            ont_kyc_data=self.kycItem.get('ont_kyc_data'),
            ont_OntPassOntId=self.kycItem.get('ont_OntPassOntId'),
            ont_Claims=self.kycItem.get('ont_Claims'),
            ont_Signature=self.kycItem.get('ont_Signature'),
            ont_UserOntId=self.kycItem.get('ont_UserOntId'),

            ont_Claims_clm_IssuerName=self.kycItem.get('ont_Claims_clm_IssuerName'),
            ont_Claims_clm_Email=self.kycItem.get('ont_Claims_clm_Email'),
            ont_Claims_clm_Country=self.kycItem.get('ont_Claims_clm_Country'),
            ont_Claims_clm_PhoneNumber=self.kycItem.get('ont_Claims_clm_PhoneNumber'),
            ont_Claims_clm_DocumentType=self.kycItem.get('ont_Claims_clm_DocumentType'),
            ont_Claims_clm_Name=self.kycItem.get('ont_Claims_clm_Name'),

            ont_Claims_context=self.kycItem.get('ont_Claims_context'),
            ont_Claims_iat=self.kycItem.get('ont_Claims_iat'),
            ont_Claims_exp = self.kycItem.get('ont_Claims_exp'),
         )

        # 成功，返回应答.
        respond = {
            'Action' :  'AuthConfirm', "Error": 0, "Desc": "SUCCESS", "Result": 'true',
        }
        return self.write( tornado.escape.json_encode(respond) )


    def check_data(self):
        """
        检查数据.
        """
        # [手机号]异常.
        if not (self.kycItem['ont_Claims_clm_PhoneNumber'] and len(self.kycItem['ont_Claims_clm_PhoneNumber'])>0):
            respond = {
                'Action': 'AuthConfirm', "Error": 102, "Desc": self.error['102'], "Result": 'false',
            }
            return 102, respond

        return 0, None



class TestNotifyHandler(tornado.web.RequestHandler):
    """
    测试，ont数据解析.
    """
    def get(self):
        data = b'{"OntPassOntId":"did:ont:AUiPt6NWppcrRMFLA9QPUV2BHEwfeAwPUt","Claims":["eyJraWQiOiJkaWQ6b250OkFScjZBcEsyNEVVN251Zk5ENHMxU1dwd1VMSEJlcnRwSmIja2V5cy0xIiwidHlwIjoiSldULVgiLCJhbGciOiJPTlQtRVMyNTYifQ==.eyJjbG0tcmV2Ijp7InR5cCI6IkF0dGVzdENvbnRyYWN0IiwiYWRkciI6IjM2YmI1YzA1M2I2YjgzOWM4ZjZiOTIzZmU4NTJmOTEyMzliOWZjY2MifSwic3ViIjoiZGlkOm9udDpBYTdCeXdDUWV6TDNHTERyTXJxMnFQNmJMZjVWV2gzYWRWIiwidmVyIjoidjEuMCIsImNsbSI6eyJJc3N1ZXJOYW1lIjoiSWRlbnRpdHlNaW5kIiwiRW1haWwiOiJubHB4X2RjQGhvdG1haWwuY29tIiwiQ291bnRyeSI6IkNOIiwiUGhvbmVOdW1iZXIiOiIrODYgMTM3OTU0MDg3NzMiLCJEb2N1bWVudFR5cGUiOiJQUCIsIk5hbWUiOiJ6aG91cWlhbmcifSwiaXNzIjoiZGlkOm9udDpBUnI2QXBLMjRFVTdudWZORDRzMVNXcHdVTEhCZXJ0cEpiIiwiZXhwIjoxNTY1NDk0Njc4LCJpYXQiOjE1MzM5NTg2NzksIkBjb250ZXh0IjoiY2xhaW06aWRtX3Bhc3Nwb3J0X2F1dGhlbnRpY2F0aW9uIiwianRpIjoiOTA5YmEwOTU5NzE1MGQyYjI3NzgzZWZkYjczY2Y0NDJlYzRjYzY4M2ViNmI5MTcxNTRmMGQ4MmZiOTdkN2ZiMCJ9.AXmwbnXmuzTIJvm1SZF4Gq5BcY2wG+2Mi+jaBYc04avt9bb7ZGSAKIf7sx8MwYXET4VGvZvDkxUnp+7bh8qNp+Q=\\\\\\\\.eyJQcm9vZiI6eyJUeXBlIjoiTWVya2xlUHJvb2YiLCJNZXJrbGVSb290IjoiMDM3MmViOGRjZGYxMzdiOTFjNTFhOTA2YjQzZDVhYWRiYzM1ZWY1Y2RhODlmYmM4YWViZTc5OTgwNjhjYmI2MSIsIlR4bkhhc2giOiIzNWQ4ZWQ0OTNiM2VkMWVmM2U2NTIzNTlkZDA1NjdiN2ZlNTg0ODljYzk5ODY1NjRkMDc0NTc4NzA2MTQ0M2M5IiwiQmxvY2tIZWlnaHQiOjEyNzgxMywiTm9kZXMiOlt7IlRhcmdldEhhc2giOiIwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwIiwiRGlyZWN0aW9uIjoiTGVmdCJ9LHsiVGFyZ2V0SGFzaCI6ImUxNDE3MmM4YTZlMTkzOTQzNDY1NjQ4ZTFjNTg2YTkxODZhMzc4NGVlN2VlMjlkYjllZGJmNmFmZTA0ZjUzOTAiLCJEaXJlY3Rpb24iOiJMZWZ0In0seyJUYXJnZXRIYXNoIjoiZGNmYWI0ZDg5YjFiMzk4ZDQ4ZjZlNDQ3MDBlMjE4MzEzZWNjOWIwOTMzMjAyZGI1MjEzOGJkMjk4ZmE5NTE5NCIsIkRpcmVjdGlvbiI6IkxlZnQifSx7IlRhcmdldEhhc2giOiJiNzg0NWEyYjFkZDBlNGFlZWU1NzdlODVjNTdiNmRlNTVmYWU5NjI5ZjkwYzM5MzBjZDYxMjRmNDJjNmFiNjY0IiwiRGlyZWN0aW9uIjoiTGVmdCJ9LHsiVGFyZ2V0SGFzaCI6IjMyMjY1NTBmOGIzZDlkNzAyZGViYjllNGZmYjczMDNhMmU5NjY5NDQwZjVmY2JlMTVhZWU2OWRlYWFjYTkwOTUiLCJEaXJlY3Rpb24iOiJMZWZ0In0seyJUYXJnZXRIYXNoIjoiNjk5YTY5N2E1MDFkNTJlNTFkOTJlNjNmZDMwOWU5MzExY2JhZDYzOWRjZjIwZGM1YzQxMGE1MmE5OGUyN2E1MiIsIkRpcmVjdGlvbiI6IkxlZnQifSx7IlRhcmdldEhhc2giOiJlNTc5ZGU4MzgxMjFlNTQ5NzcxMmQzZmM3ZGZiMTJiMWJjMDA0MWM0YjhhZWU3NWI1Zjc4NjUwN2UyMGE2YmU1IiwiRGlyZWN0aW9uIjoiTGVmdCJ9LHsiVGFyZ2V0SGFzaCI6ImM4ZmE0ZWU2MGE4NThmOTZmNzljMmQ0OGY2NGY2MTMwYzA3ZDVlNjkxZjBjZDJjYjI2ZTc2Njc1OTBjNmQ2NjkiLCJEaXJlY3Rpb24iOiJMZWZ0In0seyJUYXJnZXRIYXNoIjoiZTc3NWYxZDEzYzVhMDlkNGQyZjkxZTYwZTllYTNmMzhjMTQyNmExZDlhMWM3YWZkNTYxMzUxYjE0NGI2YTY1NCIsIkRpcmVjdGlvbiI6IkxlZnQifSx7IlRhcmdldEhhc2giOiI5YWMxZmVkZTZmNzZjYTFiMjA2NmM5MjFjNmZhMTMwOTFlN2QyMTA5MDIxYmIyYjA2MTdlYWFkODcxZWE3ZDU0IiwiRGlyZWN0aW9uIjoiTGVmdCJ9XSwiQ29udHJhY3RBZGRyIjoiMzZiYjVjMDUzYjZiODM5YzhmNmI5MjNmZTg1MmY5MTIzOWI5ZmNjYyJ9fQ=="],"Signature":"ATOXcb/O7Z7VPSKv2tDKfrA78bBWqoaWigNQC6luKuHHk/aY/Xskx7/LK/DS7ztPlTuD6nNnASnHkPuJRFAYoJY=","UserOntId":"did:ont:Adoro6hu2qakpnLTzq7KPMNEBqwQJWctWz"}'
        parser = ParseOntData(data)
        parser.parse_data()

        respond = {
            'Action': 'AuthConfirm', "Error": 0, "Desc": "SUCCESS", "Result": 'true',
        }
        return self.write(tornado.escape.json_encode(respond))

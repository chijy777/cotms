import base64
import json




data =b'{\r\n\t"OntPassOntId": "did:ont:AUiPt6NWppcrRMFLA9QPUV2BHEwfeAwPUt",\r\n\t"Claims": ["eyJraWQiOiJkaWQ6b250OkFScjZBcEsyNEVVN251Zk5ENHMxU1dwd1VMSEJlcnRwSmIja2V5cy0xIiwidHlwIjoiSldULVgiLCJhbGciOiJPTlQtRVMyNTYifQ==.eyJjbG0tcmV2Ijp7InR5cCI6IkF0dGVzdENvbnRyYWN0IiwiYWRkciI6IjM2YmI1YzA1M2I2YjgzOWM4ZjZiOTIzZmU4NTJmOTEyMzliOWZjY2MifSwic3ViIjoiZGlkOm9udDpBYTdCeXdDUWV6TDNHTERyTXJxMnFQNmJMZjVWV2gzYWRWIiwidmVyIjoidjEuMCIsImNsbSI6eyJJc3N1ZXJOYW1lIjoiSWRlbnRpdHlNaW5kIiwiRW1haWwiOiJubHB4X2RjQGhvdG1haWwuY29tIiwiQ291bnRyeSI6IkNOIiwiUGhvbmVOdW1iZXIiOiIrODYgMTM3OTU0MDg3NzMiLCJEb2N1bWVudFR5cGUiOiJQUCIsIk5hbWUiOiJ6aG91cWlhbmcifSwiaXNzIjoiZGlkOm9udDpBUnI2QXBLMjRFVTdudWZORDRzMVNXcHdVTEhCZXJ0cEpiIiwiZXhwIjoxNTY1NDk0Njc4LCJpYXQiOjE1MzM5NTg2NzksIkBjb250ZXh0IjoiY2xhaW06aWRtX3Bhc3Nwb3J0X2F1dGhlbnRpY2F0aW9uIiwianRpIjoiOTA5YmEwOTU5NzE1MGQyYjI3NzgzZWZkYjczY2Y0NDJlYzRjYzY4M2ViNmI5MTcxNTRmMGQ4MmZiOTdkN2ZiMCJ9.AXmwbnXmuzTIJvm1SZF4Gq5BcY2wG+2Mi+jaBYc04avt9bb7ZGSAKIf7sx8MwYXET4VGvZvDkxUnp+7bh8qNp+Q=\\\\\\\\.eyJQcm9vZiI6eyJUeXBlIjoiTWVya2xlUHJvb2YiLCJNZXJrbGVSb290IjoiMDM3MmViOGRjZGYxMzdiOTFjNTFhOTA2YjQzZDVhYWRiYzM1ZWY1Y2RhODlmYmM4YWViZTc5OTgwNjhjYmI2MSIsIlR4bkhhc2giOiIzNWQ4ZWQ0OTNiM2VkMWVmM2U2NTIzNTlkZDA1NjdiN2ZlNTg0ODljYzk5ODY1NjRkMDc0NTc4NzA2MTQ0M2M5IiwiQmxvY2tIZWlnaHQiOjEyNzgxMywiTm9kZXMiOlt7IlRhcmdldEhhc2giOiIwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwIiwiRGlyZWN0aW9uIjoiTGVmdCJ9LHsiVGFyZ2V0SGFzaCI6ImUxNDE3MmM4YTZlMTkzOTQzNDY1NjQ4ZTFjNTg2YTkxODZhMzc4NGVlN2VlMjlkYjllZGJmNmFmZTA0ZjUzOTAiLCJEaXJlY3Rpb24iOiJMZWZ0In0seyJUYXJnZXRIYXNoIjoiZGNmYWI0ZDg5YjFiMzk4ZDQ4ZjZlNDQ3MDBlMjE4MzEzZWNjOWIwOTMzMjAyZGI1MjEzOGJkMjk4ZmE5NTE5NCIsIkRpcmVjdGlvbiI6IkxlZnQifSx7IlRhcmdldEhhc2giOiJiNzg0NWEyYjFkZDBlNGFlZWU1NzdlODVjNTdiNmRlNTVmYWU5NjI5ZjkwYzM5MzBjZDYxMjRmNDJjNmFiNjY0IiwiRGlyZWN0aW9uIjoiTGVmdCJ9LHsiVGFyZ2V0SGFzaCI6IjMyMjY1NTBmOGIzZDlkNzAyZGViYjllNGZmYjczMDNhMmU5NjY5NDQwZjVmY2JlMTVhZWU2OWRlYWFjYTkwOTUiLCJEaXJlY3Rpb24iOiJMZWZ0In0seyJUYXJnZXRIYXNoIjoiNjk5YTY5N2E1MDFkNTJlNTFkOTJlNjNmZDMwOWU5MzExY2JhZDYzOWRjZjIwZGM1YzQxMGE1MmE5OGUyN2E1MiIsIkRpcmVjdGlvbiI6IkxlZnQifSx7IlRhcmdldEhhc2giOiJlNTc5ZGU4MzgxMjFlNTQ5NzcxMmQzZmM3ZGZiMTJiMWJjMDA0MWM0YjhhZWU3NWI1Zjc4NjUwN2UyMGE2YmU1IiwiRGlyZWN0aW9uIjoiTGVmdCJ9LHsiVGFyZ2V0SGFzaCI6ImM4ZmE0ZWU2MGE4NThmOTZmNzljMmQ0OGY2NGY2MTMwYzA3ZDVlNjkxZjBjZDJjYjI2ZTc2Njc1OTBjNmQ2NjkiLCJEaXJlY3Rpb24iOiJMZWZ0In0seyJUYXJnZXRIYXNoIjoiZTc3NWYxZDEzYzVhMDlkNGQyZjkxZTYwZTllYTNmMzhjMTQyNmExZDlhMWM3YWZkNTYxMzUxYjE0NGI2YTY1NCIsIkRpcmVjdGlvbiI6IkxlZnQifSx7IlRhcmdldEhhc2giOiI5YWMxZmVkZTZmNzZjYTFiMjA2NmM5MjFjNmZhMTMwOTFlN2QyMTA5MDIxYmIyYjA2MTdlYWFkODcxZWE3ZDU0IiwiRGlyZWN0aW9uIjoiTGVmdCJ9XSwiQ29udHJhY3RBZGRyIjoiMzZiYjVjMDUzYjZiODM5YzhmNmI5MjNmZTg1MmY5MTIzOWI5ZmNjYyJ9fQ=="],\r\n\t"Signature": "AdpQBPKI+2s1bbWb10fwvBbWEUhrc5iLDRpiz4kplCwYvhyMCEL4WDEvkUClqLPmJTbkaFzVTHcIoC0MgfD7p1Q=",\r\n\t"UserOntId": "did:ont:Adoro6hu2qakpnLTzq7KPMNEBqwQJWctWz"\r\n}'
jsonData = json.loads(data)
print(jsonData)

for k, v in jsonData.items():
    print(k, v)

OntPassOntId = jsonData.get('OntPassOntId')
Claims = jsonData.get('Claims')
Signature = jsonData.get('Signature')
UserOntId = jsonData.get('UserOntId')
print('...',OntPassOntId)
print('...',Claims)
print('...',Signature)
print('...',UserOntId)

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
if isinstance(Claims, list):
    print('claims_len...',len(Claims))
    for i in Claims:
        print('i...',i)
        aa = i.split('\\.')
        print('aa_len...', len(aa))
        for k in aa:
            print('k...',k)
            b64 = base64.b64decode(k)
            print(b64)
            jb64 = json.loads(b64)
            for k, v in jb64.items():
                print('k/v...',k, v)
                # jv = json.loads(v)
                # print('jv...',jv)
                # for k1,v1 in jv.items():
                #     print('k/v...',k1, v1)




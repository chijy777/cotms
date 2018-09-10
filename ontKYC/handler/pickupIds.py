# -*- coding: utf-8 -*-
import logging
from handler.parseOntData import ParseOntData
from model.ontKycIds import OntKycIds
from model.ontKycLog import OntKycLog

logger = logging.getLogger("pickup_ids")


class PickupIds():
    """
    提取身份证.
    """
    def process(self):
        # [ont_kyc_log_new]，取id列表.
        logIdList = OntKycLog.find_all_id()

        if not logIdList:
            print("Error, [PickupIds] / logIdList null error ! ")

        for no, logId in enumerate(logIdList):
            # [ont_kyc_log_new]，根据id，取记录.
            log = OntKycLog.find_one(logId[0])
            print("101====>{}, {}, {}".format(no, logId, logId[0]))
            # print("102====>{}".format(log.ont_kyc_data))

            # 已经存在，跳过.
            res = OntKycIds.find_by_logId(log_id=logId[0])
            if res:
                print("jump...==============================")
                continue

            # 解析、入库[ont_kyc_ids].
            self.parseIds(
                log_id=logId[0],
                kyc_data=log.ont_kyc_data
            )

            # if no > 10:
            #     break


    def parseIds(self, log_id, kyc_data):
        """
        解析，身份证.
        """

        # 解析.
        parser = ParseOntData(kyc_data)
        kycItem = parser.parse_data()
        print("[PickupIds] / ..., kycItem={}, type={}".format(kycItem, type(kycItem)))

        print("201====>UserOntId=[{}], issuer=[{}]，context=[{}]，mail=[{}]，phone=[{}], name=[{}], "
                "country=[{}], docType=[{}], id_name=[{}], id_no=[{}]".
            format(
                kycItem.get('ont_UserOntId'),
                kycItem.get('ont_Claims_clm_IssuerName'),
                kycItem.get('ont_Claims_context'),
                kycItem.get('ont_Claims_clm_Email'),
                kycItem.get('ont_Claims_clm_PhoneNumber'),
                kycItem.get('ont_Claims_clm_Name'),
                kycItem.get('ont_Claims_clm_Country'),
                kycItem.get('ont_Claims_clm_DocumentType'),
                kycItem.get('id_name'),
                kycItem.get('id_no'),
        ))

        # 入库，[ont_kyc_ids].
        OntKycIds.insert(
            log_id=log_id,
            issuer_name=kycItem.get('ont_Claims_clm_IssuerName'),
            email=kycItem.get('ont_Claims_clm_Email'),
            phone=kycItem.get('ont_Claims_clm_PhoneNumber'),
            country=kycItem.get('ont_Claims_clm_Country'),
            name=kycItem.get('ont_Claims_clm_Name'),
            context=kycItem.get('ont_Claims_context'),
            user_ontid=kycItem.get('ont_UserOntId'),
            id_name=kycItem.get('id_name'),
            id_no=kycItem.get('id_no')
        )


if __name__ == '__main__':
    pickup = PickupIds()
    pickup.process()

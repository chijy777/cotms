import json
import logging
import tornado
import tornado.web

class KycItem(object):
    ont_kyc_data = None
    ont_OntPassOntId = None
    ont_UserOntId = None
    ont_Signature = None
    ont_Claims = None

    ont_payload = None
    ont_Claims_clm_IssuerName = None
    ont_Claims_clm_Email = None
    ont_Claims_clm_Country = None
    ont_Claims_clm_PhoneNumber = None
    ont_Claims_clm_DocumentType = None
    ont_Claims_clm_Name = None

    ont_Claims_sub = None
    ont_Claims_context = None
    ont_Claims_iat = None
    ont_Claims_exp = None

    update_time = None


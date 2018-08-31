import time
from lib.database import Base, db_session
from sqlalchemy import Column, Integer, String

class OntKycLog(Base):
    __tablename__ = 'ont_kyc_log_new'

    id = Column(Integer, primary_key=True)

    ont_kyc_data = Column(String(20480))
    ont_payload = Column(String(20480))
    ont_Claims_sub = Column(String(128))

    ont_Claims_clm_IssuerName = Column(String(128))
    ont_Claims_clm_Email = Column(String(128))
    ont_Claims_clm_Country = Column(String(128))
    ont_Claims_clm_PhoneNumber = Column(String(128))
    ont_Claims_clm_DocumentType = Column(String(128))
    ont_Claims_clm_Name = Column(String(128))

    ont_Claims_context = Column(String(128))
    ont_Claims_iat = Column(String(50))
    ont_Claims_exp = Column(String(50))

    ont_OntPassOntId = Column(String(2048))
    ont_UserOntId = Column(String(2048))
    ont_Signature = Column(String(2048))
    ont_Claims = Column(String(20480))

    create_time = Column(Integer)
    update_time = Column(Integer)


    def __init__(self, ont_kyc_data=None, ont_payload=None, ont_Claims_sub=None,
                    ont_Claims_clm_IssuerName=None, ont_Claims_clm_Email=None, ont_Claims_clm_Country=None,
                    ont_Claims_clm_PhoneNumber=None, ont_Claims_clm_DocumentType=None, ont_Claims_clm_Name=None,
                    ont_Claims_context=None, ont_Claims_iat=None, ont_Claims_exp=None,
                    ont_OntPassOntId = None, ont_UserOntId = None, ont_Signature = None, ont_Claims = None,
                ):
        if ont_kyc_data:
            self.ont_kyc_data = ont_kyc_data
        if ont_payload:
            self.ont_payload = ont_payload
        if ont_Claims_sub:
            self.ont_Claims_sub = ont_Claims_sub

        if ont_Claims_clm_IssuerName:
            self.ont_Claims_clm_IssuerName = ont_Claims_clm_IssuerName
        if ont_Claims_clm_Email:
            self.ont_Claims_clm_Email = ont_Claims_clm_Email
        if ont_Claims_clm_Country:
            self.ont_Claims_clm_Country = ont_Claims_clm_Country
        if ont_Claims_clm_PhoneNumber:
            self.ont_Claims_clm_PhoneNumber = ont_Claims_clm_PhoneNumber
        if ont_Claims_clm_DocumentType:
            self.ont_Claims_clm_DocumentType = ont_Claims_clm_DocumentType
        if ont_Claims_clm_Name:
            self.ont_Claims_clm_Name = ont_Claims_clm_Name

        if ont_Claims_context:
            self.ont_Claims_context = ont_Claims_context
        if ont_Claims_iat:
            self.ont_Claims_iat = ont_Claims_iat
        if ont_Claims_exp:
            self.ont_Claims_exp = ont_Claims_exp

        if ont_OntPassOntId:
            self.ont_OntPassOntId = ont_OntPassOntId
        if ont_UserOntId:
            self.ont_UserOntId = ont_UserOntId
        if ont_Signature:
            self.ont_Signature = ont_Signature
        if ont_Claims:
            self.ont_Claims = ont_Claims

        if not self.create_time:
            self.create_time = int(time.time())
        self.update_time = int(time.time())

    @classmethod
    def find_one(cls, id):
        return db_session.query(OntKycLog).filter(OntKycLog.id == id).first()

    @classmethod
    def insert(cls, ont_kyc_data=None, ont_payload=None, ont_Claims_sub=None,
                ont_Claims_clm_IssuerName=None, ont_Claims_clm_Email=None, ont_Claims_clm_Country=None,
                ont_Claims_clm_PhoneNumber=None, ont_Claims_clm_DocumentType=None, ont_Claims_clm_Name=None,
                ont_Claims_context=None, ont_Claims_iat=None, ont_Claims_exp=None,
                ont_OntPassOntId=None, ont_UserOntId=None, ont_Signature=None, ont_Claims=None,
               ):
        newOKL = OntKycLog(
            ont_kyc_data=ont_kyc_data, ont_payload=ont_payload, ont_Claims_sub=ont_Claims_sub,
            ont_Claims_clm_IssuerName=ont_Claims_clm_IssuerName, ont_Claims_clm_Email=ont_Claims_clm_Email,
            ont_Claims_clm_Country=ont_Claims_clm_Country, ont_Claims_clm_PhoneNumber=ont_Claims_clm_PhoneNumber,
            ont_Claims_clm_DocumentType=ont_Claims_clm_DocumentType, ont_Claims_clm_Name=ont_Claims_clm_Name,
            ont_Claims_context=ont_Claims_context, ont_Claims_iat=ont_Claims_iat, ont_Claims_exp=ont_Claims_exp,
            ont_OntPassOntId=ont_OntPassOntId, ont_UserOntId=ont_UserOntId,
            ont_Signature=ont_Signature, ont_Claims=ont_Claims,
        )
        db_session.add(newOKL)

        try:
            db_session.commit()
        except:
            db_session.rollback()
        if newOKL.id:
            return cls.find_one(newOKL.id)
        return None

# -*- coding: utf-8 -*-
from lib.database import Base, db_session
from sqlalchemy import Column, Integer, String

class OntKycIds(Base):
    """
    """
    __tablename__ = 'ont_kyc_ids'

    id = Column(Integer, primary_key=True)

    log_id = Column(Integer)
    issuer_name = Column(String(128))
    email = Column(String(128))
    phone = Column(String(128))
    country = Column(String(128))
    name = Column(String(128))

    context = Column(String(128))
    user_ontid = Column(String(255))

    id_name = Column(String(128))
    id_no = Column(String(128))


    def __init__(self, log_id=None, issuer_name=None, email=None, phone=None, country=None, name=None,
                    context=None, user_ontid=None, id_name=None, id_no=None):
        if log_id:
            self.log_id = log_id
        if issuer_name:
            self.issuer_name = issuer_name
        if email:
            self.email = email
        if phone:
            self.phone = phone
        if country:
            self.country = country
        if name:
            self.name = name

        if context:
            self.context = context
        if user_ontid:
            self.user_ontid = user_ontid

        if id_name:
            self.id_name = id_name
        if id_no:
            self.id_no = id_no


    @classmethod
    def insert(cls, log_id=None, issuer_name=None, email=None, phone=None, country=None, name=None,
                    context=None, user_ontid=None, id_name=None, id_no=None):
        newRec = cls(
            log_id=log_id, issuer_name=issuer_name, email=email, phone=phone, country=country, name=name,
            context=context, user_ontid=user_ontid, id_name=id_name, id_no=id_no,
        )
        db_session.add(newRec)

        try:
            db_session.commit()
        except:
            db_session.rollback()
        return True


    @classmethod
    def find_by_logId(cls, log_id):
        return db_session.query(
            cls
        ).filter(cls.log_id == log_id).first()

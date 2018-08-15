from ontKYC.handler.kycServer import IndexHandler, NotifyHandler, TestNotifyHandler

__all__ = ['urls_pattern']

# [mobile Apps].
urls_pattern = [
    ("/ontkyc", IndexHandler),
    ("/ontkyc/notify", NotifyHandler),

    ("/ontkyc/test_notify", TestNotifyHandler),
]


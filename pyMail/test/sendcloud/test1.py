#!/usr/bin/python
#coding:utf-8
import requests, json
import settings

subject = """
COT 邮件订阅申请确认 COT mail subscription application confirmation  (请勿回复本邮件) 
"""

# body = """
# 亲爱的COT粉丝，
# Dear COT fans，
#
# 您好！
#
# 感谢您参与了第一期COT邮件订阅计划！请您继续关注我们的社区（微信公众号、微信群、QQ群、电报群、Facebook、Twitter）以免错过重要信息。为了尽量确保COT订阅真实性，我们还将进行一些KYC等相关操作流程，感谢您能积极的配合我们的工作。相关信息将通过我们的社区及时发布！
# Thank you for joining the first COT email subscription plan! Please pay attention to our community （Telegram 、 Facebook、Twitter、Wechat 、 QQ Group），so you wouldn’t miss important information.  In order to ensure the authenticity of COT subscription as much as possible, we will also carry out some related operation procedures such as KYC. Thank you for your active cooperation in our work. Relevant information will be released through our community in time!
#
#
# 感谢您一直以来对COT的支持和信任！
# Thank you for your continued support and trust in COT!
#
# Best Regards！
#
# COT团队
# COT Team
#
# 2018.7.6
#
# COT官方网站：
# COT Official website:
# https://www.cot.io
# """

body = """
<p>
    &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;&nbsp;<img width="261px" height="93px" src="http://www.aihuinong.com/WebAsset/AssetLib/webUploader/images/cot_logo.png"/>
</p>
<p style=";margin-bottom:0">
    <span style="font-size: 14px;color:black;background:white">&nbsp;</span>
</p>
<p style=";margin-bottom:0">
    <span style="font-size:14px;color:black;background:white">亲爱的</span><span style="font-size:14px;font-family:&#39;Calibri&#39;,&#39;sans-serif&#39;;color:black;background:white">COT</span><span style="font-size:14px;color:black;background:white">粉丝，</span><span style="font-family:&#39;Arial&#39;,&#39;sans-serif&#39;;color:black"><br/> </span><span style="font-size:14px;font-family:&#39;Calibri&#39;,&#39;sans-serif&#39;;color:black;background:white">Dear COT fans</span><span style="font-size:14px;color:black;background:white">，</span><span style="font-family:&#39;Arial&#39;,&#39;sans-serif&#39;;color:black"><br/> <br/> </span><span style="font-size:14px;color:black;background:white">您好！</span><span style="font-family:&#39;Arial&#39;,&#39;sans-serif&#39;;color:black"><br/> <br/> </span><span style="font-size:14px;color:black;background:white">感谢您参与了第一期</span><span style="font-size:14px;font-family:&#39;Calibri&#39;,&#39;sans-serif&#39;;color:black;background:white">COT</span><span style="font-size:14px;color:black;background: white">邮件订阅计划！</span>请您继续关注我们的社区，以免错过重要信息。<span style="font-size:14px;color:black;background:white">相关信息将通过COT官方社区及时发布！</span><span style="font-family:&#39;Arial&#39;,&#39;sans-serif&#39;;color:black"><br/> </span><span style="font-size:14px;font-family:&#39;Tahoma&#39;,&#39;sans-serif&#39;;color:#434343;background:white">Thank you for joining the first COT email subscription plan! </span><span style=";font-family:&#39;Tahoma&#39;,&#39;sans-serif&#39;;color:#434343">Please pay attention to our community, so you wouldn’t miss important information. </span><span style="font-size:14px;font-family:&#39;Tahoma&#39;,&#39;sans-serif&#39;;color:#434343;background:white">Relevant information will be released through COT official community in time!</span><span style="font-family:&#39;Arial&#39;,&#39;sans-serif&#39;;color:black"><br/> <br/> <br/> </span><span style="font-size:14px;color:black;background:white">感谢您一直以来对</span><span style="font-size:14px;font-family:&#39;Calibri&#39;,&#39;sans-serif&#39;;color:black;background:white">COT</span><span style="font-size:14px;color:black;background: white">的支持和信任！</span><span style="font-family:&#39;Arial&#39;,&#39;sans-serif&#39;;color:black"><br/> </span><span style="font-size:14px;font-family:&#39;Tahoma&#39;,&#39;sans-serif&#39;;color:#434343;background:white">Thank you for your continued support and trust in COT!</span><span style="font-family:&#39;Arial&#39;,&#39;sans-serif&#39;;color:black"><br/> <br/> </span><span style="font-size:14px;font-family:&#39;Calibri&#39;,&#39;sans-serif&#39;;color:black;background:white">Best Regards</span><span style="font-size:14px;color:black;background:white">！</span><span style="font-family:&#39;Arial&#39;,&#39;sans-serif&#39;;color:black"><br/> <br/> </span><span style="font-size:14px;font-family:&#39;Calibri&#39;,&#39;sans-serif&#39;;color:black;background:white">COT</span><span style="font-size:14px;color:black;background:white">团队</span><span style="font-family:&#39;Arial&#39;,&#39;sans-serif&#39;;color:black"><br/> </span><span style="font-size:14px;font-family:&#39;Calibri&#39;,&#39;sans-serif&#39;;color:black;background:white">COT Team</span><span style="font-family: &#39;Arial&#39;,&#39;sans-serif&#39;;color:black"><br/> <br/> </span><span style="font-size:14px;font-family:&#39;Calibri&#39;,&#39;sans-serif&#39;;color:black;background:white">2018.7.6</span><span style="font-family: &#39;Arial&#39;,&#39;sans-serif&#39;;color:black"><br/> <br/> </span>
</p>
<p style=";margin-bottom:0">
    <strong><span style="font-size:12px;font-family:&#39;微软雅黑&#39;,&#39;sans-serif&#39;;color:black;background:white;font-weight:normal">COT</span></strong><strong><span style="font-size:12px;font-family:&#39;微软雅黑&#39;,&#39;sans-serif&#39;;color:black;background:white;font-weight:normal">官方网站：</span></strong>
</p>
<p style="margin-top:5px;margin-right:0;margin-bottom:5px;margin-left: 0">
    <strong><span style="font-size:12px;font-family:&#39;微软雅黑&#39;,&#39;sans-serif&#39;;color:black;background:white;font-weight:normal">COT Official website:</span></strong>
</p>
<p style="margin-top:5px;margin-right:0;margin-bottom:5px;margin-left: 0">
    <strong><span style="font-size:18px;font-family:&#39;Calibri&#39;,&#39;sans-serif&#39;;color:black;background:white;font-weight:normal">https://www.cot.io</span></strong>
</p>
<p>
    <br/>
</p>
"""

content = {
    "apiUser": settings.SEND_CLOUD_API_USER,
    "apiKey" : settings.SEND_CLOUD_API_KEY,
    "from"   : settings.SEND_CLOUD_FROM,
    "fromName" : settings.SEND_CLOUD_FROM_NAME,
    "to" : "1178937142@qq.com",
    "subject" : subject,
    "html": body,
}
print(content)

result = requests.post(
    settings.SEND_CLOUD_API_URL, files={}, data=content
)
print(result.text)


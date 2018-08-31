package demo._cot;

import com.alibaba.fastjson.JSON;
import com.alibaba.fastjson.JSONObject;
import com.github.ontio.OntSdk;
import com.github.ontio.account.Account;
import com.github.ontio.common.Helper;
import com.github.ontio.core.DataSignature;

import java.util.Base64;

/**
 * @author zhouq
 * @version 1.0
 * @date 2018/7/24
 */
public class Test01 {
    public static void main(String[] args) {

        try {
            OntSdk ontSdk = getOntSdk();

            /////////////////////////////////////////////////////////
            //根据创建的ontid身份获取ontid的公钥，私钥信息
            /////////////////  [chijy add 725] /////////////////
            String ontid = "did:ont:AU33gcuRJMNgDyLSSRHzfAuBri4wcY2jzh";
            String password = "081699";
            String salt = "B/l6YW49ZFCYIx1RmVffIQ==";
            byte[] ontidsaltByte = Base64.getDecoder().decode(salt);

            ///////////////// [chijy add 725] /////////////////
            Account testAcct = ontSdk.getWalletMgr().getAccount(ontid, password, ontidsaltByte);
            String identityPubkey = Helper.toHexString(testAcct.serializePublicKey());
            System.out.println("identityPubkey:" + identityPubkey);
            String identityPrikey = Helper.toHexString(testAcct.serializePrivateKey());
            System.out.println("identityPrikey:" + identityPrikey);

            //待签名原文
            JSONObject obj = new JSONObject();
            obj.put("OntId", "did:ont:AU33gcuRJMNgDyLSSRHzfAuBri4wcY2jzh");
            obj.put("Lan", "EN");
            String orig = obj.toJSONString();
            System.out.println("origdata:" + orig);

            //使用ontid的私钥对原文进行签名
            DataSignature sign = new DataSignature(ontSdk.defaultSignScheme, testAcct, orig.getBytes());
            //签名后数据
            String sigdata = Base64.getEncoder().encodeToString(sign.signature());
            System.out.println("sigdata:" + sigdata);
            obj.put("Sig", sigdata);

            System.out.println("byte length:" + obj.toJSONString().getBytes().length);
            System.out.println("req str:" + obj.toJSONString());

            //获取ontid的公钥对签名后数据进行验签
            String ontid2 = ontid;
            String issuerDdo = ontSdk.nativevm().ontId().sendGetDDO(ontid2);
            String pubkeyStr = JSON.parseObject(issuerDdo).getJSONArray("Owners").getJSONObject(0).getString("Value");
            System.out.println("pubkey:" + pubkeyStr);

            Account account = new Account(false, Helper.hexToBytes(pubkeyStr));
            DataSignature sign2 = new DataSignature();
            Boolean rs = sign2.verifySignature(account, orig.getBytes(), Base64.getDecoder().decode(sigdata));
            System.out.println("verify:" + rs);
        } catch (Exception e) {
            e.printStackTrace();
        }
    }


    public static OntSdk getOntSdk() throws Exception {
        OntSdk wm = OntSdk.getInstance();

        wm.setRestful("http://dappnode1.ont.io:20334");
        wm.setRpc("http://dappnode1.ont.io:20336");
        wm.setDefaultConnect(wm.getRestful());
        wm.openWalletFile("account.json");
        return wm;
    }


}

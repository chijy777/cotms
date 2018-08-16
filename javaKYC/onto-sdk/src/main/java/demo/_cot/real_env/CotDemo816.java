/*
 * Copyright (C) 2018 The ontology Authors
 * This file is part of The ontology library.
 *
 *  The ontology is free software: you can redistribute it and/or modify
 *  it under the terms of the GNU Lesser General Public License as published by
 *  the Free Software Foundation, either version 3 of the License, or
 *  (at your option) any later version.
 *
 *  The ontology is distributed in the hope that it will be useful,
 *  but WITHOUT ANY WARRANTY; without even the implied warranty of
 *  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 *  GNU Lesser General Public License for more details.
 *
 *  You should have received a copy of the GNU Lesser General Public License
 *  along with The ontology.  If not, see <http://www.gnu.org/licenses/>.
 *
 */

package demo._cot.real_env;

import com.alibaba.fastjson.JSON;
import com.alibaba.fastjson.JSONObject;
import com.github.ontio.OntSdk;
import com.github.ontio.account.Account;
import com.github.ontio.common.Helper;
import com.github.ontio.core.DataSignature;
import com.github.ontio.sdk.info.IdentityInfo;
import com.github.ontio.sdk.wallet.Identity;

import java.util.Base64;

/**
 * * * password=[cotontblockchain] * * *
 */
public class CotDemo816
{
    public static void main(String[] args) {
        try {
            OntSdk ontSdk = getOntSdk();

            /////////////////////////////////////////////////////////
            //Get钱包账户
            String cotPrikey = "86d66845345cf17a33e387c118429a8a4658f44955521344eb21cb8d3cfaff38";

            Account account01 = new Account(Helper.hexToBytes(cotPrikey), ontSdk.defaultSignScheme);
            //地址
            String address = account01.getAddressU160().toBase58();
            System.out.println("address:" + address);
            //私钥
            String prikey = Helper.toHexString(account01.serializePrivateKey());
            System.out.println("prikey:" + prikey);
            //公钥
            String pubkey = Helper.toHexString(account01.serializePublicKey());
            System.out.println("pubkey:" + pubkey);
            //wif
            String wif = account01.exportWif();
            System.out.println("wif:" + wif);


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
            obj.put("OntId", "did:ont:ASsU6AYGTuJ2jUymoZF8Wr2fyk7hvDxQ5y");
            obj.put("Lan", "EN");
            //  obj.put("Name","COT");
            //   obj.put("Des","blockchain");
            //   obj.put("Logo","https://cot.chain/logo/cot.jpg");
            //   obj.put("CallBackAddr", "http://127.0.0.1:10090/test");
            //   obj.put("Type","blockchain");

            JSONObject reqObj = new JSONObject();
            reqObj.put("Des", "require the kyc claim");
            reqObj.put("Contexts", "claim:idm_authentication");
            obj.put("Req", reqObj);

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

            com.github.ontio.account.Account account = new com.github.ontio.account.Account(false, Helper.hexToBytes(pubkeyStr));
            DataSignature sign2 = new DataSignature();
            Boolean rs = sign2.verifySignature(account, orig.getBytes(), Base64.getDecoder().decode(sigdata));
            System.out.println("verify:" + rs);

        } catch (Exception e) {
            e.printStackTrace();
        }
    }


    public static OntSdk getOntSdk() throws Exception
    {
        OntSdk wm = OntSdk.getInstance();

//      ont测试环境
//        wm.setRestful("http://polaris1.ont.io:20334");
//        wm.setRpc("http://polaris1.ont.io:20336");

//      ont正式环境，http://dappnode1.ont.io
        wm.setRestful("http://dappnode1.ont.io:20334");
        wm.setRpc("http://dappnode1.ont.io:20336");

        wm.setDefaultConnect(wm.getRestful());
        wm.openWalletFile("account.json");
        return wm;
    }
}

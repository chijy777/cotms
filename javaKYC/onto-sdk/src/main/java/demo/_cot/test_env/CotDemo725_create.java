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

package demo;

import com.alibaba.fastjson.JSON;
import com.alibaba.fastjson.JSONObject;
import com.github.ontio.OntSdk;
import com.github.ontio.common.Helper;
import com.github.ontio.core.DataSignature;
import com.github.ontio.sdk.wallet.Account;
import com.github.ontio.sdk.wallet.Identity;

import java.util.Base64;

/**
 * @author zhouq
 * @version 1.0
 * @date 2018/7/24
 */
public class CotDemo725_create
{
    public static void main(String[] args) {

        try {
            OntSdk ontSdk = getOntSdk();
            /////////////////////////////////////////////////////////
            //创建钱包账户
            com.github.ontio.account.Account account01 = new com.github.ontio.account.Account(ontSdk.defaultSignScheme);
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
            //创建ontid身份账户
//            String password = "passwordtest";
            String password = "cotontblockchain";
            Identity identity = ontSdk.getWalletMgr().createIdentity(password);
            //ontid
            String ontid = identity.ontid;
            System.out.println("ontid:" + ontid);
            //ontid的盐，安全参数
            String salt = identity.controls.get(0).salt;
            System.out.println("ontid salt:" + salt);
            byte[] ontidsaltByte = Base64.getDecoder().decode(salt);

            //发送注册ontid身份交易到区块链,手续费由钱包账户代付
            String txnhash2 = ontSdk.nativevm().ontId().sendRegister(identity, password,
                    account01, 20000, 500);
            System.out.println("txnhash:" + txnhash2);
            //将ontid身份账户信息写入账户文件
            ontSdk.getWalletMgr().writeWallet();

            /////////////////////////////////////////////////////////
            //根据创建的ontid身份获取ontid的公钥，私钥信息
            com.github.ontio.account.Account testAcct = ontSdk.getWalletMgr().getAccount(ontid, password, ontidsaltByte);
            String identityPubkey = Helper.toHexString(testAcct.serializePublicKey());
            System.out.println("identityPubkey:" + identityPubkey);
            String identityPrikey = Helper.toHexString(testAcct.serializePrivateKey());
            System.out.println("identityPrikey:" + identityPrikey);

            //待签名原文
            JSONObject obj = new JSONObject();
            obj.put("OntId", "did:ont:AUiPt6NWppcrRMFLA9QPUV2BHEwfeAwPUt");
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


    public static OntSdk getOntSdk() throws Exception {
        OntSdk wm = OntSdk.getInstance();

        wm.setRestful("http://polaris1.ont.io:20334");
        wm.setRpc("http://polaris1.ont.io:20336");
        wm.setDefaultConnect(wm.getRestful());
        wm.openWalletFile("account.json");
        return wm;
    }
}

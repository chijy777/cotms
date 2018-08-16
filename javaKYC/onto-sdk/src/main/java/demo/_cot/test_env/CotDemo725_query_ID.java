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
import com.github.ontio.account.Account;
import com.github.ontio.common.Helper;
import com.github.ontio.core.DataSignature;

import java.util.Base64;

/**
 * password=[cotontblockchain]
 address:ASsU6AYGTuJ2jUymoZF8Wr2fyk7hvDxQ5y
 prikey:86d66845345cf17a33e387c118429a8a4658f44955521344eb21cb8d3cfaff38
 pubkey:038854cb585335ba336a943709822ef3121522eaadbef95e9d8e0e28146d38283c
 wif:L1jpN3WkEjbxfTNyQbC7DoFE8KDyaakgp3mfQSqCBa7ouYtS9U72

 ontid:did:ont:ASsU6AYGTuJ2jUymoZF8Wr2fyk7hvDxQ5y
 ontid salt:Gxx9n0qJB93+P+LYeUzUqg==
 */
public class CotDemo725_query_ID
{
    public static void main(String[] args) {

        try {
            OntSdk ontSdk = getOntSdk();

            String cotOntid = "ASsU6AYGTuJ2jUymoZF8Wr2fyk7hvDxQ5y";
            String ddo = ontSdk.nativevm().ontId().sendGetDDO(cotOntid);
            System.out.println("ddo:" + ddo);

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

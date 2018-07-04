<?php

namespace AppBundle\Controller\Backend;

use AppBundle\Controller\BaseController;
use Symfony\Component\HttpFoundation\Request;

class MailController extends BaseController
{
    /**
     * 发送邮件
     */
    public function sendAction(Request $request)
    {
        return $this->render('AppBundle:Backend\Mail:send.html.twig', array(
        ));
    }

	public function sendCommitAction(Request $request)
	{
		$receivers = $request->request->get('receivers');
		$subject = $request->request->get('subject');
		$mailbody = $request->request->get('mailbody');
//		dump($receivers);
//		dump($subject);
//		dump($mailbody);
//		exit();

		$result = $this->send_mail($receivers, $subject, $mailbody);
		$jsonResult = json_decode($result);
//		dump($result);
//		dump($jsonResult);
//		exit();

		if( $jsonResult->result == 'True' ){
			return $this->render('AppBundle:Backend\Mail:send_ok.html.twig', array(
				'result' => '发送成功',
				'apiReturn' => $result
			));
		}
		else{
			return $this->render('AppBundle:Backend\Mail:send_fail.html.twig', array(
				'result' => '邮件发送失败',
				'apiReturn' => $result
			));
		}
	}


	/**
	 * SendCloud.API调用.
	 */
	public function send_mail($receivers, $subject, $mailbody)
	{
//		$url = 'http://api.sendcloud.net/apiv2/mail/send';
//		$API_USER = 'chijy777_test_TbNuhy';
//		$API_KEY = '2v6yRT9hrHO6PERD';
//		$FROM = 'service@sendcloud.im';
//		$FROM_NAME = 'SendCloud测试邮件';

//		send_cloud_api_url: 'http://api.sendcloud.net/apiv2/mail/send'
//    	send_clound_api_user: 'chijy777_test_TbNuhy'
//    	send_clound_api_key: '2v6yRT9hrHO6PERD'
//    	send_clound_from: 'service@sendcloud.im'
//    	send_clound_from_name: 'SendCloud测试邮件'

//您需要登录SendCloud创建API_USER，使用API_USER和API_KEY才可以进行邮件的发送。
		$param = array(
			'apiUser'  => $this->getParameter('send_clound_api_user'),
			'apiKey'   => $this->getParameter('send_clound_api_key'),
			'from'     => $this->getParameter('send_clound_from'),
			'fromName' => $this->getParameter('send_clound_from_name'),
			'to'      => $receivers,
			'subject'=> $subject,
			'html'   => $mailbody,
			'respEmailId' => 'true'
		);
//		dump($param);
//		exit();

		$data = http_build_query($param);
		$options = array(
			'http' => array(
				'method'  => 'POST',
				'header'  => 'Content-Type: application/x-www-form-urlencoded',
				'content' => $data
			)
		);
		$context  = stream_context_create($options);

		$result = file_get_contents(
			$this->getParameter('send_cloud_api_url'),
			false, $context
		);
		return $result;
	}

}

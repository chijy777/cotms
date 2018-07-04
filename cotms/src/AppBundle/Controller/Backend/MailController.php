<?php

namespace AppBundle\Controller\Backend;

use AppBundle\Controller\BaseController;
use Symfony\Component\HttpFoundation\Request;

class MailController extends BaseController
{
    /**
     * 列表页
     */
    public function indexAction(Request $request)
    {
        // 取设备.
		$list = null;
//		dump($list); exit();

        return $this->render('AppBundle:Backend\Mail:index.html.twig', array(
            'pagination' => null
        ));
    }

}

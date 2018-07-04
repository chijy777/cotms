<?php

namespace AppBundle\Controller\Backend;

use Symfony\Bundle\FrameworkBundle\Controller\Controller;

class IndexController extends Controller
{
    /**
     * 后台.首页.
     */
    public function indexAction()
    {
        return $this->render('AppBundle:Backend:layout.html.twig');
    }

}

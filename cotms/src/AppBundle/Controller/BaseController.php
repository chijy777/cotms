<?php

namespace AppBundle\Controller;

use Symfony\Bundle\FrameworkBundle\Controller\Controller;
use Doctrine\Common\Util\Debug;
use Symfony\Component\Filesystem\Filesystem;
use Symfony\Component\HttpFoundation\JsonResponse;
use Symfony\Component\HttpFoundation\Request;
use Symfony\Component\VarDumper\VarDumper;


class BaseController extends Controller
{
    /**
     * Doctrine对象
     * @return \Doctrine\Common\Persistence\ObjectManager|object
     */
    public function em(){
        return $this->getDoctrine()->getManager();
    }

	/**
	 * @param $code 0是失败，1成功, 2提示
	 * @return JsonResponse
	 */
	public function FinalJson($code , $data='', $msg='提示消息')
	{
	    switch ($code) {
			case 0:
				return new JsonResponse(
				    ["rcode" => 0, "msg" => "执行成功", "data" => $data], 200,
                    ['Access-Control-Allow-Origin'=>'*','Access-Control-Allow-Headers'=>'Content-Type']);
				break;
            case 1:
                return new JsonResponse(
                    ["rcode" => 1, "msg" => "执行失败", "data" => $data], 200,
                    ['Access-Control-Allow-Origin'=>'*','Access-Control-Allow-Headers'=>'Content-Type']);
                break;
            default:
                return new JsonResponse(
                    ["rcode" => $code, "msg" => $msg, "data" => $data], 200,
                    ['Access-Control-Allow-Origin'=>'*','Access-Control-Allow-Headers'=>'Content-Type']);
		}
	}

    /**
     * 创建消息提示响应
     *
     * @param  string     $type     消息类型（0为成功(success) 1为信息(info) 2为(primary) 3为警告(warning) 4为失败(danger) ）
     * @param  string     $message  消息内容
     * @param  integer    $goto     消息跳转的页面
     * @param  string     $sec      消息提示的时间
     * @param  integer    $webType  页面类型 0为PC 1为M
     * @return Response
     */
    const MSG_WARN = 3;

    protected function createMessageResponse($type = 0,$message = '操作成功！', $goto = null, $sec = 3,$webType = 0)
    {
        switch ($type)
        {
            case 0:
                $typeClass = 'success';
                break;
            case 1:
                $typeClass = 'info';
                break;
            case 2:
                $typeClass = 'primary';
                break;
            case 3:
                $typeClass = 'warning';
                break;
            case 4:
                $typeClass = 'danger';
                break;
        }
        switch ($webType)
        {
            case 0:
                $rederView = 'AppWebBundle:Frontend/Common:message.html.twig';
                break;
            case 1:
                $rederView = 'AppWeChatBundle:Common:message.html.twig';
                break;
            case 2:
                $rederView = 'AppWeChatBundle:Common:infomsg.html.twig';
                break;
        }
        return $this->render($rederView, array(
            'sec'       =>  $sec,
            'type'      => $type,
            'message'   => $message,
            'url'       => $goto,
            'typeclass' => $typeClass
        ));
    }

    /**
     * 创建用户Sn码
     * @param $cityId
     * @param $uid
     * @return string
     */
    public function createUserSn($cityId,$uid)
    {
        $cid = substr($cityId,0,4);
        $year = date('ymd');
        $newUid= sprintf('%07s', $uid);
        return $cid .$year .$newUid;
    }

    /**
     * 打印数据
     * @param $data
     */
    public function dp($data)
    {
        echo '<pre>';
        Debug::dump($data);
        echo '</pre>';
    }

    /**
     * 打印普通的数组
     * @param $data
     */
    public function p($data)
    {
        echo '<pre>';
        print_r($data);
        echo '</pre>';
        exit();
    }

    /**
     * 分页数据
     * @param $data     要传入的分页数据
     * @param $num      分页第几个数据
     * @param int $pageNum      每页要展示多少数据
     * @return \Knp\Component\Pager\Pagination\PaginationInterface
     */
    public function pageData($data,$num,$pageNum = 16)
    {
        $request = new Request();
        $paginator  = $this->get('knp_paginator');
        $pagination = $paginator->paginate(
            $data, /* query NOT result */
            $num/*page number*/,
            $pageNum/*limit per page*/
        );
        return $pagination;
    }



    /**
     * 获取文件资源
     * @param $file_name
     * @return string
     */
    function getContractResource($file_name)
    {
        $path = __DIR__ . '/../Resources/contract/' . $file_name;
        return file_get_contents($path);
    }

    function getContractImgResource($file_name)
    {
        $path = __DIR__ . '/' . $file_name;
        return file_get_contents($path);
    }

    /**
     * 打印数据
     * @param $var
     */
    function d($var)
    {
        foreach (func_get_args() as $var) {
            VarDumper::dump($var);
        }
        exit();
    }


    public function delFileAction(Request $request)
    {
        //获取要删除图片的路径
        $delPath = $request->get('delPath');

        $fs = new Filesystem();
        $fs->remove($this->get('kernel')->getRootDir().'/../web/'.$delPath);
        return new JsonResponse(1);
    }

}

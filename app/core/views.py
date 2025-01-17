from django.shortcuts import render, redirect
import requests

# Create your views here.
from order.models import Order


def index(request):
    """
    IOS에서 해줄 부
    """
    if request.method == 'POST':

        URL = 'https://kapi.kakao.com/v1/payment/ready'
        headers = {
            "Authorization": "KakaoAK " + "f9f70eb192ef14919735fb40a6e599f5",
            "Content-type": "application/x-www-form-urlencoded;charset=utf-8",
        }
        try:
            order_ins = Order.objects.last()
        except Order.DoesNotExist:
            order_ins = None

        if order_ins:
            cart_ins = order_ins.items.last().cart

            params = {
                "cid": "TC0ONETIME",  # 테스트용 코드
                "partner_order_id": f'{order_ins.id}',  # 주문번호
                "partner_user_id": 'admin',  # 유저 아이디
                "item_name": f'admin의 상품 구매',  # 구매 물품 이름
                "quantity": f'{cart_ins.quantity_of_goods}',  # 구매 물품 수량
                "total_amount": f'{order_ins.discount_payment}',  # 구매 물품 가격
                "tax_free_amount": "0",  # 구매 물품 비과세
                "approval_url": f"http://localhost:8000/api/order/{order_ins.id}/approve",
                "cancel_url": "https://developers.kakao.com/fail",
                "fail_url": "https://developers.kakao.com/cancel",
            }



            res = requests.post(URL, headers=headers, params=params)
            request.session['tid'] = res.json()['tid']  # 결제 고유 번호, 20자 결제 승인시 사용할 tid를 세션에 저장
            request.session['partner_order_id'] = order_ins.id
            request.session['partner_user_id'] = 'admin'
            next_url = res.json()['next_redirect_pc_url']  # 카카오톡 결제 페이지 Redirect URL

            request.session.modified = True
        return redirect(next_url)
    return render(request, 'base.html')


def success(request):
    """
    서버에서 할 부분
    """
    # 결제 성공
    URL = 'https://kapi.kakao.com/v1/payment/approve'
    headers = {
        "Authorization": "KakaoAK " + "f9f70eb192ef14919735fb40a6e599f5",
        "Content-type": "application/x-www-form-urlencoded;charset=utf-8",
    }
    params = {
        "cid": "TC0ONETIME",  # 테스트용 코드
        "tid": request.session['tid'],  # 결제 요청시 세션에 저장한 tid
        "partner_order_id": "1",  # 주문번호
        "partner_user_id": "admin",  # 유저 아이디
        "pg_token": request.GET.get("pg_token"),  # 쿼리 스트링으로 받은 pg토큰
    }
    res = requests.post(URL, headers=headers, params=params)
    amount = res.json()['amount']['total']
    res = res.json()
    context = {
        'res': res,
        'amount': amount,
    }
    return render(request, 'success.html')


def fail(request):
    return render(request, 'fail.html')

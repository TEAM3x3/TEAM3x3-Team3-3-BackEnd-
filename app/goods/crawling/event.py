def evenvt_crawling():
    import os
    import re
    import urllib

    from django.core.files import File
    from selenium.common.exceptions import NoSuchElementException
    from config.settings.base import MEDIA_ROOT
    from selenium import webdriver

    from goods.models import Goods, GoodsExplain, GoodsDetail, GoodsDetailTitle
    from event.models import Event

    driver = webdriver.Chrome('/Users/mac/projects/ChromeWebDriver/chromedriver')

    event_name_list = [
        # '[모음전] 해물육수',
        '[모음전] 오미자', '[모음전] 키친타올', '[모음전] 뷰코', '[모음전] 미당']
    goods_no_detail_list = [
        # ['https://www.kurly.com/shop/goods/goods_view.php?goodsno=51726',
        #  'https://www.kurly.com/shop/goods/goods_view.php?goodsno=51712',
        #  'https://www.kurly.com/shop/goods/goods_view.php?goodsno=51711',
        #  'https://www.kurly.com/shop/goods/goods_view.php?goodsno=51710',
        #  'https://www.kurly.com/shop/goods/goods_view.php?goodsno=51709',
        #  'https://www.kurly.com/shop/goods/goods_view.php?goodsno=51708',
        #  'https://www.kurly.com/shop/goods/goods_view.php?goodsno=49279',
        #  'https://www.kurly.com/shop/goods/goods_view.php?goodsno=51713',
        #  'https://www.kurly.com/shop/goods/goods_view.php?goodsno=47700',
        #  'https://www.kurly.com/shop/goods/goods_view.php?goodsno=10082'],
        [
            # 'https://www.kurly.com/shop/goods/goods_view.php?goodsno=52772',
            # 'https://www.kurly.com/shop/goods/goods_view.php?goodsno=52771',
            # 'https://www.kurly.com/shop/goods/goods_view.php?goodsno=51016',
            # 'https://www.kurly.com/shop/goods/goods_view.php?goodsno=50998',
            # 'https://www.kurly.com/shop/goods/goods_view.php?goodsno=41370',
            # 'https://www.kurly.com/shop/goods/goods_view.php?goodsno=57762',
            # 'https://www.kurly.com/shop/goods/goods_view.php?goodsno=35415',
            'https://www.kurly.com/shop/goods/goods_view.php?goodsno=29548',
            'https://www.kurly.com/shop/goods/goods_view.php?goodsno=29581',
            'https://www.kurly.com/shop/goods/goods_view.php?goodsno=57761',
            'https://www.kurly.com/shop/goods/goods_view.php?goodsno=57760',
            'https://www.kurly.com/shop/goods/goods_view.php?goodsno=52136',
            'https://www.kurly.com/shop/goods/goods_view.php?goodsno=52137'],
        ['https://www.kurly.com/shop/goods/goods_view.php?goodsno=45698',
         'https://www.kurly.com/shop/goods/goods_view.php?goodsno=37652',
         'https://www.kurly.com/shop/goods/goods_view.php?goodsno=45699',
         'https://www.kurly.com/shop/goods/goods_view.php?goodsno=37522',
         'https://www.kurly.com/shop/goods/goods_view.php?goodsno=37520'],
        ['https://www.kurly.com/shop/goods/goods_view.php?goodsno=53385',
         'https://www.kurly.com/shop/goods/goods_view.php?goodsno=44438',
         'https://www.kurly.com/shop/goods/goods_view.php?goodsno=53389',
         'https://www.kurly.com/shop/goods/goods_view.php?goodsno=53388',
         'https://www.kurly.com/shop/goods/goods_view.php?goodsno=53387',
         'https://www.kurly.com/shop/goods/goods_view.php?goodsno=53386',
         'https://www.kurly.com/shop/goods/goods_view.php?goodsno=51313'],
        ['https://www.kurly.com/shop/goods/goods_view.php?goodsno=37539',
         'https://www.kurly.com/shop/goods/goods_view.php?goodsno=37538',
         'https://www.kurly.com/shop/goods/goods_view.php?goodsno=37540',
         'https://www.kurly.com/shop/goods/goods_view.php?goodsno=37541']]
    for event_name, event_url in zip(event_name_list, goods_no_detail_list):
        print('event_name', event_name)
        event_ins, created = Event.objects.get_or_create(title=event_name)
        print('event', event_ins, created)
        for url in event_url:
            driver.get(url)
            driver.implicitly_wait(10)
            print('------------------------------------------- start ----------------------')
            # 안전빵
            transfer = None
            packing = None
            goods_origin = None
            goods_each = None
            allergy = None
            info = None
            expiration = None
            print(url)

            goods_image = driver.find_element_by_xpath(
                '/html/body/div/div[2]/div[2]/div/div[2]/div[2]/div/div[1]').get_attribute('style')
            goods_image = goods_image.split('"')
            print('goods_image', goods_image[1])

            goods_title = driver.find_element_by_xpath(
                '/html/body/div/div[2]/div[2]/div/div[2]/div[2]/div/p[1]/strong').get_attribute('innerText')
            print('goods_title', goods_title)

            short_desc = driver.find_element_by_xpath(
                '/html/body/div/div[2]/div[2]/div/div[2]/div[2]/div/p[1]/span[2]').get_attribute('innerText')
            print('short_desc', short_desc)

            try:
                # 미 할인 상품
                goods_price = driver.find_element_by_xpath(
                    '/html/body/div/div[2]/div[2]/div/div[2]/div[2]/div/p[2]/span[1]/span/span').get_attribute(
                    'innerText')
            except NoSuchElementException:
                # 할인 상품
                goods_price = driver.find_element_by_xpath(
                    '/html/body/div/div[2]/div[2]/div/div[2]/div[2]/div/p[3]/span[1]/span[1]/span[1]').get_attribute(
                    'innerText')

            price = re.findall('\d+', goods_price)
            result = ''
            for value in price:
                result += value
            print('price result', result)

            goods_each_innerText = driver.find_element_by_xpath(
                '/html/body/div/div[2]/div[2]/div/div[2]/div[2]/div/div[2]/dl[1]/dt').get_attribute('innerText')
            if '판매단위' in goods_each_innerText:
                goods_each = driver.find_element_by_xpath(
                    '/html/body/div/div[2]/div[2]/div/div[2]/div[2]/div/div[2]/dl[1]/dd').get_attribute(
                    'innerText')
                print('goods_each', goods_each)
            elif '배송구분' in goods_each_innerText:
                transfer = driver.find_element_by_xpath(
                    '/html/body/div/div[2]/div[2]/div/div[2]/div[2]/div/div[2]/dl[1]/dd').get_attribute(
                    'innerText')
                print('transfer', transfer)

            goods_each_weight = driver.find_element_by_xpath(
                '/html/body/div/div[2]/div[2]/div/div[2]/div[2]/div/div[2]/dl[2]/dd').get_attribute('innerText')
            print('goods_each_weight', goods_each_weight)

            # 배송 구분 또는 포장 타입
            try:
                transfer_innerText = driver.find_element_by_xpath(
                    '/html/body/div/div[2]/div[2]/div/div[2]/div[2]/div/div[2]/dl[3]/dt').get_attribute(
                    'innerText')
                if '배송구분' in transfer_innerText:
                    transfer = driver.find_element_by_xpath(
                        '/html/body/div/div[2]/div[2]/div/div[2]/div[2]/div/div[2]/dl[3]/dd').get_attribute(
                        'innerText')
                    print('transfer', transfer)
                elif '포장타입' in transfer_innerText:
                    packing = driver.find_element_by_xpath(
                        '/html/body/div/div[2]/div[2]/div/div[2]/div[2]/div/div[2]/dl[3]').get_attribute(
                        'innerText')
                    print('packing', packing)
            except NoSuchElementException:
                pass

            try:
                goods_origin_innerText = driver.find_element_by_xpath(
                    '/html/body/div/div[2]/div[2]/div/div[2]/div[2]/div/div[2]/dl[4]/dt').get_attribute(
                    'innerText')
                print(goods_origin_innerText)
                if '원산지' in goods_origin_innerText:
                    goods_origin = driver.find_element_by_xpath(
                        '/html/body/div/div[2]/div[2]/div/div[2]/div[2]/div/div[2]/dl[4]/dd').get_attribute(
                        'innerText')
                    print('goods_origin', goods_origin)
                elif '포장타입' in goods_origin_innerText:
                    packing = driver.find_element_by_xpath(
                        '/html/body/div/div[2]/div[2]/div/div[2]/div[2]/div/div[2]/dl[4]/dd').get_attribute(
                        'innerText')
                    print('transfer', packing)
            except NoSuchElementException:
                pass

            # 포장 정보 또는 알레르기
            try:
                goods_packing_innerText = driver.find_element_by_xpath(
                    '/html/body/div/div[2]/div[2]/div/div[2]/div[2]/div/div[2]/dl[5]/dt').get_attribute(
                    'innerText')
                if '포장' in goods_packing_innerText:
                    packing = driver.find_element_by_xpath(
                        '/html/body/div/div[2]/div[2]/div/div[2]/div[2]/div/div[2]/dl[5]/dd').get_attribute(
                        'innerText')
                    print('packing', packing)
                elif '알레르기' in goods_packing_innerText:
                    allergy = driver.find_element_by_xpath(
                        '/html/body/div/div[2]/div[2]/div/div[2]/div[2]/div/div[2]/dl[5]/dd').get_attribute(
                        'innerText')
                    print('allergy', allergy)
            except NoSuchElementException:
                packing = None
                allergy = None

            # 안내사항, 유통기한, 안내사항
            try:
                goods_info_innerText = driver.find_element_by_xpath(
                    '/html/body/div/div[2]/div[2]/div/div[2]/div[2]/div/div[2]/dl[6]/dt').get_attribute(
                    'innerText')
                if '안내' in goods_info_innerText:
                    info = driver.find_element_by_xpath(
                        '/html/body/div/div[2]/div[2]/div/div[2]/div[2]/div/div[2]/dl[6]/dd').get_attribute(
                        'innerText')
                    print('info', info)
                elif '유통기한' in goods_info_innerText:
                    expiration = driver.find_element_by_xpath(
                        '/html/body/div/div[2]/div[2]/div/div[2]/div[2]/div/div[2]/dl[6]/dd').get_attribute(
                        'innerText')
                    print('expiration', expiration)
                elif '알레르기정보' in goods_info_innerText:
                    allergy = driver.find_element_by_xpath(
                        '/html/body/div/div[2]/div[2]/div/div[2]/div[2]/div/div[2]/dl[6]/dd').get_attribute(
                        'innerText')
                    print('allergy', allergy)
            except NoSuchElementException:
                info = None
                expiration = None
                allergy = None

            try:
                image_one = driver.find_element_by_xpath(
                    '/html/body/div/div[2]/div[2]/div/div[3]/div/div[1]/div/div/div[1]/img').get_attribute('src')
                print('image_one', image_one)
            except NoSuchElementException:
                print('----------------------건너 뜁니다!!!')
                continue

            text__title = driver.find_element_by_xpath(
                '//*[@id="goods-description"]/div/div[1]/div[2]/h3/small').get_attribute('innerText')
            print('text__title', text__title)

            text__context_dummy = driver.find_element_by_xpath(
                '//*[@id="goods-description"]/div/div[1]/div[2]/h3').get_attribute('innerText')

            text__context_dummy = text__context_dummy.split('\n')
            text__context = ''
            for i in text__context_dummy[1:]:
                text__context += i + ' '
            print('text__context', text__context)

            text__description = driver.find_element_by_xpath(
                '//*[@id="goods-description"]/div/div[1]/div[2]/p').get_attribute('innerText')
            print('text__description', text__description)
            try:
                check_point_image = driver.find_element_by_xpath(
                    '//*[@id="goods-description"]/div/div/div/div/img').get_attribute('src')
                print('check_point_image', check_point_image)
            except NoSuchElementException:
                check_point_image = None

            info_image = driver.find_element_by_xpath(
                '//*[@id="goods_pi"]/p/img').get_attribute('src')

            # 이미지 생성
            try:
                GOODS_IMAGE_DIR = os.path.join(MEDIA_ROOT, f'goods/{goods_title}/')
                if not os.path.exists(GOODS_IMAGE_DIR):
                    os.makedirs(GOODS_IMAGE_DIR, exist_ok=True)
                image_save_name = os.path.join(GOODS_IMAGE_DIR, f'{goods_title}_goods_image.jpg')
                urllib.request.urlretrieve(goods_image[1], image_save_name)

                main_image = open(os.path.join(GOODS_IMAGE_DIR, f'{image_save_name}'), 'rb')

                image_save_name2 = os.path.join(GOODS_IMAGE_DIR, f'{goods_title}_info_image.jpg')
                urllib.request.urlretrieve(info_image, image_save_name2)

                info_image = open(os.path.join(GOODS_IMAGE_DIR, f'{image_save_name2}'), 'rb')

                image_save_name3 = os.path.join(GOODS_IMAGE_DIR, f'{goods_title}_image_one.jpg')
                urllib.request.urlretrieve(image_one, image_save_name3)

                extra_image = open(os.path.join(GOODS_IMAGE_DIR, f'{image_save_name3}'), 'rb')
            except FileNotFoundError:
                print(' 건너 뜁니다 !_________________________________________________')
                continue
            print('File')
            print(File(main_image))
            # try:
            #     goods_ins = Goods.objects.get(title=goods_title, price=result)
            #     created = False

            # except Goods.DoesNotExist:
            goods_ins = Goods.objects.create(
                img=File(main_image),
                info_img=File(info_image),
                title=goods_title,
                short_desc=short_desc,
                price=result,
                each=goods_each,
                weight=goods_each_weight,
                transfer=transfer,
                packing=packing,
                origin=goods_origin,
                allergy=allergy,
                info=info,
                expiration=expiration,
                event=event_ins,
            )
            created = True
            print('goods>>>>>>>>>>>>>>>>..', goods_ins, created)

            goods_explain, created = GoodsExplain.objects.get_or_create(
                img=File(extra_image),
                text_title=text__title,
                text_context=text__context,
                text_description=text__description,

                goods=goods_ins,
            )
            print('goods_explain, created', goods_explain, created)

            # 디테일 정보
            var_titles = driver.find_elements_by_xpath('//*[@id="goods-infomation"]/table/tbody/tr/th')
            var_descs = driver.find_elements_by_xpath('//*[@id="goods-infomation"]/table/tbody/tr/td')
            # print('var_titles>>>>>>>>>>>>>>>>>.', var_titles)
            # print('var_descs >>>>>>>>>>>>>>>>>>', var_descs)
            if len(var_titles) >= 1:
                for var_detail_title, var_detail_desc in zip(var_titles, var_descs):
                    detail_goods_title_ins, created = GoodsDetailTitle.objects.get_or_create(
                        title=var_detail_title.get_attribute('innerText')
                    )
                    # print(var_detail_title.get_attribute('innerText'))
                    # print(var_detail_desc.get_attribute('innerText'), '\n')
                    detail_ins, created = GoodsDetail.objects.get_or_create(
                        detail_title=detail_goods_title_ins,
                        detail_desc=var_detail_desc.get_attribute('innerText'),
                        goods=goods_ins,
                    )
                    # print('goods_detail_ins, created', detail_ins, created)
            # 타입 명시
            # print(type_name_ins)
            # print(goods_ins)
            # print(goodstype_ins, created)

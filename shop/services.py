from shop.models import Ip


def add_view_product(func):
    def get_client_ip(request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

    def view_ip_check(**kwargs):
        objects = func()
        ip = get_client_ip(objects['request'])
        product = objects['product']

        if Ip.objects.filter(ip=ip).exists():
            product.ip_view.add(Ip.objects.get(ip=ip))
        else:
            Ip.objects.create(ip=ip)
            product.ip_view.add(Ip.objects.get(ip=ip))
        return objects

    return view_ip_check

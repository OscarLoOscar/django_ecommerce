from .models import Order
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from .models import Order

# instance, the saved order in checkout(request,cart_id)
# created . true = new Order,false = updated order 
@receiver(post_save,sender=Order)
def send_order_confirmation(sender,instance,created,**kwargs):
  if instance.status=="Paid" and not instance.is_email_sent:
    item_list_text=""
    for item in instance.items.all():
      product_name = item.product.title if item.product else "已下架產品"
      item_list_text += f"- {product_name} x {item.quantity} (單價： ${item.price})\n"
    subject = f"Only_K - 訂單確認 #{instance.id}"

    message=(
      f"親愛的 {instance.user.username},\n\n"
            f"我哋已確認收到你嘅付款！以下係你嘅訂單詳情：\n"
            f"--------------------------\n"
            f"{item_list_text}" 
            f"--------------------------\n"
            f"總金額： ${instance.total_price}\n"
            f"送貨方式：{instance.get_delivery_method_display()}\n\n"
            f"我們會盡快安排發貨，謝謝支持！"
    )
    recipient_list = [instance.user.email]

    send_mail(
      subject,
      message,
      'freetousegpt@gmail.com',
      recipient_list,
      fail_silently=False
    )

    Order.objects.filter(id=instance.id).update(is_email_sent=True)
    print(f"DEBUG: 成功寄出訂單 #{instance.id} 嘅產品清單信畀 {instance.user.email}")
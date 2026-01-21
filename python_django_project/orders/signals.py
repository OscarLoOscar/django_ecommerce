from .models import Order
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
import os

# instance, the saved order in checkout(request,cart_id)
# created . true = new Order,false = updated order 
# @receiver(post_save,sender=Order)
# def send_order_confirmation(sender,instance,created,**kwargs):
#   if instance.status=="Paid" and not instance.is_email_sent:
#     item_list_text=""
#     for item in instance.items.all():
#       product_name = item.product.title if item.product else "已下架產品"
#       item_list_text += f"- {product_name} x {item.quantity} (單價： ${item.price})\n"
#     subject = f"Only_K - 訂單確認 #{instance.id}"

#     message=(
#       f"親愛的 {instance.user.username},\n\n"
#             f"我哋已確認收到你嘅付款！以下係你嘅訂單詳情：\n"
#             f"--------------------------\n"
#             f"{item_list_text}" 
#             f"--------------------------\n"
#             f"總金額： ${instance.total_price}\n"
#             f"送貨方式：{instance.get_delivery_method_display()}\n\n"
#             f"我們會盡快安排發貨，謝謝支持！"
#     )
#     recipient_list = [instance.user.email]

#     send_mail(
#       subject,
#       message,
#       'freetousegpt@gmail.com',
#       recipient_list,
#       fail_silently=False
#     )

#     Order.objects.filter(id=instance.id).update(is_email_sent=True)
#     print(f"DEBUG: 成功寄出訂單 #{instance.id} 嘅產品清單信畀 {instance.user.email}")

@receiver(post_save,sender=Order)
def order_status_notification(sender,instance,created,**kwargs):
  if created:
    return 
  
  item_list_text=""
  for item in instance.items.all():
    product_name = item.product.title if item.product else "已下架產品"
    item_list_text += f"- {product_name} x {item.quantity} (單價： ${item.price})\n"

  subject = ""
  body_header = ""
  body_footer = "謝謝支持！"

  if instance.status=="Paid" and not instance.is_paid_sent:
    subject = f"Only_K - 訂單付款確認 #{instance.id}"
    print(f"DEBUG_Paid: 準備寄信到 {instance.user.email}...")
    body_header = f"我哋已確認收到你嘅付款！我哋會盡快安排發貨。"
    Order.objects.filter(id=instance.id).update(is_paid_sent=True)

  elif instance.status == 'Shipping'and not instance.is_shipping_sent:
    subject = f"Only_K - 訂單準備發貨中 #{instance.id}"
    print(f"DEBUG_Shipping: 準備寄信到 {instance.user.email}...")
    body_header = f"好消息！你嘅訂單正喺度包裝緊，準備交畀快遞公司。"
    Order.objects.filter(id=instance.id).update(is_shipping_sent=True)

  elif instance.status == 'Shipped'and not instance.is_shipped_sent:
    subject = f"Only_K - 訂單已經出貨 #{instance.id}"
    print(f"DEBUG_Shipping_Shipped: 準備寄信到 {instance.user.email}...")
    body_header = f"你嘅訂單已經正式出貨喇！請留意物流電話。"  
    body_header += f"\n順豐單號: {instance.tracking_number}"
    Order.objects.filter(id=instance.id).update(is_shipped_sent=True)

  if subject:
      message = (
          f"親愛的 {instance.user.username},\n\n"
          f"{body_header}\n\n"
          f"--- 訂單詳情 ---\n"
          f"{item_list_text}"
          f"------------------\n"
          f"總金額： HK${instance.total_price}\n"
          f"送貨方式：{instance.get_delivery_method_display()}\n\n"
          f"{body_footer}"
      )
        
      try:
          send_mail(
              subject,
              message,
              'freetousegpt@gmail.com',# From
              # [instance.user.email],
              ['lokongkitoscar@gmail.com'],# To, must List
              fail_silently=False #deploy env set True , 費事因為Email Server斷線導致 Admin Save 唔到單
          )
          print(f"DEBUG_ENV: {os.getenv('EMAIL_USER')} / {os.getenv('EMAIL_PASS')}")
          print(f"DEBUG: 成功寄出狀態【{instance.status}】Email 畀 {instance.user.email}")
      except Exception as e:
          print(f"DEBUG: 寄信失敗 - {str(e)}")

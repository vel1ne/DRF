from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import Payment
from .services import PaymentService


@receiver(pre_save, sender=Payment)
def payment_pre_save(sender, instance, **kwargs):
    """"Обработчки перед сохранением платежа"""
    # Сохраняем предыдущий статус для отслеживания изменений
    if instance.pk:
        try:
            previous = Payment.objects.get(pk=instance.pk)
            instance._previous_status = previous.status
        except Payment.DoesNotExist:
            instance._previous_status = None


@receiver(post_save, sender=Payment)
def payment_post_save(sender, instance, created, **kwargs):
    """Обработчик сохранения платежа"""
    if not created and hasattr(instance, '-previous_status'):
        # Если статус измениялся на succeeded
        if (instance._previous_status in ['pending', 'processing'] and
            instance.status == 'succeedded'):
            PaymentService.process_successful_payment(instance)

        # Если статус изменился на failed
        elif (instance._previous_status in ['pending', 'processing'] and
              instance.status == 'failed'):
            PaymentService.process_failed_payment(instance)

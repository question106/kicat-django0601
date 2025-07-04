# Generated by Django 4.2.21 on 2025-06-10 07:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('quotes', '0002_quoteitem'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='quote',
            options={'ordering': ['-created_at'], 'verbose_name': '견적서', 'verbose_name_plural': '견적서'},
        ),
        migrations.AlterModelOptions(
            name='quoteitem',
            options={'ordering': ['created_at'], 'verbose_name': '견적 항목', 'verbose_name_plural': '견적 항목'},
        ),
        migrations.AlterModelOptions(
            name='quotestatus',
            options={'verbose_name': '견적 상태', 'verbose_name_plural': '견적 상태'},
        ),
        migrations.AlterModelOptions(
            name='servicecategory',
            options={'verbose_name': '서비스 카테고리', 'verbose_name_plural': '서비스 카테고리'},
        ),
        migrations.AlterModelOptions(
            name='servicetype',
            options={'verbose_name': '서비스 유형', 'verbose_name_plural': '서비스 유형'},
        ),
        migrations.AddField(
            model_name='quote',
            name='admin_notified',
            field=models.BooleanField(default=False, verbose_name='관리자 알림 전송됨'),
        ),
        migrations.AddField(
            model_name='quote',
            name='customer_notified',
            field=models.BooleanField(default=False, verbose_name='고객 알림 전송됨'),
        ),
        migrations.AddField(
            model_name='quote',
            name='last_notification_sent',
            field=models.DateTimeField(blank=True, null=True, verbose_name='마지막 알림 전송일'),
        ),
        migrations.AddField(
            model_name='quote',
            name='quote_sent_notified',
            field=models.BooleanField(default=False, verbose_name='견적서 발송 알림됨'),
        ),
        migrations.AlterField(
            model_name='quote',
            name='company',
            field=models.CharField(max_length=255, verbose_name='회사명'),
        ),
        migrations.AlterField(
            model_name='quote',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='생성일'),
        ),
        migrations.AlterField(
            model_name='quote',
            name='email',
            field=models.EmailField(max_length=254, verbose_name='이메일'),
        ),
        migrations.AlterField(
            model_name='quote',
            name='file',
            field=models.FileField(blank=True, null=True, upload_to='quotes/', verbose_name='첨부파일'),
        ),
        migrations.AlterField(
            model_name='quote',
            name='google_drive_link',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='구글 드라이브 링크'),
        ),
        migrations.AlterField(
            model_name='quote',
            name='message',
            field=models.TextField(verbose_name='메시지'),
        ),
        migrations.AlterField(
            model_name='quote',
            name='name',
            field=models.CharField(max_length=255, verbose_name='고객명'),
        ),
        migrations.AlterField(
            model_name='quote',
            name='phone',
            field=models.CharField(max_length=255, verbose_name='전화번호'),
        ),
        migrations.AlterField(
            model_name='quote',
            name='prepared_quote_pdf',
            field=models.FileField(blank=True, help_text='생성된 견적서 PDF', null=True, upload_to='prepared_quotes/', verbose_name='견적서 PDF'),
        ),
        migrations.AlterField(
            model_name='quote',
            name='service_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='quotes.servicetype', verbose_name='서비스 유형'),
        ),
        migrations.AlterField(
            model_name='quote',
            name='status',
            field=models.CharField(choices=[('pending', '대기중'), ('prepare_quote', '견적서 준비'), ('quote_sent', '견적서 발송'), ('work_in_progress', '작업중'), ('completed', '완료'), ('cancelled', '취소')], default='pending', max_length=255, verbose_name='상태'),
        ),
        migrations.AlterField(
            model_name='quote',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, verbose_name='수정일'),
        ),
        migrations.AlterField(
            model_name='quoteitem',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='생성일'),
        ),
        migrations.AlterField(
            model_name='quoteitem',
            name='item_description',
            field=models.CharField(help_text='서비스 또는 항목 설명', max_length=500, verbose_name='항목 설명'),
        ),
        migrations.AlterField(
            model_name='quoteitem',
            name='quantity',
            field=models.PositiveIntegerField(default=1, verbose_name='수량'),
        ),
        migrations.AlterField(
            model_name='quoteitem',
            name='quote',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='quotes.quote', verbose_name='견적서'),
        ),
        migrations.AlterField(
            model_name='quoteitem',
            name='total_price',
            field=models.DecimalField(decimal_places=2, help_text='총 가격 (수량 × 단가)', max_digits=10, verbose_name='총 금액'),
        ),
        migrations.AlterField(
            model_name='quoteitem',
            name='unit_price',
            field=models.DecimalField(decimal_places=2, help_text='원화 단위 가격', max_digits=10, verbose_name='단가'),
        ),
        migrations.AlterField(
            model_name='quoteitem',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, verbose_name='수정일'),
        ),
        migrations.AlterField(
            model_name='quotestatus',
            name='description',
            field=models.TextField(verbose_name='설명'),
        ),
        migrations.AlterField(
            model_name='quotestatus',
            name='name',
            field=models.CharField(max_length=255, verbose_name='상태명'),
        ),
        migrations.AlterField(
            model_name='servicecategory',
            name='description',
            field=models.TextField(blank=True, null=True, verbose_name='설명'),
        ),
        migrations.AlterField(
            model_name='servicecategory',
            name='name',
            field=models.CharField(max_length=255, verbose_name='카테고리명'),
        ),
        migrations.AlterField(
            model_name='servicetype',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='quotes.servicecategory', verbose_name='카테고리'),
        ),
        migrations.AlterField(
            model_name='servicetype',
            name='description',
            field=models.TextField(blank=True, null=True, verbose_name='설명'),
        ),
        migrations.AlterField(
            model_name='servicetype',
            name='is_active',
            field=models.BooleanField(default=True, verbose_name='활성화'),
        ),
        migrations.AlterField(
            model_name='servicetype',
            name='name',
            field=models.CharField(max_length=255, verbose_name='서비스명'),
        ),
    ]

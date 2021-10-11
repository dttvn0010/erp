# Generated by Django 3.2.7 on 2021-09-25 23:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_alter_user_phone'),
    ]

    operations = [
        migrations.AlterField(
            model_name='codesystem',
            name='code',
            field=models.CharField(max_length=100, verbose_name='Mã'),
        ),
        migrations.AlterField(
            model_name='codesystem',
            name='name',
            field=models.CharField(max_length=200, verbose_name='Tên'),
        ),
        migrations.AlterField(
            model_name='codesystem',
            name='status',
            field=models.CharField(choices=[('DRAFT', 'Nháp'), ('ACTIVE', 'Đang hoạt động'), ('RETIRED', 'Không còn sử dụng')], max_length=50),
        ),
        migrations.AlterField(
            model_name='coding',
            name='code',
            field=models.CharField(max_length=100, verbose_name='Mã'),
        ),
        migrations.AlterField(
            model_name='coding',
            name='display',
            field=models.CharField(max_length=200, verbose_name='Tên'),
        ),
        migrations.AlterField(
            model_name='company',
            name='address',
            field=models.CharField(blank=True, max_length=300, verbose_name='Địa chỉ'),
        ),
        migrations.AlterField(
            model_name='company',
            name='name',
            field=models.CharField(blank=True, max_length=200, verbose_name='Tên'),
        ),
        migrations.AlterField(
            model_name='company',
            name='phone',
            field=models.CharField(blank=True, max_length=20, verbose_name='Số điện thoại'),
        ),
        migrations.AlterField(
            model_name='company',
            name='status',
            field=models.CharField(choices=[('DRAFT', 'Nháp'), ('ACTIVE', 'Đang hoạt động'), ('INACTIVE', 'Ngừng hoạt động')], default='DRAFT', max_length=50),
        ),
        migrations.AlterField(
            model_name='modelproperty',
            name='code',
            field=models.CharField(max_length=100, verbose_name='Mã'),
        ),
        migrations.AlterField(
            model_name='modelproperty',
            name='datatype',
            field=models.CharField(choices=[('INTEGER', 'Integer'), ('FOREIGN_KEY', 'Foreign Key'), ('MANY_TO_MANY_FIELD', 'Many-To-Many Field'), ('BOOLEAN', 'codesystem.datatype.boolean'), ('FLOAT', 'Boolean'), ('DATE', 'Date'), ('DATETIME', 'Datetime'), ('STRING', 'String')], max_length=50, verbose_name='Loại dữ liệu'),
        ),
        migrations.AlterField(
            model_name='modelproperty',
            name='model',
            field=models.CharField(blank=True, max_length=200, verbose_name='Model'),
        ),
        migrations.AlterField(
            model_name='modelproperty',
            name='name',
            field=models.CharField(max_length=200, verbose_name='Tên'),
        ),
        migrations.AlterField(
            model_name='modelproperty',
            name='related_model',
            field=models.CharField(blank=True, max_length=200, verbose_name='Model liên kết'),
        ),
        migrations.AlterField(
            model_name='partner',
            name='partner_type',
            field=models.CharField(choices=[('CUSTOMER', 'Khách hàng'), ('COMPANY', 'Công ty'), ('AGENT', 'Đại lý')], max_length=50),
        ),
        migrations.AlterField(
            model_name='user',
            name='address',
            field=models.CharField(blank=True, max_length=300, verbose_name='Địa chỉ'),
        ),
        migrations.AlterField(
            model_name='user',
            name='address_block',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='core.addressblock', verbose_name='Khu vực'),
        ),
        migrations.AlterField(
            model_name='user',
            name='birth_date',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Ngày sinh'),
        ),
        migrations.AlterField(
            model_name='user',
            name='display',
            field=models.CharField(blank=True, max_length=100, verbose_name='Tên'),
        ),
        migrations.AlterField(
            model_name='user',
            name='gender',
            field=models.CharField(blank=True, choices=[('MALE', 'Nam'), ('FEMALE', 'Nữ'), ('OTHER', 'Khác'), ('UNKNOWN', 'Không xác định')], max_length=50, null=True, verbose_name='Giới tính'),
        ),
        migrations.AlterField(
            model_name='user',
            name='is_admin',
            field=models.BooleanField(blank=True, default=False, verbose_name='Là admin'),
        ),
        migrations.AlterField(
            model_name='user',
            name='phone',
            field=models.CharField(blank=True, max_length=20, verbose_name='Số điện thoại'),
        ),
        migrations.AlterField(
            model_name='user',
            name='profile_picture',
            field=models.ImageField(blank=True, null=True, upload_to='static/images/profiles', verbose_name='Ảnh đại diện'),
        ),
    ]
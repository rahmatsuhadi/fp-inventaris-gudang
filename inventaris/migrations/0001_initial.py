# Generated by Django 5.2.4 on 2025-07-20 16:29

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Kategori',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nama', models.CharField(max_length=100, unique=True)),
                ('deskripsi', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Pemasok',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nama_pemasok', models.CharField(max_length=150)),
                ('kontak_person', models.CharField(blank=True, max_length=100)),
                ('nomor_telepon', models.CharField(blank=True, max_length=20)),
                ('alamat', models.TextField(blank=True)),
                ('email', models.EmailField(blank=True, max_length=254, null=True, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Barang',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nama', models.CharField(max_length=100)),
                ('deskripsi', models.TextField(blank=True)),
                ('jumlah_stok', models.IntegerField(default=0)),
                ('harga_beli', models.FloatField(blank=True, null=True)),
                ('harga_jual', models.FloatField(blank=True, null=True)),
                ('kategori', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='inventaris.kategori')),
                ('pemasok', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='inventaris.pemasok')),
            ],
        ),
        migrations.CreateModel(
            name='Transaksi',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('jumlah', models.IntegerField()),
                ('tipe_transaksi', models.CharField(choices=[('MASUK', 'Barang Masuk'), ('KELUAR', 'Barang Keluar')], max_length=10)),
                ('tanggal_transaksi', models.DateTimeField(default=django.utils.timezone.now)),
                ('catatan', models.TextField(blank=True)),
                ('barang', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventaris.barang')),
            ],
        ),
    ]

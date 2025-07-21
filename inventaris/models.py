from django.db import models

from django.utils import timezone

# Create your models here.


class Kategori(models.Model):
    nama = models.CharField(max_length=100, unique=True)
    deskripsi = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nama

class Pemasok(models.Model):
    nama_pemasok = models.CharField(max_length=150)
    kontak_person = models.CharField(max_length=100, blank=True)
    nomor_telepon = models.CharField(max_length=20, blank=True)
    alamat = models.TextField(blank=True)
    email = models.EmailField(blank=True, null=True, unique=True)

    def __str__(self):
        return self.nama_pemasok

class Barang(models.Model):
    nama = models.CharField(max_length=100)
    deskripsi = models.TextField(blank=True)
    jumlah_stok = models.IntegerField(default=0)
    harga_beli = models.FloatField(blank=True, null=True)
    harga_jual = models.FloatField(blank=True, null=True)
    
    # Hubungan Foreign Key
    kategori = models.ForeignKey(Kategori, on_delete=models.SET_NULL, null=True, blank=True)
    pemasok = models.ForeignKey(Pemasok, on_delete=models.SET_NULL, null=True, blank=True)

    sku = models.CharField(max_length=50, unique=True, null=True, blank=True, help_text="Stock Keeping Unit")
    stok_minimum = models.IntegerField(default=10, help_text="Batas stok minimum untuk notifikasi")


    def __str__(self):
        return self.nama

class Transaksi(models.Model):
    TIPE_CHOICES = [
        ('MASUK', 'Barang Masuk'),
        ('KELUAR', 'Barang Keluar'),
    ]
    
    barang = models.ForeignKey(Barang, on_delete=models.CASCADE)
    jumlah = models.IntegerField()
    tipe_transaksi = models.CharField(max_length=10, choices=TIPE_CHOICES)
    tanggal_transaksi = models.DateTimeField(default=timezone.now)
    catatan = models.TextField(blank=True)
    harga_saat_transaksi = models.FloatField(null=True, blank=True, help_text="Harga satuan barang pada saat transaksi")

    def __str__(self):
        return f"{self.tipe_transaksi} - {self.barang.nama} ({self.jumlah})"

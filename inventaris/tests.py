

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Barang, Kategori, Pemasok, Transaksi

class InventarisModelTest(TestCase):

    def setUp(self):
        """Menyiapkan data awal untuk semua tes di kelas ini."""
        self.kategori = Kategori.objects.create(nama="Elektronik")
        self.pemasok = Pemasok.objects.create(nama_pemasok="PT Elektronik Jaya")
        self.barang = Barang.objects.create(
            nama="Laptop",
            jumlah_stok=10,
            harga_beli=10000,
            harga_jual=15000,
            kategori=self.kategori,
            pemasok=self.pemasok
        )

    def test_barang_str(self):
        """Tes representasi string dari model Barang."""
        self.assertEqual(str(self.barang), "Laptop")

    def test_kategori_str(self):
        """Tes representasi string dari model Kategori."""
        self.assertEqual(str(self.kategori), "Elektronik")

    def test_pemasok_str(self):
        """Tes representasi string dari model Pemasok."""
        self.assertEqual(str(self.pemasok), "PT Elektronik Jaya")


class InventarisViewTest(TestCase):

    def setUp(self):
        """Menyiapkan user dan data awal untuk tes view."""
        # Membuat user untuk login
        self.user = User.objects.create_user(username='testuser', password='password123')
        
        # Data untuk pengujian
        self.barang = Barang.objects.create(nama="Mouse", jumlah_stok=20, harga_jual=200)

    def test_redirect_if_not_logged_in(self):
        """Tes bahwa halaman akan redirect ke login jika user belum login."""
        response = self.client.get(reverse('index'))
        # 302 adalah kode status untuk redirect
        self.assertEqual(response.status_code, 302)
        # Memastikan redirect ke URL login
        self.assertRedirects(response, '/login/?next=/')

    def test_dashboard_view_if_logged_in(self):
        """Tes bahwa halaman dashboard bisa diakses setelah login."""
        self.client.login(username='testuser', password='password123')
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'inventaris/index.html')

    def test_barang_list_view(self):
        """Tes halaman daftar barang."""
        self.client.login(username='testuser', password='password123')
        response = self.client.get(reverse('barang_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Mouse") # Memastikan nama barang ada di halaman
        self.assertTemplateUsed(response, 'inventaris/barang_list.html')


class TransaksiLogicTest(TestCase):

    def setUp(self):
        """Menyiapkan user dan data barang untuk tes logika transaksi."""
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.client.login(username='testuser', password='password123')
        
        self.barang = Barang.objects.create(
            nama="Keyboard", 
            jumlah_stok=50, 
            harga_beli=1000, 
            harga_jual=1500
        )
        self.url_tambah_transaksi = reverse('transaksi_tambah')

    def test_transaksi_stok_masuk(self):
        """Tes bahwa transaksi STOK MASUK akan menambah jumlah stok."""
        # Stok awal adalah 50
        self.assertEqual(self.barang.jumlah_stok, 50)

        # Membuat request POST untuk transaksi masuk
        self.client.post(self.url_tambah_transaksi, {
            'barang': self.barang.pk,
            'jumlah': 10,
            'tipe_transaksi': 'MASUK',
        })

        # Ambil ulang data barang dari database
        self.barang.refresh_from_db()
        # Stok sekarang harus menjadi 60
        self.assertEqual(self.barang.jumlah_stok, 60)

    def test_transaksi_stok_keluar(self):
        """Tes bahwa transaksi STOK KELUAR akan mengurangi jumlah stok."""
        # Stok awal adalah 50
        self.assertEqual(self.barang.jumlah_stok, 50)

        # Membuat request POST untuk transaksi keluar
        self.client.post(self.url_tambah_transaksi, {
            'barang': self.barang.pk,
            'jumlah': 5,
            'tipe_transaksi': 'KELUAR',
        })

        self.barang.refresh_from_db()
        # Stok sekarang harus menjadi 45
        self.assertEqual(self.barang.jumlah_stok, 45)

    def test_transaksi_stok_keluar_gagal_jika_stok_kurang(self):
        """Tes validasi bahwa transaksi keluar tidak bisa melebihi stok."""
        # Stok awal adalah 50
        self.assertEqual(self.barang.jumlah_stok, 50)

        # Mencoba mengeluarkan 100 unit (lebih dari stok)
        response = self.client.post(self.url_tambah_transaksi, {
            'barang': self.barang.pk,
            'jumlah': 100,
            'tipe_transaksi': 'KELUAR',
        })

        self.barang.refresh_from_db()
        # Stok harus tetap 50 karena transaksi gagal
        self.assertEqual(self.barang.jumlah_stok, 50)
        # Memastikan form menampilkan error
        self.assertContains(response, "Jumlah keluar melebihi stok")
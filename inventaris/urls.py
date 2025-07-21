# inventaris/urls.py
from django.urls import path
from . import views

urlpatterns = [
    # Homepage
    path('', views.index, name='index'),

    # URL untuk Kategori
    path('kategori/', views.kategori_list, name='kategori_list'),
    path('kategori/tambah/', views.kategori_tambah, name='kategori_tambah'),
    path('kategori/edit/<int:pk>/', views.kategori_edit, name='kategori_edit'),
    path('kategori/hapus/<int:pk>/', views.kategori_hapus, name='kategori_hapus'),
    
    # URL untuk Pemasok
    path('pemasok/', views.pemasok_list, name='pemasok_list'),
    path('pemasok/tambah/', views.pemasok_tambah, name='pemasok_tambah'),
    path('pemasok/edit/<int:pk>/', views.pemasok_edit, name='pemasok_edit'),
    path('pemasok/hapus/<int:pk>/', views.pemasok_hapus, name='pemasok_hapus'),
    # ... (tambahkan path untuk edit & hapus pemasok) ...

    # URL untuk Barang
    path('barang/', views.barang_list, name='barang_list'),
    path('barang/tambah/', views.barang_tambah, name='barang_tambah'),
    path('barang/edit/<int:pk>/', views.barang_edit, name='barang_edit'),
    path('barang/hapus/<int:pk>/', views.barang_hapus, name='barang_hapus'),
    # ... (tambahkan path untuk edit & hapus barang) ...
    
    # URL untuk Transaksi
    path('transaksi/', views.transaksi_list, name='transaksi_list'),
    path('transaksi/<int:pk>/', views.transaksi_detail, name='transaksi_detail'), # <-- TAMBAHKAN INI
    path('transaksi/tambah/', views.transaksi_tambah, name='transaksi_tambah'),
]
# inventaris/forms.py
from django import forms
from .models import Kategori, Pemasok, Barang, Transaksi

class KategoriForm(forms.ModelForm):
    class Meta:
        model = Kategori
        fields = ['nama', 'deskripsi']
        widgets = {
            'nama': forms.TextInput(attrs={'class': 'form-control'}),
            'deskripsi': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

class PemasokForm(forms.ModelForm):
    class Meta:
        model = Pemasok
        fields = ['nama_pemasok', 'kontak_person', 'nomor_telepon', 'alamat', 'email']
        widgets = {
            'nama_pemasok': forms.TextInput(attrs={'class': 'form-control'}),
            'kontak_person': forms.TextInput(attrs={'class': 'form-control'}),
            'nomor_telepon': forms.TextInput(attrs={'class': 'form-control'}),
            'alamat': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }

class BarangForm(forms.ModelForm):
    class Meta:
        model = Barang
        fields = ['nama', 'sku', 'deskripsi', 'stok_minimum', 'harga_beli', 'harga_jual', 'kategori', 'pemasok']
        # Pastikan semua widget sudah memiliki class 'form-control' atau 'form-select'
        widgets = {
            'nama': forms.TextInput(attrs={'class': 'form-control'}),
            'sku': forms.TextInput(attrs={'class': 'form-control'}),
            'deskripsi': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'stok_minimum': forms.NumberInput(attrs={'class': 'form-control'}),
            'harga_beli': forms.NumberInput(attrs={'class': 'form-control'}),
            'harga_jual': forms.NumberInput(attrs={'class': 'form-control'}),
            'kategori': forms.Select(attrs={'class': 'form-select'}),
            'pemasok': forms.Select(attrs={'class': 'form-select'}),
        }

class TransaksiForm(forms.ModelForm):
    class Meta:
        model = Transaksi
        fields = ['barang', 'jumlah', 'tipe_transaksi', 'catatan']
        widgets = {
            'barang': forms.Select(attrs={'class': 'form-select'}),
            'jumlah': forms.NumberInput(attrs={'class': 'form-control'}),
            'tipe_transaksi': forms.Select(attrs={'class': 'form-select'}),
            'catatan': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
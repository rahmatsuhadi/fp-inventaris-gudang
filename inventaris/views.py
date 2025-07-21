# inventaris/views.py
from django.shortcuts import render, redirect, get_object_or_404
from .models import Kategori, Pemasok, Barang, Transaksi
from .forms import KategoriForm, PemasokForm, BarangForm, TransaksiForm
from django.db import transaction # Untuk memastikan integritas data

from django.db.models import Sum, F, Q, Value, FloatField, ExpressionWrapper ,Count

  # Import F, Q, dan Sum,Count 
from django.core.paginator import Paginator
from django.db.models.functions import Coalesce # Untuk menangani nilai NULL
from django.utils import timezone
from datetime import timedelta
# Import dekorator login_required
from django.contrib.auth.decorators import login_required

# Homepage
@login_required # <-- TAMBAHKAN INI
def index(request):
    """
    Menyiapkan data untuk ditampilkan di halaman dashboard utama.
    """
    # --- Kalkulasi untuk Kartu Statistik ---

    # Total jenis produk yang ada
    total_produk = Barang.objects.count()
    
    # Jumlah produk yang stoknya di bawah atau sama dengan batas minimum
    produk_stok_rendah_count = Barang.objects.filter(
        jumlah_stok__lte=F('stok_minimum')
    ).count()
    
    # Total pemasok yang terdaftar
    total_pemasok = Pemasok.objects.count()
    
    # Jumlah transaksi yang terjadi hari ini
    hari_ini = timezone.now().date()
    transaksi_hari_ini_count = Transaksi.objects.filter(
        tanggal_transaksi__date=hari_ini
    ).count()

    # --- Query untuk Daftar di Kartu ---

    # Mengambil 5 transaksi terakhir
    transaksi_terbaru = Transaksi.objects.select_related(
        'barang', 'barang__pemasok'
    ).order_by('-tanggal_transaksi')[:5]
    
    # Mengambil 5 barang dengan stok menipis
    barang_stok_menipis = Barang.objects.select_related('kategori').filter(
        jumlah_stok__lte=F('stok_minimum')
    ).order_by('jumlah_stok')[:5]

    # Menyiapkan context untuk dikirim ke template
    context = {
        'total_produk': total_produk,
        'produk_stok_rendah_count': produk_stok_rendah_count,
        'total_pemasok': total_pemasok,
        'transaksi_hari_ini_count': transaksi_hari_ini_count,
        'transaksi_terbaru': transaksi_terbaru,
        'barang_stok_menipis': barang_stok_menipis,
    }
    
    return render(request, 'inventaris/index.html', context)

# === Views untuk Kategori ===
@login_required # <-- TAMBAHKAN INI
def kategori_list(request):
    # Tambahkan .annotate() untuk menghitung barang di setiap kategori
    kategoris = Kategori.objects.annotate(
        jumlah_barang=Count('barang')
    ).order_by('nama')
    
    return render(request, 'inventaris/kategori_list.html', {'semua_kategori': kategoris})


@login_required # <-- TAMBAHKAN INI
def kategori_tambah(request):
    if request.method == 'POST':
        form = KategoriForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('kategori_list')
    else:
        form = KategoriForm()
    return render(request, 'inventaris/generic_form.html', {'form': form, 'title': 'Tambah Kategori Baru'})

@login_required # <-- TAMBAHKAN INI
def kategori_edit(request, pk):
    kategori = get_object_or_404(Kategori, pk=pk)
    if request.method == 'POST':
        form = KategoriForm(request.POST, instance=kategori)
        if form.is_valid():
            form.save()
            return redirect('kategori_list')
    else:
        form = KategoriForm(instance=kategori)
    return render(request, 'inventaris/generic_form.html', {'form': form, 'title': f'Edit Kategori: {kategori.nama}'})

@login_required # <-- TAMBAHKAN INI
def kategori_hapus(request, pk):
    kategori = get_object_or_404(Kategori, pk=pk)
    if request.method == 'POST':
        kategori.delete()
        return redirect('kategori_list')
    return render(request, 'inventaris/generic_delete_confirm.html', {'objek': kategori, 'title': 'Hapus Kategori'})


# === Views untuk Pemasok (Struktur sama dengan Kategori) ===
@login_required # <-- TAMBAHKAN INI
def pemasok_list(request):
    pemasoks = Pemasok.objects.all()
    return render(request, 'inventaris/pemasok_list.html', {'semua_pemasok': pemasoks})

@login_required # <-- TAMBAHKAN INI
def pemasok_tambah(request):
    if request.method == 'POST':
        form = PemasokForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('pemasok_list')
    else:
        form = PemasokForm()
    return render(request, 'inventaris/generic_form.html', {'form': form, 'title': 'Tambah Pemasok Baru'})

@login_required # <-- TAMBAHKAN INI
def pemasok_edit(request, pk):
    pemasok = get_object_or_404(Pemasok, pk=pk)
    if request.method == 'POST':
        form = PemasokForm(request.POST, instance=pemasok)
        if form.is_valid():
            form.save()
            return redirect('pemasok_list')
    else:
        form = PemasokForm(instance=pemasok)
    return render(request, 'inventaris/generic_form.html', {'form': form, 'title': f'Edit Pemasok: {pemasok.nama_pemasok}'})

@login_required # <-- TAMBAHKAN INI
def pemasok_hapus(request, pk):
    pemasok = get_object_or_404(Pemasok, pk=pk)
    if request.method == 'POST':
        pemasok.delete()
        return redirect('pemasok_list')
    return render(request, 'inventaris/generic_delete_confirm.html', {'objek': pemasok, 'title': 'Hapus Pemasok'})


# ... (buat juga view untuk edit dan hapus pemasok seperti contoh kategori) ...


# === Views untuk Barang (LENGKAP) ===
@login_required # <-- TAMBAHKAN INI
def barang_list(request):
    # Ambil data filter dari request GET
    search_query = request.GET.get('q', '')
    kategori_id = request.GET.get('kategori', '')

    # Query dasar
    queryset = Barang.objects.select_related('kategori', 'pemasok').all()

    # Logika Pencarian
    if search_query:
        queryset = queryset.filter(
            Q(nama__icontains=search_query) |
            Q(sku__icontains=search_query)
        )
    
    # Logika Filter Kategori
    if kategori_id:
        queryset = queryset.filter(kategori_id=kategori_id)

    # Kalkulasi untuk Kartu Statistik (berdasarkan hasil filter)
    total_produk = queryset.count()
    stok_rendah_count = queryset.filter(jumlah_stok__lte=F('stok_minimum')).count()
    
    # Kalkulasi Total Nilai (Stok * Harga Beli)
    total_nilai_inventaris_data = queryset.aggregate(
        total_nilai=Sum(F('jumlah_stok') * F('harga_beli'))
    )
    total_nilai_inventaris = total_nilai_inventaris_data['total_nilai'] or 0

    # Ambil semua kategori untuk dropdown filter
    semua_kategori = Kategori.objects.all()

    context = {
        'semua_barang': queryset,
        'semua_kategori': semua_kategori,
        'total_produk': total_produk,
        'stok_rendah_count': stok_rendah_count,
        'total_nilai_inventaris': total_nilai_inventaris,
        'search_query': search_query, # Untuk menampilkan kembali query di search box
        'selected_kategori': int(kategori_id) if kategori_id else None,
    }
    return render(request, 'inventaris/barang_list.html', context)

@login_required # <-- TAMBAHKAN INI
def barang_tambah(request):
    if request.method == 'POST':
        form = BarangForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('barang_list')
    else:
        form = BarangForm()
    return render(request, 'inventaris/generic_form.html', {'form': form, 'title': 'Tambah Barang Baru'})

@login_required # <-- TAMBAHKAN INI
def barang_edit(request, pk):
    barang = get_object_or_404(Barang, pk=pk)
    if request.method == 'POST':
        form = BarangForm(request.POST, instance=barang)
        if form.is_valid():
            form.save()
            return redirect('barang_list')
    else:
        form = BarangForm(instance=barang)
    return render(request, 'inventaris/generic_form.html', {'form': form, 'title': f'Edit Barang: {barang.nama}'})

@login_required # <-- TAMBAHKAN INI
def barang_hapus(request, pk):
    barang = get_object_or_404(Barang, pk=pk)
    if request.method == 'POST':
        barang.delete()
        return redirect('barang_list')
    return render(request, 'inventaris/generic_delete_confirm.html', {'objek': barang, 'title': 'Hapus Barang'})
    

# ... (buat juga view untuk edit dan hapus barang seperti contoh kategori) ...

@login_required # <-- TAMBAHKAN INI
def transaksi_list(request):
    search_query = request.GET.get('q', '')
    tipe_query = request.GET.get('tipe', '')
    tanggal_mulai_query = request.GET.get('tanggal_mulai', '')
    tanggal_selesai_query = request.GET.get('tanggal_selesai', '')

    transaksi_qs = Transaksi.objects.select_related('barang','barang__pemasok').all()

    # Logika Filter
    if search_query:
        transaksi_qs = transaksi_qs.filter(
            Q(barang__nama__icontains=search_query) |
            Q(barang__pemasok__nama_pemasok__icontains=search_query)
        )
    if tipe_query:
        transaksi_qs = transaksi_qs.filter(tipe_transaksi=tipe_query)
    if tanggal_mulai_query:
        transaksi_qs = transaksi_qs.filter(tanggal_transaksi__date__gte=tanggal_mulai_query)
    if tanggal_selesai_query:
        transaksi_qs = transaksi_qs.filter(tanggal_transaksi__date__lte=tanggal_selesai_query)


    # Kalkulasi Kartu Statistik
    total_transaksi = transaksi_qs.count()
    
    # PERBAIKAN KUNCI: output_field diterapkan langsung di dalam Sum()
    # nilai_masuk_data = transaksi_qs.filter(tipe_transaksi='MASUK').aggregate(
    #     total=Coalesce(Sum(
    #         F('jumlah') * F('harga_saat_transaksi'),
    #         output_field=FloatField()
    #     ), Value(0))
    # )

    
    nilai_masuk_data = transaksi_qs.filter(tipe_transaksi='MASUK').aggregate(
        total=Sum(ExpressionWrapper(
            F('jumlah') * F('harga_saat_transaksi'),
            output_field=FloatField()
        ))
    )

    nilai_masuk = nilai_masuk_data['total'] or 0

    nilai_keluar_data = transaksi_qs.filter(tipe_transaksi='KELUAR').aggregate(
        total=Sum(ExpressionWrapper(
            F('jumlah') * F('harga_saat_transaksi'),
            output_field=FloatField()
        ))
    )

    nilai_keluar = nilai_keluar_data['total'] or 0

    
    selisih = nilai_masuk - nilai_keluar

    # Anotasi untuk tabel dan Paginasi
    transaksi_qs = transaksi_qs.annotate(
        total_nilai=ExpressionWrapper(F('jumlah') * F('harga_saat_transaksi'), output_field=FloatField())
    ).order_by('-tanggal_transaksi')

    paginator = Paginator(transaksi_qs, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'total_transaksi': total_transaksi,
        'nilai_masuk': nilai_masuk,
        'nilai_keluar': nilai_keluar,
        'selisih': selisih,
        'search_query': search_query,
        'selected_tipe': tipe_query,
        'selected_tanggal_mulai': tanggal_mulai_query,
        'selected_tanggal_selesai': tanggal_selesai_query,
    }
    return render(request, 'inventaris/transaksi_list.html', context)

@login_required # <-- TAMBAHKAN INI
def transaksi_detail(request, pk):
    transaksi = get_object_or_404(
        Transaksi.objects.select_related('barang', 'barang__pemasok'), 
        pk=pk
    )
    # Anotasi untuk menghitung nilai transaksi ini saja
    transaksi.total_nilai = transaksi.jumlah * (transaksi.harga_saat_transaksi or 0)
    
    return render(request, 'inventaris/transaksi_detail.html', {'trx': transaksi})


@transaction.atomic # Menjaga data konsisten
@login_required # <-- TAMBAHKAN INI
def transaksi_tambah(request):
    if request.method == 'POST':
        form = TransaksiForm(request.POST)
        if form.is_valid():
            transaksi = form.save(commit=False)
            barang = transaksi.barang
            
            if transaksi.tipe_transaksi == 'MASUK':
                barang.jumlah_stok += transaksi.jumlah
                transaksi.harga_saat_transaksi = barang.harga_beli
            elif transaksi.tipe_transaksi == 'KELUAR':
                if barang.jumlah_stok < transaksi.jumlah:
                    form.add_error('jumlah', f'Jumlah keluar melebihi stok yang ada ({barang.jumlah_stok} unit)!')
                    # Cukup kembalikan form dan title
                    return render(request, 'inventaris/generic_form.html', {
                        'form': form,
                        'title': 'Buat Transaksi Baru'
                    })
                barang.jumlah_stok -= transaksi.jumlah
                transaksi.harga_saat_transaksi = barang.harga_jual

            barang.save()
            transaksi.save()
            
            return redirect('transaksi_list')
    else:
        form = TransaksiForm()

    # Context disederhanakan, hanya butuh form dan title
    context = {
        'form': form,
        'title': 'Buat Transaksi Baru'
    }
    # Render template generik
    return render(request, 'inventaris/generic_form.html', context)
<!--
.. date: 2018/08/09 00:40:00
.. slug: euler-8
.. title: (Euler 8) Çarpımı en büyük alt dizi
.. description: Bir dizi sayı içerisinde, çarpımı en yüksek alt diziyi bulacağız
.. tags: mathjax
-->


Belirtilen 1000 haneli sayıda, çarpımları en büyük olan 4 ardışık rakam 9 x 9 x 9 x 9 = 5832'dir

<pre>
73167176531330624919225119674426574742355349194934
96983520312774506326239578318016984801869478851843
85861560789112949495459501737958331952853208805511
12540698747158523863050715693290963295227443043557
66896648950445244523161731856403098711121722383113
62229893423380308135336276614282806444486645238749
30358907296290491560440772390713810515859307960866
70172427121883998797908792274921901699720888093776
65727333001053367881220235421809751254540594752243
52584907711670556013604839586446706324415722155397
53697817977846174064955149290862569321978468622482
83972241375657056057490261407972968652414535100474
82166370484403199890008895243450658541227588666881
16427171479924442928230863465674813919123162824586
17866458359124566529476545682848912883142607690042
24219022671055626321111109370544217506941658960408
07198403850962455444362981230987879927244284909188
84580156166097919133875499200524063689912560717606
05886116467109405077541002256983155200055935729725
71636269561882670428252483600823257530420752963450
</pre>

Çarpımları en büyük olan 13 ardışık rakamı bulunuz. Bu çarpım kaçtır? <!-- TEASER_END -->

İlk işimiz bu sayıyı Python'a aktarmak olacak.

    :::python
    sayi_dizisi = "".join("""73167176531330624919225119674426574742355349194934
    96983520312774506326239578318016984801869478851843
    85861560789112949495459501737958331952853208805511
    12540698747158523863050715693290963295227443043557
    66896648950445244523161731856403098711121722383113
    62229893423380308135336276614282806444486645238749
    30358907296290491560440772390713810515859307960866
    70172427121883998797908792274921901699720888093776
    65727333001053367881220235421809751254540594752243
    52584907711670556013604839586446706324415722155397
    53697817977846174064955149290862569321978468622482
    83972241375657056057490261407972968652414535100474
    82166370484403199890008895243450658541227588666881
    16427171479924442928230863465674813919123162824586
    17866458359124566529476545682848912883142607690042
    24219022671055626321111109370544217506941658960408
    07198403850962455444362981230987879927244284909188
    84580156166097919133875499200524063689912560717606
    05886116467109405077541002256983155200055935729725
    71636269561882670428252483600823257530420752963450""".splitlines())

Sayı dizisini satırlara bölünmüş olarak yapıştırdığımdan, düz bir sayı dizisi elde etmek için, satırları bölüp tekrar birleştirdim.

Kod yazmaya başlamadan önce, problem hakkında biraz akıl yürütelim. 100 karakterli bir sayı dizisinin 88 adet 13 haneli alt dizisi olacak.
Tüm 88 altdizi için, elemanları kendi içinde çarpıp, aralarından en büyük olanı bulabiliriz.

    :::python
    from operator import mul
    
    def elemanlari_carp(sayi_listesi):
        return reduce(mul, sayi_listesi)
    
    def euler8(sayi_dizisi, alt_dizi_uzunluk):
        
        sayi_dizisi = map(int, sayi_dizisi) # string olan sayıyı, sayı listesine çevir
        
        sayi_dizisi_uzunluk = len(sayi_dizisi)
        
        alt_diziler = [
            sayi_dizisi[i:(i+alt_dizi_uzunluk)] for i in range(sayi_dizisi_uzunluk - alt_dizi_uzunluk)
        ]
        
        alt_dizi_carpimlar = map(elemanlari_carp, alt_diziler)
        
        en_buyuk_carpim = max(alt_dizi_carpimlar)
        en_buyuk_carpimli_dizi = alt_diziler[alt_dizi_carpimlar.index(en_buyuk_carpim)]
        
        return (en_buyuk_carpim, en_buyuk_carpimli_dizi)
        
Evet, hepsi bu. Doğru sonuca ulaştık bile. Python gibi bir dille Euler Problemi çözmenin böyle bir dezavantajı var, C veya C++ gibi
daha alt seviye dillerde karşılaşmanız muhtemel bir takım zorlukları Python sizin için hallettiğinden, problemler birtakım eğitici
özelliklerini yitirebiliyor.

Her ne kadar 100 elemanlı bir dizi için, yapılabilecek optimizasyonları pratik faydası yok denecek kadar az olacak olsa da, egzersiz
amaçlı olarak birkaç şey deneyebiliriz. Öncelikle, problemi daha rahat analiz edebilmek için, biraz notasyon oluşturalım. Sayı dizisindeki
her bir elemanı \\(n\\) ile ifade edelim. Listedeki sırası \\(i\\) olan eleman da \\(n_i\\) olsun. Başlangıç indisi \\(i\\) ve uzunluğu \\(k\\)
olan altdizinin elemanları çarpımına da \\(P_{i,k}\\) diyelim. Burada ilk yapacağımız gözlem, iki ardışık altdizi arasındaki ilişki olacak;

$$
P_{i,k} = n_i \cdot n_{i+1} \cdot \dots \cdot n_{i+k-1} \\\\
P_{i+1,k} = n_{i+1} \cdot n_{i+2} \cdot \dots \cdot n_{i+k} \\\\
P_{i+1,k} = \frac{P_{i,k} \cdot n_{i+k}}{n_i}, n_i \neq 0
$$

Çok güzel, gelecek altdizinin çarpımını şu anki altdizinin çarpımı ve sınırdaki elemanlar cinsinden ifade ettik. Bu sayede bir miktar çarpım
işleminden kar etmiş olduk. Şu an tek problem, \\(n_i\\) teriminin sıfır olması ihtimali. O ihtimali ortadan kaldırmak için, içinde 0 olan
bölgeleri atlayabiliriz. Zaten içinde 0 olan bir bölgenin en büyük çarpımlı bölge olma ihtimali neredeyse yok. (Eğer tamamen yok demiş olsaydık,
içinde 0 olmayan bölgelerin varlığından emin olduğumuz anlamına gelecekti. Ancak, böyle bir varsayım yanlış olabilir.) Eğer listeyi tek geçişte
istediğimiz herşeyi hesaplarsak, en çabuk şekilde sonuca ulaşmış olacağız.

    :::python
    def euler8_v2(sayi_dizisi, alt_dizi_uzunluk):

        sayi_dizisi_uzunluk = len(sayi_dizisi)
        
        gecerli_altdize_baslangic = 0
        gecerli_altdize_bitis = 0
        
        ara_carpim = 1
        
        max_carpim = 0
        max_carpim_baslangic = 0
        
        while gecerli_altdize_bitis < sayi_dizisi_uzunluk:
            
            eleman = int(sayi_dizisi[gecerli_altdize_bitis])
            
            if eleman == 0:
                "icinde 0 olan bolgeyi atla"
                ara_carpim = 1
                gecerli_altdize_bitis += 1
                gecerli_altdize_baslangic = gecerli_altdize_bitis
                continue
                
            ara_carpim *= eleman
            
            if gecerli_altdize_bitis - gecerli_altdize_baslangic + 1 == alt_dizi_uzunluk:
                "Istedigimiz uzunlukta bir altdizeyi taradik"
                
                if ara_carpim > max_carpim:
                    "Bu bolgedeki ara carpim, simdiye kadar gordugumuzun en fazlasi"
                    max_carpim = ara_carpim
                    max_carpim_baslangic = gecerli_altdize_baslangic
                
                "Su anki bolgenin baslangicini bir eleman ileri aliyoruz"
                ilk_elem = int(sayi_dizisi[gecerli_altdize_baslangic])
                ara_carpim /= ilk_elem
                gecerli_altdize_baslangic += 1
                
            gecerli_altdize_bitis += 1
            
        return (max_carpim, sayi_dizisi[max_carpim_baslangic:(max_carpim_baslangic+alt_dizi_uzunluk)])
        
Her zaman olduğu gibi, optimizasyon yapabilmek için ince detayları kendimiz kontrol etmek zorunda kaldık ve böylece kodlarımızın
ne yaptığını bir bakışta görmek zorlaştı. Değişkenlerin isimlerini kasten uzun tuttum. Aşağıdaki resimler, bu algoritmanın `"2106554958"` sayısı
içindeki 3 elemanlı altdizeleri için çalışan versiyonunu anlatıyor. Rakamların üzerinde görünen aşağı dönmüş ok, `gecerli_altdize_bitis` değişkenini
ifade ediyor. Kırmızı ok ise `gecerli_altdize_baslangic` değişkeni için. Algoritma ilerledikçe, `max_carpim`, `max_carpim_baslangic` ve `ara_carpim`
değerlerinin nasıl değiştiğini takip edebilirsiniz.
        
<iframe src="/slideshow.html" style="width: 100%; height:220px; border:1px solid #ccc; border-radius: 1px;padding:0; margin-left:2em; margin-right:2em;"></iframe>

Her zamanki gibi, kodlarımızın performansını karşılaştıralım.

    >>> import timeit
    >>> timeit.timeit("euler8(sayi_dizisi,  13)","from euler8 import euler8, sayi_dizisi", number=10000)
    12.45510180960197
    >>> timeit.timeit("euler8_v2(sayi_dizisi,  13)","from euler8 import euler8_v2, sayi_dizisi", number=10000)
    7.013994897381153

Öyle görünüyor ki, emeğimizin karşılığını almışız. Bu problemle ilgili söylenebilecek daha fazla birşey yok sanırım.

## Gelecek Problem

Pisagor üçlüsü \\(a^2 + b^2 = c^2\\) eşiliğini sağlayan \\(a < b < c\\) üçlüsüne verilen isimdir. Örneğin, \\(3^2 + 4^2 = 9+16 = 25 = 5^2\\) gibi.

\\(a+b+c=1000\\) olan tek bir pisagor üçlüsü vardır. Bu üçlüde \\(a \cdot b \cdot c\\) çarpımını bulunuz.
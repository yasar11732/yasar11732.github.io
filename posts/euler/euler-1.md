<!--
.. date: 2018/07/16 23:52:00
.. slug: euler-1
.. title: (Euler 1) 3 ve 5'in katları
.. description: Project Euler problemlerini çözdüğüm bu yeni serinin ilk sayısında, en kolay Project Euler sorusunu çözeceğiz
-->

Merhabalar,

Blog'umda yeni yazı dizisine başlıyorum. [Project Euler](https://projecteuler.net/archives) sorularını, en kolaydan
en zora doğru, Python programlama dili kullanarak çözeceğiz. Bazı sorularda bonus olarak haskell dilinde de çözüm yazmayı
düşünüyorum. Python kullanarak programlama öğrenmek isteyen arkadaşlara faydalı olması dileklerimle, başlayalım... <!-- TEASER_END -->

[Project Eulerdeki 1 numaralı problem](https://projecteuler.net/problem=1) şu şekilde; Eğer 10'dan küçük sayılardan 3'ün
veya 5'in katları olan sayıları listelersek, 3,5,6 ve 9 sayılarını elde ederiz. Bu sayıların toplamı 23 eder. 1000den küçük sayılardan
3 veya 5'in katı olan sayıların toplamını bulunuz.

Tavsiye edilen okuma listesi;

 * [Kümeler](https://belgeler.yazbel.com/python-istihza/kumeler_ve_dondurulmus_kumeler.html#kumeler)
 * [Küme Üreteçleri](https://belgeler.yazbel.com/python-istihza/kumeler_ve_dondurulmus_kumeler.html#kume-uretecleri-set-comprehensions)
 * [Range Fonksiyonu](https://belgeler.yazbel.com/python-istihza/donguler.html#range-fonksiyonu)
 * [sum Fonksiyonu](https://belgeler.yazbel.com/python-istihza/sayilar.html#sum)

Problemin Çözümü için, 1000'den küçük sayıların içinde 3'ün katlarını ve 5'in katlarını bulmalı, daha sonra bu kümeleri toplamalıyız. İşin püf noktası ise,
hem 3'ün hem de 5'in katı olan sayıları, birden fazla işleme dahil etmemek. Bunun için liste kullanmak yerine Küme kullanacağız.

    :::python
    "1000'den küçük sayilardan 3'ün katlarini alalım"
    sayilar = set(range(3, 1000, 3))
    
    "5'in katlarını da deneyelim"
    sayilar.update(range(5, 1000, 5))
    
    "Şimdi toplamı alabiliriz."
    print(sum(sayilar))
    

###Alternatif Çözüm

    :::python
    sum(x for x in range(1000) if x % 3 == 0 or x % 5 == 0)
    

###Ek Alıştırma

Aynı problemi 2000'den küçük 7 ve 11'in katları için tekrar edin.

###Bonus (Haskell Versiyonu)
    
Burada dikkat edilmesi gereken nokta, Python'dan farklı olarak, haskell'in aralıktaki son noktayı işleme dahil etmesi. Bu nedenle, `[1..999]` yazılması gerekiyor.
    
    :::haskell
    sum [x | x <- [1..999], (x `mod` 3 == 0 || x `mod` 5 == 0)]
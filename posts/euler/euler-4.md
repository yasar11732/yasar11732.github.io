<!--
.. title: (Euler 4) Palindrom
.. slug: euler-4
.. date: 2018/07/24 23:10:00
.. tags: 
.. description: 3 haneli iki sayının çarpımı olan en büyük palindromu bulacağız
.. has_math: yes
-->

Palindrom bir sayı, hem baştan hem sondan aynı şekilde okunur. İki adet iki basamaklı sayının çarpımı ile elde edilebilecek en büyük palidrom \\(9009 = 91 × 99\\).

3-basamaklı sayıların çarpımı ile elde edilebilecek en büyük palindromu bulunuz. <!-- TEASER_END -->

Tersten okunuşu kendisi ile aynı olan cümle, kelime veya sayılara palindrom diyoruz. [Üstün Alsaç kişisel web sitesinde](https://web.archive.org/web/20160421051645/http://www.ustunalsac.com/lang/tr/oyunlar/palindromlar/palindrom-ornekleri-1)
bir çok Türkçe palindrom örneği bulabilirsiniz.

![Tersten konuşan adam](/images/20180723_212927.png)

Problem şu haliyle oldukça sade, bu nedenle doğrudan çözümüme geçeceğim;

    :::python
    from itertools import combinations_with_replacement

    def is_palindrom(number):
        num_str = str(number)
        return num_str == num_str[::-1]

    print(max(x for x in
        (a*b for (a,b) in combinations_with_replacement(range(100,1000),2))
        if is_palindrom(x)))
        
Kodları çalıştırdığımızda doğru cevabı \\(906609\\) olarak buluyoruz. Ziyadesiyle kolay oldu. Daha iyisini de yapabilir miyiz? Aynı
kodlar üzerinde ufak bir değişiklikle, 4 haneli iki sayının çarpımı olacak şekilde en büyük palindromu da bulabiliriz. `range(100,1000)`
kısmını `range(1000,10000)` olarak değiştirirsek, sonucu \\(99000099\\) olarak buluruz. Yalnız bu sefer sonucu almak biraz uzun sürecek.
Küçük bir optimizasyonla kodumuzu daha hızlı hale getirebiliriz. Öncelikle, ince ayar yapabilmek için, `combinations_with_replacement`
yerine, iki döngü kullanacağız.


    :::python
    def palindrom_test1(basla, bitir):
    max_palindrom = 0
    
    for i in range(basla, bitir):
        for k in range(i, bitir):
            p = i*k
            if is_palindrom(p):
                if p > max_palindrom:
                    max_palindrom = p
                    
    return max_palindrom
    
Bunun ilk çözümden bir farkı yok. `combinations_with_replacement` yerine, kendimiz döngü yazdık. Optimizasyon olarak, çarpma
ve test etme işlemini büyük sayılardan küçük sayılara doğru yaparsak, içiçe `for` döngülerinden erken çıkabiliriz.

    :::python
    def palindrom_test1(basla, bitir):
        max_palindrom = 0
        
        for i in range(bitir, basla, -1):
            for k in range(i, basla, -1):
                p = i*k
                
                "optimizasyonu saglayan sey burada"
                if p < max_palindrom:
                    break
                    
                if is_palindrom(p):
                    if p > max_palindrom:
                        max_palindrom = p
                        
        return max_palindrom

Kodları test ettiğim makinede (Python 2.7 4. nesil i7 laptop) orjinal fonksiyon ortamala 18 saniyede tamamlanırken, son hali
yalnızca yarım saniyede tamamlanıyor.

## Gelecek Problem

1den 10a kadar tüm sayılara kalansız bölünebilen en küçük sayı 2520'dir. 1den 20ye kadar tüm sayılara kalansız bölünebilen
en küçük sayı kaçtır.



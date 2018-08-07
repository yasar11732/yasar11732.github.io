<!--
.. date: 2018/08/07 21:40:00
.. slug: euler-7
.. title: (Euler 7) 10001. Asal Sayı
.. description: Belli Bir Sıradaki Asal Sayıları Sayacağız
.. tags: mathjax
-->


İlk 6 asal sayıyı listelersek:  2, 3, 5, 7, 11, ve 13, 6. asal sayının 13
olduğunu görürüz.

10001'inci asal sayı kaçtır. <!-- TEASER_END -->

[Euler-7 Silinmiş Sahneler](/euler/euler-7-silinmis-sahneler.html) yazısını okuduysanız, asal
sayılar konusunun dipsiz bir kuyu olduğunu anlamışsınızdır. Bu nedenle bu yazıda, ilk akla gelen
yöntemle, Eratosten kalburu yöntemini çalışma süresi açısından karşılaştırıp, yazıyı tamamlayacağım.
Öncelikle, sırasıyla sayıların asallığını kontrol edip, 10001 adet asal sayı bulan fonksiyona bakalım.
Çift sayılar asal sayı olamayacağı için, sadece tek sayıları kontrol edeceğiz. Bir sayıyı, yarısına eşit
veya küçük asal sayılara kalansız bölünmüyorsa, asal sayı olarak kabul edeceğiz. 

    :::python
    def euler7_basit(x):
        
        asallar = [2]
        test = 3
        
        while len(asallar) < x:
            
            kontrol_limit = int(test/2)
            asal_bulduk = True
            
            for asal in asallar:
                
                if asal > kontrol_limit:
                    break
                    
                if test % asal == 0:
                    asal_bulduk = False
                    break
                    
            if asal_bulduk:
                asallar.append(test)
                
            test += 2
        
        return asallar[x-1]
    
Basit ve işlevsel oldu. `euler7_basit(10001)` şeklinde bir çağrı ile sonuca erişebiliyoruz. Tabi ki, Eratosten kalburunu
burada bir yerde mutlaka kullanacağız. Yalnız, [3. Euler Problemi](/euler/euler-3.html) yazısında
kullandığımız `basit_sieve`, anlaşılır olması açısından, algoritmanın aslından biraz uzaklaşmıştı. Önce, bu fonksiyonu teknik
olarak doğru olacak şekilde tekrar yazalım.

    :::python
    from math import sqrt
    def basit_sieve2(limit):
        
        candidates = range(3, limit+1, 2)
        n = len(candidates)
        limit_sq_root = int(sqrt(limit))
        
        for i in range(n):
            c = candidates[i]
            if c > limit_sq_root:
                break
                
            if c != 0:
                i = int(c**2 / 2)-1
                slice_size = int((n - i - 1) / c) + 1
                candidates[i::c] = [0] * slice_size
                
        return [2] + [x for x in candidates if x != 0]
        
Güzeliz. Şimdi iki yöntemi birleştirelim. Belirli bir sayıya kadar olan asal sayıları `basit_sieve2` ile tespit edip, eksik
kalan sayıdaki asalları ise eski yöntemle tamamlayabiliriz. Peki, `basit_sieve2` yöntemini hangi sayıya kadar çalıştıracağız?
Eğer elde etmek istediğimiz asal sayı sayısına \\(x\\) dersek, \\(x * \log(x)\\) [iyi bir başlangıç gibi görünüyor.](https://math.stackexchange.com/a/2874304/65342)

    :::python
    from math import log
    def euler7_sieve(x):
        
        l = int(x * log(x))
        if l % 2 == 0:
            l = l+1
        
        asallar = basit_sieve2(l)
        test = l+2
        
        while len(asallar) < x:
            
            kontrol_limit = int(sqrt(test))
            asal_bulduk = True
            
            for asal in asallar:
                
                if asal > kontrol_limit:
                    break
                    
                if test % asal == 0:
                    asal_bulduk = False
                    break
                    
            if asal_bulduk:
                asallar.append(test)
                
            test += 2
        
        return asallar[x-1]
        
        
İki yöntem de bir hayli hızlı sonuç veriyor. Bu iki versiyonu yüzer kere çalıştırdığımda, ilk versiyon 5.52 saniyede tamamlanırken, ikinci
versiyon 1.2 saniyede tamamlanıyor. Mesele asal sayılarsa, genellikle eratosten kalburu ilk akla gelen çözüm olmalı. Her ne kadar
bu fonksiyonumuz üzerine koyulabilecek şeyler olsa da, sadece 7. problemde olduğumuzu hatırlayıp, abartmamak gerekir diye düşünüyorum.

## Gelecek Problem

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

Çarpımları en büyük olan 13 ardışık rakamı bulunuz. Bu çarpım kaçtır?
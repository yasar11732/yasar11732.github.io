<!--
.. date: 2018/08/20 00:57:00
.. slug: euler-10
.. title: (Euler 10) Asal Sayılar Toplamı
.. description: 2 milyondan küçük asal sayıları toplayacağız
.. tags: mathjax
-->

10'dan küçük asal sayıların toplamı \\(2 + 3 + 5 + 7 = 17\\) dir.

İki milyondan küçük asal sayıların toplamını bulunuz. <!-- TEASER_END -->

Bir başka asal sayı problemi. [7. Euler Problemi çözümünde](/euler/euler-7.html) yazdığımız `basit_sieve2` fonksiyonu ile bu problemi
kolayca çözebiliriz.

    :::python
    print(sum(basit_sieve2(2000000))
    
Bu problemin çözümünü bu kadar kısa tutmamak için, klasik kalbur yöntemine yapılabilecek geliştirmeleri biraz araştırdım. Sonuç olarak, aşağıdaki
fonksiyonu yazdım. ([Stackoverflowda daha hızlı çalışan fonksiyonlar var](https://stackoverflow.com/a/3035188/886669) ancak, daha anlaşılır olması
açısından, kendi yazdığım versiyonu kullanacağım.)

    :::python
    def basit_sieve3(limit):
        candidates = range(5, limit, 6)
        candidates.extend(range(7, limit, 6))
        
        candidates.sort()
        
        for i in xrange(int(limit ** 0.5) / 3 + 1):
            c = candidates[i]
            if c:
                candidates[(c*c/3)-1::2*c] = [0] * ((limit - c*c)/(6*c)+1)
                candidates[(c * (c+4-2*(c%3==2)) / 3)-1::2*c] = [0] * ((limit - c*(c+4-2*(c%3==2)) )/(6*c)+1)
                    
        return [2,3] + [x for x in candidates if x]
        
İlk görüşte bir hayli karışık geliyor, ancak, parça parça incelediğimizde her şey anlaşılır olacak. Öncelikle, burada yapılan optimizasyonun
ana fikrini anlamak için, [`basit_sieve`](/euler/euler-3.html) ve [`basit_sieve2`](/euler/euler-7) fonksiyonlarını karşılaştıralım.

    :::python
    from math import sqrt
    def basit_sieve(limit):
        sieve_limit = sqrt(limit)

        primes = []
        candidates = range(2, limit+1)

        while len(candidates) > 0:
            next_prime = candidates.pop(0)
            primes.append(next_prime)
            candidates = [x for x in candidates if x % next_prime != 0]

            if next_prime > sieve_limit:
                primes.extend(candidates)
                candidates = []

        return primes
        
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
        
Burada dikkat çekmek istediğim kısım, muhtemel asal sayı listelerinin nasıl oluşturulduğu. Önceki versiyonda, `candidates = range(2, limit+1)` iken,
sonraki versiyonda `candidates = range(3, limit+1, 2)` olarak yazdık. İkinci versiyonda, 3'den başlayarak, sadece tek sayıları listeledik. Bunun
nedeni, çift sayıların asal sayı olamayacağını biliyor olmamız. Peki, bu fikri daha ileriye götürebilir miyiz? Mesela, 2 ve 3'ün katları olmayan
sayıları listeleyerek başlayabilir miyiz? Evet, yapabiliriz. 

    :::python
    candidates = range(5, limit, 6)
    candidates.extend(range(7, limit, 6))
    
    candidates.sort()
    
    
Bu kodlar çalıştıdığında, örneğin `limit = 50` ise, `candidates = [5, 7, 11, 13, 17, 19, 23, 25, 29, 31, 35, 37, 41, 43, 47, 49]` olacak. Peki, bunun
avantajı ne? Üzerinde çalıştığımız listenin uzunluğu, limitimizin üçte birine düştü. Bu avantajla birlikte, başka bir komplikasyon karşımıza çıkıyor.
Listede olması gereken sayıların üçte ikisi yerinde olmadığı için, indekslerin ona göre kayıdırılması lazım. Aşağıdaki kısımların yaptığı da tam olarak bu;

    :::python
    candidates[(c*c/3)-1::2*c] = [0] * ((limit - c*c)/(6*c)+1)
    candidates[(c * (c+4-2*(c%3==2)) / 3)-1::2*c] = [0] * ((limit - c*(c+4-2*(c%3==2)) )/(6*c)+1)
    
Kodların karmaşasını ortadan kaldırmak için, küçük parçalar halinde inceleyeceğiz. Öncelikle, eskiden, asal sayı olmayan sayıları bir hamlede
elekten geçirirken (`candidates[i::c] = [0] * slice_size`), şimdi, bunu iki kısım halinde yapıyoruz. Böylece, elememiz gereken sayıların indekslerini
çok daha kolay bir şekilde hesaplayabileceğiz. Bu işlemi iki parçada yaptığımız için, dilimlemede kullandığımız adım, `c` yerine `2*c` oldu. Önceki
seferde olduğu gibi, asal sayıların katlarını elemeye, o döngüde bulduğumuz asal sayının karesi ile başlıyoruz. Ancak, sayıların üçte ikisi yerinde
olmadığında, asal sayının karesinin listedeki yerini `c*c/3` olarak hesapladık. Sıfır tabanlı indeksleme yaptığımız için, `-1` eklememiz
gerekti. `((limit - c*c)/(6*c)+1)` kısmı ise, klasik ardışık sayılarda terim sayısı formülü (\\(\text{terim sayisi} = \frac{\text{son terim} - \text{ilk terim}}{\text{artis miktari}} + 1\\))
Artış miktarı `6*c` çünkü, listede `2*c` adımlar atıyoruz, ve sayıların `1/3`ü yerinde yok.

Asıl bomba şimdi geliyor. İkinci kısımdaki başlangıç noktasını bulmak için, asal sayıyı, ya iki fazlasıyla, ya da dört fazlasıyla çarpacağız. Nedenine gelirsek,
eğer bulduğumuz asal sayının iki fazlası, 3'ün tam katı ise, `c * (c+2)`listede bulunmayacaktır. Çünkü, 3'ün katların daha listeyi oluştururken elemiştik. Peki, 2 veya 4 olduğuna
nasıl karar vereceğiz? Öncelikle, ardışık tek sayıların mod 3'deki değerlerine bir göz atalım. 

$$
\begin{align}
5 \equiv 2 &(mod 3)\\\\
7 \equiv 1 &(mod 3)\\\\
9 \equiv 0 &(mod 3)\\\\
11 \equiv 2 &(mod 3)\\\\
13 \equiv 1 &(mod 3)\\\\
\end{align}
$$

Yukarıdaki denklikleri incelersek, \\(n \equiv 2 (mod 3)\\) olduğunda 2 artırmamız, \\(n \equiv 1 (mod 3)\\) olduğunda ise 4 artırmamız gerektiği
anlaşılıyor. \\(n \equiv 0 (mod 3)\\) olduduğu bir durum olamaz, çünkü, bu sayıları zaten baştan eledik. `c+4-2*(c%3==2)` ifadesi, `c`nin değerine
göre, `c+2` veya `c+4` sayılarına eşit oluyor. Böylece, başlangıç noktasını hesaplayabiliyoruz. Programın geri kalanının, daha önce gördüklerimizden
bir farkı yok. Şimdi de, zamanlamaya bir göz atalım.

    >>> import timeit
    >>> timeit.timeit("sum(basit_sieve2(2000000))", "from euler10 import basit_sieve2", number=100)
    29.754030365461645
    >>> timeit.timeit("sum(basit_sieve3(2000000))", "from euler10 import basit_sieve3", number=100)
    24.98745897986229
    
Yaklaşık yüzde 16 hız kazandık. Fonksiyonumuzun zaten bir hayli hızlı olduğunu göz önünde bulundurursak, gayet iyi bir performans artışı.

## Kaynakça

 - [The Genuine Sieve of Eratosthenes](https://www.cs.hmc.edu/~oneill/papers/Sieve-JFP.pdf)
 - [Lazy wheel sieves and spirals of primes](http://eprints.whiterose.ac.uk/3784/1/runcimanc1.pdf)
 - [Fastest way to list all primes below N](https://stackoverflow.com/a/3035188/886669)
 
## Gelecek Problem

Aşağıdaki 20x20 şeklinde dizilmiş sayılardan, köşegen üzerinde bulunan 4 tanesi kırmızıyla işaretlenmiştir.

<p style="font-family:'courier new';text-align:center;font-size:10pt;">
08 02 22 97 38 15 00 40 00 75 04 05 07 78 52 12 50 77 91 08<br>
49 49 99 40 17 81 18 57 60 87 17 40 98 43 69 48 04 56 62 00<br>
81 49 31 73 55 79 14 29 93 71 40 67 53 88 30 03 49 13 36 65<br>
52 70 95 23 04 60 11 42 69 24 68 56 01 32 56 71 37 02 36 91<br>
22 31 16 71 51 67 63 89 41 92 36 54 22 40 40 28 66 33 13 80<br>
24 47 32 60 99 03 45 02 44 75 33 53 78 36 84 20 35 17 12 50<br>
32 98 81 28 64 23 67 10 <span style="color:#ff0000;"><b>26</b></span> 38 40 67 59 54 70 66 18 38 64 70<br>
67 26 20 68 02 62 12 20 95 <span style="color:#ff0000;"><b>63</b></span> 94 39 63 08 40 91 66 49 94 21<br>
24 55 58 05 66 73 99 26 97 17 <span style="color:#ff0000;"><b>78</b></span> 78 96 83 14 88 34 89 63 72<br>
21 36 23 09 75 00 76 44 20 45 35 <span style="color:#ff0000;"><b>14</b></span> 00 61 33 97 34 31 33 95<br>
78 17 53 28 22 75 31 67 15 94 03 80 04 62 16 14 09 53 56 92<br>
16 39 05 42 96 35 31 47 55 58 88 24 00 17 54 24 36 29 85 57<br>
86 56 00 48 35 71 89 07 05 44 44 37 44 60 21 58 51 54 17 58<br>
19 80 81 68 05 94 47 69 28 73 92 13 86 52 17 77 04 89 55 40<br>
04 52 08 83 97 35 99 16 07 97 57 32 16 26 26 79 33 27 98 66<br>
88 36 68 87 57 62 20 72 03 46 33 67 46 55 12 32 63 93 53 69<br>
04 42 16 73 38 25 39 11 24 94 72 18 08 46 29 32 40 62 76 36<br>
20 69 36 41 72 30 23 88 34 62 99 69 82 67 59 85 74 04 36 16<br>
20 73 35 29 78 31 90 01 74 31 49 71 48 86 81 16 23 57 05 54<br>
01 70 54 71 83 51 54 69 16 92 33 48 61 43 52 01 89 19 67 48<br></p>

Bu sayıların çarpımı 26 × 63 × 78 × 14 = 1788696 yapar.

Bu sayıların içerisinde, yatay, dikey veya çapraz olarak ardışık
4 sayının çarpımı en fazla kaçtır?
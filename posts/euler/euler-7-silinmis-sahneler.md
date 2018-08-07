<!--
.. date: 2018/08/07 21:25:00
.. slug: euler-7-silinmis-sahneler
.. title: (Euler 7) 10001. Asal Sayı (SİLİNMİŞ SAHNELER)
.. description: Euler 7 çözümü ilk denemesi
.. tags: mathjax
-->

Bu yazıya 7. Euler Probleminin çözümüyle ilgili birşeyler yazma niyetiyle başlamıştım. Ancak, yazdıkça
asıl konudan çok uzaklaştığımı farkedip, yeniden başlamaya karar verdim. Yine de, yazdıklarımı kaybetmek
istemedim, olduğu kadarıyla yayınlıyorum.


<!-- TEASER_END -->
İlk 6 asal sayıyı listelersek:  2, 3, 5, 7, 11, ve 13, 6. asal sayının 13
olduğunu görürüz.

10001'inci asal sayı kaçtır.

[3. Euler problemi çözümünde](/euler/euler-3.html) belli bir aralıktaki asal
sayıları tespit etmek için Eratosten Kalburu yöntemini kullanmıştık. Bu
yöntemde, belli bir aralıktaki asal sayıları tespit etmek için, asal olduğunu
kanıtladığımız sayıların katlarını listeden silme yöntemini kullandık. Bu
yöntem sayesinde, hızlı bir şekilde asal sayı tespiti yapabilmiştik.
Hatırlatma amacıyla, kodlarımıza tekrar bir göz atalım.

    :::python
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
        
    def gelismis_sieve(limit, known_primes):

        if not known_primes:
            return basit_sieve(limit)
            
        sieve_limit = sqrt(limit)
        
        primes = known_primes[:]
        
        candidates = range(known_primes[-1]+1, limit+1)
        
        
        for prime in known_primes:
            if prime > sieve_limit:
                primes.extend(candidates)
                candidates = []
                break
            candidates = [x for x in candidates if x % prime != 0]
            
        while len(candidates) > 0:
            next_prime = candidates.pop(0)
            primes.append(next_prime)
            candidates = [x for x in candidates if x % next_prime != 0]
            
            if next_prime > sieve_limit:
                primes.extend(candidates)
                candidates = []
                
        return primes

Euler Problemleri orjinal olarak modern bilgisayalara nazaran çok daha zayıf
bilgisayalar göz önünde bulunarak tasarlandığı için, biz euler problemini
100001. asal sayı için çözeceğiz. Hedefimiz, bu sonuca 1sn'den daha hızlı bir
şekilde ulaşmak. Bu problemin çözümü için, `basit_sieve` yöntemini doğrudan
kullanamayız, çünkü, 100001. asal sayıyı tespit etmek için, kaçıncı sayıya
kadar olan asal sayıları bulmamız gerektiğini bilmiyoruz. Bu nedenle, 100001.
asal sayıya ulaşana dek, `gelismis_sieve` fonksiyonunu çalıştıracağız. İlk
denemem aşağıdaki şekilde olacak:

    :::python
    def euler7(x):
        
        p = [2,3,5,7]
        
        while len(p) < x:
            p = gelismis_sieve(2*max(p), p)
            
        return p[x-1]
        
        
Bu kodlar 100001. asal sayı için benim bilgisayarımda ortalama 6.3sn'de
tamamlanıyor. Daha iyisini yapabilir miyiz? Burada akla gelen ilk optimizasyon,
 `gelismis_sieve` fonksiyonunun çağrılma sayısını azaltmak, hatta mümkün
olursa, bu fonksiyonun yerine, sadece `basit_sieve` fonksiyonu ile sonuca
ulaşmak. Çünkü, `gelismis_sieve` çalışabilmek için, `basit_sieve` fonksiyonun
yaptığı bazı işlemleri tekrar etmek zorunda olduğundan, performans kaybına yol
açıyor.

Küçük bir gözlemle, hesap yapmaya çok daha iyi bir noktadan başlayabiliriz.
Dikkat ederseniz, bir sayıya kadar olan asalların sayısı o sayının yarısından
fazla olamaz. Örneğin, 100'e kadar olan asal sayılar en fazla 50 adet olabilir,
 çünkü, 2 hariç çift sayılar asal olamazlar. İkinin kendisi asal sayı olduğu 
için bu sınırın 51 olması gerektiğini düşünebilirsiniz, ancak, 1 sayısı asal
olmadığından hesap tekrar 50'ye geri düşüyor. Bir sayıya kadar olan asalların
sayısını veren fonksiyona \\(\pi(x)\\) dersek, \\(\pi(x)<=\frac{x}{2}\\)
olduğunu kanıtlamış olduk. Programın başlangıç parametleri biraz daha optimize
olduğundan, her döngüde üst sınırı 2 kat artırmak yerine, 1.6 kat artırmak daha
uygun olur tahmininden yola çıkarak (1.6 tamamen tahmin üzerine verilmiş bir
değer, siz bununla oynayarak farklı ihtimaller deneyebilirsiniz), kodları
aşağıdaki şekilde revize edebiliriz.

    :::python
    def euler7(x):
        
        p = basit_sieve(2*x)
        
        while len(p) < x:
            p = gelismis_sieve(int(1.6*max(p)), p)
            
        return p[x-1]
        
Yukardaki versiyon benim bilgisayarımda 1.9-2.0 saniye ortalamasında sonuç
veriyor. İlk versiyona göre oldukça başarılı. Daha iyisini yapabilir miyiz?
İkinin katlarını hesapladığımız gibi, üçün katlarını da hesaba dahil ederek,
ilk tahmini biraz daha güçlendirebiliriz.Yeni tahminimiz
\\(\pi(x) <= x - \frac{x}{2} - \frac{x}{3} + \frac{x}{6}\\). Bu aralıkta hem
ikinin hem de üçün katı olan sayılar iki kere çıkarma işlemine tabi
tutulduğundan, hesabı düzeltmek için altının katı olan sayıları tekrar tahmine
ekledik. Yukarıdaki ifadeyi sadeleştirirsek, yeni tahminimiz
\\(\pi(x)<=\frac{x}{3}\\) oldu. Kodları tekrar revize edebiliriz.

    :::python
    def euler7(x):
        
        p = basit_sieve(3*x)
        
        while len(p) < x:
            p = gelismis_sieve(int(1.2*max(p)), p)
            
        return p[x-1]
        
Bu kodları çalıştırdığımda, yaklaşık olarak ikinci versiyonla aynı sonucu
aaldım. Ciddi bir ilerleme kaydedemedik gibi görünüyor.

Peki `basit_sieve` fonksiyonunu tamamen bir kenara bırakamaz mıyız? Netice
itibariyle, ilk yüzbin asal sayının hangileri olduğunu bilmemize gerek yok.
Ancak, bunu yapabilmek için, ilk yüzbin asal sayıyı bilmeden, yüzbinbirinci
sırada olduğumuzu bilmemiz gerekiyor. Bunu yapabilmek için de, \\(\pi(x)\\)
değerini tahmini olarak değil, tam olarak hesaplamamız gerek. \\(\pi(x)\\)'i
tam olarak hesaplayabildiğimiz durumda x yerine farklı sayılar deneyerek,
\\(\pi(300000)<1000<\pi(1500000)\\) benzeri bir eşitsizlik elde edip, aralığı
daralta daralta istediğimiz sayıya ulaşabiliriz.

Eğer 2'nin ve 3'ün katlarında yaptığımız gibi, belli bir aralıktaki sayıların
içinden, asal sayıların katları olan - dolayısıyla asal olmayan - sayıları
çıkarırsak, geriye sadece asal sayılar kalır. Bizim istediğimiz de bu. Bir tek
problemimiz var, 2'nin, 3'ün ve 5'in katsayılarını silmek istediğimizde işler
bir adım daha karmaşıklaşacak. \\(S(2)\\) ikinin katlarının sayısı, \\(S(3)\\)
üçün katlarının sayısı, \\(S(5)\\)'in katlarının sayısı dersek;

$$\begin{eqnarray} 
S(2 \cup 3 \cup 5) &= S(2) + S(3) + S(5) \\\\
                   & -(S(2 \cap 3) + S(2 \cap 5) + S(3 \cap 5)) \\\\
                   & + S(2 \cap 3 \cap 5) \\\\
\end{eqnarray}$$

Elemek istediğimiz asal sayılar, birkaçdan daha fazla olduğunda nasıl bir yöntem
izleyeceğiz?

## Ekleme - Çıkarma Prensibi

Yukarıda kullandığımız yöntemin daha genel şekline Kombinatorik teoride Ekleme-Çıkarma
prensibi demişler. Prensibin genel şekli matematik notasyonunda aşağıdaki şekilde gösterilir.

$$
\begin{align}
\left|\bigcup_{i=1}^n A_i\right| = {} & \sum_{i=1}^n |A_i| - \sum_{1 \le i < j \le n} |A_i\cap A_j| + \cdots {} \\\\
& {} \cdots + \sum_{1 \le i < j < k \le n} |A_i \cap A_j\cap A_k| - \cdots + (-1)^{n-1} \left|A_1\cap\cdots\cap A_n\right|.
\end{align}
$$

Birçok garip sembol, büyüklü küçüklü harfler falan, formül kafa karıştırmasın. Biz kelimelerle ifade
edelim. Birden fazla kümenin birleşiminin eleman sayısını hesaplarken, önce kümelerin teker teker eleman
sayılarını toplayacağız. Daha sonra, ikili kesişimlerinin eleman sayılarını çıkaracağız. Sonra 3'lü kesişimlerinin
eleman sayılarını geri ekleyeceğiz, sonra 4lü kesişimlerinin eleman sayılarını geri çıkaracağız, vs... Adı üstünde
ekleme çıkarma prensibi. Prensip güzelmiş, Python ile yapalım. Birden başlayıp, bir üst sınıra kadar olan sayılar içinde,
listemizdeki sayılara bölünmeyen kaç sayı olduğunu hesaplayalım.

    :::python
    from itertools import combinations
    from functools import reduce
    from operator import mul

    def ekle_cikar(limit, sayilar):
        
        return limit - sum(
            (-1)**i * int(limit / reduce(mul, grb) )
            for i in range(len(sayilar))
            for grb in combinations(sayilar, i+1)
        )
        
Fonksiyon güzel oldu, küçük birkaç modifikasyon ile \\(\pi(x)\\) fonksiyonunu kesin olarak hesaplayabiliriz.

## Legendre’nin Formulü
 
$$
\pi(x) + 1 = \pi(\sqrt{x}) + \lfloor x \rfloor - \sum_{p_i \leq \sqrt{x}} \left \lfloor \frac{x}{p_i} \right \rfloor + \sum_{p_i < p_j \leq \sqrt{x}} \left \lfloor \frac{x}{p_i p_j} \right \rfloor - \sum_{p_i < p_j < p_k \leq \sqrt{x}} \left \lfloor \frac{x}{p_i p_j p_k} \right \rfloor + \dots
$$

Eratosten kalburu yönteminden bildiğimiz üzere, 1 ile \\(n\\) arasındaki asal sayıları bulmak için, kalburu \\(\sqrt{n}\\) sayısına kadar
işletiyoruz. Neden? Diyelim ki, 2..100 aralığındaki asal sayıları bulmak istiyoruz. Bunun için bu aralıktaki 2, 3, 5 ve 7 sayılarının katlarını
temizliyoruz. 11 ve daha büyük asalların katlarını temizlemeye ihtiyacımız yok, çünkü, bunların katları aynı zamanda 2,3,5 veya 7'nin katları
olmak zorunda. Aynı fikir,  Legendre’nin Formulü yönteminde de kullanılmış. Ekleme-Çıkarma prensibi ile birleştirince, yukarıdaki formül
ortaya çıkıyor. Python ile yapalım;

    :::python
    def Legendre(x):
        
        p = basit_sieve(sqrt(x))
        return -1 + len(p) + ekle_cikar(x, p)
        
Fonksiyonun çalışma süresini test etmek için uygun bir zaman.

<div class="centered">
<svg class="line5" version="1.1" viewBox="0 0 68.012 30.0602" xmlns="http://www.w3.org/2000/svg"><defs><clipPath id="b"><path d="m51.36 649.3h191.81v87.744h-191.81z" clip-rule="evenodd"/></clipPath><clipPath id="a"><path d="m49.44 647.26h195.77v91.704h-195.77z" clip-rule="evenodd"/></clipPath></defs><g transform="translate(-47.2211 -88.5595)"><g transform="matrix(.352778 0 0 -.352778 29.4446 347.675)"><g clip-path="url(#b)"><g><path d="m50.88 678.72h191.93v14.64h-191.93z" fill="#d8d8d8" fill-rule="evenodd"/><path d="m50.88 649.66h191.93v14.664h-191.93z" fill="#d8d8d8" fill-rule="evenodd"/><text transform="matrix(1,0,0,-1,53.04,726.84)" fill="#000000" font-family="cmbxti10" font-size="11.04px"><tspan x="0 7.1760001 14.0208 24.46464 30.337919 36.211201 41.742241 51.468479 57.948959" y="0">number=10</tspan></text></g><text transform="matrix(1,0,0,-1,53.04,697.2)" fill="#000000" font-family="cmcsc8" font-size="11.04px" stroke="#000000" stroke-miterlimit="10" stroke-width=".31543"><tspan x="0 6.2265601 13.65648 20.72208 28.03056 33.418079 37.006081 44.071678 51.501598" y="0">fonksiyon</tspan></text><text transform="matrix(1,0,0,-1,159.02,697.2)" fill="#000000" font-family="cmcsc8" font-size="11.04px" stroke="#000000" stroke-miterlimit="10" stroke-width=".31543"><tspan x="0 7.9046402 14.97024 23.603519 30.669121 37.734718 43.718399 50.784 59.417278" y="0">Zamanlama</tspan></text><g fill="#000000" font-size="11.04px"><text transform="matrix(1,0,0,-1,53.04,682.68)" font-family="cmbxti10"><tspan x="0 7.69488 13.56816 19.441441 25.31472 32.490719 39.015362 44.546398 50.419682 55.663681 62.144161 68.624641 75.105118" y="0">Legendre(100)</tspan></text><text transform="matrix(1,0,0,-1,173.42,682.68)" font-family="cmbx10"><tspan x="0 6.348 9.8697596 16.21776 22.56576 28.913759 35.261761 41.60976 47.990879 54.338879 60.686878" y="0">0,000222643</tspan></text><text transform="matrix(1,0,0,-1,53.04,668.16)" font-family="cmbxti10"><tspan x="0 7.69488 13.56816 19.441441 25.31472 32.490719 39.015362 44.546398 50.419682 55.663681 62.144161 68.624641 75.105118 81.585602" y="0">Legendre(1000)</tspan></text><text transform="matrix(1,0,0,-1,173.42,668.16)" font-family="cmbx10"><tspan x="0 6.348 9.8697596 16.21776 22.56576 28.913759 35.261761 41.60976 47.990879 54.338879 60.686878" y="0">0,010299206</tspan></text><text transform="matrix(1,0,0,-1,53.04,653.64)" font-family="cmbxti10"><tspan x="0 7.69488 13.56816 19.441441 25.31472 32.490719 39.015362 44.546398 50.419682 55.663681 62.144161 68.624641 75.105118 81.585602 88.066078" y="0">Legendre(10000)</tspan></text><text transform="matrix(1,0,0,-1,173.42,653.64)" font-family="cmbx10"><tspan x="0 6.348 12.696 19.06608 22.54368 28.89168 35.239681 41.60976 47.95776 54.305759 60.675838" y="0">752,3459562</tspan></text></g></g><g clip-path="url(#a)"><path d="m50.46 723.42v-74.06" fill="none" stroke="#000" stroke-linecap="square" stroke-linejoin="round" stroke-miterlimit="10" stroke-width=".14"/><path d="m50.4 649.3h0.96v74.184h-0.96z" fill-rule="evenodd"/><path d="m156.44 722.46v-73.1" fill="none" stroke="#000" stroke-linecap="square" stroke-linejoin="round" stroke-miterlimit="10" stroke-width=".14"/><path d="m156.38 649.3h0.95999v73.224h-0.95999z" fill-rule="evenodd"/><path d="m242.27 722.46v-73.1" fill="none" stroke="#000" stroke-linecap="square" stroke-linejoin="round" stroke-miterlimit="10" stroke-width=".14"/><path d="m242.21 649.3h0.95999v73.224h-0.95999z" fill-rule="evenodd"/><path d="m51.42 723.42h191.69" fill="none" stroke="#000" stroke-linecap="square" stroke-linejoin="round" stroke-miterlimit="10" stroke-width=".14"/><path d="m51.36 722.52h191.81v0.96h-191.81z" fill-rule="evenodd"/><path d="m51.42 693.78h191.69" fill="none" stroke="#000" stroke-linecap="square" stroke-linejoin="round" stroke-miterlimit="10" stroke-width=".14"/><path d="m51.36 692.88h191.81v0.96h-191.81z" fill-rule="evenodd"/><path d="m51.42 679.26h191.69" fill="none" stroke="#000" stroke-linecap="square" stroke-linejoin="round" stroke-miterlimit="10" stroke-width=".14"/><path d="m51.36 678.36h191.81v0.96h-191.81z" fill-rule="evenodd"/><path d="m51.42 664.74h191.69" fill="none" stroke="#000" stroke-linecap="square" stroke-linejoin="round" stroke-miterlimit="10" stroke-width=".14"/><path d="m51.36 663.84h191.81v0.96h-191.81z" fill-rule="evenodd"/><path d="m51.42 650.2h191.69" fill="none" stroke="#000" stroke-linecap="square" stroke-linejoin="round" stroke-miterlimit="10" stroke-width=".14"/><path d="m51.36 649.3h191.81v0.95999h-191.81z" fill-rule="evenodd"/></g></g></g></svg>
</div>

Hmm. Bir sorunumuz var. Bu fonksiyonun çalışması oldukça uzun sürüyor. Aslını söylemek gerekirse, Legendre'nin formulü, asal sayıları saymak için
pek etkili bir yöntem değil. Ancak, bu kadar yavaş çalışmasında bizim de payımız var. Formulün orjinaline bağlı kalmak adına, yapılacak bir takım
optimizasyonlardan vazgeçtik. `ekle_cikar` fonksiyonunu optimize ederek, biraz hız kazanabiliriz. `ekle_cikar` fonksiyonunun ilk versiyonunda
bir sürü gereksiz kombinasyon hesaplıyoruz. Mesela, \\(\pi(200)\\) hesaplanırken, 200'den küçük ve 2,3,5,7 ve 11'in ortak katı olan herhangi bir
sayı olamayacağını biliyoruz, çünkü \\(ekok(2,3,5,7,11) = 2310\\). Bu durumda, 2,3,5,7 ve 13 sayılarının ortak katını kontrol etmeye gerek yok, çünkü
bu bir öncekinden bile daha büyük bir sayı olamak zorunda. Eğer kombinasyon hesabını fonksiyonumuzun içine dahil edersek,
gereksiz kombinasyon hesapları yapmaktan kurtulabiliriz. Böylece fonksiyonumuz hızlanacaktır.

    :::python
    def ekle_cikar2(limit, sayilar):
        
        t = 0
        n = len(sayilar)
        
        for i in range(len(sayilar)):
            "Döngüden erken çıkabilmek için, kombinasyonları kendimiz hesaplayacağz"
            indices = range(i+1)

            grb = tuple(sayilar[k] for k in indices)
            denominator = reduce(mul, grb)
            
            if denominator > limit:
                "Erken çıkış noktalarından biri"
                break
                
            t += (-1)**i * int(limit / denominator )
            
            while True:
                
                for k in reversed(range(i+1)):
                    if indices[k] != k + n - (i+1):
                        break
                else:
                    break
                    
                indices[k] += 1
                
                for j in range(k+1, (i+1)):
                    indices[j] = indices[j-1] + 1
                    
                grb = tuple(sayilar[k] for k in indices)
                denominator = reduce(mul, grb)
                

                if denominator > limit:
                    "Erken çıkış noktalarından diğeri"
                    indices[-1] = n-1
                    continue
                
                t += (-1)**i * int(limit / denominator )
        
        return limit - t
        
    def Legendre2(x):
        
        p = basit_sieve(int(sqrt(x) + 1))
        return -1 + len(p) + ekle_cikar2(x, p)
        
Bu optimizasyon yüzünden, fonksiyonumuz oldukça karmaşık bir hal aldı. Yukarıda neler döndüğünü anlamakta güçlük çekerseniz, fazla kafaya takmayın. Yazının
ilerleyen bölümlerinde asal sayı saymak için daha etkin bir algoritmayı inceleyeceğiz. Şimdiye kadar yaptıklarımız, o algoritmayı anlamaya
yardımcı olacak fikir egzersizleri. Yine de, yaptığımız optimizasyonu bir test edelim.

<style>
img[alt=legendre2benchmark] {
    width: 280px;
    display: block;
    margin: auto;
}
</style>
![legendre2benchmark](/images/Legendre2_Timeit.svg)

Çok daha iyi, ama hala Eratosten kalburunun yerini tutamaz. Yalnız hafıza gereksinimi bir hayli düşük. Hafıza problemi yaşayacak kadar büyük
sayılarla muhatap olacaksanız, bu fonksiyonu (mümkünse C ile yazarak) deneyebilirsiniz, ancak, biraz beklemeyi göze almanız gerekiyor. Biz asıl
konumuza dönelim.

## Meissel-Lehmer Algoritması

Şu ana kadar yaptıklarımız bizi sonuca pek yaklaştırmamış olsa da, artık Meissel-Lehmer algorimatsını incelemek için gerekli fikirsel altyapıya
sahibiz.Öncelikle bazı tanımlar yapacağız. \\(\phi(x, a)\\) fonksiyonu, x'e kadar olan sayıların içinde, \\(a\\)'ıncı sıradaki asal sayıdan
küçük veya eşit asal çarpanı olmayan sayıların sayısı olsun. Örneğin, \\(\phi(20, 2) = \left \vert{\\{ 1, 5, 7, 11, 13, 17, 19\\}} \right \vert = 7\\).
Örnekte, \\(x = 20\\) için birinci ve ikinci asal sayının (2 ve 3) katlarını silerek, kalan elemanların sayısını aldık. Bu tanıma ile birlikte
Legendre'nin formulünü şu şekilde de yazabiliriz; \\( \pi(x) = \phi(x, a) + a - 1 : a = \pi(\sqrt{x})\\). Şimdi de, \\(P_k(x, a)\\), 1 ile x arasındaki
sayılardan, tam olarak k adet asal çarpanı olan ve, bu asal çarpanlardan hiçbiri \\(p_a\\)'dan (a'ıncı sıradaki asal sayı) küçük veya eşit olmayan
sayıların sayısı olsun. Örneğin, \\(P_2(50, 2) = \left \vert{\\{ 25, 35, 49 \\}} \right \vert = 3 \\). Bu iki tanımdan yola çıkarak, aşağıdaki tanıma
ulaşabiliriz. (\\(P_0(x,a) = 1\\))

$$
\phi(x, a) = P_0(a, x) + P_1(x, a) + P_2(x, a) + \dots
$$

Buraya kadar yaptıklarımızın, asal sayıların sayısını hesaplamakla bir ilgisi yok gibi görünse de, yukarıdaki tanımda \\(P_1(x, a)\\) terimi çok
ilginç bir terim. Kelimelerle ifade edersek, 1 ile x arasındaki sayılardan, tam olarak 1 adet asal çarpanı olan, ve bu asal çarpanlardan hiçbiri
\\(p_a\\)'dan küçük veya eşit olmayan sayıların sayısı. Tam olarak 1 adet asal çarpanı olmak demek, zaten o sayının kendisinin asal sayı
olduğu anlamına geldiğine göre, \\(P_1(x, a) = \pi(x) - a\\) diyebiliriz. O zaman;

$$
\begin{align}
\phi(x, a) &= P_0(a, x) + (\pi(x) - a) + P_2(x, a) + \dots \\\\
\pi(x)     &= \phi(x, a) + a - 1 - P_2(x, a) - P_3(x, a) - \dots
\end{align}
$$

Hmm, eğer \\(a = \pi(\sqrt{x})\\) dersek, Legendre'nin formulüne geri dönmüş oluyoruz. Bu gözlemle birlikte, sağlama yapmış kadar olduk.

Formül bir hayli karışık görünebilir, ama, terimleri hesaplamak daha da karışık. Öhm. Devam edelim. 

## \\(P_i(x, a)\\) Hesabı

Bu kısmın anlaşılması ilk bakışta biraz güç olabilir. Bu nedenle, küçük parçalara bölerek anlatmaya çalışacağım.  \\(P_2(x, a)\\) ile başlarsak,
tanım gereği, \\(P_a\\)'dan büyük iki asal sayının çarpımından elde edilen ve (Burada, yazmaya devam etmemeye karar verdim, kaynakça kısmındaki
kaynaklarda burada olması gereken bilgiler mevcut. İsteyenler oradan devam edebilir.)

## Kaynakça

 - [Efficient Prime Counting with the Meissel-Lehmer Algorithm](http://acganesh.com/blog/2016/12/23/prime-counting)
 - [Computation of π(n) by Sieving, Primality Testing,
Legendre’s Formula and Meissel’s Formula](https://www.cs.jhu.edu/~jason/software/primes/primes.pdf)
 - [How Many Primes Are There?](https://primes.utm.edu/howmany.html)
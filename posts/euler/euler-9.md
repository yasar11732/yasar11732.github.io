<!--
.. date: 2018/08/16 21:38:00
.. slug: euler-9
.. title: (Euler 9) Pisagor Üçlüsü
.. description: Toplamı 1000 eden Pisagor üçlüsünü bulacağız
.. tags: mathjax
-->

Pisagor üçlüsü \\(a^2 + b^2 = c^2\\) eşiliğini sağlayan \\(a < b < c\\) üçlüsüne verilen isimdir. Örneğin, \\(3^2 + 4^2 = 9+16 = 25 = 5^2\\) gibi.

\\(a+b+c=1000\\) olan tek bir pisagor üçlüsü vardır. Bu üçlüde \\(a \cdot b \cdot c\\) çarpımını bulunuz. <!-- TEASER_END -->

İlk akla gelen yöntem, teker teker tüm ihtimalleri denemek.

    :::python
    from math import sqrt

    def euler9():
        
        for b in range(2, 1001):
            for a in range(b, 0, -1):
                
                c = sqrt(a ** 2 + b ** 2)
                
                if a + b + c == 1000:
                    return (a,b,c)
                

Her zamanki gibi, Euler Problemlerinde ilk akla gelenden daha iyisi var. \\(a^2 + b^2 = c^2\\) eşitliğini sağlayan terimlerin her birini
sabit bir sayıyla çarpığınızda eşitlik bozulmaz. Şu şekilde gösterelim;

$$\begin{align}
a^2 + b^2 = c^2 && \text{Bunu doğru kabul ediyoruz.} \\\\
k^2(a^2 + b^2) = k^2 \cdot c^2 && \text{Eşitliğin her iki tarafını } k^2 \text{ ile çarpalım} \\\\
k^2 \cdot a^2 + k^2 \cdot b^2 = k^2 \cdot c^2 && k^2 \text{ terimini parantez içine dağıtalım} \\\\
(k \cdot a)^2 + (k \cdot b)^2 = (k \cdot c)^2 && \text{kareli terimleri parantez içine gruplarsak, önermemizi kanıtlamış olduk.}
\end{align}$$

O halde, eğer \\(a^2 + b^2 = c^2\\) olduğunda \\(\frac{1000}{a + b + c} = k\\) dersek, \\((k \cdot a)^2 + (k \cdot b)^2 = (k \cdot c)^2 \\)
eşitliğinde terimler toplamı 1000 olur. Öyleyse, kodları tekrar gözden geçirelim;

    :::python
    from math import sqrt

    def euler9_v2():
        
        for b in range(2, 1001):
            for a in range(b, 0, -1):
                
                c = sqrt(a ** 2 + b ** 2)
                
                k, n = divmod(1000, a + b + c)
                
                if n == 0:
                    return (k*a, k*b, k*c)
                    
Sanırım bu problemde yapılabilecek en iyisi bu, o yüzden karşılaştırmaya geçebiliriz.

    >>> timeit.timeit("euler9()", "from euler9 import euler9", number=1000)
    16.17503372204979
    >>> timeit.timeit("euler9_v2()", "from euler9 import euler9_v2", number=1000)
    0.05705214216433774
    
Yaklaşık 284 kat hızlandık. Gayet başarılı.

## Gelecek Problem

10'dan küçük asal sayıların toplamı \\(2 + 3 + 5 + 7 = 17\\) dir.

İki milyondan küçük asal sayıların toplamını bulunuz.


<!--
.. date: 2018/08/21 23:15:00
.. slug: python-ile-hizli-asal-sayi-bulma
.. title: Python ile Hızlı Asal Sayı Tespiti
.. description: Eratosten Kalburu yöntemine Tekerlek Optimizasyonu uygulayıp, hızlı asal sayı tespiti yapan bir fonksiyon yazacağız.
.. tags: mathjax
-->

Normalde bugün Euler Problemleri serisinde 12. yazıyı yazacaktım, ama kendimi asal sayı tespit programlarına biraz fazla kaptırdım. Euler
problemine geçmeden önce, son yazdığım asal sayı bulma fonksiyonunu paylaşayım istedim. <!-- TEASER_END -->

    :::python
    def gen_candidates3(limit):
        
        w = [7, 11, 13, 17, 19, 23, 29, 31]
        w2 = w[:]
        
        for _ in xrange(limit / 30):
            w = [x+30 for x in w]
            w2.extend(w)
        
        while w2[-1] > limit:
            w2.pop()
        
        return w2
        
    def basit_sieve4(limit):
        rotations = {
            1:  (0, 6, 4, 2, 4, 2, 4, 6),
            7:  (0, 4, 2, 4, 2, 4, 6, 2),
            11: (0, 2, 4, 2, 4, 6, 2, 6),
            13: (0, 4, 2, 4, 6, 2, 6, 4),
            17: (0, 2, 4, 6, 2, 6, 4, 2),
            19: (0, 4, 6, 2, 6, 4, 2, 4),
            23: (0, 6, 2, 6, 4, 2, 4, 2),
            29: (0, 2, 6, 4, 2, 4, 2, 4)
            
        }
        
        candidates = gen_candidates3(limit)
        limit = candidates[-1]
        
        for i in xrange(4 * int(limit ** 0.5) / 15 + 1):
            
            c = candidates[i]
            if c:
                n = c
                for k in rotations[c % 30]:
                    n+=k
                    candidates[4*c*n/15 - 1::8*c] = [0] * ((limit - c*n)/(30*c)+1)
            
        return [2,3,5] + filter(None, candidates)
        
Bu yazıya algoritmanın tamamını açıklayacak kadar vakit harcamak istemiyorum. Merak edenler [Google'da Wheel Factorization aramasına](https://www.google.com/search?q=wheel+factorization)
bakabilirler. Tekerlek olarak (2,3,5) tekeri kullandım. Performans karşılaştırmasına gelirsek;

<pre>
>>> import timeit
>>> timeit.timeit("basit_sieve3(20000000)", "from euler10 import basit_sieve3",
number=10)
23.53885076855179
>>> timeit.timeit("basit_sieve4(20000000)", "from euler10 import basit_sieve4",
number=10)
15.435177794462824
</pre>

Yirmimilyon'a kadar asal sayıları bulma konusunda yüzde 35-40 arası bir hızlanma sağladık. Bu performans artışında `get_candidates3` fonksiyonunun da
önemli bir payı var. Asal sayı adayları listesini oluşturmak için kullandığım diğer yöntemlerde bu denli bir performans artışı sağlayamamıştım. Kayda
geçmesi açısından onları da buraya bırakıyorum.

    :::python
    def gen_candidates(limit):
        w = [7, 11, 13, 17, 19, 23, 29, 31]
        n = 8
        c = 30
        
        while w[-1] < limit:
            w.extend(x + c for x in w[(-1*n):])
            
            n *= 2
            c *= 2
        
        return w[:(4*limit/15)-1]
        
    def gen_candidates2(limit):
        w = range(7, limit, 30)
        w.extend(range(11, limit, 30))
        w.extend(range(13, limit, 30))
        w.extend(range(17, limit, 30))
        w.extend(range(19, limit, 30))
        w.extend(range(23, limit, 30))
        w.extend(range(29, limit, 30))
        w.extend(range(31, limit, 30))
        w.sort()
        return w
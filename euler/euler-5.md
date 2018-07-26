<!--
.. date: 2018/07/26 21:13:00
.. slug: euler-5
.. title: (Euler 5) EBOB EKOK
.. description: Birden fazla sayının en küçük ortak katını hesaplayacağız.
.. tags: mathjax
-->

1den 10a kadar tüm sayılara kalansız bölünebilen en küçük sayı 2520'dir. 1den 20ye kadar tüm sayılara kalansız bölünebilen
en küçük sayı kaçtır. <!-- TEASER_END -->

Bu problemin çözümü için, birden fazla sayının en küçük ortak katını hesaplamamız gerekiyor. İki sayılar için kullanılan
standard ekok bulma yöntemini ikiden fazla sayı için de aynen kullanabiliriz.

![İkinden fazla sayının ekokunu bulmak](/images/ekok.svg)

Bu algoritmayı uygulayabilmek için öncelikle sayıların içindeki en büyük sayıya kadar olan asal sayıları tespit etmeliyiz.
Bunun için [3. Euler Problemi çözümünde](euler-3.html) oluşturduğumuz `basit_sieve` yöntemini kullanacağız. Ekok tespiti için
ise yukarıdaki resimdeki yönteme aynen bağlı kalacağız.
    
    :::python
    from functools import reduce
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
        
    def toplu_ekok(numbers):
        
        primes = basit_sieve(max(numbers))
        prime_index = 0
        
        prods = []
        prime = primes.pop(0)
        
        while numbers:
            
            
            t1 = []
            
            prime_used = False
            
            for n in numbers:
                d,m = divmod(n, prime)
                
                if m == 0:
                    t1.append(d)
                    prime_used = True
                else:
                    t1.append(n)
                    
            
            if prime_used:
                prods.append(prime)
            else:
                prime = primes.pop(0)
                
            numbers = [x for x in t1 if x != 1]
        
        return reduce(lambda x,y: x*y, prods)
        
Yukarıdaki `toplu_ekok` fonksiyonunu `toplu_ekok(range(1,21))` şeklinde çağırarak,
bu euler probleminin sonucunu elde edebilirsiniz.

Her ne kadar bu çözüm doğru sayıya ulaşmamız için yeterli olsa da, aynı soruyu çok daha etkin bir yöntemle çözebiliriz. Bunun
için öklit algoritmasını kullanacağız. Öklit algoritması iki sayının ebob'unu bulmak için kullanılabilecek çok etkin bir yöntem.
İki sayının ebob'u hesaplandıktan sonra, \\(ekok(a,b) = a*b/ebob(a,b)\\) eşitliğini kullanarak ekok'u da hesaplayabileceğiz. Öklit
algoritmasından bahsetmeden önce, algoritmanın temelindeki fikirlere bir göz atmakta fayda var.

 1. \\(a|b \wedge a|c \to a|(b+c)\\) ve aynı şekilde \\(a|b \wedge a|c \to a|(b-c)\\). Bunu kanıtlamak da çok kolay olacaktır.
Eğer \\(a|b\\) (a, b'yi tam bölüyor) ise, \\( b = a\*n \\) diyebiliriz. Aynı şekilde \\(a|c\\) ise, \\(c = a\*k\\) diyebiliriz. Bu durumda
\\(b+c = a\*n + a\*k = a(n+k)\\) olur ki, bu sayının \\(a\\) sayısına kalansız bölündüğünü görebiliyoruz. Örnek vermek gerekirse, \\(7\\) sayısı
hem \\(14\\) sayısını hem de \\(21\\) sayısını tam bölebildiği için,  bu iki sayının toplamı olan \\(35\\) sayısını ve bu iki sayının
farkı olan \\(7\\) sayısını da tam bölüyor diyebiliriz.
 2. Bir numaralı gözlemden yola çıkarak, \\(ebob(a,b) = ebob(a, a-b)\\) diyebiliriz. Bunu da şu şekilde gösterebiliriz. Tanım gereği,
iki sayının ebob'u, bu sayılardan ikisini de kalansız böler. Bu sayıya \\(g\\) sayısı dersek, \\(g|a\\) ve \\(g|b\\) diyebiliriz. Bir numaralı
gözlemden anlaşılacağı üzere \\(g|(a-b)\\)'dir. \\(a\\) ve \\(b\\) sayılarını bölen her sayı, \\(a-b\\)'yi tam bölmek zorunda olacağından, \\(ebob(a,b) = ebob(a, a-b)\\)
olmak zorundadır. Böylece, \\(ebob(a,b)\\) problemini biraz daha basitleştirmiş olduk.
 3. Aynı çıkarma işlemine devam edersek, \\(ebob(a,b) = ebob(b, mod(a,b))\\) sonucuna varabiliriz. Bu işlemi \\(mod(a,b) = 0\\) olana kadar
 devam ettiğimizde, elimizde kalan \\(b\\) sayısı, ilk terimin ebob'u olacaktır. Bu şekilde ebob bulmaya, öklit algoritması deniyor.
 
Yukarıdaki gözlemlerden yola çıkarak, euler problemini aşağıdaki şekilde çözebiliriz.

    :::python
    from itertools import reduce
    def ebob(x,y):
        "Iki sayinin e.b.o.b'unu bulur"
        if not y:
            return x
        return ebob(y, x % y)
        
    def ekok(x,y):
        "Iki sayinin ekokunu bulur"
        return (x*y)//ebob(x,y)
        
    def euler5(sayilar):
        "Verilen sayilarin toplu halde ekokunu bulur"
        return reduce(ekok, sayilar)
 
Öklit algoritmasıyla ilk kez karşılaşıyorsanız, elinize kağıt kalem alarak farklı sayılarla algoritmayı deneyerek, çalışma
tarzını anlamaya çalışmanızı tavsiye ederim.

## Gelecek Problem

İlk 10 doğal sayının karelerinin toplamı

$$1^2+2^2+...+10^2=385$$

ilk 10 doğal sayının toplamının karesi ise,

$$(1+2+3...+10)^2=55^2=3025$$

olduğundan, ilk 10 sayının karelerinin toplamı ile toplamlarının karelerinin farkı \\(3025-385=2640\\)dır. İlk 100 doğal sayının
karelerinin toplamı ile toplamlarının karesi arasındaki farkı bulunuz.
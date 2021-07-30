<!--
.. title: (Euler 2) Çift Fibonacci Sayıları
.. slug: euler-2
.. date: 2018/07/18 23:21:00
.. tags: 
.. description: Çift fibonacci sayılarını toplayacağız.
.. has_math: yes
-->

[Project Eulerdeki 2 numaralı problem](https://projecteuler.net/problem=2) şu şekilde; Fibonacci dizisinde her bir sayı, kendinden
önce gelen iki sayının toplamı alınarak bulunur. 1 ve 2 ile başlayarak, ilk 10 sayı şu şekildedir;

$$
    1,2,3,5,8,13,21,34,55,89, ...
$$

dört milyonu geçmeyen fibonacci sayıları içerisinde, çift olanlarının toplamını bulunuz. <!-- TEASER_END -->


Tavsiye edilen okuma listesi;

 * [Fibonacci Sayı Dizisi](https://www.tech-worm.com/fibonacci-dizisi-nedir-nerelerde-kullanilir/)
 
Fibonacci sayıları denince, şüphesiz çoğunuzun aklına _özyinelemeli_ (_recursive_) fonksiyonlar gelmiştir. Kısa bir hatırlatmaya
ihtiyacı olanlarımız için kısaca bahsedelim... Bir algoritmanın kendini tekrar etmesiyle bir fonksiyon tanımı ya da hesap
yapmaya özyineleme diyoruz. Örneğin, faktoriyel fonksiyonunun tanımını şu şekilde yapabiliriz.

$$n! =
\begin{cases}
1,  & \text{$n$ = 0 ise} \\\\
1, & \text{$n$ = 1 ise}  \\\\
n*(n-1)! &\text{$n$ > ise}
\end{cases}$$

Yukarıdaki tanımda gördüğümüz üzere, faktoriyel fonksiyonunu, yine faktoriyel fonksiyonu kullanarak yapıyoruz. Bunu Python
programlama diline birebir çevirebiliriz.

    :::python
    def faktoriyel(n):
        if n < 0:
            raise ValueError("Faktoriyel fonksiyonu negatif sayilar icin tanimli değildir")
        if n in (0, 1):
            return 1
        
        return n*faktoriyel(n-1)
        
Euler Problemindeki fibonacci tanımını da _özyinelemeli_ olarak şu şekilde ifade edebiliriz.

$$fib(n) =
\begin{cases}
1,  & \text{$n$ = 1 ise} \\\\
2,  & \text{$n$ = 2 ise}  \\\\
n+fib(n-1) &\text{$n$ > 2 ise}
\end{cases}$$ 
        
Yukarıdaki tanıma uygun olarak, aşağıdaki testi başarıyla geçecek bir fonksiyonu Python dilinde yazabilirsiniz. 
    
    :::python
    def fibo_recurse(n):
        pass
        
    if all([
        fibo_recurse(1) == 1,
        fibo_recurse(2) == 2,
        fibo_recurse(3) == 3,
        fibo_recurse(4) == 5,
        fibo_recurse(5) == 8,
        fibo_recurse(8) == fibo_recurse(6) + fibo_recurse(7)
    ]):
        print("Fonksiyon testi başarılı.")
    else:
        print("Fonksiyon testi başarısız.")
        
Her ne kadar bu tarz fonksiyonlar fibonacci sayıları için çok zarif ve sıkça kullanılan bir yöntem olsa da, bilgisayarın
kaynaklarını kullanması açısından incelediğinizde, pek de verimli olmadığını göreceksiniz. Örneğin, `fibo_recurse(40)` fonksiyonunu
çağırdığınızda, gözle görülür bir bekleme ile karşılaşırsınız. Bunun nedenini ve muhtemel çözümünü yazının sonundaki bonus kısmına
bırakacağım.

Bu euler probleminin çözümü için, ben aşağıdaki prosedürel fonksiyonu kullanacağım;


    :::python
    def fibo_up_to_n(n):
        a, b = 1, 2
        fibo_list = [1, 2]
        
        while True:
            next = a + b
            if next > n:
                break
                
            fibo_list.append(next)
            a, b = b, next
            
        return fibo_list
        
Burada, belirli bir sıradaki fibonacci sayısını döndürmek yerine, bir sayıdan küçük bütün fibonacci sayılarının bir listesini
döndürüyoruz. Euler problemin çözümü için ise, geriye sadece şu kalıyor;

    :::python
    print(sum(x for x in fibo_up_to_n(4000000) if x % 2 == 0))
    
Küme üreteci yazım tarzına aşina olmayanlar, aşağıdaki çözümü daha anlaşılır bulabilir.
    
    :::python
    sum = 0
    for x in fibo_up_to_n(4000000):
        if x % 2 == 0:
            sum += x
            
    print(sum)
    
## Bonus: Özyinelemeli versiyon, sorunları ve çözümleri

Yukarıda boş bırakılmış, özyinelemeli versiyonu şu şekilde yazabilirsiniz;

    :::python
    def fibo_recurse(n):
        if n == 1:
            return 1
        if n == 2:
            return 2
        
        return fibo_recurse(n-1) + fibo_recurse(n-2)

Bu fonksiyonu yirmiden büyük sayılarla denediğinizde, hissedilir gecikmelere neden olduğunu görebilirsiniz. Bunun nedenini incelemek için,
fonksiyonu şu şekilde değiştirelim.

    :::python
    def fibo_recurse(n):
        print("fibo_recurse(%s)" %n)
        if n == 1:
            return 1
        if n == 2:
            return 2
            
        return fibo_recurse(n-1) + fibo_recurse(n-2)
        
Ekrana yazdırılan satır sayısına göre, fonksiyonun kaç kere tekrar ettiğini anlayabiliriz. Bu fonksiyonu birkaç farklı argümanla deneyin. 
Fonksiyona verilen argüman ile yazdırılan satır sayısı arasında, aşağıdaki gibi bir ilişki ortaya çıkacak.

$$
\newcommand\T{\Rule{0pt}{1em}{.3em}}
\begin{array}{|c|c|}
\hline  3 \\T & 3 \\\\\hline
  5 \\T & 9 \\\\\hline
  7 \\T & 25 \\\\\hline
  10 \\T & 109 \\\\\hline
  20 \\T & 13529 \\\\\hline
  30 \\T & 1664079 \\\\\hline
  40 \\T & 204668309 \\\\\hline
\end{array}
$$
 
Gördüğünüz üzere, argüman ve fonksiyon tekrarı arasında expansiyonel bir ilişki var.

Ekrana yazdırılan çıktı sayesinde, fonksiyonun hangi argümanlarla çalıştırıldığını da inceleyebiliriz. `fibo_recurse(8)`
fonksiyonunun değeri hesaplanırken, birkaç defa `fibo_recurse(5)` değerinin hesaplandığını göreceksiniz. Aynı hesaplamanın
defalarca yapılıyor olması problemi, hesapladığımız değer büyükdükçe, daha da ciddileşiyor.

Bu sorunun önüne geçmek için, yabancı kaynaklarda _memoization_ olarak geçen tekniği kullanabiliriz. Ana fikir şu şekilde, eğer
daha önce hesapladığımız değerlerin bir kaydını tutarsak, aynı hesabı tekrar yapmaktansa, kayıt ettiğimiz değeri kullanabiliriz.
Bunun bir örneğini aşağıda bulabilirsiniz.

    :::python
    def fibo_recursive_memoize(n, memory = {1:1, 2:2}):
        if n in memory:
            return memory[n]
            
        result = fibo_recursive_memoize(n-1, memory) + fibo_recursive_memoize(n-2, memory)
        memory[n] = result
        return result
        
Yaptığımız işi özetlemek gerekirse, fonksiyon için öntanımlı bir hafıza sözlüğü tanımladık. Bu fonksiyon ile yapılan bütün
hesaplamaların sonucu, bunun içinde kayıtlı tutulacak. Fonksiyonun basit versiyonunda yaptığımız egzersizi burada tekrar edersek,
şu şekilde sonuç alacağız. (İki örnek arasında karşılaştırma yapmaya imkan sağlaması için, denemeler arasında hafıza sözlüğünü sıfırladım.)

$$
\newcommand\T{\Rule{0pt}{1em}{.3em}}
\begin{array}{|c|c|}
\hline  3 \\T & 3 \\\\\hline
  5 \\T & 7 \\\\\hline
  7 \\T & 11 \\\\\hline
  10 \\T & 17 \\\\\hline
  20 \\T & 37 \\\\\hline
  30 \\T & 57 \\\\\hline
  40 \\T & 77 \\\\\hline
  100 \\T & 197 \\\\\hline
  1000 \\T & 1997 \\\\\hline
\end{array}
$$

Gördüğünüz gibi, normal versiyondaki fibonacci fonksiyonu kırkıncı fibonacci de ruhunu teslim etmeye başlarken, ikinci versiyonu
bininci fibonacci de bile hiçbir zorlanma yaşamıyor. Merak edenler için, bininci sıradaki fibonacci sayısı

$$
703303677114228158218352548771835497701812698\\\\
363587327426049050871545371181969335797422494\\\\
945626117334877504492417659910881863632654502\\\\
236471060120533741212738673391111981393731255\\\\
98767690091902245245323403501
$$

##Bonus 2

Eğer farkettiyseniz, fibonacci sayı dizisi iki tek sayı ve bir çift sayı şeklinde ilerliyor. Bunun bu şekilde olması matematiksel bir zorunluluk.
Bu nedenle, çözümü şu şekilde de yazabiliriz;

    :::python
    sum(fibo_up_to_n(4000000)[1::3])
    
Egzersiz olarak, fibonacci dizisinin iki tek, bir çift sayı olarak ilerlediğini tümevarım yoluyla kanıtlayabilirsiniz
    
##Bonus 3

Fibonacci sayıları arasındaki oran yaklaşık olarak \\(1.618\\) olduğundan, bir önceki fibonacci sayısını \\(1.618\\) ile çarpıp en yakın
tam sayıya yuvarlayarak da fibonacci sayılarını elde edebilirsiniz.

    :::python
    def fibo_up_to_n(n):
        fibos = []
        
        fibo = 1
        fibos.append(fibo)
        
        while True:
            fibo = int(round(fibo * 1.618))
            if fibo > n:
                break
            fibos.append(fibo)
        
        return fibos
            
    
## Gelecek Problem


\\(13195\\) sayısının asal çarpanları \\(5\\), \\(7\\), \\(13\\) ve \\(29\\)'dur.

\\(600851475143\\) sayısının en büyük asal çarpanı nedir.

Tavsiye edilen okuma listesi olarak, asal sayılar ve çarpanlara ayırma konularını araştırabilirsiniz.
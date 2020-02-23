<!--
.. date: 2020-02-22 20:35
.. description: 
.. slug: buyuk-sayi-islemleri-giris
.. title: Büyük Sayı Algoritmaları - Giriş
-->

İşlemciler aritmetik işlemleri gerçekleştirken, genellikle 8-64 bit
arasında sayılar üzerinde işlem yapar. Bir program, daha büyük sayılar
üzerinde işlem yapmak için, birden fazla sayıdan oluşan bir array
üzerinde işlem yapabilir. Python programlama dilinde, sınırsız
uzunlukta sayılar üzerinde işlem yapmak, dilin bir özelliği olarak
sunulmuştur. Java'da ve C#'da ise, BigInteger sınıf ile, sınırsız
uzunluktaki sayılar üzerinde işlem yapılabiliyor. Ben de,
[(Euler 13) C Programlama Dilinde Büyük Sayıları Toplama](../euler/euler-13.html) 
yazısını yazdığım günden bu yana, C ile büyük sayı
kütüphanesi yazmaya niyetliydim. Geçtiğimiz günlerde,
kısmen de olsa, bunu gerçekleştirebildim.

İlk yazdığım büyük sayı kütüphanesi, test edebildiğim kadarıyla
doğru çalışmasına rağmen, aynı zamanda oldukça yavaştı. Bu nedenle,
fikir alabilmek adına, [GMP](https://gmplib.org/) kütüphanesini,
ve [OpenSSL](https://github.com/openssl/openssl/tree/master/crypto/bn)
kütüphanesinin ilgili bölümlerini inceledim. Her ikisi de,
benim ilk yazdığım kütüphaneye göre oldukça iyi olsa da, ikisi
arasında tercih yapmak gerekirse, GMP'nin tasarımını daha
başarılı buldum.

Bu yazı ile, GMP'yi örnek olarak olarak C ile yazacağım
büyük sayı kütüphanesini anlatacak bir yazı dizisine başlamak
istiyorum. Burada anlatacağım algoritmalar ve kütüphane, performans
açısından GMP kadar iyi olmayacak. Bunun nedenlerinden aklıma gelen
birkaç tanesi şu şekilde;

 - GMP kütüphanesi, neredeyse her işlemci mimarisi için ayrı
   ayrı optimize edilmiş assembly kodları içeriyor. Benim
   yazacağım kütüphane sadece C kodlarından oluşacak. İşlemci
   mimarisine uygun kod oluşturma işini C derleyecilerine
   bırakacağım.
 - GMP kütüphanesi, her bir işlem için, bilinen en iyi algoritmaları
   kullanıyor. Hatta bazı işlemler için, birkaç farklı algoritma
   içerisinden, sayıların büyüklüğüne göre uygun olan algoritmayı
   seçip kullanıyor. Burada bahsedeceğim algoritmalar, belki
   ufak tefek optimizasyonlar içerse de, en temel seviyedeki
   algoritmalar olacak.
 - GMP, her bir platform için, en uygun integer türünü seçip
   kullanıyor. Bunu gerçekleştirebilmek için, derleme
   hedefinin özelliklerini test edebilecek bir build sistemi
   gerekiyor. Düzgün bir build sistemi yapmak başlı başına
   ayrı bir iş olduğundan, ve bu konuya çok hakim olmadığım için,
   platforma özgü veri tipi seçimi yapmayacağım.
   
GMP kütüphanesi kadar iyi olmayacak olsa da, bir büyük sayı
kütüphanesi geliştirmenin eğitsel değeri olduğuna inanıyorum.

Veri Tipleri ve Makrolar
------------------------

`bn.h` dosyası, büyük sayı kütüphanesinin header dosyası olacak. İlk versiyonu aşağıdaki gibi;

```
#ifndef __BN_H_
#define __BN_H_
#include <limits.h> // CHAR_BIT
#include <stdint.h>

typedef int32_t bn_size_t;
typedef uint32_t bn_digit_t;
typedef uint64_t bn_long_digit_t;

#define BN_DIGIT_BITS ((sizeof(bn_digit_t)) * CHAR_BIT)
#define BN_DIGIT_MAX ((bn_digit_t) ~ (bn_digit_t)0)
#define BN_DIGIT_HI ((bn_digit_t) (1 << (BN_DIGIT_BITS / 2)))
#define BN_DIGIT_LOWMASK (BN_DIGIT_HI - 1)

#define BN_MAX(a,b) ((a) > (b) ? (a) : (b))
#define BN_MIN(a,b) ((a) < (b) ? (a) : (b))
#define BN_ABS(a) ((a) >= 0 ? (a) : -(a))
#define BN_CMP(a,b) (((a) > (b)) - ((b) > (a)))


#endif
```

Veri tiplerinin anlamları şu şekilde;

 - `bn_size_t`: Uzunluk ile ilgili verileri tutan veri tipi. Bazı fonksiyonlardan
   negatif uzunluk döndürmemiz gerekeceği için, signed 32 bit integer iyi bir tercih olacaktır.
 - `bn_digit_t`: Aritmetik işlemlerde kullanılacak veri tipi. Temel aritmetik
   işlemleri negatif olmayan sayıların üzerinde yapacağımız için, bu veri tipi unsigned olacak.
 - `bn_long_digit_t`: `bn_digit_t`'nin iki katı bit genişliğindeki veri tipi. Genişleyen çarpma
   ve daralan bölme işlemleri için kolaylık sağlayacak.

`bn_digit_t` tipine "digit" adını vermemizin nedeni, bu sayıların `2^32`'lik sayı tabanında
bir haneyi ifade etmesi. Örneğin, onluk tabanda işlem yaparken, `0..(10-1)` arasındaki
her bir rakam, sayının bir hanesini temsil ediyor. Biz yapacağımız işlemlerde,
`0..(2^32 - 1)` arasındaki sayıları tek hane olarak kabul edip işlem yapacağız. Birden fazla
haneden oluşan sayıları ifade etmek için, `bn_digit_t[]` veya `bn_digit_t*` tiplerini
kullanacağız. Yazacağımız bütün algoritmalar, sayıların little-endian olarak sıralandığı
varsayımıyla çalışacak. Örneğin, `2^32`'lik tabandaki `bn_digit_t a[3] = {1, 2, 3}` sayısı, 
onluk tabanda `1 + 2^32 * 2 + 2 ^ 64 * 3 = 55340232229718589441` sayısına karşılık geliyor.

Bahsedeceğimiz algoritmaları denerken, veya hata tespiti yapmaya çalışırken, onluk taban
ile `2^32`'lik taban arasında sık sık dönüşüm yapma ihtiyacı hissedebilirsiniz. Ben bunu
daha pratik yapabilmek adına aşağıdaki iki python fonksiyonunu kullanıyorum.

```python
base = 2**32

def to2_32(x):
    xs = []
    while x > base:
		xs.append(x % base)
		x = int(x / base)

    if(x):
        xs.append(x)

    return xs

def from2_32(xs):

	num = 0
	for i in range(len(xs)):
		num += xs[i] * base ** i
	return num
```

64 bit aritmetiği destekleyen işlemcilerde, `bn_long_digit_t` üzerindeki işlemler, doğrudan
işlemci üzerinde yapılırken, diğer işlemcilerde 64 bit aritmetiği taklit
eden kodları derleyici ekleyecektir. Dolayısıyla, 64 bit işlemcilerde
bir nebze daha iyi bir performans bekleyebiliriz. 64 bit mimarisine sahip işlemciler
için, GCC'nin bazı sürümleri 128 bit integer türünü destekliyor.
Böyle bir platformda kütüphaneyi derlerken, `bn_digit_t`'yi 64 bit,
`bn_long_digit_t`'yi 128 bit olarak ayarlayabilirsiniz. 128 bit aritmetiği
desteklemeyen platformlar için, 128 bit aritmetiği kendimiz taklit edebiliriz.
Çarpma ve Bölme ile ilgili yazılarda, bununla ilgili bir bölüm olacak.


Makrolar oldukça standart, bu nedenle, kısaca bahsedip geçeceğim;

 - `BN_DIGIT_BITS`: `bn_digit_t`'nin bit genişliği. Yukarıdaki örnekte bu makro 32 değerini alacak.
 - `BN_DIGIT_MAX`: `bn_digit_t`'nin alabileceği en büyük değer. Yukarıdaki örnekte `2^32 - 1` (diğer bir ifadeyle `0xFFFFFFFF`) değerini alacak.
 - `BN_DIGIT_HI`: `bn_digit_t`'nin, üst yarısının, alt biti. 
 - `BN_DIGIT_LOWMASK`: `bn_digit_t`'nin alt yarısını elde etmeye yarayan maske.
 - `BN_MAX`, `BN_MIN` : iki sayının büyük ve küçük olanını seçmeye yarayan makrolar.
 - `BN_ABS` : Bir sayının mutlak değerini döndürür. Standart C kütüphanesinde `abs` fonksiyonu olsa da, bu fonksiyonun
              inline derlenme garantisi yok. Ekstra fonksiyon çağrısına gerek bırakmamak için, bu makroyu tercih edeceğiz.
 - `BN_CMP` : İki sayıyı karşılaştır. İlk sayı ikinci sayıdan büyükse 1, küçükse -1, eşitse 0 döndürür.
 
Bir sonraki yazıda, negatif olmayan tamsayılar üzerinde toplama ve çıkarma fonksiyonlarını tanımlayacağız.

Ek Kaynaklar
------------

 - Eli Bendersky's website
: [64-bit types and arithmetic on 32-bit CPUs](https://eli.thegreenplace.net/2010/10/21/64-bit-types-and-arithmetic-on-32-bit-cpus)
 - GCC Documentation: [Double-Word Integers](https://gcc.gnu.org/onlinedocs/gcc/Long-Long.html#Long-Long)
 - GNU MP Manual: [Introduction to GNU MP](https://gmplib.org/manual/Introduction-to-GMP.html#Introduction-to-GMP)
 - Wikipedia: [128-bit computing](https://en.wikipedia.org/wiki/128-bit_computing)
 - Wikipedia: [Endianness](https://en.wikipedia.org/wiki/Endianness)
 - Wikipedia: [Arbitrary-precision arithmetic](https://en.wikipedia.org/wiki/Arbitrary-precision_arithmetic)
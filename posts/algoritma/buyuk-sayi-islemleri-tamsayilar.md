<!--
.. date: 2020-03-09 01:14
.. description: 
.. slug: buyuk-sayi-islemleri-tamsayilar
.. title: Büyük Sayı Algoritmaları - Tam Sayılara Giriş
.. tags: mathjax
-->

Yazı dizisinin ilk 4 yazısında, doğal sayılar üzerinde işlem
yapan temel fonksiyonlar yazdık. Genellikle, bu fonksiyonları
doğrudan kullanmayacağız. Onun yerine, bu yazıdan itibaren
ele alacağımız daha üst seviye fonksiyonları kullanacağız.Yeni
fonksiyonlarımız, önceki yazılarda değinmediğimiz hafıza
yönetimini sağlayacağı gibi, negatif sayılar üzerinde de
işlem yapabilecek.

Bilgisayarlarla negatif sayıları işlemenin çeşitli yöntemleri var.
Öncelikle, kısaca bu yöntemlerin üzerinden geçelim.

İşaret ve Mutlak Değer (Signed Magnitude Representation - SMR)
--------------------------------------------------------------

Yazı dilinde negatif sayının önüne eksi işareti koyduğumuz gibi,
bu yöntemde de sayının başına eksi işareti koyuyoruz. Tabi ki,
binary sistemde eksi işareti yok. Onun yerine, sayının en üst
bitini 1 olarak ayarlayarak, sayıyı negatif yapacağız. Bu gösterimde,
0 sayısı iki farklı şekilde (+0 ve -0) yazılabildiği için,
`n` bit kullanarak, `2^n - 1` farklı sayı ifade edilebiliyor.
Bu sayılar üzerinde aritmetik işlem yaparken, pozitif/negatif
kontrolü yapmak gerekiyor. Bu düzenin kullanım alanına örnek
olarak, `float` türündeki sayıları verebiliriz.


1'in Tümleyeni (One's Complement)
---------------------------------

Bu gösterimde, pozitif sayıların bitlerini tersine çevirerek, negatif
sayıları ifade ediyoruz. Örneğin, 8 bitlik '00000001' sayısı +1'i
ifade ederken, '11111110' sayısı ise -1'i ifade ediyor. SMR'de olduğu
gibi, en üst biti kontrol ederek, sayının işaretini tespit edilebiliyor.
Yine SMR'de olduğu gibi, sıfırın iki farklı gösterimi olduğundan, `n`
bit kullanarak, `2^n - 1` farklı değer ifade edebiliyoruz. Rivayet
odur ki, çok eski bilgisayarda bu yöntem kullanılırmış, ama çoğu
modern bilgisayarda negatif tam sayılar için 2'nin tümleyeni düzeni
kullanılıyor.

2'nin Tümleyeni (Two's Complement)
----------------------------------

Bu yöntem üzerinde biraz daha fazla duracağım, çünkü modern
bilgisayarlarda tam sayılar bu şekilde ifade ediliyor. Aşağıdaki
tablodan, 8 bit signed bir tam sayının her bitinin değerini
inceleyebilirsiniz.

<pre>
+-------+------+-----+-----+-----+-----+-----+-----+-----+
| Bit   | 7    | 6   | 5   | 4   | 3   | 2   | 1   | 0   |
+-------+------+-----+-----+-----+-----+-----+-----+-----+
| İkili | -2^7 | 2^6 | 2^5 | 2^4 | 2^3 | 2^2 | 2^1 | 2^0 |
+-------+------+-----+-----+-----+-----+-----+-----+-----+
| Onlu  | -128 | 64  | 32  | 16  | 8   | 4   | 2   | 1   |
+-------+------+-----+-----+-----+-----+-----+-----+-----+
</pre>

Bu yöntem bir farkla, 1'in tümleyeni ile aynı. 1'in tümleyeni
yöntemi ile, bir sayının negatifini almak istediğinizde, tüm
bitlerini tersine çevirmeniz gerekiyor. 2'nin tümleyeni yönteminde
ise, tüm bitleri çevirip, sonuca 1 eklemeniz gerekiyor.

Bu yöntemin en büyük avantajı, modüler aritmetik kurallarını bozmuyor
olması. Örneğin, \\(127 + 1 \equiv -128 \mod 128 \\). Aynı şekilde,
signed integer değerleri arasında toplama yaparken, 127 ile 1 sayısını
topladığınızda, `-128` sonucunu elde edersiniz.

<pre>
  0 1 1 1 1 1 1 1
+ 0 0 0 0 0 0 0 1
-----------------
  1 0 0 0 0 0 0 0
</pre>

Toplama işlemi yaparken, sayıların pozitif olup olmadığına dikkat etmeksizin, işlem yapabiliriz.
Aşağıdaki örnekte, +1 ile -1'in toplamını 0 olarak buluyoruz.

<pre>
  0 0 0 0 0 0 0 1 (+1)
+ 1 1 1 1 1 1 1 1 (-1)
-----------------
1 0 0 0 0 0 0 0 0
</pre>

Sonucun bir biti dışarıya taşdığı için, +1 ile -1 toplamından 0 sonucu elde
ediyoruz. Çıkarma işlemi de, negatif sayı ile toplamaya eşdeğer olduğundan,
yukarıdaki örneği birden bir çıkarma olarak da düşünebilirsiniz.

Bu düzenin yapısı gereği, toplama, çıkarma ve çarpma
yaparken, sayıların pozitif olmasına dikkat edilmeksizin işlem yapılabilir.
Bu avantaj işlemci üreticilerine cazip gelmiş olacak ki, signed işlem yapabilen
çoğu işlemci bu düzeni kullanıyor.

Kaydırılmış İkili (Offset Binary)
---------------------------------

Bu düzende, her sayıyı kendinden `n` fazla bir
sayı ile ifade ediyoruz. Örneğin, 8 bitlik signed
integer için, `n` 128 olsun.

<pre>
+------+----------+
|Sayı  | Kodlanışı|
+------+----------+
| 127  | 255      |
| 126  | 254      |
| 1    | 129      |
| 0    | 128      |
| -1   | 127      |
| -127 | 1        |
| -128 | 0        |
+------+----------+
</pre>

`float` türündeki sayıların exponent kısmı için, bu düzen kullanılıyor.

Hangisini Kullanmalıyız
-----------------------

Yazdığım ilk büyük sayı kütüphanesi için, 2'nin tümleyeni
yöntemini tercih etmiştim. Dört işlemin kolaylığı konusu
çok cazip gelmişti. Ancak, işlemcilerin yaptığı gibi
sabit genişlikteki sayılarla ilgilenmediğimiz için,
2'nin tümleyeni düzeninin avantajları çok da önemli
olmuyor. Aynı zamanda, büyük sayıların mutlak
değerini almak gerektiğinde, tüm sayının üzerinden
geçip, tüm bitlerini tersine çevirip sonuca bir eklemek
gerektiği için, oldukça uzun sürüyor. Bu bölme işlemi
için büyük bir sorun, çünkü pozitif ve negatif sayılar
arasında bölme yaparken, mutlak değer üzerinden
bölme yapmak gerekiyor. Modüler aritmeği de bölme işlemi
üzerinden yapacağımız için, 2'nin tümleyeni çok kötü
bir tercih. Kendim acı bir şekilde tecrübe ettim. Bu nedenle,
GMP kütüphanesinin yaptığı gibi, Signed Magnitude (SMR) düzenini
kullanacağız.

Artık biraz kod yazabiliriz.

	:::C
	typedef struct {
		bn_size_t alloc;
		bn_size_t length;
		bn_digit_t *digits;
	} bnz_t;

	typedef bnz_t *bnz_ptr;
	typedef const bnz_t *bn_constptr;
	
Tam sayıları, dinamik array veri yapısında tutacağız. `bnz_t`
veri yapısının `alloc` üyesi, kaç hanelik yer ayırdığımızı tutacak.
`length` üyesi, hem sayının kaç haneli (2^32lik tabanda) olduğunu
hem de pozitif mi yoksa negatif mi olduğunu tutacak. Örneğin, `length` -5 ise,
sayının 5 haneli ve negatif olduğunu anlayacağız. Eğer `length`
0 ise, tamsayının da 0 olduğunu anlayacağız. Eğer `length` sıfır
değilse, ama `alloc` 0 ise, hafızanın stack üzerinde ayrıldığını
anlayacağız.

`bnz_t`'yi kullanıma hazırlamak için, aşağıdaki fonksiyonu kullanacağız. 

	:::c
	void bnz_init(bnz_ptr bnz)
	{
		memset(bnz, 0, sizeof(bnz_t));
	}

`bnz_init` bir kez çağırıldıktan sonra, `bnz_t` türü farklı sayıları tutmak için tekrar tekrar kullanılabilir.

Hafızada ayırdığımız yerin, `n` haneli bir sayıyı tutabilecek kadar büyük olmasını temin etmek için, aşağıdaki makroyu kullanacağız.

	:::c
	#define BN_GROW(bn, n) ((n) > (bn)->alloc ? \
		bnz_resize((bn), (n)) \
		: (bn)->digits)
		
Bu makro, eğer zaten yeterli yer ayrılmışsa, `digits` üyesini
döndürecek, aksi takdirde, `bnz_resize` fonksiyonunu çağıracak.

	:::c

	bn_digit_t *bn_xrealloc(bn_digit_t *p_old, bn_size_t size)
	{
		bn_digit_t *p_new = realloc(p_old, size * sizeof(bn_digit_t));
		if (!p_new)
			exit(-1);
		return p_new;
	}

	bn_digit_t *bn_xmalloc(bn_size_t size)
	{
		bn_digit_t *p = malloc(size * sizeof(bn_digit_t));
		if (!p)
			exit(-1);
		return p;
	}

	bn_digit_t *bnz_resize(bnz_ptr bn, bn_size_t size)
	{
		if (bn->alloc)
			bn->digits = bn_xrealloc(bn->digits, size);
		else
			bn->digits = bn_xmalloc(size);

		bn->alloc = size;

		return bn->digits;
	}
	
`bn_xmalloc` ve `bn_xrealloc` fonksiyonları, `malloc` ve `realloc`
kullanarak gerekli hafıza alanlarını ayıramazlarsa, hata koduyla
programı sonlandırıyor. `bnz_resize` fonksiyonu, daha önce
ayrılmış bir hafıza alanı varsa, onu genişletiyor. Eğer daha
önce bir hafıza ayrılmamışsa, yeni yer ayırıyor.

Büyük tamsayılara, signed integer değeri atamak için, aşağıdaki
fonksiyonu kullanacağız.

	:::c
	bn_size_t bn_trim(bn_digit_t *digits, bn_size_t current_size)
	{
		while (digits[current_size - 1] == 0 && current_size > 0)
			current_size--;
		return current_size;
	}

	void bnz_set_int(bnz_ptr bn, int i)
	{
		if (!i)
		{
			bn->length = 0;
			return;
		}

		bn_size_t num_digits = ((sizeof(int) - 1) / sizeof(bn_digit_t)) + 1;
		bn_digit_t *rp = BN_GROW(bn, num_digits);
		*((int *)rp) = BN_ABS(i);
		if (*((int *)rp) == i) // sayi positif
			bn->length = bn_trim(rp, num_digits);
		else // sayi negatif
			bn->length = -bn_trim(rp, num_digits);
	}

Eğer, `i`'nin değeri sıfır ise, tek yapmamız gereken `length`'i
sıfıra atamak. `num_digits`, `i`'nin kaç hanede saklanacağını
tutuyor. Eğer `sizeof(int) == sizeof(bn_digit_t)` ise, bu değer
1 olacak. Yeterli yer ayırdığımızdan emin olmak için, `BN_GROW`
makrosunu çağırıyoruz. `digits` array'i içinde her zaman pozitif
sayılar saklayacağımız için, mutlak değer alıyoruz. `bn_trim`
fonksiyonu ise, sayının başındaki sıfır haneleri silindikten
sonra kalan hane sayısını veriyor. Tam sayılar üzerinde
işlem yapacak algoritmaları `digits[length-1]`'in
sıfır olmadığı varsayımına göre çalıştıracağımız için,
`bn_trim` kullanarak, üstteki 0 hanelerini silmemiz gerekiyor.

Sonraki yazılarda, iki sayının mutlak değerlerini karşılaştırmamız
gerekecek, bunun için, aşağıdaki fonksiyonları kullanacağız.

	:::c
	int bn_cmp_n(const bn_digit_t *op1, const bn_digit_t *op2, bn_size_t opsize)
	{
		while (--opsize >= 0)
		{
			if (op1[opsize] != op2[opsize])
			{
				return (op1[opsize] > op2[opsize]) - (op1[opsize] < op2[opsize]);
			}
		}
		return 0;
	}


	int bn_cmp_nn(const bn_digit_t *op1, bn_size_t op1size, const bn_digit_t *op2, bn_size_t op2size)
	{
		if (op1size != op2size)
			return (op1size > op2size) - (op1size < op2size);
		
		return bn_cmp_n(op1, op2, op1size);
	}
	
İlk fonksiyon, uzunlukları eşit olan iki doğal sayıyı karşılaştırmaya yarıyor. İkinci fonksiyon
ise, tüm uzunluklardaki doğal sayılar için kullanılabilir. İki doğal sayıyı karşılaştırırken,
eğer birinin hane sayısı diğerinden büyükse, özel bir inceleme yapmadan, hane sayısı
çok olanı büyük ilan edebiliriz. Hane sayılarının aynı olduğu durumlarda, üstten alta
doğru haneleri kontrol etmemiz gerekiyor. Herhangi bir hanede farklılık olduğunda,
sayıların hangisinin büyük olduğunu tespit edebiliriz. Eğer tüm haneleri eşitse,
sayılar da eşit olmak zorunda. Bu iki fonksiyon da, birinci argüman büyükse 1,
ikinci argüman büyükse -1, argümanlar eşit ise 0 döndürecek.

Gelecek yazılarda, tamsayılar üzerinde dört işlem yapacağız. Bunun için, daha önceki
fonksiyonlardan faydalanmakla birlikte, işleme giren sayıların pozitif veya negatif
olma durumlarına dikkat edeceğiz.

Ek Kaynaklar
------------

 - Knuth D. Art of The Computer Programming Vol 2 Section 4.3.1
 - Wikipedia. [Signed number representations](https://en.wikipedia.org/wiki/Signed_number_representations)
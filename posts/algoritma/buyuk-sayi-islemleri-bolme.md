<!--
.. date: 2020-03-04 23:18
.. description: 
.. slug: buyuk-sayi-islemleri-bolme
.. title: Büyük Sayı Algoritmaları - Bölme
.. tags: mathjax
-->

Daha önceki yazılarda, değişken-genişlikteki doğal sayılar üzerinde
toplama, çıkarma ve çarpma algoritmalarına değinmiştik. Bu yazıda, D. Knuth'un
*The Art of The Computer Programming* kitabının 4.3.1'inci kısmında anlatılan
*Algoritm D.*'den bahsedeceğim. Bu algoritma, değişken-genişlikteki doğal
sayılarda bölme işlemi yaparken, kabul edilebilir bir performansa sahip.
Kodlara geçmeden önce, algoritmayı inceleyelim. <!-- TEASER_END -->

<p>
İki doğal sayı olan \( u = (u_{m+n-1} \ldots u_1u0)_b \) ve \(v = (v_{n-1} \ldots v_1v0)_b\) için,
\(v_{n-1} \neq 0\) ve \(n > 1\) olmak üzere, b-tabanındaki bölümü \(\lfloor u / v \rfloor = (q_mq_{m-1} \ldots q_0)_b\)
ve kalanı \(u \mod v = (r_{n-1} \ldots r_1r_0)_b\) olarak tanımlıyoruz.
</p>

 - __D.1__ \[Normalizasyon] Bu adımda, bölenin en üst hanesi sayı tabanının yarısından büyük veya eşit olacak, ancak, bölenin
   hane sayısı artmayacak şekilde, bölünen ve böleni bir \\(d\\) sayısı ile çarpıyoruz. Bu işlemi bilgisayarda yaparken,
   bölenin en üst biti 1 olacak kadar, iki sayıyı kaydırabiliriz. Bu adımda, bölünenin hane sayısı 1 artmalı.
   Eğer \\(d\\) ile çarpıldığında hane sayısı artmamışsa, sayının başına bir 0 eklememiz gerekiyor.
 - __D.2__ \[Döngü Başlangıcı] \\(j = m\\). Döngü sayacını bölünen ve bölenin hane sayılarının farkına eşitliyoruz.
 - __D.3__ \[\\(\hat{q}\\) hesabı] \\(\hat{q} \leftarrow \lfloor (u_{j+n}b + u_{j+n-1}) / (v_{n-1}) \rfloor\\) ve
  \\(\hat{r} \leftarrow(u_{j+n}b + u_{j+n-1}) \mod v_{n-1} \\) olsun. Türkçe ifade edersek, bölünenin üstten
  iki hanesini, bölenin en üst hanesine bölüp, sonucu \\(\hat{q}\\) ve kalanı \\(\hat{r}\\) olarak tanımla.
  Burada hesaplanan \\(\hat{q}\\), bölümün bir hanesinin tahmini değeri olacak. Kitaptaki açıklamalardan,
  burada hesaplanan tahmini değerin, olması gerekenden en çok 2 fazla olabileceği anlaşılıyor. Eğer  \\(\hat{q} = b\\)
  ise, veya \\(\hat{q}v_{n-2} > b\hat{r} + u_{j+n-2}\\) ise \\(\hat{q}\\) değerini 1 azaltıp, \\(\hat{r}\\)
  değerine \\(v_{n-1}\\) ekleyip, \\(\hat{r} < b\\) ise bu testi tekrar ediyoruz. Burada yapılan işlemi de
  Türkçe ifade etmek gerekirse, bölen ve bölünenin birer hanelerine daha bakarak, \\(\hat{q}\\) değerini
  düzeltiyoruz. Böylece, \\(\hat{q}\\)'in 2 fazla olduğu durumların tümünü, 1 fazla olduğu durumların büyük
  bir çoğunluğunu hızlıca elemiş oluyoruz. Ben bu iddiayı kanıtlamadım, ancak, birçok farklı sayı ile test
  ederek teyit ettim.
 - __D.4__ \[Çarp Çıkar] \\((u\_{j+n} \ldots u\_j)\_b = (u\_{j+n} \ldots u\_j)\_b - \hat{q}(v\_{n-1} \ldots v\_0)\_b \\).
   Bu adımda, bir önceki adımda hesaplanan \\(\hat{q}\\) ile böleni çarpıp, j (döngü sayacı) kadar
   hane kaydırarak, bölünenden çıkarıyoruz. Çıkarma işleminin sonucu negatif ise, bunu hatırlamamız gerekiyor.
 - __D.5__ \[Kalanı Kontrol Et] \\(q_j \leftarrow \hat{q}\\) olarak ayarla. Eğer, bir önceki adımın sonucu negatif
   ise __D.6__'ya, değilse, __D.7__'ye geç.
 - __D.6__ \[Geri Ekle] \\(q_j\\)'yi 1 azalt ve \\((u\_{n+j} \ldots u\_j)\_b\\)'ye \\((0v\_{n-1} \ldots v\_n)\_b\\) ekle.
   D. Knuth bu adımın gerekli olduğu durumların çok nadir olduğunu belirtmiş. Ben de
   algoritmayı test ederken, milyarlarca rastgele bölme işlemi yapmama rağmen bu adıma gelemediğim için, bu adımı
   tetikleyecek bir [rastgele sayı üreticisi](rastgele-sayi-uretici.html) yazmak zorunda kaldım.
   D. Knuth, bu adımın gerekli olma ihtimalini 2/b olarak vermiş. Benim bulabildiğim örneklerin çoğunda,
   hem bölenin, hem bölünenin üstten bir alttaki hanesi sıfırdı.
 - __D.7__ \[Döngü] j'yi 1 azalt ve, eğer \\(j >= 0\\) ise __D.3__'e git.
 - __D.8__ \[Düzelt] Bölme işleminin sonucu \\((q\_m \ldots q\_0)\_b\\). Eğer kalan bulmak gerekiyorsa,
   \\((u\_{n-1} \ldots u\_0)\_b\\) sayısını __D.1__'deki \\(d\\) sayısına bölmeliyiz. Eğer __D.1__'de
   bit kaydırma yapılmışsa, aynı miktarda sağa bit kaydırarak kalanı elde edebiliriz.
   
Algoritmayı C'de yazmadan önce, onluk tabanda bir örnek yapalım. Bölünen 713892 ve bölen
152 olsun.

 - __D.1__ \[Normalizasyon] Onluk tabanda işlem yaptığımız için, bölenin üst hanesinin 5 veya
 daha büyük bir sayı olmasını istiyoruz. \\(d\\)'yi 6 seçersek, bölünen 713892 x 6 = 4283352,
 bölen ise 152 x 6 = 912 olur.
 - __D.2__ \[Döngü Başlangıcı] j = (6 - 3) = 3.
 - __D.3__ \[\\(\hat{q}\\) hesabı] \\(\hat{q} = \lfloor \frac{42}{9} \rfloor = 4 \\), \\(\hat{r} = 42 \mod 9 = 6\\).
 Düzeltme testini yaptığımızda, \\(4 \* 1 \ngtr 68\\) olduğundan, düzeltme yapmayacağız. Bu hesaptaki 4 \\(\hat{q}\\), 1 bölenin bir sonraki hanesi,
 6 \\(\hat{r}\\) ve 8 bölünenin bir sonraki hanesi.
 - __D.4__ \[Çarp Çıkar] 4 x 912 = 3648. 4283 - 3648 = 635. Bölünenin yeni değeri, 635352.
 - __D.5__ \[Kalanı Kontrol Et] Sonucun 3. hanesi (0 tabanlı indekslemeye göre) 4 olarak tespit edildi.
   Bir önceki adımın sonucu (635) pozitif olduğu için, __D.7__'ye geç.
 - __D.7__ \[Döngü] j = 2, __D.3__'e geç.
 - __D.3__ \[\\(\hat{q}\\) hesabı] \\(\hat{q} = \lfloor \frac{63}{9} \rfloor = 7 \\), \\(\hat{r} = 63 \mod 9 = 0\\).
 Düzeltme testini yaptığımızda, \\(7 \* 1 \> 5\\) olduğu için, \\(\hat{q} = 6\\) ve \\(\hat{r} = 0 + 9 = 9\\). Testi tekrar
 yaptığımızda, \\(7 \* 1 \ngtr 95\\) olduğundan, devam ediyoruz.
 - __D.4__ \[Çarp Çıkar] 6 x 912 = 5472. 6353 - 5472 = 881. Bölünenin yeni değeri, 88152.
 - __D.5__ \[Kalanı Kontrol Et] Sonucun 2. hanesi (0 tabanlı indekslemeye göre) 6 olarak tespit edildi. Bir önceki
 adımın sonucu (881) pozitif olduğu için, __D.7__'ye geç.
 - __D.7__ \[Döngü] j = 1, __D.3__'e geç.
 - __D.3__ \[\\(\hat{q}\\) hesabı] \\(\hat{q} = \lfloor \frac{88}{9} \rfloor = 9 \\), \\(\hat{r} = 88 \mod 9 = 7\\).
 Düzeltme testini yaptığımızda, \\(9 \* 1 \ngtr 71\\) olduğundan, düzeltme yapılmayacak.
 - __D.4__ \[Çarp Çıkar] 9 x 912 = 8208. 8815 - 8208 = 607. Bölünenin yeni değeri, 6072.
 - __D.5__ \[Kalanı Kontrol Et] Sonucun 1. hanesi (0 tabanlı indekslemeye göre) 9 olarak tespit edildi. Bir önceki
 adımın sonucu (607) pozitif olduğu için, __D.7__'ye geç.
 - __D.7__ \[Döngü] j = 0, __D.3__'e geç.
 - __D.3__ \[\\(\hat{q}\\) hesabı] \\(\hat{q} = \lfloor \frac{60}{9} \rfloor = 6 \\), \\(\hat{r} = 60 \mod 9 = 6\\).
 Düzeltme testini yaptığımızda, \\(6 \* 1 \ngtr 67\\) olduğu için, herhangi bir düzeltme yapmayacağız.
 - __D.4__ \[Çarp Çıkar] 6 x 912 = 5472. 6072 - 5472 = 600. Bölünenin yeni değeri, 600.
 - __D.5__ \[Kalanı Kontrol Et] Sonucun 0. hanesi (0 tabanlı indekslemeye göre) 6  olarak tespit edildi. Bir önceki
   adımın sonucu (600) pozitif olduğu için, __D.7__'ye geç.
 - __D.7__ \[Döngü] j = -1, döngüden çık.
 - __D.8__ \[Düzelt] Elde ettiğimiz haneleri yanyana getirerek, bölümü 4696 olarak buluyoruz.
   kalanı bulmak için, 600'ü 6'ya bölmemiz gerekiyor. Dolayısıyla, kalan, 600/6 = 100 oluyor.

Algoritmayı dikkatli takip ettiyseniz, normalizasyon adımı haricinde, kağıt/kalemle bölme
işleminden bir farkı yok. Kağıt/kalemle 4283352 sayısını, 912 ile bölerek bunu teyit
edebilirsiniz.

Algoritmanın ilk adımında yapılacak kaydırma miktarını hesaplamak için, sayının üst 0 bitlerini
saymamız gerekiyor. Bunun için, aşağıdaki `nlz` (number of leading zeros) fonksiyonunu kullanacağız.

	:::C
	#if defined(__GNUC__)
	#define nlz(x) __builtin_clz(x)
	#elif defined(_MSC_VER)
	#define nlz(x) __lzcnt(x)
	#else
	int nlz(unsigned int value)
	{
		int i;
		for (i = 0; value; i++)
			value >>= 1;
		return 32 - i;
	}
	#endif
	
Tanıdığımız derleyecilerde, derleyecilerin intrinsic fonksiyonlarını kullanacağız, aksi durumda,
`nlz` fonksiyonunu kendimiz sağlamak zorundayız. Aşağıdaki fonksiyonda, kitaptakinden farklı bir
notasyon kullandım. Bölüm ve kalan, yukarıdaki gibi `q` ve `r`, bölünen `n`, bölünenin uzunluğu `nlen`,
bölen `d` ve bölenin uzunluğu `dlen`. Döngü sayacı olarak da, `j` yerine `i` kullandım.

	:::C
	void bn_div_n(bn_digit_t *q, bn_digit_t *r, bn_digit_t *n, bn_size_t nlen, bn_digit_t *d, bn_size_t dlen)
	{
		// Geçiçi kullanılacak hafıza alanları.
		
		// nn => Bölünenin normalizasyon geçirmiş hali
		bn_digit_t *nn = alloca((nlen + 1) * sizeof(bn_digit_t));
		
		// dn => Bölenin normalizasyon geçirmiş hali.
		bn_digit_t *dn = alloca((dlen) * sizeof(bn_digit_t));
		
		
		// D.1
		// ================
		
		// normalizasyon için kaydırma miktarı
		int s = nlz(d[dlen - 1]);

		// Kaydırma işlemleri
		bn_size_t i;

		for (i = dlen - 1; i > 0; i--)
		{
			dn[i] = (d[i] << s) | ((bn_long_digit_t)(d[i - 1]) >> (BN_DIGIT_BITS - s));
		}
		dn[0] = d[0] << s;

		nn[nlen] = ((bn_long_digit_t)(n[nlen - 1]) >> (BN_DIGIT_BITS - s));
		for (i = nlen - 1; i > 0; i--)
		{
			nn[i] = (n[i] << s) | ((bn_long_digit_t)(n[i - 1]) >> (BN_DIGIT_BITS - s));
		}
		nn[0] = n[0] << s;

		// D.2 DÖNGÜ
		for (i = nlen - dlen; i >= 0; i--)
		{
			// D.3 - şapkalı q hesabı için, 64 bit aritmetik kullanacağız.
			bn_long_digit_t qhat;
			bn_long_digit_t rhat;
			bn_long_digit_t ulong = ((bn_long_digit_t)(nn[dlen + i]) << BN_DIGIT_BITS) + (bn_long_digit_t)(nn[dlen + i - 1]);
			
			qhat = ulong / dn[dlen - 1];
			
			// Düzgün bir derleyici (i.e GCC/Clang) bunu optimize edecektir.
			// eğer etmiyorsa, rhat = ulong - (qhat * dn[dlen - 1])
			rhat = ulong % dn[dlen - 1]; 
			
			// qhat 2 haneli mi kontrolü
			if (qhat > BN_DIGIT_MAX)
			{
				--qhat;
				rhat += dn[dlen - 1];
			}
			
			// Düzeltme döngüsü
			while ((rhat >> BN_DIGIT_BITS) == 0 && (qhat * dn[dlen - 2]) >((rhat << BN_DIGIT_BITS) + nn[dlen + i - 2]))
			{
				--qhat;
				rhat += dn[dlen - 1];
			}

			// D.4 - Çarp-Çıkar
			bn_digit_t borrow = 0;
			bn_size_t k;
			for (k = 0; k < dlen; k++)
			{
				ulong = dn[k] * qhat;
				ulong += borrow;
				borrow = nn[i + k] < ((bn_digit_t)ulong);
				nn[i + k] -= (bn_digit_t)ulong;
				borrow += ulong >> BN_DIGIT_BITS;
			}

			// Elimizde kalanı bir üst haneye taşımak için
			ulong = borrow;
			borrow = (nn[i + k] < borrow);
			nn[i + k] -= (bn_digit_t)ulong;
			
			// D.6 - Çıkarma sonucu negatif ise, düzelt. Burası nadiren çalışacak.
			if (borrow)
			{
				--qhat;
				bn_add_n(nn + i, nn + i, dn, dlen);
			}
			
			// D.5 - Sonucun ilgili hanesini yazıyoruz.
			q[i] = (bn_digit_t)qhat;
			
			// D.7 - i'yi eksiltip, i >= 0 ise D.3'e geç.
		}

		// D.8 Eğer kalan istenmişse, düzelt
		if (r)
		{
			for (i = 0; i < dlen-1; i++)
			{
				r[i] = (nn[i] >> s) | ((bn_long_digit_t)nn[i + 1]) << (BN_DIGIT_BITS - s);
			}
			r[i] = nn[i] >> s;
		}
	}
	
Bu fonksiyonla ilgili değinmek istediğim birkaç husus var. Öncelikle, geçici hafıza için `malloc`/`free` yerine
`alloca` kullandım. Geçici hafızayı stack üzerinde tutmak genellikle daha etkin olsa da, eğer çok büyük
sayılar arasında bölme işlemi yapacaksanız, stack alanını tüketebilirsiniz. Böyle bir riski öngörüyorsanız,
`alloca` yerine `malloc`/`free` tercih etmelisiniz. Bir diğer konu da, çarp/çıkar aşaması. Daha önceki
yazılarda, çarpma ve çıkarma işlemleri için ayrı fonksiyonlar tanımlamıştık. Ancak, döngü içerisinde ekstra
fonksiyon çağrısından ve çarpma/çıkarmanın ara sonucu için ekstra hafıza ayırma yükünden kaçınmak için,
çarpma ve çıkarma işlemlerini buraya bir `for` döngüsü ile dahil ettim.

Yukarıdaki algoritma, GMP kütüphanesinde, *basecase division* olarak geçiyor. Bazı özel durumlar için,
daha verimli algoritmalar kullansalar da, bölme işlemi için genellikle kullanılan algoritma bu gibi
görünüyor.

Ek Kaynaklar
------------

 - Knuth D. Art of The Computer Programming Vol 2 Section 4.3.1
 - [GMP Division Algorithms](https://gmplib.org/manual/Division-Algorithms.html#Division-Algorithms)
 - [Wikipedia - Division algorithm](https://en.wikipedia.org/wiki/Division_algorithm)
 
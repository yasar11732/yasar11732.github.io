<!--
.. date: 2021-03-01 22:44
.. description: 
.. slug: buyuk-sayi-islemleri-bolme
.. title: Büyük Sayı Algoritmaları - Bölme
.. tags: mathjax
-->

İki doğal sayı arasında bölme işlemi yaparken kullanılabilecek
en basit algoritmalardan biri, tekrar eden çıkarma işlemidir. 20'yi
9'a bölmek için, iki defa çıkarma işlemi yapıp, böleni 2, kalanı 2
bulabiliriz. Ancak, sayılar büyüdükçe, bu yöntem pratik olmaktan çıkacaktır.
Örneğin, kağıt kalem ile 51234 sayısını 7'ye bölmek için, tekrar eden çıkarma
işlemi yapmayı deneyebilirsiniz. Tekrar eden çıkarma işlemini büyük sayılara
uygulayamacağımız için, daha iyi bir algoritma tercih etmek zorundayız. Dört işlem
içinde, işlemci zamanı açısından, en pahalı işlemin bölme işlemi olmasını
bekleyebilirsiniz. Aşağıda bahsedilecek algoritma, D. Knuth'un *The Art of The Computer Programming*
kitabının ikinci cildinde geçen *Algoritm D.*'nin, mümkün olduğu ölçüde C diline aktarılmış hali.

Kodlara geçmeden önce, algoritmayı aşağıdaki şekilde tarif edebiliriz. Bölünen `n`,
bölünen hane sayısı `nlen`, bölen `d` bölünen hane sayısı `dlen` olsun.

 1. Bölen'i en üst biti 1 olana kadar sola kaydır, aynı miktarda bölüneni de kaydır.
 2. Döngü sayacına (i olsun), bölen ve bölünenin hane sayılarının farkını ata. (i = nlen - dlen)
 3. \\(\hat{q} \leftarrow \lfloor \frac{(n_{dlen+i},n_{dlen+i-1})\_{2^{32}}}{d_{dlen-1}} \rfloor\\). Bu adımda,
    bölünenin üstten 2 hanesi, bölenin en üst hanesine bölünür. Burada, üstten 2 hane alırken,
	algoritmanın birinci adımında, bölünenin hane sayısının bir arttığını hesaplayarak alınması gerekiyor.
	Eğer hane sayısı artmamışsa, üst haneyi sıfırla doldurmak gerekiyor.
 4. Bir önceki adımda hesaplanan \\(\hat{q}\\) ile bölen çarpılıp, i (döngü sayacı) kadar
    hane kaydırarak, bölünenden çıkar.
 5. Eğer bir önceki adımın sonucu negatif ise, bölünen'e bölen'i ekleyip (yine i kadar kaydırdıktan sonra), \\(\hat{q}\\)'den
    1 çıkar.
 6. Bölümün i hanesine (0 tabanlı indeksleme) \\(\hat{q}\\)'i yazıyoruz.
 7. i'yi 1 eksiltip, eğer 0 veya büyükse, üçüncü adıma dön.
 8. Eğer kalan hesaplanmak isteniyorsa, bölünendeki miktarı, birinci adımdaki kadar, sağa
    kaydır.
	
Burada açıklanması gereken birkaç nokta var. Üçüncü ve dördüncü adımda kullanılan \\(\hat{q}\\)
değişkeni, bölümün bir hanesinin tahmini değeri, çünkü, bölme işleminde sadece bölenin
en üst hanesini kullanıyoruz. Birinci adımda yapılan normalizasyon, bu tahmini değerin
hata aralığını azaltmaya yarıyor. Beşinci adıma, \\(\hat{q}\\) yanlış hesaplandığında
girilecek. Bu adıma girme ihtimali çok düşük olduğu için, nadiren performansa etkisi olacaktır.

Algoritmanın daha iyi anlaşılabilmesi için, onluk taban 713892 ile 152 sayısını bölelim.

 - 1a. Normalizasyon için
    iki sayıyı da 6 ile çarpalım. 713892 x 6 = 4283352, 152 x 6 = 912. Bu adımın amacı
	bölenin en üst hanesinin mümkün olduğunca büyük bir rakam olması.
 - 2a. Döngü sayacı 6 - 3 = 3.
 - 3a. \\(\hat{q} = \lfloor \frac{42}{9} \rfloor = 4 \\)
 - 4a. 4 x 912 = 3648. 4283 - 3648 = 635. Bölünenin yeni değeri, 635352.
 - 5a. Bu adıma gerek yok.
 - 6a. Bölümün 3. hanesini 4 olarak ayarla.
 - 7a. Döngü sayacı 2.
 - 3b. \\(\hat{q} = \lfloor \frac{63}{9} \rfloor = 7 \\)
 - 4b. 7 x 912 = 6384. 6353 - 6384 = -31.
 - 5b. Bir önceki adım negatif olduğu için, \\(\hat{q} = 6\\). 912 - 25 = 881. Bölünenin yeni değeri 88152.
 - 6b. Bölümün 2. hanesi 6.
 - 7b. Döngü sayacı 1.
 - 3c. \\(\hat{q} = \lfloor \frac{88}{9} \rfloor = 9 \\)
 - 4c. 9 x 912 = 8208. 8815 - 8208 = 607. Bölünenin yeni değeri 6072.
 - 5c. Beşinci adıma gerek yok.
 - 6c. Bölümün 1. hanesi 9.
 - 7c. Döngü sayacı 0.
 - 3d. \\(\hat{q} = \lfloor \frac{60}{9} \rfloor = 6 \\)
 - 4d. 6 x 912 = 5472. 6072 - 5472 = 600. Bölünenin yeni değeri 600.
 - 5d. Beşinci adıma gerek yok.
 - 6d. Bölümün 0. hanesi 6.
 - 7d. Döngü sayacı -1, döngüden çık.
 - 8d. Bölme sonucu 4696. Kalan 600 / 6 = 100. (6 sayısı birinci adımdan geliyor.)

Algoritmayı dikkatli takip ettiyseniz, normalizasyon adımı haricinden, kağıt/kalemle bölme
işleminden bir farkı yok. Kağıt/kalemle 4283352 sayısını, 912 ile bölerek bunu teyit
edebilirsiniz.
	
2/1 bölme işlemi için ayrı bir fonksiyon yazmak yerine, makro yazmayı tercih ettim. Böylece,
ekstra bir fonksiyon çağrısından kurtulmuş olacağız. Aynı zamanda, derleyicinin ekstra
optimizasyonlar yapmasına da yardımcı olabilir. Eğer bölme işleminin sonucu tek bir
haneye sığamayacak kadar büyük olursa, `BN_DIGIT_MAX` döndürülecek.

Algoritmanın ilk adımında, yapılacak kaydırma miktarını hesaplamak için, sayının üst 0 bitlerini
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
`nlz` fonksiyonunu kendimiz sağlamak zorundayız. Yardımcı fonksiyonlarla birlikte, bölme işlemini
aşağıdaki gibi yapabiliriz.

	:::C
	
	void bn_div_n(bn_digit_t *q, bn_digit_t *r, bn_digit_t *n, bn_size_t nlen, bn_digit_t *d, bn_size_t dlen)
	{
		// Geçiçi kullanılacak hafıza alanları.
		bn_digit_t *nn = alloca((nlen + 1) * sizeof(bn_digit_t));
		bn_digit_t *dn = alloca((dlen) * sizeof(bn_digit_t));
		bn_digit_t *tmp = alloca((nlen + 1) * sizeof(bn_digit_t));
		
		// normalizasyon için kaydırma miktarı
		int s = nlz(d[dlen - 1]);

		// 1 - Bölen ve Bölüneni kaydırıp, nn ve dn array'lerine kaydet.
		bn_size_t i;
		for (i = dlen - 1; i > 0; i--)
		{
			dn[i] = (d[i] << s) | (d[i - 1] >> (BN_DIGIT_BITS - s));
		}
		dn[0] = d[0] << s;

		nn[nlen] = (n[nlen - 1] >> (BN_DIGIT_BITS - s));
		for (i = nlen - 1; i > 0; i--)
		{
			nn[i] = (n[i] << s) | (n[i - 1] >> (BN_DIGIT_BITS - s));
		}
		nn[0] = n[0] << s;
		
		// 2 - Döngü sayacını hesapla
		for (i = nlen - dlen; i >= 0; i--)
		{
			// 3 - Bölünenin üst 2 hanesini, bölenin üst hanesine böl.
			bn_digit_t qhat;
			__div2_by_1q(qhat, nn[dlen + i - 1], nn[dlen + i], dn[dlen - 1]);
			
			// 4 - Çarp Çıkar.
			tmp[dlen] = bn_mul_n_1(tmp, dn, dlen, qhat);
			bn_digit_t borrow = bn_sub_n(nn + i, nn + i, tmp, dlen + 1);
			
			// 5 - Çıkarma sonucu negatif ise, düzelt.
			if (borrow)
			{
				--qhat;
				bn_add_n(nn + i, nn + i, dn, dlen);
			}
			
			q[i] = qhat;
		}

	}


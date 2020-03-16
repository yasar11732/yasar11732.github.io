<!--
.. date: 2020-03-17 00:14
.. description: 
.. slug: buyuk-sayi-islemleri-tamsayi-dort-islem
.. title: Büyük Sayı Algoritmaları - Tamsayılarda Dört İşlem
-->

Daha önceki yazılarda, doğal sayılarda dört işlem algoritmalarına değinmiştik.
Bu yazıda, önceden yazdığımız alt seviye fonksiyonları kullanarak, tam sayılar üzerinde
dört işlem gerçekleştiren fonksiyonları kodlayacağız.  <!-- TEASER_END -->

Projenin bu yazıya kadar olan kısmını [Github üzerinden indirebilirsiniz](https://github.com/yasar11732/LibBigNumber/archive/buyuk-sayi-islemleri-metin.zip)

Tamsayılar üzerinde toplama yaparken, dört farklı durumla karşılaşabiliriz.

 - **Sayıların ikisi de pozitif:** Doğal sayılarda toplama işlemi yapacağız.
 - **Sayılardan biri negatif, negatif olanın mutlak değeri küçük:** Doğal sayılarda çıkarma yapacağız.
 - **Sayılardan biri negatif, negatif olanın mutlak değeri büyük:** Negatif sayının mutlak değerinden,
   diğer sayıyı çıkarıp, sonucu negatif olarak ayarlayacağız.
 - **Sayıların ikisi de negatif**: Sayıların mutlak değerlerini toplayıp, sonucu negatif olarak ayarlayacağız.
 
Bu dört durumu, aşağıdaki gibi iki duruma sadeleştirmek mümkün.

 - **Sayıların İşareti Aynı**: Sayıların mutlak değerlerini topla, aynı işareti kullan.
 - **Sayıların İşareti Farklı**: İlk sayının mutlak değerinden, ikinci sayının mutlak değerini
   çıkar. Eğer sonuç pozitif ise, ilk sayının işaretini kullan, değilse, ilk sayının işaretinin
   zıttını kullan.
   
Bu algoritmayı kodlayabilmek için, mutlak değerler üzerinde toplama çıkarma yapan
fonksiyonlara ihtiyacımız olacak.

	:::C
	bn_size_t bnz_add_abs(bnz_ptr result, bnz_constptr op1, bnz_constptr op2)
	{
		bn_size_t s1 = BN_ABS(op1->length);
		bn_size_t s2 = BN_ABS(op2->length);
		bn_digit_t carry;
		bn_digit_t *rp;
		
		if (s1 < s2)
		{
			bnz_constptr tmp = op1;
			op1 = op2;
			op2 = tmp;

			bn_size_t tmps = s1;
			s1 = s2;
			s2 = tmps;
		}

		rp = BN_GROW(result, s1 + 1);
		carry = bn_add_nn(rp, op1->digits, s1, op2->digits, s2);

		rp[s1] = carry;
		return s1 + carry;
	}
	
Eğer argümanlardan ilki, diğerinden kısa ise, işaretçilerin yerlerini
değiştiriyoruz, çünkü, `bn_add_nn` fonksiyonu ilk argümanın daha kısa
olmadığını varsayıyor. Fonksiyondan, sonucun hane sayısını döndürüyoruz.

	:::C
	bn_size_t bnz_sub_abs(bnz_ptr result, bnz_constptr op1, bnz_constptr op2)
	{
		int s1 = BN_ABS(op1->length);
		int s2 = BN_ABS(op2->length);
		bn_digit_t *rp;

		int cmp = bn_cmp_nn(op1->digits, s1, op2->digits, s2);

		if (cmp > 0)
		{
			rp = BN_GROW(result, s1);
			bn_sub_nn(rp, op1->digits, s1, op2->digits, s2);
			return bn_trim(rp, s1);
		}
		else if (cmp < 0)
		{
			rp = BN_GROW(result, s2);
			bn_sub_nn(rp, op2->digits, s2, op1->digits, s1);
			return -bn_trim(rp, s2);
		}
		else
		{
			return 0;
		}
	}
	
İki sayının mutlak değerleri arasında çıkarma yaparken, hangisinin mutlak
değerinin daha büyük olduğunu kontrol etmeliyiz. Bunun için, [daha önce tanımladığımız](buyuk-sayi-islemleri-tamsayilar.html)
`bn_cmp_nn` fonksiyonunu kullanacağız. Burada,
`bn_cmp_nn` fonksiyonuna argüman olarak, sayıların uzunluklarının mutlak
değerlerini göndermemiz gerekiyor. Böylece, mutlak değerler arasında karşılaştırma
yapılmış oluyor. Karşılaştırma yaptıktan sonra, eğer birinci sayının büyük
olduğunu tespit edersek, birinciden ikinciyi çıkarıp, pozitif uzunluk
döndüreceğiz. Aksi takdirde, ikinciden birinciyi çıkarıp, negatif uzunluk
döndüreceğiz. Sayıların eşit olması durumunda, sıfır uzunluk döndürmemiz yeterli.

Yukarıdaki fonksiyonda, `bn_sub_n1` ve `bn_sub_nn` fonksiyonları kullandık,
ancak, bunları daha önce kodlamamıştık. Yeri gelmişken, onları da kodlayalım.

	:::C
	bn_digit_t bn_sub_n1(bn_digit_t *result, const bn_digit_t *op1, bn_digit_t op2, bn_size_t n)
	{
		bn_size_t i;
		bn_digit_t carry = op1[0] < op2;
		result[0] = op1[0] - op2;

		for (i = 1; i < n; i++)
		{
			bn_digit_t a = op1[i];
			bn_digit_t b = carry;
			carry = a < b;
			result[i] = a - b;
		}

		return carry;
	}

	bn_digit_t bn_sub_nn(bn_digit_t *result, const bn_digit_t *op1, bn_size_t n1, const bn_digit_t *op2, bn_size_t n2)
	{
		bn_digit_t carry = bn_sub_n(result, op1, op2, n2);
		if (n1 > n2)
			carry = bn_sub_n1(result + n2, op1 + n2, carry, n1 - n2);

		return carry;
	}

`bnz_add_abs` ve `bnz_sub_abs` fonksiyonlarını kullanarak, `bn_add` fonksiyonunu aşağıdaki gibi yazabiliriz;

	:::C
	void bnz_add(bnz_ptr result, bnz_constptr op1, bnz_constptr op2)
	{
		bn_size_t result_size;

		if ((op1->length ^ op2->length) >= 0)
		{
			result_size = bnz_add_abs(result, op1, op2);
		}
		else
		{
			result_size = bnz_sub_abs(result, op1, op2);
		}

		result->length = op1->length > 0 ? result_size : -result_size;
	}

Bu fonksiyonda nispeten ilginç olan tek şey, `op1->length ^ op2->length` ifadesi.
Bunu, sayıların işaretlerini karşılaştırmak için kullanıyoruz. Bu ifade, eğer
sayıların işaretleri aynı ise pozitif, değil ise negatif sonuç döndürecek. Binary `xor`
kurallarını ve [2'nin tümleyeni](buyuk-sayi-islemleri-tamsayilar.html) düzenini düşünürseniz,
`op1->length ^ op2->length` ifadesini anlamanız kolay olacaktır.

Çıkarma fonksiyonu da aşağıdaki gibi kodlanabilir;

	:::C
	void bnz_sub(bnz_ptr result, bnz_constptr op1, bnz_constptr op2)
	{
		bn_size_t result_size;
		if ((op1->length ^ op2->length) >= 0)
		{
			result_size = bnz_sub_abs(result, op1, op2);
		}
		else
		{
			result_size = bnz_add_abs(result, op1, op2);
		}

		result->length = op1->length > 0 ? result_size : -result_size;
	}
	
Bu fonksiyonun toplamadan tek farkı, işaretler aynı olduğunda çıkarma,
farklı olduğunda toplama yapılıyor olması.

Tamsayılarda çarpma işleminin mantığı, toplama çıkarmaya göre daha kolay.
Doğal sayılarda çarpma işlemi yaptıktan sonra, işleçlerin işaretleri aynı ise
sonucu pozitif, farklı ise negatif yapacağız.

	:::C
	void
	bnz_mul(bnz_t *result, bnz_constptr op1, bnz_constptr op2)
	{
		if (op1->length == 0 || op2->length == 0)
		{
			result->length = 0;
			return;
		}

		bn_size_t op1_len = BN_ABS(op1->length);
		bn_size_t op2_len = BN_ABS(op2->length);
		
		bn_size_t len = op1_len + op2_len;
		bn_digit_t *rp;
		if (result->digits == op1->digits || result->digits == op2->digits)
		{
			rp = bn_xmalloc(len);
		}
		else
		{
			rp = BN_GROW(result, len);
		}


		if (op1_len >= op2_len)
			bn_mul_n(rp, op1->digits, op1_len, op2->digits, op2_len);
		else
			bn_mul_n(rp, op2->digits, op2_len, op1->digits, op1_len);

		if (rp != result->digits)
		{
			free(result->digits);
			result->digits = rp;
			result->alloc = len;
		}

		len = bn_trim(rp, len);

		result->length = (op1->length ^ op2->length) < 0 ? -len : len;
	}

Kısaca birkaç noktaya değineyim;
	
	:::C
	if (op1->length == 0 || op2->length == 0)
	{
		result->length = 0;
		return;
	}
	
Burada, işleçlerden biri sıfırsa, başka bir işlem yapmadan, sonucu sıfıra ayarlıyoruz.

	:::C
	bn_size_t len = op1_len + op2_len;
	bn_digit_t *rp;
	if (result->digits == op1->digits || result->digits == op2->digits)
	{
		rp = bn_xmalloc(len);
	}
	else
	{
		rp = BN_GROW(result, len);
	}
	
İşleçlerin biri, aynı zamanda sonuç olarak verilmiş olabilir (Örn. bnz_mul(a, a, b) -> a = a x b). Bunu
test etmek için, işaretçileri karşılaştırıyoruz. Eğer çakışma tespit edersek, hafızada yeni yer
açmak zorundayız. Aksi halde, var olan alanı kullanacağız.

	:::C
	if (rp != result->digits)
	{
		free(result->digits);
		result->digits = rp;
		result->alloc = len;
	}

Eğer başlangıçta hafızada yeni bir yer açmış isek, `result`'ı bu alanı kullanacak şekilde ayarlamak gerekiyor.
Fonksiyonun geri kalanında yeni birşey yok.

Bölme işlemine geçmeden önce, bölmenin sonucu tam sayı olmadığında, nasıl yuvarlayacağımıza karar vermemiz
gerekiyor. Bu konuda 3 farklı standart var.

 - **Sıfıra Doğru Yuvarlama:** Bu yöntemde, sayının noktadan sonraki kısmını siliyoruz.
 - **Pozitif Sonsuza Yuvarlama:** Bu yöntemde, sayıyı yukarıya yuvarlıyoruz.
 - **Negatif Sonsuza Yuvarlama:** Bu yöntemde, sayıyı aşağıya yuvarlıyoruz.
 
Bu yazı için, sıfıra doğru yuvarlama yöntemini seçeceğim. Aşağıdaki tabloda, farklı bölen/bölünenler
için, bölüm ve kalanın olması gerektiği değerleri görebilirsiniz.

<pre>
+---------+-------+-------+-------+
| Bölünen | Bölen | Bölüm | Kalan |
+---------+-------+-------+-------+
|  3      |  2    |  1    | 1     |
+---------+-------+-------+-------+
|  3      | -2    | -1    | 1     |
+---------+-------+-------+-------+
| -3      |  2    | -1    | -1    |
+---------+-------+-------+-------+
| -3      | -2    |  1    | -1    |
+---------+-------+-------+-------+
</pre>

Kodlarımız da aşağıdaki gibi;

	:::C
	int bnz_div(bnz_ptr q, bnz_ptr r, bnz_constptr n, bnz_constptr d)
	{
		bn_size_t
			nlen, // bolunen uzunluk
			dlen, // bolen uzunluk
			qlen, // bolum uzunluk
			qsign, // bolum isareti (negatifse bolum negatif)
			nsign, // bolunen isareti (1 ise bolunen negatif)
			i;

		// bolum ve kalan icin isaretci
		bn_digit_t *qp, *rp;
		
		// bolunen ve bolen uzunluklari
		nlen = n->length;
		dlen = d->length;

		// sifirla bolme 
		if (dlen == 0)
		{
			fputs("Division By Zero", stderr);
			exit(-1);
		}

		// bolunen sifir
		if (nlen == 0)
		{
			if (q) q->length = 0;
			if (r) r->length = 0;
			return 0;
		}

		// bolum isareti
		qsign = nlen ^ dlen;
		
		// bolunen isareti
		nsign = n->length < 0;

		// bolen ve bolunen uzunluklari mutlak degeri
		dlen = BN_ABS(dlen);
		nlen = nsign ? -nlen : nlen;

		// bolunen bolenden kucuk
		if (nlen < dlen)
		{
			if (r)
			{
				BN_GROW(r, nlen);
				i = nlen;
				while (--i >= 0)
				{
					r->digits[i] = n->digits[i];
				}
				r->length = n->length < 0 ? -nlen : nlen;
					
			}

			if (q)
				q->length = 0;

			return 1;
		}

		// bolum max. uzunluk
		qlen = nlen - dlen + 1;
		
		// eger bolum verildiyse, uzunlugu ayarla
		// verilmediyse, gecici yer ac
		if (q)
		{
			qp = BN_GROW(q, qlen);
		}
		else
		{
			qp = bn_xmalloc(qlen);
		}
		
		// eger kalan verildiyse, uzunlugu ayarla
		// verilmediyse, gecici yer ac.
		if (r)
		{
			rp = BN_GROW(r, dlen);
		}
		else
		{
			rp = bn_xmalloc(dlen);
		}

		// bn_div_n icin, bolen en az 2 haneli olmali
		// degilse, bn_div_n1'i kullanmak zorundayız.
		if (dlen == 1)
			*rp = bn_div_n1(qp, n->digits, nlen, d->digits[0]);
		else
			bn_div_n(qp, rp, n->digits, nlen, d->digits, dlen);
		
		
		// kalanin uzunlugunu hesapla
		bn_size_t rlen = bn_trim(rp, dlen);
		if (r)
		{
			r->length = nsign ? -rlen : rlen;
		}
		else
		{
			// eger kalan istenmediyse,
			// gecici hafizayi birakabiliriz.
			free(rp);
		}

		// bolum icin uzunluk ayarla
		qlen = bn_trim(qp, qlen);
		if (q)
		{
			q->length = qsign < 0? -qlen : qlen;
		}
		else
		{
			// eger bolum istenmediyse
			// gecici alani birakabiliriz.
			free(qp);
		}
		
		return rlen != 0;
	}
	
Yukarıdaki fonksiyon uzun gorunse de, karmasik birşey yok. Açıklayıcı notları
satır aralarında bulabilirsiniz.

Bu yazı ile, kütüphanenin temel kısımlarını bitirmiş olduk. Bir sonraki yazıda,
tam sayılardaki dört işlem fonksiyonları için test yazacağız.
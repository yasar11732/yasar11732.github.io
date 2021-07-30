<!--
.. title: Büyük Sayı Algoritmaları - Metin Dönüşümleri
.. slug: buyuk-sayi-islemleri-metin
.. date: 2020-03-12 18:25
.. tags: 
.. has_math: yes
-->

Büyük sayı algoritmaları yazı dizisine, sayıdan metne,
metinden sayıya dönüşüm fonksiyonları ile devam ediyoruz.
Bu yazıda, onluk tabandaki metinler üzerinde işlem yapacağız.
Bu fonksiyonlardan yola çıkarak, diğer sayı tabanlarında
dönüşüm yapan fonksiyonlar da yazabilirsiniz.

<!-- TEASER_END -->

Projenin bu yazıya kadar olan kısmını [Github üzerinden indirebilirsiniz](https://github.com/yasar11732/LibBigNumber/archive/buyuk-sayi-islemleri-tamsayilar.zip)

Öncelikle, onluk tabandaki metni, `bnz_t`'ye çeviren
fonksiyonla başlayalım.

	:::C
	int bnz_set_ds(bnz_ptr bnz, const char *str)
	{
		int sign = 0;
		if (*str == '-')
		{
			str++;
			sign = 1;
		}

		while (*str == '0')
		{
			str++;
		}

		if (!*str)
		{
			bnz->length = 0;
			return 0;
		}

		bn_size_t length = 0;

		const char *tmp = str;

		while (*tmp++)
			length++;

		bn_digit_t *mem = BN_GROW(bnz, (bn_size_t)(length * 4 / BN_DIGIT_BITS + 1));

		length = 1;
		mem[0] = 0;
		char c;

		while (c = *str++)
		{
			if (c >= '0' && c <= '9') {
				bn_digit_t carry = bn_mul_n1(mem, mem, 10, length);
				carry += bn_add_n1(mem, mem, c - '0', length);
				if (carry)
					mem[length++] = carry;
			}
			else {
				return -1;
			}
		}

		if (sign)
		{
			bnz->length = -length;
		}
		else
		{
			bnz->length = length;
		}

		return 0;
	}
	
Fonksiyon biraz uzun görünüyor, o yüzden parça parça inceleyelim.

	:::C
	int sign = 0;
	if (*str == '-')
	{
		str++;
		sign = 1;
	}
	
Eğer metin eksi işareti ile başlıyorsa, sayının negatif olduğunu hatırlamamız gerek.
Eksi işaretini bulursak, bir adım ilerliyoruz.

	:::C
	while (*str == '0')
	{
		str++;
	}
	
Varsa, metnin başındaki sıfırları da atlayabiliriz.

	:::C
	if (!*str)
	{
		bnz->length = 0;
		return 0;
	}
	
Eğer metin boş ise, sıfır döndüreceğiz.

	:::C
	bn_size_t length = 0;

	const char *tmp = str;

	while (*tmp++)
		length++;
		
Bu kısımda metinde kaç karakter olduğunu sayıyoruz. Bunun için `strlen`
de kullanabiliriz. Ayrı bir fonksiyon çağrısı kullanmamak için, basit bir
döngü ile uzunluğu hesapladım.

	:::C
	bn_digit_t *mem = BN_GROW(bnz, (bn_size_t)(length * 4 / BN_DIGIT_BITS + 1));

Onluk tabanda `n` haneli bir sayı, ikili tabanda [yaklaşık 3.32n](https://www.wolframalpha.com/input/?i=log%2810%29%2Flog%282%29)
haneli bir sayıya karşılık gelir. Metin içindeki karakter sayısını 4 ile
çarparak, ihtiyacımız olan bit sayısının biraz fazlasını elde edebiliriz. Elde
ettiğimiz sayıyı, `bn_digit_t`'nin bit sayısına böldüğümüzde, hafızada
kaç hanelik yer açmamız gerektiğini tespit etmiş oluyoruz. C'de bölme
işleminin sıfıra doğru yuvarlamasından dolayı, `+1` ekliyoruz. Böylece
işlemin sonucunun sıfır olması ihtimalini ortadan kaldırıyoruz. 

	:::C
	length = 1;
	mem[0] = 0;
	char c;

	while (c = *str++)
	{
		if (c >= '0' && c <= '9') {
			bn_digit_t carry = bn_mul_n1(mem, mem, 10, length);
			carry += bn_add_n1(mem, mem, c - '0', length);
			if (carry)
				mem[length++] = carry;
		}
		else {
			return -1;
		}
	}
	
Burası fonksiyonun kalbi. Metni soldan sağa doğru tarayıp,
her bir karakter için, elimizdeki sayıyı 10 ile çarpıp, o karakterin
değerini sayıya ekliyoruz. Aynı zamanda, `bn_mul_n1` ve `bn_add_n1`
fonksiyonlarının `carry` döndürüp döndürmediğine dikkat etmemiz gerekiyor.
Bu fonksiyonlardan `carry` dönmesi halinde, dönen değeri bir üst haneye
taşımamız gerekiyor. Bu sayede, elde ettiğimiz sayının kaç haneli
olduğunu da takip etmiş oluyoruz.

	:::C
	if (sign)
	{
		bnz->length = -length;
	}
	else
	{
		bnz->length = length;
	}
	
`bnz`'nin hane sayısını ayarlarken, pozitif veya negatif olmasına dikkat ediyoruz.
Böylece, `char* -> bnz_t` dönüşümünü tamamlamış olduk.

`bnz_t -> char*` dönüşümüne
geçmeden önce [bölme yazısında](buyuk-sayi-islemleri-bolme.html) atladığım, tek
haneli sayı ile bölme fonksiyonuna ihtiyacımız olacak.

	:::C
	bn_digit_t bn_div_n1(bn_digit_t *q, bn_digit_t *op1, bn_size_t len, bn_digit_t op2)
	{
		bn_digit_t carry = 0;
		bn_size_t i;

		for (i = len - 1; i >= 0; i--)
		{
			bn_long_digit_t u = ((bn_long_digit_t)carry << BN_DIGIT_BITS) + (op1[i]);
			q[i] = (bn_digit_t)(u / op2);
			carry = u % op2;
		}

		return carry;
	}
	
Bu fonksiyon standart bölme fonksiyonuna göre oldukça sade, çünkü, bölen tek
haneli olduğunda, önceki gibi bölümün tahmini değerini bulup düzeltmek yerine,
doğrudan bölümü hesaplayabiliyoruz.

Büyük sayıyı, metne çevirmek için, aşağıdaki fonksiyonu kullanacağız.

	:::C
	char *bnz_tods(bn_constptr bnz)
	{
		char *ds;
		bn_size_t length = BN_ABS(bnz->length);

		if (!length)
		{
			ds = malloc(2);
			ds[0] = '0';
			ds[1] = '\0';
			return ds;
		}

		ds = malloc(length * BN_DIGIT_BITS / 3 + 1);

		bn_digit_t *tmp = alloca(length * sizeof(bn_digit_t));

		bn_size_t i;

		for (i = 0; i < length; i++)
		{
			tmp[i] = bnz->digits[i];
		}

		char *tds = ds;

		while (length)
		{
			*tds++ = '0' + bn_div_n1(tmp, tmp, length, 10);
			length = bn_trim(tmp, length);
		}

		if (bnz->length < 0)
			*tds++ = '-';

		*tds-- = 0;

		char *tds2 = ds;
		while (tds2 < tds)
		{
			char c = *tds2;
			*tds2++ = *tds;
			*tds-- = c;
		}

		return ds;
	}

Bu fonksiyonu da, küçük parçalar halinde inceleyelim.

	:::C
	char *ds;
	bn_size_t length = BN_ABS(bnz->length);

	if (!length)
	{
		ds = malloc(2);
		ds[0] = '0';
		ds[1] = '\0';
		return ds;
	}

	ds = malloc(length * BN_DIGIT_BITS / 3 + 1);
	
Burada, metnin kaç karakterden oluşacağını hesaplıyoruz. Eğer,
`bnz`'nin uzunluğu sıfır ise, fonksiyondan erken çıkma şansımız var. Aksi takdirde,
sayının toplam bit sayısını üçe bölerek, metnin karakter sayısını tahmini
olarak tespit edebiliriz.

	:::C
	bn_digit_t *tmp = alloca(length * sizeof(bn_digit_t));

	bn_size_t i;

	for (i = 0; i < length; i++)
	{
		tmp[i] = bnz->digits[i];
	}

Fonksiyon orjinal sayı üzerinde herhangi bir değişiklik yapmayacağı için,
sayıyı geçici bir alana kopyalamamız gerekiyor.

	:::C
	char *tds = ds;
	while (length)
	{
		*tds++ = '0' + bn_div_n1(tmp, tmp, length, 10);
		length = bn_trim(tmp, length);
	}

Döngünün her adımında sayıyı 10'a bölüp, kalanı metne ekliyoruz.
Her bölme işleminden sonra, `tmp` içinde kaç karakter kaldığını kontrol
ediyoruz. Böylece, döngüden çıkmamız mümkün olacak.

	:::C
	if (bnz->length < 0)
		*tds++ = '-';

Eğer sayı negatif ise, sayının sonuna eksi işareti atıyoruz. Eksi
işaretini daha sonra doğru yerine alacağız.

	:::C
	*tds-- = 0;
	
Metnin sonuna `null` atıp, işaretçiyi bir adım geri alıyoruz. `tds` bu adımda,
metnin `null` değerinden önceki karakterine işaret ediyor.

	:::C
	char *tds2 = ds;
	while (tds2 < tds)
	{
		char c = *tds2;
		*tds2++ = *tds;
		*tds-- = c;
	}

Metni oluştururken, küçük hanesinden büyük hanesine doğru oluşturduğumuz için,
metni tersine çevirmemiz gerekiyor. Buradaki döngü ile bunu gerçekleştiriyoruz.

Aşağıdaki gibi bir fonksiyonla, yukarıdaki dönüşümleri test edebiliriz.

	:::C
	void multiplication_test()
	{
		const char *str1 = "171428254796861184094610329674505562801";
		const char *str2 = "298502530806920071071164312285418709253";
		const char *str3;

		bnz_t bn1, bn2, bn3;
		bnz_init(&bn1);
		bnz_init(&bn2);
		bnz_init(&bn3);

		bnz_set_ds(&bn1, str1);
		bnz_set_ds(&bn2, str2);

		bn_digit_t *mem = BN_GROW(&bn3, bn1.length + bn2.length);

		bn_mul_n(mem, bn1.digits, bn1.length, bn2.digits, bn2.length);
		bn3.length = bn_trim(mem, bn1.length + bn2.length);

		str3 = bnz_tods(&bn3);
		printf("%s * %s = %s", str1, str2, str3);
	}
	
Eğer herşey yolunda giderse, bu fonksiyonun çıktısı aşağıdaki gibi olacak;

<pre>
171428254796861184094610329674505562801 x 298502530806920071071164312285418709253 =
 51171767908676599055325833877649182072670634054758144917604139267629751297653
</pre>

Performans Üzerine Düşünceler
------------------------------

Bu başlık altında, yukarıdaki iki fonksiyon için yapılabilecek bazı
optimizasyonlardan bahsedeceğim. İsterseniz bu kısmı atlayabilirsiniz,
ancak, çok fazla okuma/yazma yapacaksanız,
optimizasyonun ölçülebilir faydaları olduğunu göreceksiniz.

Yapabileceğimiz ilk optimizasyon aşağıdaki döngü ile ilgili;

	:::C
	while (c = *str++)
	{
		if (c >= '0' && c <= '9') {
			bn_digit_t carry = bn_mul_n1(mem, mem, 10, length);
			carry += bn_add_n1(mem, mem, c - '0', length);
			if (carry)
				mem[length++] = carry;
		} else {
			return -1;
		}			
	}
	
Bu döngüde, metindeki her bir karakter için `bn_mul_n1` ve `bn_add_n1`fonksiyonları
çalıştırılıyor. `bn_mul_n1` içinde, `length` adet çarpma işlemi yapılıyor. Benzer şekilde, `bn_add_n1`
içinde ise, `length` adet toplama işlemi yapılıyor. İşlediğimiz sayı
büyüdükçe, bu iki fonksiyonun ağırlığını hissetmeye başlarız. Bu iki fonksiyonu
her karakterden sonra çağırmak yerine, metni küçük gruplar
halinde işleyip, bu iki fonksiyonu her gruptan sonra birer kez çağırmak yeterli olacaktır.
 `bn_digit_t` 32 bit iken, 9 haneli gruplar halinde çalışabiliriz.
Bu optimizasyon ile birlikte, yukarıdaki fonksiyonun ilgili kısmı
aşağıdaki hali alacaktır.

	:::C
	bn_digit_t *mem = BN_GROW(bnz, (bn_size_t)(length * 4 / BN_DIGIT_BITS + 1));
	
	// oncelikle metinde kalan karakter
	// sayısı 9'un katı olacak şekilde,
	// "length % 9" karakter
	// işlememiz gerekiyor
	bn_size_t rdigits = length % 9;
	bn_digit_t tmp_val;
	bn_size_t k;

	tmp_val = 0;
	for (k = 0; k < rdigits; k++)
	{
		tmp_val = tmp_val * 10 + (*str++ - '0');
	}

	// işlediğimiz haneleri sayıya ekle
	mem[0] = tmp_val;
	
	// sayının şu anki uzunluğu
	length = 1;
	
	while (*str)
	{
		// 9 karakter işle
		tmp_val = *str++ - '0';
		for (k = 1; k < 9; k++)
		{
			tmp_val = tmp_val * 10 + (*str++ - '0');
		}
		
		// işlenilen 9 karakteri, asıl sonuca ekle
		// Eski halinde 1 hane işlediğimiz için, mem = mem * 10^1 idi.
		// Şimdi 9 hane işlediğimiz için, mem = mem * 10^9
		bn_digit_t carry = bn_mul_n1(mem, mem, 1000000000, length);
		
		// Eskiden burada tek bir hanenin değerini ekliyorduk.
		// Şimdi 9 hanenin toplam değerini ekliyoruz.
		carry += bn_add_n1(mem, mem, tmp_val, length);
		if (carry)
			mem[length++] = carry;
	}
	

Yapılabilecek bir diğer optimizasyon da, `bnz_tods` içindeki, aşağıdaki
döngü ile ilgili.

	:::C
	char *tds2 = ds;
	while (tds2 < tds)
	{
		char c = *tds2;
		*tds2++ = *tds;
		*tds-- = c;
	}
	
Eğer onluk hane sayısı en baştan düzgün hesaplansaydı,
fonksiyon sonunda metni ters çevirmek yerine, metni sağdan
sola doğru oluşturabilirdik. Malesef, sadece sayının
bit sayısına bakarak, onluk hane sayısını tespit
etmek mümkün değil. Aşağıdaki tabloyu inceleyelim; 

<pre>
+------------+-----------+-----------+-----------+
| İkili H.S. | Min. Onlu | Max. Onlu | Onlu H.S. |
+------------+-----------+-----------+-----------+
| 1          | 1         | 1         | 1         |
+------------+-----------+-----------+-----------+
| 2          | 2         | 3         | 1         |
+------------+-----------+-----------+-----------+
| 3          | 4         | 7         | 1         |
+------------+-----------+-----------+-----------+
| 4          | 8         | 15        | 1-2 (%80) |
+------------+-----------+-----------+-----------+
| 5          | 16        | 31        | 2         |
+------------+-----------+-----------+-----------+
| 6          | 32        | 63        | 2         |
+------------+-----------+-----------+-----------+
| 7          | 64        | 127       | 2-3 (%44) |
+------------+-----------+-----------+-----------+
| 8          | 128       | 255       | 3         |
+------------+-----------+-----------+-----------+
| 9          | 256       | 511       | 3         |
+------------+-----------+-----------+-----------+
| 10         | 512       | 1023      | 3-4 (%4)  |
+------------+-----------+-----------+-----------+
| 11         | 1024      | 2047      | 4         |
+------------+-----------+-----------+-----------+
| 12         | 2048      | 4095      | 4         |
+------------+-----------+-----------+-----------+
| 13         | 4096      | 8191      | 4         |
+------------+-----------+-----------+-----------+
| 14         | 8192      | 16383     | 4-5 (%77) |
+------------+-----------+-----------+-----------+
| 15         | 16384     | 32767     | 5         |
+------------+-----------+-----------+-----------+
| 16         | 32768     | 65535     | 5         |
+------------+-----------+-----------+-----------+
</pre>

Yukarıdaki tabloya göre, ikili hane sayısını
bildiğimiz bir sayının, onluk hane sayısını
yaklaşık %70 ihtimalle kesin olarak tespit edebiliriz.
Kesin olarak tespit edemediğimiz durumlarda ise, iki
ihtimalden birini seçmek zorundayız. Yukarıdaki tabloda,
büyük sayının seçilmesi halinde, doğru tahminde bulunma
oranını parantez içinde belirttim. Parantez içindeki
değerleri incelediğimizde, ne küçük seçenek, ne de büyük
seçenek diğerinden daha avantajlı görünüyor. Her zaman
büyük seçeneği tercih ederek, %50 ihtimalle doğru tahminde
bulunduğumuzu varsayarsak, toplamda `%70 + %30 * %50 = %85`
ihtimalle, ikili hane sayısına bakarak, onluk hane sayısını tespit
edebileceğimiz yönünde bir tahminde bulunabiliriz.

C ile yukarıdaki tablonun son sütununu tespit etmek için, ikili
hane sayısını \\(\frac{ln 10}{ln 2} \approx 3.3219 \\) sayısına
bölmemiz gerekiyor. `float` sayılara ve bölme işlemine başvurmadan
işlemin sonucunu aşağıdaki gibi bulabiliriz.

	:::C
	(((bn_long_digit_t)nbits * 1292913986) >> 32) + 1
	
Devam etmeden önce, `1292913986` sayısını nasıl elde ettiğimize
de değinelim. Bu sayı aslında `1 / 3.3219... * 2^32` sayısının aşağıya
yuvarlanmış hali. İşlemi bu şekilde yapmak, genellikle `float` sayılar
üzerinde bölme işlemi yapmaktan daha hızlı olacaktır.

Yukarıdaki hesabın doğru sonuç vermesi için, bit sayısını da doğru
hesaplamalıyız. Bunun için, daha önce tanımladığımız `nlz` fonksiyonunu
kullanacağız.

	:::C
	bn_size_t nbits = length * BN_DIGIT_BITS - nlz(bnz->digits[length - 1]);
	bn_size_t ndecimals = ((bn_long_digit_t)nbits * 1292913986 >> 32) + 1;
	if(bnz->length < 0)
		ndecimals++; 
	
Eğer sayı negatif ise, eksi işareti için de bir yer ayırdık.
Fonksiyonun ilk halinde, metni soldan sağa oluşturuyorduk, artık sağdan sola
oluşturabiliriz.

	:::C
	ds = malloc(ndecimals + 1);
	char *tds = ds + ndecimals;
	*tds-- = 0;

	while (length)
	{
		*tds-- = '0' + bn_div_n1(tmp, tmp, length, 10);
		length = bn_trim(tmp, length);
	}
	
	if(bnz->length < 0)
		*tds-- = '-';
	
Bu aşamada, yaklaşık %15 ihtimalle, metnin ilk karakterinde anlamsız bir
değer olacaktır. Bunu düzeltmek için, hafızayı 1 karakter sola kaydırmamız gerek.

	:::C
	if (tds == ds)
	{
		memmove(ds, ++tds, ndecimals);
	}
	
Böylece, bu optimizasyonu da uygulamaya geçirmiş olduk.

Bir sonraki yazıda, doğal sayılar üzerinde yaptığımız dört işlemi
kullanarak, tam sayılar üzerinde dört işlem yapan fonksiyonlarla devam
edeceğiz.
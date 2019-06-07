<!--
.. date: 2019-06-07 19:51
.. slug: utf8-kodlama
.. title: UTF-8 Kodlama Algoritması
-->

[RFC2231 Kodlaması](https://ysar.net/yazilim-dunyasi/rfc2231.html) başlıklı yazıda, `wchar_t` türündeki
bir string'i utf8 olarak kodlamak için işletim sisteminin sağladığı fonksiyonları kullanmıştım. Ancak,
daha sonra, kodlama egzersizi olarak `wchar_t` türündeki bir string'i utf8 olarak kodlayan fonksiyonu kendim
yazmak istedim. Referans olarak, [RFC 3629](https://tools.ietf.org/html/rfc3629)'daki tanımlamaları kullandım.
Bu yazıda, geniş karakter (`wchar_t`) türündeki veriyi, nasıl utf8 olarak kodlayabileceğimizden bahsedeceğim.

Bahsettiğim RFC'nin 3. başlığı altında, UTF-8'in tanımı yapılmış. Buna göre, `0x0` ile `0x10FFFF` arasındaki
unicode karakterler, 1-4 byte dizilimle kodlanıyor. Kodlamada kullanılan her bir byte'a octet (eng. sekizli)
deniyor. Tek bir octet'den oluşan dizilimde üst bit (MSB) 0 olmak zorunda, kalan 7 bit ile karakterimizi
kodluyoruz. Dolayısıyla, karakter kodu 127 ve altı için, UTF8 kodlama ile us-ascii kodlama eşdeğer oluyor.
`n` octetli'li (`n > 1`) dizilimlerde iste, ilk octet'in üst `n` biti 1 olarak, bunları takip eden ilk bit
ise 0 olarak ayarlanıp, kalan bitler kodlama amaçlı kullanılıyor. Devamında gelen octetlerin ise, hepsinin
en üst biti 1, onu takip eden bit ise 0 olarak ayarlanıp, kalan bitler kodlama amaçlı kullanılıyor.
RFC'deki örnek tabloyu buraya kopyalıyorum.

	   Karakter Kodu Aralığı  |        UTF-8 octet dizilimi
		     (hexadecimal)    |              (binary)
	      --------------------+---------------------------------------------
	      0000 0000-0000 007F | 0xxxxxxx
	      0000 0080-0000 07FF | 110xxxxx 10xxxxxx
	      0000 0800-0000 FFFF | 1110xxxx 10xxxxxx 10xxxxxx
	      0001 0000-0010 FFFF | 11110xxx 10xxxxxx 10xxxxxx 10xxxxxx

Şimdi adım adım, UTF8 kodlama algoritmasının aşamalarına geçeceğiz. Aşamalara geçmeden
önce, işimizi daha anlaşılır yapabilmek için, tanımlamalarımızı yapalım.

	:::c
	#define UTF8_OCTET1_MAX 0x7F
	#define UTF8_OCTET2_MAX 0x7FF
	#define UTF8_OCTET3_MAX 0xFFFF
	#define UTF8_OCTET4_MAX 0x10FFFF

	#define UTF8_SEQUENCE1_START 0x00
	#define UTF8_SEQUENCE2_START 0xC0
	#define UTF8_SEQUENCE3_START 0xE0
	#define UTF8_SEQUENCE4_START 0xF0

	#define UTF8_CONTINUATION_BYTE 0x80
	#define UTF8_CONTINUATION_BYTE_MASK 0x3F
	
İlk 4 tanım, sırasıyla 1 octet, 2 octet, 3 octet ve 4 octet ile kodlanabilecek karakter
kodlarının üst sınırını belirtiyor. Bu sayılarını doğrudan örnek tablodan kopyaladım.
Daha sonra gelen 4 tanım ise, yine sırasıyla 1 octet, 2 octet, 3 octet ve 4 octet dizilimlerinde
ilk octet'in üst bitlerinde olması gereken değeri belirtiyor. Bu sayıları
elde etmek için, örnek tabloda binary olarak gösterilen birinci octet'leri (`b00000000`,`b11000000`,`b11100000`,`b11110000`), hex gösterimine
çevirdim. `UTF8_CONTINUATION_BYTE` tanımı, çoklu octet dizilimlerinde, her bir octet'in
üst bitlerinin alması gerektiği değeri gösteriyor. Bunu da aynı şekilde
örnek tablodan hex'e çevirdim. Son olarak, `UTF8_CONTINUATION_BYTE_MASK` ile
tanımlanan değeri, bir sayının en alttaki 6 bitini maskelemek için kullanacağım.

Şimdi adım adım, algoritmayı inceleyelim. Birinci adım olarak, karakterin kaç octet
ile kodlanacağını hesaplayacağız. Bunun için mümkün olan en düşük octet sayının
kullanacağız.  
	
	:::c
    // 1. Gerekli Octet Sayısını Hesapla
    size_t cbOctet = 1  
                   + (c > UTF8_OCTET1_MAX)
                   + (c > UTF8_OCTET2_MAX)
                   + (c > UTF8_OCTET3_MAX)
                   + (c > UTF8_OCTET4_MAX);
			
Yukarıdaki örnekte, eğer `UTF8_OCTET4_MAX`'dan büyük bir karakter kodu
ile karşılaşırsak, `cbOctet` 5 olacak. En fazla 4 octet kullanabileceğimiz
için, bu durumu hata durumu olarak değerlendireceğiz. İkinci adımda ise,
kullanılacak octet'lerin, üst bitleri tabloda gösterildiği şekilde ayarlayacağız.

	:::c
    // 2a. Başlangıç octet'inin üst bitlerini ayala
    switch (cbOctet)
    {
        case 1:
            result[0] = UTF8_SEQUENCE1_START;
            break;
        case 2:
            result[0] = UTF8_SEQUENCE2_START;
            break;
        case 3:
            result[0] = UTF8_SEQUENCE3_START;
            break;
        case 4:
            result[0] = UTF8_SEQUENCE4_START;
            break;
        default: // utf8 ile kodlanamayacak bir karakter varsa, 0 döndür
            return 0;
    }

    // 2b. devam octetlerinin üst bitlerini ayarla
    size_t i;
    for(i = 1; i < cbOctet; i++)
    {
        result[i] = UTF8_CONTINUATION_BYTE;
    }

İkinci adımda çok ilginç birşey yok. Her bir octet'in üst bitlerini
olması gerektiği gibi ayarlayıp, kalan bitlerini sıfırladık. Üçüncü
adımda, karakter kodundaki bitleri, octet'lerdeki kullanılabilir bitlere
kopyalacağız. Bunun için, karakter kodunun en alttaki bitlerini
en sondaki octet'e kopyalarak, yukarı doğru devam edeceğiz. Bunu
yapmak için, en baştaki octet dışında, `UTF8_CONTINUATION_BYTE_MASK` maskesi
ile alttaki 6 biti seçip, karakter kodunu 6 bit sağa kaydıracağız.
En baştaki octet'e gelindiğinde, sadece ihtiyacımız olan bitler
kaldığı için, herhangi bir maskeleme yapmamıza gerek yok.

	:::c
    // 3. Son octetten başa doğru, bitleri
    // doldur. Her devam octet'inde 6'şar
    // bit kullanacağız. Geriye kalan bitler
    // teknik olarak başlangıç octet'ine
    // sığmak zorunda
    for(i = cbOctet; i > 1; i--)
    {
        result[i-1] |= c & UTF8_CONTINUATION_BYTE_MASK;
        c = c >> 6;
    }
    
    result[0] |= c;
	
Böylece, tek bir unicode karakteri, utf8 olarak kodlamış olduk. Bu işlemi
bir string üzerinde gerçekleştirmek için, sırayla tüm karakleri yukarıdaki
şekilde kodlamak yeterli. Örnek programın son hali aşağıdaki gibi olacak.

	:::c

	#include <stdlib.h> // malloc
	#include <string.h> // memcpy
	#include <stdio.h>  // fopen, fwrite, fclose
	#include <wchar.h>  // wchar_t

	#define UTF8_OCTET1_MAX 0x7F
	#define UTF8_OCTET2_MAX 0x7FF
	#define UTF8_OCTET3_MAX 0xFFFF
	#define UTF8_OCTET4_MAX 0x10FFFF

	#define UTF8_SEQUENCE1_START 0x00
	#define UTF8_SEQUENCE2_START 0xC0
	#define UTF8_SEQUENCE3_START 0xE0
	#define UTF8_SEQUENCE4_START 0xF0

	#define UTF8_CONTINUATION_BYTE 0x80
	#define UTF8_CONTINUATION_BYTE_MASK 0x3F

	size_t utf8_encode_char(wchar_t c, unsigned char result[4])
	{
		// 1. Gerekli Octet Sayısını Hesapla
		size_t cbOctet = 1  
					   + (c > UTF8_OCTET1_MAX)
					   + (c > UTF8_OCTET2_MAX)
					   + (c > UTF8_OCTET3_MAX)
					   + (c > UTF8_OCTET4_MAX);

		
		// 2a. Başlangıç octet'inin üst bitlerini ayala
		switch (cbOctet)
		{
			case 1:
				result[0] = UTF8_SEQUENCE1_START;
				break;
			case 2:
				result[0] = UTF8_SEQUENCE2_START;
				break;
			case 3:
				result[0] = UTF8_SEQUENCE3_START;
				break;
			case 4:
				result[0] = UTF8_SEQUENCE4_START;
				break;
			default: // utf8 ile kodlanamayacak bir karakter varsa, 0 döndür
				return 0;
		}

		// 2b. devam octetlerinin üst bitlerini ayarla
		size_t i;
		for(i = 1; i < cbOctet; i++)
		{
			result[i] = UTF8_CONTINUATION_BYTE;
		}
		
		// 3. Son octetten başa doğru, bitleri
		// doldur. Her devam octet'inde 6'şar
		// bit kullanacağız. Geriye kalan bitler
		// teknik olarak başlangıç octet'ine
		// sığmak zorunda
		for(i = cbOctet; i > 1; i--)
		{
			result[i-1] |= c & UTF8_CONTINUATION_BYTE_MASK;
			c = c >> 6;
		}
		
		result[0] |= c;

		return cbOctet;
	}

	/*
		IN: wchar_t *pwszWide: NULL ile biten, wchar_t stringi
		OUT: size_t *cbEncoded : Kodlamış string'in boyutu
		
		RETURN: utf8 ile kodlanmış, NULL ile biten array
	*/
	char *utf8_encode(wchar_t *pwszWide, size_t *cbEncoded)
	{
		*cbEncoded = 0;
		size_t cbTemp;
		unsigned char encoded_char[4];
		wchar_t *pwcTemp;
		char    *pcTemp2;

		// realloc yapmak zorunda kalmamak için
		// pwszWide üzerinden 1 tur geçip, kodlanmış
		// veri için gerekli hafızayı hesaplayacağız.
		for(pwcTemp = pwszWide; *pwcTemp; pwcTemp++)
		{
			*cbEncoded += utf8_encode_char(*pwcTemp, encoded_char);
		}

		char *pszEncoded = malloc(*cbEncoded + 1); // +1 null
		
		for(pwcTemp = pwszWide, pcTemp2 = pszEncoded; *pwcTemp; pwcTemp++)
		{
			cbTemp = utf8_encode_char(*pwcTemp, encoded_char);
			memcpy(pcTemp2, encoded_char, cbTemp);
			pcTemp2 += cbTemp;
		}

		*pcTemp2 = 0; // NULL terminator

		return pszEncoded;
	}

	int main(void)
	{

		wchar_t example1[] = L"İŞTE BUNLAR HEP TÜRKÇE KARAKTERLER: ÜĞİŞÇÖ";
		wchar_t example2[] = {0xD55C, 0xAD6D, 0xC5B4, 0x0}; // korece korece
		wchar_t example3[] = {0x65E5, 0x672C, 0x8A9E, 0x0}; // japonca japon
		wchar_t example4[] = {0x233B4, 0x0};                // çince bir karater

		FILE *f = fopen("examples.txt","wb");

		size_t cbEncoded;
		char *pszEncoded = utf8_encode(example1, &cbEncoded);
		fprintf(f, "%s\n", pszEncoded);
		free(pszEncoded);

		pszEncoded = utf8_encode(example2, &cbEncoded);
		fprintf(f, "%s\n", pszEncoded);
		free(pszEncoded);

		pszEncoded = utf8_encode(example3, &cbEncoded);
		fprintf(f, "%s\n", pszEncoded);
		free(pszEncoded);

		pszEncoded = utf8_encode(example4, &cbEncoded);
		fprintf(f, "%s\n", pszEncoded);
		free(pszEncoded);

		fclose(f);


	}
Öyle sanıyorum ki, yukarıdaki kodlarda optimize edilebilecek kısımlar vardır. Ancak,
kolayca anlaşılabilr olması açısından, yapılabilecek optimizasyonlara dikkat etmedim.
Faydalı bir yazı olmuştur diye ümit ediyorum.
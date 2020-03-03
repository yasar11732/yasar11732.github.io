<!--
.. date: 2020-03-04 01:28
.. description: 
.. slug: rastgele-sayi-uretici
.. title: Rastgele Sayı Üretici
.. tags: mathjax
-->

Merhabalar,

[Multi-precision](https://en.wikipedia.org/wiki/Arbitrary-precision_arithmetic) doğal sayılarda bölme yapan bir fonksiyonu test etmek için, C'deki `rand()`
fonksiyonu ile rastgele sayı oluştururken, oluşturduğum sayıların
yeterince rastgele olmadığına (artık o ne demekse) karar verdim. Fonksiyon içinde, çok
nadiren de olsa çalışması gereken bir `if` bloguna, milyarlarca sayı üretmeme rağmen girememiştim.
Hal böyle olunca, C'deki `rand()`
fonksiyonuna alternatif olarak, [RC4](https://en.wikipedia.org/wiki/RC4) tabanlı
bir rastgele sayı üretici oluşturdum.

Bu rastgele sayı üreticinin özelliği, küçük sayılara daha fazla ağırlık veriyor olması. Dolayısı ile,
uniform dağılımda sayılar üretmiyor. Kriptografi alanında kullanılmaması gerektiğini de özellikle
vurgulamak istiyorum. Kodlar aşağıdaki gibi;

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

	#include <stdint.h>

	typedef int32_t bn_size_t;
	typedef uint32_t bn_digit_t;

	struct rngstate
	{
		uint8_t i, j, s[256];
	};

	static struct rngstate RNGSTATE;

	void init_rng(char *key)
	{
		int keysize = strlen(key);
		RNGSTATE.i = 0;
		RNGSTATE.j = 0;

		int i;
		uint8_t j;
		for (i = 0; i < 256; i++)
		{
			RNGSTATE.s[i] = i;
		}

		j = 0;
		for (i = 0; i < 256; i++)
		{
			j += RNGSTATE.s[i] + key[i % keysize];
			int tmp = RNGSTATE.s[i];
			RNGSTATE.s[i] = RNGSTATE.s[j];
			RNGSTATE.s[j] = tmp;
		}
	}

	uint8_t myarc4()
	{
		RNGSTATE.i++;
		RNGSTATE.j += RNGSTATE.s[RNGSTATE.i];
		uint8_t temp = RNGSTATE.s[RNGSTATE.i];
		RNGSTATE.s[RNGSTATE.i] = RNGSTATE.s[RNGSTATE.j];
		RNGSTATE.s[RNGSTATE.j] = temp;
		return RNGSTATE.s[(uint8_t)(RNGSTATE.i + RNGSTATE.j)];
	}

	void fill_random(bn_digit_t *arr, bn_size_t len)
	{
		do {
			bn_digit_t num = 0;
			bn_digit_t k = myarc4() % 33;
			bn_digit_t _nlz = 32;

			while (_nlz > (32 - k))
			{
				int shift = (_nlz + k) - 32;
				if (shift > 8)
					shift = 8;

				int mask = (1 << shift) - 1;
				num = (num << shift) | (myarc4() & mask);
				_nlz = nlz(num);
			}
			
			arr[--len] = num;

		} while (len);
	}

Burada kullanmak isteyebileceğiniz iki fonksiyon var; `fill_random` ve `myarc4`. `myarc4` fonksiyonu
RC4 şifrelemeden esinlenerek(!) yazdım. Her çağrıldığında, rastgele 8 bit bir değer döndürüyor. Ancak,
fonksiyonu kullanmadan önce, program başlangıcında bir kez `init_rng` fonksiyonunu çağırmanız gerekiyor.
Argüman olarak statik bir string verirseniz, her seferinde aynı sayıları üretir. Eğer istediğiniz bu değilse,
`key` olarak kullanılacak string'i `/dev/urandom`'u okuyarak veya [CryptGenRandom](https://docs.microsoft.com/en-us/windows/win32/api/wincrypt/nf-wincrypt-cryptgenrandom)
 fonksiyonunu kullanarak oluşturup, bununla birlikte `init_rng`
fonksiyonunu çağırabilirsiniz.

Herhangi uzunluktaki 32bit integer array'ini rastgele sayılarla doldurmak için, `fill_random` fonksiyonu
kullanabilirsiniz. İlk argüman olarak array'i, ikinci argüman olarak da array uzunluğunu göndermeniz gerekiyor.
Yukarıda da bahsettiğim gibi, burada oluşacak sayılar, sıfıra doğru meyilli. Yaklaşık olarak 1/32 ihtimalle 0,
1/32 ihtimalle 1, 1/64 ihtimalle 2 ve 3 döndürmesini bekleyebilirsiniz. 

Standart kütüphanedeki `rand()` fonksiyonuna nazaran oldukça yavaş kalabilir, ama, farklı bir dağılıma
sahip rastgele sayılar üretmek isterseniz işinize yarayabileceğini düşünüyorum.

Kriptografi için kullanılmaması gerektiğini tekrar hatırlatayım.
<!--
.. date: 2019-06-18 09:53
.. slug: setjmp-h
.. title: <setjmp.h> Ne İşe Yarar
-->

Son bir hafta, veya biraz daha uzun bir süre boyunca, akademik bir merak neticesinde deflate formatında sıkıştırma/açma
yapan bir programın nasıl yazılabileceğini araştıyordum. Zlib kütüphanesinin içinde, deflate formatını açmaya yarayan
referans niteliğinde yazılmış, [puff.c](https://github.com/madler/zlib/blob/master/contrib/puff/puff.c) adında bir C
programı var. Bu programı incelerken, içinde `setjmp()` ve `longjmp()` fonksiyonlarını gördüm. Kodlarda, bu fonksiyonların
tanımının `setjmp.h` içerisinde yapıldığı yazıyordu. Zlib kaynak kodları içerisinde bu header dosyasını bir süre aradıktan
sonra, `setjmp.h`'nin C standardı içinde olduğunu öğrendim. Şimdiye kadar C dilini iyi kullandığını
vehmetmiş biri olarak, hiç duymadığım bir header dosyasıyla karşılaşmak beni heyecanlandırdı. Hemen internetten araştırmaya
koyuldum.

`setjmp.h` header dosyası, 3 şey tanımlıyor; `setjmp()`, `longjmp()` ve `jmp_buf`. Bu üçü sayesinde, normal fonksiyon çağırma
ve fonksiyondan değer döndürme mekanizmasının dışına çıkıp, programın başka bir yerine zıplayabiliyoruz. Bunu fonksiyon sınırlarını
aşan `goto` gibi düşünebiliriz. Okuduğum kaynaklarda 2 çeşit kullanımı var. Birincisi, daha üst seviye dillerde bulunan özel durum (exception)
yönetimini gerçekleştirme, ikincisi de coroutine oluşturmak. Bu yazı özel durumlar üzerine kurulu olacak ama, C dilinde coroutine yazma
konusunda da çok heyecanlıyım, ilerleyen günlerde bu konuda da denemeler yapmak istiyorum.

Uygulamaya geçmeden önce, teorik bilgiyle başlamak istiyorum. `setjmp` makrosu, argüman olarak `jmp_buf` adında bir `struct`
alıyor. İleride `longjmp` tarafından kullanılmak üzere, geçerli yürütme bağlamını (execution context) `jmp_buf` tipindeki
değişkene kaydediyor. Geçerli yürütme bağlamından kasıt, `setjmp` makrosu çalıştırıldığı andaki genel amaçlı register'larla
birlikte, Instruction Pointer, Stack Pointer, EFLAGS gibi register'ların değerleri. Bunun detayları haliyle işlemci
mimarisine göre değişebilir. Bu makronun kullanıcısı olarak bizi ilgilendiren, bu makronun bir zıplama noktası kaydettiği.
Bu makronun dönüş değeri, yürütme bağlamını kaydettiği anda 0, `longjmp` ile dönüldüğü anda ise, `longjmp` tarafından ayarlanan
değere eşit oluyor. Bunu anlamak için, bir örneğe başvurmakta fayda var.

	:::c
	#include <setjmp.h>
	#include <string.h>
	#include <stdio.h>

	typedef struct{
		char *data;
		int size;
		jmp_buf env;
	} String;


	void smemset(String *s, int val, size_t size)
	{
		if (size > s->size)
			longjmp(s->env, 1);

		memset(s->data, val, size);
	}

	int main(void)
	{
		String s;
		s.data = malloc(5);
		s.size = 5;


		if (setjmp(s.env) == 1)
		{
			printf("String uzunlugu yeterli degil.");
			return 1;
		}

		int i = 0;
		while (++i)
		{
			printf("%d\n", i);
			smemset(&s, 0, i);
		}

		return 0;
	}
	
Yukarıdaki örneği incelerseniz, `setjmp` kullanımı daha anlaşılır olur diye düşünüyorum. Dikkat etmeniz gereken
en önemli kısım, `setjmp` makrosundan birden fazla kez dönüldüğü. İlk çağırıldığında, dönüş değeri 0 olacağı için,
`if` blogu içerisine girilmeyecek, ve program `while` döngüsüne girecek. `while` döngüsü sonsuz bir döngü gibi görünse
de, aslında öyle değil. `smemset` fonksiyonu, özel durumlarda (bunu exception gibi düşünebiliriz) `longjmp` fonksiyonunu
kullandığı için, sanki `setjmp` fonksiyonundan yeni dönülüyormuş gibi, `main` fonksiyonu içindeki `if` koşuluna zıplayacak.
Ancak bu sefer, `setjmp`'nin dönüş değeri `longjmp` tarafından 1 olarak ayarlandığı için, `if`in koşulu sağlanacak ve `main`
fonksiyonu hata mesajı yazdırıp dönecek. Gözünüzü kısıp, kafanızı biraz eğerek bakarsanız, tıpkı daha yüksek seviye dillerdeki
throw/catch veya raise/catch benzeri bir program davranışı ile karşı karşıyayız.

	1
	2
	3
	4
	5
	6
	String uzunlugu yeterli degil.
	

Yukarıdaki kadar küçük bir programda, `setjmp` ve `longjmp` kullanımını anlatmak mümkün olsa da, bu ikisinin
faydasını göstermek pek muhtemel görünmüyor. Ancak, fonksiyon çağrı hiyerarşisinin derinliklerinde oluşan özel
durumların, üst seviye bir fonksiyonda merkezi bir şekilde yönetilmesine imkan sağlaması açısından faydalı görünüyor.
Ayrıca, embedded programlama için de, thread benzeri bir program akışı sağlamanın tek yolu bu olabilir. Bu yazıda
söylemek istediklerim bu kadar, ama, `setjmp` ile coroutine oluşturma konusunda da ileride birşeyler yazmak istiyorum.



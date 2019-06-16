<!--
.. date: 2019-06-15 20:30
.. slug: canonical-huffman-kodlamasi
.. title: Canonical Huffman Kodlaması
-->

Deflate formatını anlama konusunda sonlara yaklaştığımı hissediyorum. [Huffman Kodlaması](huffman-kodlamasi.html)
ve [lz77](lz77.html) konusunu genel çerçevesiyle kavradım. Huffman kodlaması yapan ilk programı yazdığımda,
oluşan kodların dosyaya hangi biçimde yazılması gerektiği konusunda net bir fikrim yoktu. [RFC 1951](https://www.ietf.org/rfc/rfc1951.txt)
içindeki örnekleri takip ederek, yöntemi anlamaya çalışıyorum.

Deflate formatı içinde kullanılan Huffman Kodlamasına ait kodların aşağıdaki iki şartı taşıması gerekiyor.

 - Aynı bit genişliğine sahip tüm kodların, temsil ettiği karakterlerle aynı sırada ve
   ardışık kod değerlerine sahip olması.
 - Dar kodların, alfabetik sırada geniş kodlardan önce gelmesi.
 
Daha sonra harici kaynaklardan öğrendiğim kadarıyla, bu özellikleri taşıyan kodlamaya Canonical Huffman kodlaması
deniyor. Bu yöntem kodlama ağacını kompakt bir şekilde depolamaya yarıyor, çünkü, her karakterin kodunun kaç bit
genişliğinde olduğunu bildiğiniz zaman, kodları baştan oluşturabiliyorsunuz. Bu nedenle, sadece karakteri ve bit genişliğini
depoluyorsunuz.

RFC bu konuda biraz kriptik konuştuğu (ya da pek kafam çalışmadığı) için, işin aslını anlamak gayesiyle, farklı kaynaklardan
araştırma yaptım. Yapılan işlem sadece, tüm kodlara sırasıyla numara atamakmış. Bir önceki yazıdaki prefix kodlama örneğine
tekrar bakalım.



		   / \             d: 000 (3 bit)
		  0   1            b: 001 (3 bit)
		/   \   \          c: 01  (2 bit)
	   0     1   a         a: 1   (1 bit)
	  / \    /
	 0   1   c
	/    \
	d     b
	
Bunu canonical kodlamaya çevirmek için, önce bit genişliğine göre, bit genişliği aynı olanları da alfabetik sıraya göre
sıralıyoruz.

	a : 1
	c : 2
	b : 3
	d : 3

Daha sonra, ilk sıradaki koda, bit genişliği kadar 0 yazıyoruz. Onu takip eden
her bir kod için, bir önceki kodu 1 artırıp, eğer gerekiyorsa, bit genişliğini
ayarlamak için kod değerini 1 bit sola kaydırıyoruz.

	+----------+--------------+---------------------------------------+
	| Karakter | Huffman Kodu | Açıklama                              | 
	+----------+------------------------------------------------------+
	|   a      |        0     | İlk koda 1 bit genişliğinde 0 atadık. |
	+----------+--------------+---------------------------------------+
	|   c      |        10    | Kodu 1 artırıp, 1 kez sola kaydırdık. |
	+----------+--------------+---------------------------------------+
	|   b      |        110   | Kodu 1 artırıp, 1 kez sola kaydırdık. |
	+----------+--------------+---------------------------------------+
	|   d      |        111   | Kodu 1 artırdık, kaydırmaya gerek yok.|
	+----------+--------------+---------------------------------------+
	
Kağıt/Kalem ile canonical huffman kodlaması oluşturmak bu kadar basit. Ben tabii ki bunu bir programa
yaptırmayı tercih ederim. Neyse ki, RFC'de bunun yazılmışı var :)

Önce veri yapılarını konuşalım.
	
	:::c
	#include <stdint.h>

	/*
	* Deflate formatına uygun olması için,
	* bir kodun en fazla 15 bit olmasına izin vereceğiz.
	* Bu nedenle code için 16 bit veri yapısı yeterli.
	*/
	struct huffmancode {
		uint8_t len;
		uint16_t code;
	};

	// her bir code için uzunluk ve kod değerlerini
	// tuttuğumuz array
	struct huffmancode tree[0XFF];
	
	// her uzunlukta kaç adet kod
	// olduğunu saymak için
	uint8_t bl_count[0x10];
	
	// her uzunluktaki kodlama için
	// atanacak kodu tutar
	uint16_t next_code[0x10];

Veri yapıları bakımından, bu ikisi yeterli olacaktır. Tabii öncelikle `tree` array'ini,
her karakterin kaç bitle kodlanması gerektiği bilgisi ile doldurmak gerekiyor.
Bunun için, önce Huffman ağacını oluşturmamız gerekiyor. Gerçi [burada](huffman-kodlamasi.html)
oluşmuşu var.

Algoritmanın sonraki adımında, her bit genişliğine kaç kodlama düştüğünü saymamız gerekiyor.

	:::c
	for(i = 0; i < 0xFF; i++)
		bl_count[tree[i].len]++;
	
Her bit genişliğine kaç adet kodlama düştüğünü bilmek, her bit genişliğinin ilk kodlamasını
hesaplamamızı sağlayacak.

	:::c
	code = 0;
	bl_count[0] = 0;
	for(i = 1; i < 0x10; i++)
	{
		code = (code + bl_counts[i - 1]) << 1;
		next_code[i] = code;
	}

`code` değişkeni, döngünün girişinde, bir önceki bit genişliğindeki kodlamanın başlangıç değerine
eşit oluyor. Bu `code` değerine, önceki bit genişliğindeki kod sayısını ekleyip, 1 sola kaydırdığımızda,
o döngüde hesaplanan bit genişliğinin ilk kodu ortaya çıkıyor.

Son olarak, `tree` array'inin üzerinden bir tur daha geçerek, bir önceki adımda hesaplanan kod başlangıç
değerlerini birer artırarak, her karakterin kodunu oluşturuyoruz. Bu aşamada, `len` değeri 0 olan, yani
kodlanan metinde hiç geçmeyen karakterlere herhangi bir kod atamamamız gerekiyor.

	:::c
	for(i = 0; i < 0xFF; i++) {
		uint8_t len = tree[i].len;
		if(len)
		{
			tree[i].code = next_code[len];
			next_code[len]++;
		}
	}
	
Canonical kodlama ile ilgili anlatılması gereken herşey bu kadar. Deflate formatını tamamlamaya ramak kaldı.

Burayı kalabalık göstermemesi için, [kodların tamamını](https://gist.github.com/yasar11732/30d2fc9c1c404d776218424e5e3ca795) gist olarak yükledim:
<!--
.. date: 2019-06-26 10:25
.. description: Flex ve Bison kullanarak JSON işleyen Lexer/Parser tasarımı
.. slug: flex-bison
.. title: Flex ve Bison kullanarak JSON İşleme (1. Kısım)
-->

İki kısımdan oluşmasını planladığım bu yazı dizisinde, Flex ve Bison
kullanarak, JSON işleyen Lexer ve Parser tasarlayacağız. Bu kısımda,
Flex/Bison konusuna sıfırdan başlayacağım için, önceden bu programları
tanıyor olmanıza gerek yok. 

İhtiyaç Listesi
===============

 - Derleme ortamı olarak Linux/Unix veya Cygwin üzerinde `make`, `cc` vb. geliştirici programları
 - flex (ya da lex) ve bison (ya da yacc)
 - Başlangıç seviyesinde C Programlama Bilgisi
 - Orta Seviye Düzenli İfadeler (Regular Expressions, RegExp) Bilgisi
 
Flex ve Bison
=============

Her ne kadar Flex ve Bison iki ayrı program olsa da, neredeyse her zaman birlikte kullanılırlar. Bu programlar,
kendi dosya formatlarında yazılmış metinleri, lexer ve parser olarak ifade edilen C programlarına dönüştürürler.
Lexer'ın görevi, verilen metin dosyasını, token dediğimiz parçalara bölmektir. Token'in ne olduğu, işleyeceğimiz
metin formatına göre değişebilir. Şimdilik token'lerine ayırmayı, metni kelimelerine bölmek olarak düşünebiliriz.
Parser'ın görevi ise, tokenleri gramer kurallarına uygun olarak analiz etmektir. Eğer lexer'in görevini
metni kelimelerine ayırmak olarak düşünürsek, parser'ın görevini de kelimelerden cümleler, cümlelerden paragraflar,
paragraflardan da makaleler oluşturacak şekilde tokenleri gramer kurallarına uygun gruplara ayırmak olarak düşünebiliriz.

Flex Programının Anatomisi
==========================

Detaylara girmeden önce, yazılabilecek en küçük flex dosyalarından birini inceleyerek başlayalım.

	:::c
	%%
	username printf("%s", getlogin());

Yukarıdaki 2 satırı `example.l` adıyla kaydedin. Bu dosyadan Lexer oluşturmak için, aşağıdaki komutu kullanacağız.

	:::bash
	lex example.l
	
`lex` programının çıktı dosyasının adı `lex.yy.c`'dir. Bu `.c` dosyasını derleyip, flex kütüphanesiyle linklememiz gerekiyor.

	:::bash
	gcc lex.yy.c -lfl
	
Sizin sisteminizde flex kütüphanesinin adı farklı olabilir. Linkleme hatası ile karşılaşırsanız, `-lfl` yerine `-ll`
ile deneyebilirsiniz. Derlenen programı (gcc ile derlediyseniz `a.out`) çalıştırdığınızda, sizden birşeyler yazmanızı
bekleyecektir. `merhaba username` yazarak `enter` tuşuna basarsanız, username kelimesinin yerine, login sahibi kullanıcının
adı gelmiş şekilde size çıktı verecektir. CTRL^D tuş kombinasyonu ile programdan çıkabilirsiniz.

Örnekte de gördüğünüz gibi, bir flex dosyasında, kurallar ve bunlara karşılık gelen C kodlarını tanımlarız. Kuralları tanımlamak için, düzenli ifadeler kullanırız. Bu örnekte,
metin içinde `username` ile eşleşme sağlandığında, `printf("%s", getlogin());` C kodu çalışacak. Böylece, `username`
geçen yerleri, kullanıcının login adıyla değiştirmiş olduk. Hiçbir kuralla eşleşmeyen `merhaba` kelimesi, çıktı
olarak kopyalanır.

Pratikte göreceğiniz flex dosyaları, bundan daha karmaşık olacaktır. Daha normal bir örnek görmek isterseniz,
[C Programlama Dili için hazırlanmış Lex dosyasını](http://www.quut.com/c/ANSI-C-grammar-l-1998.html) inceleyebilirsiniz.

Bir lex dosyası, en az 1, en çok 3 kısımdan oluşur. Kısımlar birbirinden `%%` işareti ile ayrılır. Birinci kısımda,
genel tanımlamalar yapılır. Bu kısımda doğrudan C kodu kullanmak isterseniz, `%{` ve `%}` işaretleri arasına
yazmanız gerekiyor. Bu kısma yazdığınız C kodları, oluşan `lex.yy.c` dosyasının üst kısımlarına kopyalanır. Bu nedenle,
`#include` ifadesi kullanmak isterseniz, bu kısımda kullanmalısınız. İkinci kısımda,
kuralları ve kurallara karşılık glen C kodlarını tanımlıyoruz. Üçüncü kısımda ise, istediğiniz C kodunu yazabilirsiniz.
Burada yazdığınız C kodları da olduğu gibi `lex.yy.c` dosyasına kopyalanacak.
Bu 3 kısımdan sadece ikincisi zorunlu. Eğer birinci kısmı boş bırakacaksanız, ikinci kısma geçtiğinizin anlaşılması için dosyaya
`%%` ile başlamanız gerekiyor.

Aşağıda biraz daha gelişmiş bir Lex dosyası örneği var. Bu kodları test etmek için, `example2.l` adında bir dosya oluşturup,
aşağıdaki içeriği içine kopyalayın. Bu programı derlerken, `main` ve `yywrap` fonksiyonlarını biz sağladığımız için, flex
kütüphanesi ile <span style="text-decoration: underline">linklememeniz</span> gerekiyor. Bu aşamada `yywrap` fonksiyonunun
işlevi önemli değil. Olduğu gibi kabul edin. Kullandığımız `yylex` fonksiyonu ise, flex tarafından
sağlanan ve asıl işi yapan fonksiyon.

	:::c
	%{
	int num_lines = 0, num_chars = 0;
	%}

	%%
	\n ++num_lines; ++num_chars;
	.  ++num_chars;
	%%
	int main(void) {
		yylex();
		printf("satir sayisi = %d, karakter_sayisi = %d\n", num_lines, num_chars);
		return 0;
	}

	int yywrap() { return 1; }
	
Tebrikler, Lex kullanarak, metin belgesindeki karakterleri ve satırları sayan bir program ürettiniz.

Bison Programının Anatomisi
===========================

Bison dosyaları da, Flex dosyaları gibi `%%` ile ayrılmış 3 kısımdan oluşur. Aynı şekilde, birinci kısımda
tanımlamalar, ikinci kısımda kurallar, üçüncü kısımda ise, istediğimiz C kodları bulunuyor. Kuralların
hangi formatta yazılacağına, bu yazının devamında uygulamalı olarak değineceğiz.

JSON Formatı
================

JSON (JavaScript Object Notation) programlar arası veri alışverişinde yaygın olarak
kullanılan sade ve kompakt bir formattır. JSON formatında 6 çeşit veri türü ifade edilebilir.

 - String (Örn. "Bu bir string")
 - Sayı   (Örn. 12.57)
 - Boolean (true/false)
 - null
 - Object (Örn: {'key': 'value'})
 - Array (Örn: [1,2,3])
 
C dilinde, herhangi bir JSON değerini tutabilecek bir veri yapısı, ve bu veri yapısı
üzerinde işlem yapacak bir kütüphane tasarlamak geniş bir konu olduğundan, bu yazıda
tasarlanan parser'ı sadece JSON nesnelerinin türünü konsola çıktı vermek için kullanacağız. Burada
oluşturacağımız Parser ile birlikte çalışacak JSON kütüphanesini, önümüzdeki günlerde
yazmayı planladığım ayrı bir blog yazısına bırakıyorum.

Tokenler
========

JSON grameri için, aşağıdaki tokenleri kullanacağız;

 - String
 - Number
 - `true`/`false`/`null`
 - Şu karakterler: `[{:,}]`

Bu tokenlerin arasında kalan boşluk, tab, yeni satır gibi karakterleri göz ardı edeceğiz.

Projenin İskeleti
=================

Yazıyı takip etmeyi kolaylaştırmak için, [hazırladığım proje iskeletini](../jsonparser-skeleton.tar.gz)
indirerek, arşivi açtıktan sonra, `./configure` komutu ile projeyi derleme
aşamasına getirebilirsiniz. Eğer sisteminizde C derleyicisi, flex ve bison programlarından biri eksikse,
`configure` programı hata verecektir. Proje iskeletinin içinde bizi ilgilendiren 2 dosya var; `lexer.l` ve `parser.y`.
`lexer.l` flex programı tarafından okunup lexer kodlarını, `parser.y` de bison tarafından okunup parser
kodlarını oluşturacak. İskelet proje içindeki diğer dosyalar build sisteminin bir parçası olduğundan, detayları
bu yazının konusunun dışında kalıyor. İskelet projeyi indirmeden devam etmek isteyenler için, `lexer.l` ve
`parser.y` nin şablonları aşağıdaki şekilde;

`lexer.l`

	:::c
	%{
	#include "parser.h" // bison -d tarafından otomatik oluşturuluyor
	%}

	%%

	%%
	int yywrap() {
		return 1;
	}

`parser.y`

	:::c
	%{
	#include <stdlib.h>
	#include <stdio.h>
	extern int yylex();
	extern int yyparse();
	void yyerror(const char *s);
	%}
	%start line
	%token NEWLINE
	%%
	line: NEWLINE
	%%

	int main(void) {

		return 0;
	}

	void yyerror(const char *s) {
		printf("Parse error: %s\n",s);
		exit(-1);
	}
	

İşe Koyulalım
==============

Tanıyacağımız tokenleri `parser.y` içine ekleyerek başlayacağız. Bunun için iskelet projedeki `parser.y`
dosyasındaki `%start` ve `%token` ile başlayan satırları silerek, bunun yerine aşağıdaki satırları ekleyin.

	%start JValue
	%token T_STRING T_NUMBER T_TRUE T_FALSE T_NULL
	
Tek karakterden oluşan tokenler için (virgül, süslü parantez vs.), token tanımı yapmaya gerek yok.
Yukarıda `%start` ile başlayan satırda, gramer'in başlangıç sembolünü de değiştirdiğimiz için,
`parser.y` içinde `line: ` ile başlayan satırı da aşağıdaki şekilde değiştirin;

	JValue: T_STRING | T_NUMBER | T_TRUE | T_FALSE | T_NULL

Burada, gramer'imizin başlangıç kuralını da belirlemiş olduk. `JValue` kuralını `%start` kuralı
olarak belirlediğimiz için, parser'ımız tüm girdisini bir `JValue`'ya indirgemeyi deneyecek.
Kuralı tanımlarken kullandığımız "|" işareti, düzenli ifadelerde olduğu gibi, seçenek ifade ediyor.
İlk kuralı kelimelerle ifade etmek gerekirse, `JValue` bir T_STRING, ya da bir T_NUMBER, ya da bir T_TRUE, ya da bir T_FALSE, ya
da bir T_NULL olabilir. Array ve Object türleri daha karmaşık olduğu için, onları sonraki adımlarda
ekleyeceğiz.

Parser `T_STRING`, `T_NUMBER` gibi tokenleri, lexer'dan bekleyecek. Basit
tokenleri lexer'a tanımlayarak başlayalım. Projedeki `lexer.l` dosyasını açıp, iki `%%` arasındaki boş satıra,
aşağıdaki satırları ekleyin;

	":"	{ return ':'; }
	","	{ return ','; }
	"{"	{ return '{'; }
	"}"	{ return '}'; }
	"["	{ return '['; }
	"]"	{ return ']'; }
	"null"  { return T_NULL; }
	"true"   { return T_TRUE; }
	"false"  { return T_FALSE; }
	[ \t\n\r]+ { /* ignore */ }

Program şu an derlenebilir aşamada, ancak, herhangi bir çıktı vermediğimiz
için, ne başardığımızı test edemiyoruz. `parser.y` dosyası içindeki kuralları, aşağıdaki
şekilde güncelleyin.

	JValue: T_STRING {puts("String");}
		  | T_NUMBER {puts("Number");}
		  | T_TRUE   {puts("TRUE");}
		  | T_FALSE  {puts("FALSE");}
		  | T_NULL   {puts("NULL");}
		  
Nasıl lexer dosyasına eşleşme sağlandığında çalışacak kodlar ekleyebiliyorsak, parser
dosyasına da yukarıdaki örnekte olduğu gibi, kod ekleyebiliyoruz. Böylece, bir eşleşme olduğunda,
konsolda çıktı görebileceğiz. Parser'ımızın çalışması için, `main` fonksiyonuna, `yyparse` çağrısı
eklemek gerekiyor.

	int main(void) {
		yyparse();
		return 0;
	}

`yyparse` fonksiyonu, bison tarafından sağlanan ve parser'ı çalıştıran fonksiyon. Artık projeyi derleyip (`make` komutu ile)
aşağıdaki komutlarla test edebilirsiniz.

	echo "true" | ./jsonparser
	echo "false" | ./jsonparser
	echo "null" | ./jsonparser
	echo "   true   " | ./jsonparser
	echo "yok" | ./jsonparser
	
Basit tokenleri bitirdikten sonra, düzenli ifade kullanmak zorunda kalacağımız
tokenlere geçebiliriz. Önce, String ile eşleşen bir düzenli ifade ile başlayalım. `lexer.l`
içine, aşağıdaki satırı ekleyip, programı tekrar derleyin.

	\"(\\.|[^\\"\n])*\" { return T_STRING; }
	
Aşağıdaki şekilde, programı test edebilirsiniz.

	echo "   \"metin var\"  " | ./jsonparser
	
Program çalıştığında konsolda "String" çıktısını göreceksiniz, ancak, `lexer.l`
içindeki düzenli ifademiz çok karmaşık görünüyor. Bunu çözmek için,
`lexer.l`'nin birinci kısmında bazı tanımlamalar yapacağız. Aşağıdaki kodları,
`lexer.l`'deki ilk `%%` işaretinden hemen önce gelecek şekilde dosyaya ekleyin.

	TIRNAK ["]
	BIRKARAKTER .
	TERSTAKSIM \\
	KACMAKARAKTER {TERSTAKSIM}{BIRKARAKTER}
	NORMALKARAKTER [^\\"\b\f\n\r\t]
	KARAKTER {NORMALKARAKTER}|{KACMAKARAKTER}
	KARAKTERLER {KARAKTER}+

Böylece, `\"(\\.|[^\\"\n])*\"` düzenli ifadesinin yerine, `{TIRNAK}{TIRNAK}|{TIRNAK}{KARAKTERLER}{TIRNAK}`
yazabilirsiniz. Bu sayede, düzenli ifademiz çok daha okunaklı olur. `T_STRING` tokenimiz ile standart JSON
string'i arasındaki küçük farklılıkları, yazıyı kısa tutmak adına dikkate almayacağım. `T_NUMBER` ile devam edelim.
Önce aşağıdaki tanımları, `lexer.l`'nin tanımlar kısmına ekleyin.

	ONDALIK [.]
	POZITIFRAKAM [1-9]
	SIFIR 0
	RAKAM {SIFIR}|{POZITIFRAKAM}
	E     [eE]
	EXP   {E}[-+]?{RAKAM}+
	FRAC  {ONDALIK}{RAKAM}+
	INT   {SIFIR}|{POZITIFRAKAM}{RAKAM}*
	
Bu tanımlamaları yaptıktan sonra, aşağıdaki kuralı, kurallar kısmına ekleyip, projeyi tekrar test edebiliriz.

	[-]?{INT}{FRAC}?{EXP}?			{ return T_NUMBER; }
	
`lexer` artık `T_NUMBER` tokeni de gönderebildiğine göre, `lexer.l` ile daha fazla işimiz kalmadı. `parser.y` içinde
hala Object ve Array türlerini tanımlamadık. Önce, Array ile başlayalım. `parser.y` içinde kuralları aşağıdaki şekilde
yeniden düzenleyin.

	JValue: T_STRING {puts("String");}
		  | T_NUMBER {puts("Number");}
		  | T_TRUE   {puts("TRUE");}
		  | T_FALSE  {puts("FALSE");}
		  | T_NULL   {puts("NULL");}
		  | JArray   {puts("Array");}

	JArray: '[' ']'
		  | '[' Liste ']'

	Liste: JValue
		 | Liste ',' JValue 

Programı derleyip, şu komutla test ederseniz, aşağıdaki gibi bir çıktı göreceksiniz: `echo "[1, 2, 3, true, false, null ]" | ./jsonparser`

	Number
	Number
	Number
	TRUE
	FALSE
	NULL
	Array
	
Eğer konsolda tek bir satır çıktı görmeyi beklediyseniz, şaşırmış olabilirsiniz. Yazdığımız kurallara
dikkat ederseniz, `JValue` sembolü her oluştuğunda, konsola hangi türden bir `JValue` oluştuğunu
yazıyoruz. `JArray` içinde de sınırsız sayıda `JValue` bulunabildiği için, bunlara ait çıktıları
da konsolda göreceğiz. Köşeli parantez kapama tokeni (`]`) gelene kadar `JArray` tanımı eksik
kaldığı için, konsolda "Array" çıktısını en son görüyoruz.

Burada ilk kez birden fazla tokenden üretilen bir sembol tanımı yapmış olduk. `JValue` örneğinde,
tek bir T_STRING tokeni, bir `JValue` tanımlamak için yeterli iken, bir `JArray` için en azından
ardarda gelmiş `[` ve `]` tokenleri gerekiyor.

`JArray` içinde geçen `Liste` sembolü de, tanımladığımız ilk özyinelemeli (eng. recursive) sembol oldu.

	Liste: JValue
		 | Liste ',' JValue

Burada şunu ifade etmiş oluyoruz; tek başına `JValue` bir `Liste` tanımlar, ya da, `Liste` `,` `JValue`
yanyana geldiğinde bir liste tanımlar. Böyle bir gramer, bir veya daha fazla `JValue` değerinin birbirine
`,` ile bağlanarak bir liste oluşturduğunu ifade ediyor.

`Object` türünün gramer tanımı da, `JArray`'e çok yakın;

	JObject: '{' '}'
		   | '{' KVListe '}'

	KVListe: KV
		   | KVListe ',' KV

	KV: T_STRING ':' JValue
	
Bunun tek farkı, süslü parantezler içinde değerler listesi değil de, anahtar-değer çiftleri listesi var. `JValue`
tanımını da aşağıdaki şekilde güncelledikten sonra, programı yeniden derleyebiliriz.

	JValue: T_STRING {puts("String");}
	  | T_NUMBER {puts("Number");}
	  | T_TRUE   {puts("TRUE");}
	  | T_FALSE  {puts("FALSE");}
	  | T_NULL   {puts("NULL");}
	  | JArray   {puts("Array");}
	  | JObject  {puts("Object");}
	  
Bu programı, `echo "{\"sayi\":12, \"liste\": [true, false, null]}" | ./jsonparser` komutu
ile test ederseniz, ekrana aşağıdaki çıktıyı alacaksınız.

	Number
	TRUE
	FALSE
	NULL
	Array
	Object

Dikkat ederseniz, çıktının hiçbir yerinde String ifadesi geçmiyor. Anahtar-değer çiftlerinde
anahtar görevi gören string'ler, kendi başlarına bir JValue ifade etmediği için, konsolda
çıktı olarak da göremiyoruz.

Böylece, JSON formatındaki veriyi tarayan programı bitirmiş olduk. Bu yazıda, ekranda çıktı göstermek dışında,
faydalı bir iş yapmasak da, lexer ve parser kullanarak bir metni taramayı başardık. Bu serinin ikinci kısmında,
Parser'ımızla bir JSON kütüphanesini bir araya getirip, validasyon/formatlama/başka türe dönüştürme
gibi konulara değinmeyi düşünüyorum.
<!--
.. date: 2019-06-28 00:17
.. description: C dilinde JSON Kütüphanesi Tasarımı ve Flex/Bison Parser ile Entegre Edilmesi
.. slug: json-kutuphanesi
.. title: Flex ve Bison kullanarak JSON İşleme (2. Kısım)
-->

Bu yazının [birinci bölümünde](flex-bison.html) Flex/Bison kullanarak
JSON tarayan bir parser yapmıştık. Ancak, bu parser karşılaştığı
JSON türlerinin ismini konsola yazmak dışında faydalı bir iş yapmıyordu.
Bu yazıda, sıfırdan bir JSON kütüphanesi tasarlayarak, parser ile
entegre edeceğiz. Bu yazı için gerekli proje iskeletine
[bu linkten](../jsonparser-skeleton.2.tar.gz)
ulaşabilirsiniz. Projeyi derlemeye hazırlamak için `./configure`
komutunu vermeyi unutmayın.

Kütüphane Arayüzü
==================

`json.h` header dosyası içine aşağıdaki satırları ekleyin. 

	:::c
	typedef enum {
		JTYPE_NULL,
		JTYPE_BOOL,
		JTYPE_NUMBER,
		JTYPE_STRING,
		JTYPE_ARRAY,
		JTYPE_OBJECT
	} JType;

	typedef struct _json JSON;

	// deger olusturmak icin 
	JSON *json_make_null();
	JSON *json_make_bool(int c);
	JSON *json_make_number(double d);
	JSON *json_make_string(char *c);
	JSON *json_make_array();
	JSON *json_make_object();

	// json tipini almak icin
	JType json_get_type(JSON *j);

	// array ve object icine elemen eklemek icin gerekli fonksiyonlar
	JSON *json_array_push(JSON *arr, JSON *value);
	JSON *json_object_add(JSON *obj, char *key, JSON *value);
	
	// konsola yazdirmak icin
	void json_print(JSON *j, int indentation);

JSON kütüphanemizin oldukça basit bir arayüzü var. 6 farklı türde JSON oluşturmak
için, 6 farklı `json_make_*` fonksiyonumuz var. `json_get_type` adından anlaşılacağı
gibi, JSON değerinin türünü (string, null vs.) tespit etmeye yarıyor. `json_array_push`
ve `json_object_add` sırasıyla Array ve Object türlerine eleman eklemeye yarıyor.
`json_print` fonksiyonunu da okuduğumuz JSON verisini güzel bir formatta çıktı vermek
için kullanacağız.	
	
Kütüphane Kodları
=================

	Bu başlık altında yazacağımız kodları, `json.c` dosyasına ekleyin.

Kütüphanenin tek bir `_struct json` veri yapısı ile çalışabilmesi için,
bu veri yapısının 6 farklı türde JSON verisini bünyesinde barındıracak
şekilde tasarlarlanması gerekiyor. Benim kullanacağım veri yapısı aşağıdaki
gibi;

	:::c
	struct _json {
		JType type;
		struct _json *prev;
		struct _json *next;
		char   *key;
		struct _json *elems;
		char   *s_val;
		double d_val;
	};

	
`struct _json` yazacağımız kütüphanenin merkezinde olacağı için, detaylı bir açıklamayı
hak ediyor.
 
 - `type`: JSON objesinin 6 farklı JSON türünden hangisine ait olduğunu tutacağımız değişken.
 - `prev` ve `next`: Array veya Object içindeki elemanlarda, bir önceki ve bir sonraki objeye referans olarak kullanılacak.
 - `key` : Object içinde bulunan değelerin adını tutmak için kullanılacak.
 - `elems` : Object ve Array türlerinde, içerdiği eleman listesinin ilk elemanına referans olarak kullanılacak.
 - `s_val` : String türünde, string'in değerini tutmak için kullanılacak
 - `d_val` : Number ve Boolean türlerinde, değeri tutmak için kullanılacak.
 
Farklı JSON türlerinde değer oluşturacak fonksiyonlarla devam edelim.

	:::c
	JSON *json_make_empty(JType type)
	{
		JSON *j = calloc(1, sizeof(JSON));
		j->type = type;
		return j;
	}

	JSON *json_make_null()
	{
		return json_make_empty(JTYPE_NULL);
	}

	JSON *json_make_bool(int c)
	{
		JSON *j = json_make_empty(JTYPE_BOOL);
		j->d_val = !!(c);
		return j;
	}

	JSON *json_make_number(double d)
	{
		JSON *j = json_make_empty(JTYPE_NUMBER);
		j->d_val = d;
		return j;
	}

	JSON *json_make_string(char *c)
	{
		JSON *j = json_make_empty(JTYPE_STRING);
		j->s_val = c;
		return j;
	}

	JSON *json_make_array()
	{
		return json_make_empty(JTYPE_ARRAY);

	}

	JSON *json_make_object()
	{
		return json_make_empty(JTYPE_OBJECT);
	}

Bu fonksiyonlar yeterince sade olduğu için, ekstra bir açıklamaya gerek duymuyorum. `json_get_type`
fonksiyonu da, gayet basit:

	JType json_get_type(JSON *j)
	{
		return j->type;
	}

Object ve Array türlerine eleman eklemek için, aşağıdaki fonksiyonları kullanacağız.

	:::c
	JSON *_array_push(JSON *head, JSON *new)
	{
		if(head == NULL)
			return new;

		JSON *p;
		for(p = head; p->next != NULL; p = p->next)
		{
			/* skip */
		}

		p->next = new;
		return head;
	}

	JSON *json_array_push(JSON *arr, JSON *j)
	{
		arr->elems = _array_push(arr->elems, j);
		return arr;
	}

	JSON *json_object_add(JSON *obj, char *key, JSON *j)
	{
		j->key = key;
		obj->elems= _array_push(obj->elems,j);
		return obj;
	}

Parser, Lexer ve Kütüphane'yi Tanıştırmak
=========================================

Lexer ve Parser'ın kütüphanemizle uyumlu çalışabilmesi için, öncelikle, aşağıdaki kod bloğunu `parser.y`'nin
ilk satırına eklememiz gerekiyor.

	%code requires {
		  #include "json.h"
	}

Yazının devamında, parser'ın tanıdığı sembolleri, `JSON` veri tipine dönüştüreceğiz.
Bunun için, `#include "json.h"` direktifi ile,  parser'ımıza kütüphanemizi
tanıtmamız gerekiyor. Bu içe aktarma işlemini `%code requires` ile yapmak,
`#include` satırının `parser.h` içinde, `%union` tanımından önce gelmesini
temin etmek. Sırada zaten `%union` direktifi var.

Bir önceki yazıda, ne `T_NUMBER` gibi tokenler, ne de `JVvalue` gibi semboller
bir değer taşıyordu. Artık parser'ımızın bir değer üretmesini sağlayacağız. Bunun
için, token ve sembollerin veri tiplerini tanıtmamız gerekiyor. Bunun ilk
adımı da, kullanacağımız veri tipi çeşitlerini, `%union` direktifi ile
göstermek. Aşağıdaki bloğu, `%code requires` bloğunun
hemen altına ekleyin.

	%union
	{
		  char *s_val;
		  double d_val;
		  JSON   *j_val;
	}

Sembol ve tokenlerin veri tiplerini de, aşağıdaki şekilde göstereceğiz. `parser.y`
içindeki sembol ve token tanımlarını aşağıdaki şekilde değiştirin.

	%start JValue
	%type  <j_val> JValue JArray JObject Liste KVListe
	%token <s_val> T_STRING
	%token <d_val> T_NUMBER
	%token T_TRUE T_FALSE T_NULL

T_TRUE, T_FALSE ve T_NULL tokenlerinin bir değer taşımasına gerek yok. Zaten tokenin
kendisi ihtiyacımız olan tüm bilgiyi bize sağlıyor. `T_STRING` için `char *` türünde,
`T_NUMBER` için de `double` türünde veri tutacağız. Bunları bize metinden okuduğu değere
göre, lexer sağlayacak. `lexer.l` içindeki T_NUMBER ve T_STRING döndüren kuralları, aşağıdaki
şekilde değiştirin.

	{TIRNAK}{TIRNAK}|{TIRNAK}{KARAKTERLER}{TIRNAK} { yylval.s_val = strdup(yytext); return T_STRING; }
	[-]?{INT}{FRAC}?{EXP}?			               { yylval.d_val = atof(yytext); return T_NUMBER; }

`yylval`, lexer ve parser arasında veri transferi yapmaya yarayan global bir değişken. Eğer `%union`
direktifi ile ayarlama yapmamış olsaydık, `yylval` global değişkeni `char *yylval` olarak tanımlanacaktı.
Bu durumda, lexer'dan parser'a `double` türünde veri geçiremeyecektik. Doğru müdahaleyi yaptığımız için,
`yylval`, içinde `s_val`, `d_val` ve `j_val` üyelerini barındıran bir veri tipi haline geldi. `%token <s_val> T_STRING`
tanımı sayesinde de, `T_STRING` tokeni ile, `s_val` değerini birbiriyle ilişkilendirmiş olduk. Aynı
durum `T_NUMBER` için de geçerli.

Tokenlerimize değer tanımladık, sıra diğer sembollerin değerlerini oluşturmaya geldi. `parser.y`
içindeki kuralları aşağıdaki gibi değiştireceğiz;

	JValue: T_STRING {$$ = parse_result = json_make_string($1); }
		  | T_NUMBER {$$ = parse_result = json_make_number($1); }
		  | T_TRUE   {$$ = parse_result = json_make_bool(1);    }
		  | T_FALSE  {$$ = parse_result = json_make_bool(0);    }
		  | T_NULL   {$$ = parse_result = json_make_null();     }
		  | JArray   {$$ = parse_result = $1;                   }
		  | JObject  {$$ = parse_result = $1;                   }

	JArray: '[' ']'                         {$$ = json_make_array(); }
		  | '[' Liste ']'                   {$$ = $2; }

	Liste: JValue                           {JSON *arr = json_make_array(); $$ = json_array_push(arr, $1); }
		 | Liste ',' JValue                 {$$ = json_array_push($1, $3); }

	JObject: '{' '}'                         {$$ = json_make_object(); }
		   | '{' KVListe '}'                 {$$ = $2                ; }

	KVListe: T_STRING ':' JValue             { JSON *obj = json_make_object(); $$ = json_object_add(obj, $1, $3); }
		   | KVListe ',' T_STRING ':' JValue { $$ = json_object_add($1, $3, $5) ;}

Sanırım konunun en can alıcı yerine geldik. Öncelikle, `parse_result` değişkeniyle başlayalım.
Bu değişkeni, `parser.y`'nin birinci kısmında, `%{` ve `%}` arasındaki bloğun içinde, `JSON *parse_result`
olarak tanımladım. Bu sayede, parse işlemi sonuçlandığında, bu global değişken sayesinde, sonuca
erişebileceğim.

Burada ilk kez, `$$` ve `$1` gibi değişkenler kullandık. `$$` değişkeni, yeni oluşacak
sembole değer atamak için, `$1`,`$2`,`$3` gibi değişkenler de, gramer tanımındaki
1., 2., 3. vb. sembollerin değerlerine erişmek için kullanılıyor. Yukarıda yapılan
tanımları, aşağıdaki gibi hayal edebilirsiniz.
	
		JValue: T_STRING {JValue = parse_result = json_make_string(yylval.s_val); }
		  | T_NUMBER {JValue = parse_result = json_make_number(yylval.d_val); }
		  | T_TRUE   {JValue = parse_result = json_make_bool(1);    }
		  | T_FALSE  {JValue = parse_result = json_make_bool(0);    }
		  | T_NULL   {JValue = parse_result = json_make_null();     }
		  | JArray   {JValue = parse_result = JArray;                   }
		  | JObject  {JValue = parse_result = JArray;                   }

	JArray: '[' ']'                         {JArray = json_make_array(); }
		  | '[' Liste ']'                   {JArray = Liste; }

	Liste: JValue                           {JSON *arr = json_make_array(); Liste = json_array_push(arr, JValue); }
		 | Liste ',' JValue                 {Liste = json_array_push(Liste, JValue); }

	JObject: '{' '}'                         {JObject = json_make_object(); }
		   | '{' KVListe '}'                 {JObject = KVListe                ; }

	KVListe: T_STRING ':' JValue             { JSON *obj = json_make_object(); KVListe = json_object_add(obj, yylval.s_val, JValue); }
		   | KVListe ',' T_STRING ':' JValue { KVListe = json_object_add(KVListe, yylval.s_val, JValue) ;}
		   
Kodların normal haliyle, bu hayali kodlar karşılaştırıldığında, `$` değişkenlerinin işlevi yeterince kendini
belli etti diye düşünüyorum.

Böylece, metin belgesinden JSON formatında bir veriyi tarayıp, C veri yapılarına aktarmış olduk. Okuduğumuz veriyi,
C ile istediğimiz şekilde değerlendirebiliriz. Benim aklıma ilk gelen şey, JSON formatlama oldu.

Formatlanmış JSON Çıktısı
=========================

Konuyu fazla dağıtmamak adına, JSON formatlama ile ilgili kodlara burada değinmeyeceğim. İsteyenler,
[projenin tamamlanmış hali'ni](../../jsonparser-skeleton.2.tar.gz) indirerek, bu kodları
inceleyebilir. Projeyi indirip, bir yere açtıktan sonra, `./configure` ve `make` komutları
ile, projeyi derleyebilirsiniz. Klasörün içinde, projeyi test etmeniz için, `example1.json`,
`example2.json` ve `example3.json` adında 3 adet dosya var. `./jsonparser < example1.json > example1-pretty.json`
benzeri komutlarla, programı test edebilirsiniz. Formatlanmış çıktıyı oluşturan kodlar, `json.c` içinde bulunabilir.

Uyarılar
========

Bu tutorial'ın öncelikli hedefi Flex/Bison ile lexer/parser yapmak olduğu için, önemli olabilecek
bazı noktaları göz ardı ettim. Eğer burada okuduğunuz kodları gerçek bir işte kullanmaya kalkışacaksanız,
aşağıdaki noktalara dikkat etmeniz gerekiyor.

 - Lexer'ın tanıdığı string ile JSON standardındaki string arasında bazı farklılıklar var. Örneğin, json stringi
   içinde \x kaçma karakterinden sonra, 4 haneli bir sayı gelmeli. Bizim lexer'ımız buna dikkat etmiyor.
 - Sayı türünde çıktı alırken, her zaman noktadan sonra 6 hane bulunuyor. Sayı çıktılarının düzeltilmesi gerek.
 - Birçok yerde `calloc` çağrısı var ama hiç `free` çağrısı yok. Eğer uzun süre çalışacak bir program yazacaksanız,
   tuttuğunuz hafızayı işiniz bitince salmanız gerek.
 - Hata kontrolü neredeyse yok. Özellikle `json_array_push` ve `json_object_add` fonksiyonlarında, verilen
   argümanın tipi gerçekten array/object mi kontrol edilebilir.
 - Multithread bir programda denemeyin bile, malumunuz herşey global değişkenlerde. Flex/Bison ile
   reentrant parser da yapılabiliyor, ancak, ben hiç denemedim. İsterseniz, [belgeleri okuyabilirsiniz](https://www.gnu.org/software/bison/manual/html_node/Pure-Decl.html)

 
Son Sözler
==========

Siz ne düşünüyorsunuz bilmiyorum ama, ben parser konusunu çok heyecan verici buluyorum. Bu iki yazıda öğrendiklerinizin
üzerine biraz daha araştırma yaparak, CSV, HTML, XML, HTTP protokolü, ini dosyaları gibi çok çeşitli metin belgeleri
üzerinde çalışabileceğiniz gibi, bir programlama dili derleyicisi veya yorumlayıcısı da yapabilirsiniz. Haydi gidin, birşeyler kodlayın.

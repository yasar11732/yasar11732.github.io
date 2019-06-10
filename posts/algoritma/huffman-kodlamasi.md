<!--
.. date: 2019-06-10 21:29
.. slug: huffman-kodlamasi
.. title: Huffman Kodlaması
-->

Bir mesajı, rakamları kullanarak kodlayacak olsanız, en az rakam kullanarak nasıl
kodlarsınız? David Huffman 1952 yılında [A Method for the Construction of Minimum-Redundancy Codes](http://compression.ru/download/articles/huff/huffman_1952_minimum-redundancy-codes.pdf)
başlıklı makalede bu soruya cevap aramış, ve bir metot ortaya atmış. Bu metot
insanların çok etkilemiş olacak ki, png, jpeg, mp3 gibi dosya formatlarında,
ayrıca HTTP'nin standard sıkıştırma metotlarından deflate veri formatında, deflate
formatı da gzip ve zlib kütüphanelerinde kullanılmış. Ben de merak edip, Huffman
Kodlaması nasıl yapılır öğrenmek istedim.

Huffman kodlaması temelinde bir prefix kodlamadır. Prefix kodlamaya örnek olarak,
aşağıdaki örneği inceleyelim.


		   / \             d: 000
		  0   1            b: 001
		/   \   \          c: 01
	   0     1   a         a: 1
	  / \    /
	 0   1   c
	/    \
	d     b
	
Prefix kodlamada, kodlanmak istenen her karaktere, bir veya daha çok
rakamdan oluşan kodlar atanır. Bu kodlar atanırken, herhangi bir kodun,
kendinden uzun başka bir kodun başlangıcı olmaması gerekiyor. Böylece, bu kodlar
arka arkaya dizildiğinde, mükemmel şekilde geri ayrıştırılabiliyor. Yukarıdaki
tabloda, en kısa kod, a karakterine atanmış. a karakterine atanan kod
1 olduğu için, diğer kodların hiçbiri 1 ile başlayamıyor. Aynı şekilde,
c karakterine kod olarak 01 atandığı için, diğer kodların hiçbiri 01 ile
başlayamıyor. Bu özelliklere sahip kodlar oluşturmak için, yukarıdaki
gibi bir ağaç oluşturarak, ağacın yapraklarına kodlanacak karakterler
yerleştirip, her yol ayrımında bir yöne 0, diğerine 1 atayabilirsiniz.
Tepeden başlayıp, istediğiniz karaktere gelene kadar geçtiğiniz rakamlar,
o karakterin kodunu verir.

Huffman kodlamasının amacı, prefix ağacını, sıkıştıracağımız metinde
en çok kullanılan karakterlere, (veya sıkıştıracağımız veride en çok kullanılan byte'lara)
en kısa kodu verecek şekilde oluşturmaktır. Bunun için kullanılacak algoritma
şu şekilde.

 1. Karakterleri, metin içinde görünme sıklığına göre sırala.
 2. En küçük iki karakteri grupla, bunları görülme sıklıklarını toplayarak, sıraya tekrar dahil et.
 3. Tek bir grup kalana dek, gruplamaya devam et.
 
Bu algoritmayı uygulamak için, bir BST ve bir dinamik array veri yapısı kullanacağım.
Dinamik array yerine, Heap daha iyi bir tercih olabilir. Ben daha kolay anlaşılacağını
düşündüğüm için, array kullandım. Algoritmaya geçmeden önce, veri yapılarına bir göz
atalım.

	:::c
	typedef struct _huffman
	{
		char c;
		int freq;
		struct _huffman *left;
		struct _huffman *right;
	} HUFFMANTREE;

	typedef struct _huffman_array {
		int cap;
		int size;
		HUFFMANTREE **items;
	} HUFFMANARRAY;
	
HUFFMANTREE veri yapısını, gruplamaları yapmak için, HUFFMANARRAY veri yapısını ise, gruplamaları
sıralamak için kullanacağım. Sıralama algoritması olarak, klasik "selection sort" yöntemini tercih ettim.
Bu algoritmanın nasıl çalıştığını anlamadıysanız, bir listedeki elemanları, büyükten küçüğe
sıraladığını bilmeniz yeterli.

	:::c
	void huffman_array_sort(HUFFMANARRAY *arr)
	{
		int i, k;
		int max_index, max_value;

		for (i = 0; i < arr->size - 1; i++)
		{
			max_index = i;
			max_value = arr->items[i]->freq;

			for (k = i + 1; k < arr->size; k++)
			{
				if (arr->items[k]->freq > max_value)
				{
					max_value = arr->items[k]->freq;
					max_index = k;
				}
			}

			if (i != max_index)
			{
				(unsigned long)arr->items[i] ^= (unsigned long)arr->items[max_index];
				(unsigned long)arr->items[max_index] ^= (unsigned long)arr->items[i];
				(unsigned long)arr->items[i] ^= (unsigned long)arr->items[max_index];
			}

		}
	}
	
Büyükten küçüğe sıralanmış bir array'in en küçük elemanı sonda olduğu için, en
küçük elemanı kolayca array'den çıkarabiliriz.

	:::c
	HUFFMANTREE *huffman_array_pop(HUFFMANARRAY *arr)
	{
		return arr->items[--arr->size];
	}
	
Şimdi algoritmanın uygulamasına geçelim. Öncelikle metinde geçen karakterlerin
görülme sıklıklarını hesaplamamız gerekiyor.

	:::c
	unsigned long frequencies[0xFF];
	char metin[] = "bu oylesine uzun, oylesine girift bir metin ki, muhakkak gereksiz bitlerini temizlemek gerekir.";
	char *pcTemp;
	int i;

	memset(&frequencies[0], 0, sizeof(frequencies));

	for (pcTemp = &metin[0]; *pcTemp != 0; pcTemp++)
	{
		frequencies[(int)*pcTemp]++;

	}
	
Metnin üstünden bir kez geçerek, karakterleri saydım. Şimdi, sıfırdan büyük
karakleri array'imize ekleyelim.
	
	:::c
	HUFFMANARRAY *arr = huffman_array_new();
	for (i = 0; i < 255; i++)
	{
		if (frequencies[i] > 0)
		{
			huffman_array_add(arr, huffmantree_new(i, frequencies[i]));
		}
	}

Son olarak, sadece tek bir grup kalana kadar, küçükten büyüğe
gruplamak kaldı.

	:::c
	while (arr->size > 1)
	{
		huffman_array_sort(arr);
		HUFFMANTREE *t1 = huffman_array_pop(arr);
		HUFFMANTREE *t2 = huffman_array_pop(arr);
		HUFFMANTREE *t3 = calloc(1, sizeof(HUFFMANTREE));
		t3->left = t1;
		t3->right = t2;
		t3->freq = t1->freq + t2->freq;
		huffman_array_add(arr, t3);

	}
	
Bu noktada, prefix ağacımız hazır oldu. Karakterlere atanan kodları görebilmek için,
küçük bir yardımcı fonksiyon yazdım.

	:::c
	// huffmantree_print(t, "", 0) şeklinde çağrılacak.
	// prefix en uzun kodu alabilecek kadar büyük bir
	// buffer olmalı.
	void huffmantree_print(HUFFMANTREE *t, char *prefix, int size_prefix)
	{
		if (t->left == NULL && t->right == NULL)
		{
			prefix[size_prefix] = 0;
			printf("%c: %s\n", t->c, prefix);
			return;
		}

		if (t->left)
		{
			prefix[size_prefix++] = '0';
			huffmantree_print(t->left, prefix, size_prefix);
			size_prefix--;
		}

		if (t->right)
		{
			prefix[size_prefix++] = '1';
			huffmantree_print(t->right, prefix, size_prefix);
			size_prefix--;
		}

	}
	
Şimdi sonuçlara bir göz atalım.

	u: 0000
	a: 00010
	,: 00011
	o: 00100
	y: 00101
	n: 0011
	 : 010
	r: 0110
	s: 01110
	f: 011110
	.: 0111110
	h: 0111111
	b: 10000
	g: 10001
	z: 10010
	m: 10011
	i: 101
	e: 110
	k: 1110
	t: 11110
	l: 11111

Yukarıdaki tabloda görüleceği üzere, en kısa kodlar boşluk, i ve e karakterlerine, en uzun kodlar ise
nokta ve h karakterlerine verilmiş. Ayrıca kısa kodların hiçbiri, uzun kodlardan birinin başlangıcı
değil.

Huffman kodlaması ile kodlanmış bir metni veya veriyi, transfer ve depolama amacıyla kullandıktan sonra,
eski haline getirebilmek için, her bir kodun karşılığını, veri ile birlikte saklamanız
gerekiyor. Bunun için çeşitli yöntemler kullanılabilir, ancak, konuyu dağıtmamak adına, bu yazıyı
burada bitiriyorum.

Kodların tamamını aşağıda paylaşıyorum. Genel yöntemi kavradığınıza göre, daha optimize
veri yapıları ve algoritmalar kullanarak aynı kodlamayı yapmayı deneyebilirsiniz. Burada
verilen metni bit array'ine dönüştürme işlemini ve bit array'ini tekrar orjinal metne dönüştürme
işlemini de yapmadık. Bunları da denemek isteyebilirsiniz. İyi kodlamalar.

	:::c
	#include <stddef.h> // NULL
	#include <stdlib.h> // calloc
	#include <string.h> // memset
	#include <stdio.h>

	typedef struct _huffman
	{
		char c;
		int freq;
		struct _huffman *left;
		struct _huffman *right;
	} HUFFMANTREE;

	typedef struct _huffman_array {
		int cap;
		int size;
		HUFFMANTREE **items;
	} HUFFMANARRAY;

	HUFFMANTREE *huffmantree_new(char c, int freq)
	{
		HUFFMANTREE *t = malloc(sizeof(HUFFMANTREE));
		t->c = c;
		t->freq = freq;
		t->left = NULL;
		t->right = NULL;
		return t;
	}

	/*
	* Selection sort, büyükten küçüğe
	*/
	void huffman_array_sort(HUFFMANARRAY *arr)
	{
		int i, k;
		int max_index, max_value;

		for (i = 0; i < arr->size - 1; i++)
		{
			max_index = i;
			max_value = arr->items[i]->freq;

			for (k = i + 1; k < arr->size; k++)
			{
				if (arr->items[k]->freq > max_value)
				{
					max_value = arr->items[k]->freq;
					max_index = k;
				}
			}

			if (i != max_index)
			{
				(unsigned long)arr->items[i] ^= (unsigned long)arr->items[max_index];
				(unsigned long)arr->items[max_index] ^= (unsigned long)arr->items[i];
				(unsigned long)arr->items[i] ^= (unsigned long)arr->items[max_index];
			}

		}
	}

	HUFFMANTREE *huffman_array_pop(HUFFMANARRAY *arr)
	{
		return arr->items[--arr->size];
	}

	void *huffman_array_add(HUFFMANARRAY *arr, HUFFMANTREE *t)
	{
		if (arr->size + 1 == arr->cap)
		{
			arr->cap *= 2;
			arr->items = realloc(arr->items, arr->cap * sizeof(HUFFMANTREE *));
		}

		arr->items[arr->size++] = t;
	}

	HUFFMANARRAY *huffman_array_new()
	{
		HUFFMANARRAY *arr = malloc(sizeof(HUFFMANARRAY));
		arr->cap = 8;
		arr->size = 0;
		arr->items = malloc(arr->cap * sizeof(HUFFMANTREE *) );
		return arr;
	}

	void huffmantree_print(HUFFMANTREE *t, char *prefix, int size_prefix)
	{
		if (t->left == NULL && t->right == NULL)
		{
			prefix[size_prefix] = 0;
			printf("%c: %s\n", t->c, prefix);
			return;
		}

		if (t->left)
		{
			prefix[size_prefix++] = '0';
			huffmantree_print(t->left, prefix, size_prefix);
			size_prefix--;
		}

		if (t->right)
		{
			prefix[size_prefix++] = '1';
			huffmantree_print(t->right, prefix, size_prefix);
			size_prefix--;
		}

	}

	int main(void)
	{
		unsigned long frequencies[0xFF];
		char metin[] = "bu oylesine uzun, oylesine girift bir metin ki, muhakkak gereksiz bitlerini temizlemek gerekir.";
		char *pcTemp;
		int i;
		
		HUFFMANARRAY *arr = huffman_array_new();

		memset(&frequencies[0], 0, sizeof(frequencies));

		for (pcTemp = &metin[0]; *pcTemp != 0; pcTemp++)
		{
			frequencies[(int)*pcTemp]++;

		}

		for (i = 0; i < 255; i++)
		{
			if (frequencies[i] > 0)
			{
				huffman_array_add(arr, huffmantree_new(i, frequencies[i]));
			}
		}

		while (arr->size > 1)
		{
			huffman_array_sort(arr);
			HUFFMANTREE *t1 = huffman_array_pop(arr);
			HUFFMANTREE *t2 = huffman_array_pop(arr);
			HUFFMANTREE *t3 = calloc(1, sizeof(HUFFMANTREE));
			t3->left = t1;
			t3->right = t2;
			t3->freq = t1->freq + t2->freq;
			huffman_array_add(arr, t3);

		}

		char *buffer = malloc(256);
		huffmantree_print(arr->items[0], buffer, 0);

		return 0;
	}
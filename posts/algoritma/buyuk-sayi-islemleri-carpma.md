<!--
.. date: 2020-02-24 20:36
.. description: 
.. slug: buyuk-sayi-islemleri-carpma
.. title: Büyük Sayı Algoritmaları - Çarpma
.. tags: mathjax
-->

[Bir önceki yazıda](buyuk-sayi-islemleri-toplama-cikarma.html), n-haneli doğal sayılar üzerinde toplama
çıkarma algoritmalarından bahsetmiştik. Bu yazıda m-haneli doğal sayılar ile n-haneli doğal sayılar arasında
çarpma işlemi yapan bir algoritmayı inceleyeceğiz. Bu algoritmanın ön çalışması olarak, bir haneli iki
sayı çarparak, iki haneli sonuç döndüren bir fonksiyon yazacağız. 

```C
void bn_mul_n11(bn_digit_t *rl, bn_digit_t op1, bn_digit_t op2)
{
	bn_digit_t op1_h = (op1 >> (BN_DIGIT_BITS / 2));
	bn_digit_t op1_l = (op1 & BN_DIGIT_LOWMASK);
	bn_digit_t op2_h = (op2 >> (BN_DIGIT_BITS / 2));
	bn_digit_t op2_l = (op2 & BN_DIGIT_LOWMASK);

	bn_digit_t p1 = op1_l * op2_l;
	bn_digit_t p2 = op1_l * op2_h;
	bn_digit_t p3 = op1_h * op2_l;
	bn_digit_t p4 = op1_h * op2_h;

	p2 += (p1 >> (BN_DIGIT_BITS / 2));
	p2 += p3;
	if (p2 < p3) // carry
	{
		p4 += BN_DIGIT_HI;
	}
	
	rl[0] = (p2 << (BN_DIGIT_BITS / 2)) + (p1 & BN_DIGIT_LOWMASK);
	rl[1] = p4 + (p2 >> (BN_DIGIT_BITS / 2));
}
```

32 bit iki sayının çarpımı, 64 bite kadar sonuç verebileceği için, 32 bitlik
çarpanları, 16 bitlik parçalara bölüp, parçaları ikişerli olarak çarpıp,
elde ettiğimiz sonuçları farklı oranlarda kaydırarak toplayıp, 2 haneli bir
sonuç elde edebilir. Kaydırma oranlarıyla ilgili olarak, aşağıdaki tabloyu
inceleyebilirsiniz.

<pre>
64      48      32      16      0
+---------------+-------+-------+
|op1_h x op2_h  |       |       |
+-------+-------+-------+-------+
|       |op1_h x op2_l  |       |
+-------+---------------+-------+
|       |op1_l x op2_h  |       |
+-------+-------+-------+-------+
|               |op1_l x op2_l  |
+---------------+---------------+
</pre>

Bunun neden işe yaradığını anlamak için, 32 bit \\(u\\) ve \\(v\\) sayılarını çarptığımızı
varsayalım. \\(u_h\\) sayının 16 bitlik üst kısmını, \\(u_l\\) ise sayının 16 bitlik alt kısmını
temsil etsin.

<div>
$$
\begin{align}
u & = 2^{16} * u_h + u_l \\
v & = 2^{16} * v_h + v_l \\
u * v & = (2^{16} * u_h + u_l) * (2^{16} * v_h + v_l) \\
 & = 2^{32} * u_h * v_h + 2^{16} * u_h * v_l + 2^{16} * v_h * u_l + u_l * v_l \\
\end{align}
$$
</div>

32 bit değişkenlere bağlı kalarak çarpma işlemini yukarıdaki gibi yapabiliriz. Ancak, C derleyecileri
32 bit işlemcilerde 64 bit aritmetiği taklit ettiği için, işin kolayına da kaçabiliriz.

```C
void bn_mul_n11(bn_digit_t *rl, bn_digit_t op1, bn_digit_t op2)
{
	*((bn_long_digit_t *)rl) = ((bn_long_digit_t)op1) * ((bn_long_digit_t)op2);
}
```

Bu ikinci fonksiyon 32 bit işlemcilerde ilkini nazaran benzer bir performans verecektir. 64 bit
işlemcilerde ise daha iyi bir performans bekleyebiliriz. Ancak, 64 bit işlemcilerde, `bn_digit_t`'yi 64 bit
olarak ayarlarsanız, ikinci fonksiyonu kullanmak için 128 bit bir değişkene ihtiyacımız var. Bunu da
her derleyeci desteklemiyor.

1-hane x 1-hane çarpımı yaptıktan sonra, n-hane x 1-hane çarpımına geçebiliriz. Bir önceki yazıda egzersiz
olarak bıraktığım, n-haneli ve 1 haneli toplamı fonksiyonunu da burada tanımlıyorum.

```C
bn_digit_t bn_add_n1(bn_digit_t *result, const bn_digit_t *op1, bn_digit_t op2, bn_size_t n)
{
	bn_size_t i;
	result[0] = op1[0] + op2;
	bn_digit_t carry = result[0] < op2;

	for (i = 1; i < n; i++)
	{
		result[i] = op1[i] + carry;
		carry = (result[i] < carry);
	}

	return carry;
}

bn_digit_t bn_mul_n1(bn_digit_t *result, bn_digit_t *op1, bn_digit_t op2, bn_size_t n)
{
	bn_digit_t temp[2];
	bn_digit_t carry;
	bn_size_t i;

	for (i = 0, carry = 0; i < n; i++)
	{
		bn_mul_n11(temp, op1[i], op2);
		bn_add_n1(temp, temp, carry, 2); // bu carry döndüremez, döndürmemeli
		carry = temp[1];
		result[i] = temp[0];
	}

	return carry;
}
```

Burada `for` döngüsünün her bir adımında, `op1`'in bir hanesi ile, `op2`'yi
çarpıyoruz. Bu çarpım bize 2 haneli bir sonuç veriyor. Bu sonuca, bir önceki
döngüden devir aldığımız sayıyı ekliyoruz. Elde ettiğimiz sonucun küçük hanesini
sonuç olarak yazıp, büyük hanesini bir sonraki döngü adımına devrediyoruz. Aynı
algoritmanın, onluk tabanda 7381 ile 5 arasında uygulanmış halini aşağıdaki
gibi çalışacaktır.

<pre>
i = 0, carry = 0: 1 x 5 = 5, 5 + 0 = 5 -> Sonuç[0] = 5, carry = 0
i = 1, carry = 0: 8 x 5 = 40, 40 + 0 = 40 -> Sonuç[1] = 0, carry = 4
i = 2, carry = 4: 3 x 5 = 15, 15 + 4 = 19 -> Sonuç[2] = 9, carry = 1
i = 3, carry = 1: 7 x 5 = 35, 35 + 1 = 36 -> Sonuç[3] = 6, carry 3

Döngü Sonu: Sonuç[4] = 3
Döndüreceğimiz Değer: 36905

   7381
x     5
-- -- --
     05
    40
   15
+ 35
-- -- --
  36905
</pre>

Son algoritmaya geçmeden önce, yukarıdaki fonksiyonun farklı bir versiyonunu
yazalım. Bu fonksiyonun öncekinden farkı, çarpım sonucunu, `result` array'inde
önceden bulunan değerin üstüne ekliyor olması. 

```C
// result += op1 * op2
bn_digit_t bn_muladd_n1(bn_digit_t *result, bn_digit_t *op1, bn_digit_t op2, bn_size_t n)
{
	bn_digit_t temp[2];
	bn_digit_t carry;
	bn_size_t i;
	for (i = 0, carry = 0; i < n; i++)
	{
		bn_mul_n11(temp, op1[i], op2);
		bn_add_n1(temp, temp, carry, 2);
		carry = temp[1];
		result[i] += temp[0];
		carry += (result[i] < temp[0]);
	}
	return carry;
}
```

Şu ana kadar yazdığımız fonksiyonları kullanarak, m-haneli ve n-haneli sayilari
çarpan fonksiyona geçebiliriz.

```C
void bn_mul_n(bn_digit_t *result, bn_digit_t *op1, bn_size_t m, bn_digit_t *op2, bn_size_t n)
{
	bn_size_t i;
	result[m] = bn_mul_n1(result, op1, op2[0], m);

	for (i = 1; i < n; i++)
	{
		result++;
		op2++;

		result[m] = bn_muladd_n1(result, op1, op2[0], m);
	}
}
```

Bu fonksiyonda, önce `op2`'nin son hanesi ile, `op1`'i çarpıp, sonucu `result` array'ine yazıyoruz.
`for` döngüsünün her bir adımında, `op2` bir sonraki hanesini `op1` ile çarparak, `result`
array'inin bir sonraki hanesine ekliyoruz. 
<!--
.. date: 2020-02-23 18:28
.. description: 
.. slug: buyuk-sayi-islemleri-toplama-cikarma
.. title: Büyük Sayı Algoritmaları - Toplama / Çıkarma
.. tags: mathjax
-->

<style>
// http://felix11h.github.io/blog/mathjax-theorems
.theorem {
display: block;
font-style: italic;
}
.theorem:before {
content: "Teorem. ";
font-weight: bold;
font-style: normal;
}
.theorem[text]:before {
content: "Teorem (" attr(text) ") ";
}

</style>

Bu yazıda n-haneli iki doğal sayı üzerinde toplama/çıkarma işlemi yapararak,
n-haneli sonuç ve "elde" döndüren algoritmaları inceleyeceğiz. Bu algoritmalar
kağıt/kalem ile yaptığımız toplama çıkarma işlemleriyle oldukça benzer ve ilerleyen
yazılara konu olacak algoritmalara nazaran oldukça temel düzeyde. [Bir önceki yazıda](buyuk-sayi-islemleri-giris.html)
tanımlanan veri türlerini kullanacağımız için, önce o yazıyı okumanızı tavsiye ederim.

```C
bn_digit_t bn_add_n(bn_digit_t *result, const bn_digit_t *op1, const bn_digit_t *op2, bn_size_t n)
{
	bn_size_t i;
	bn_digit_t carry;
	for (i = 0, carry = 0; i < n; i++)
	{
		bn_digit_t a, b, r;

		a = op1[i];
		b = op2[i];
		r = a + carry;
		carry = (r < a);
		r += b;
		carry += (r < b);
		result[i] = r;
	}
	return carry;
}

```

Yukarıdaki fonksiyonda, `op1` ve `op2`, `n` haneli iki doğal sayıyı ifade ediyor. `result`
ise, `n` haneli sonucun yazılacağı hafıza alanının başlangıcına işaret ediyor. `i` değişkeni
standart bir döngü sayacı. `carry` ise, her toplama işlemi sonrası, bir üst haneye aktarılması
gereken "elde" değerini tutacak. Döngüye başladığımızda, toplayacağımız sayıların ilgili
hanelerini okuyoruz. Sayılardan bir tanesine, "elde" değerini ekliyoruz. Diğer sayıyı
da ekleyip, sonuç array'inin ilgili hanesine sonucu yazıyoruz.

İki sayının toplamı, sayı tabanını (\\(2^{32}\\)) aştığında, sonuç sadece düşük bitleri içerecektir. Bu
mod \\(2^{32}\\)'de toplama işlemi yapmaya eşdeğerdir. Onluk sayı tabanında düşünürsek, \\(7 + 8 \equiv 5 \mod 10\\)
sonucun birler basamağını verir. Aynı şekilde, C ile yaptığımız toplama işleminin sonucunda (\\(2^{32}\\))
tabanında toplama sonucunun birler basamağını elde ediyoruz. Üst haneye 1 eklememiz gerektiğini anlamak
için, topladığımız sayıları toplam ile karşılaştırabiliriz.

<div class="theorem" text='Tek Haneli Sayıların Toplamı'>

\(n\) tabanında tek haneli iki sayının toplamının sonucu iki haneli olduğunda, sonucun birler basamağı
iki sayıdan da küçüktür.
$$
(0 \leq a \leq b < n) \land (c = a + b \geq n) \implies (c \mod n < a) \land (c \mod n < b)
$$
</div>

Öncelikle, \\(0 \leq a \leq b < n\\) ve \\(c = a + b \geq n\\) ise, \\(c \mod n = a + b - n\\) olur.
Eğer \\(c \mod n \geq a\\) olsa idi, \\(a + b - n \geq a\\) olurdu. Buradan da, \\(b \geq n\\)
sonucunu elde ederiz. Ancak, \\(b < n\\) olduğunu bildiğimiz için, \\(c \mod n < a\\) olmak zorundadır.

Çıkarma algoritması oldukça benzer olsa da, birkaç nüans farkı var. Burada, üst haneye 1 vermek
yerine, üst haneden 1 almamız gerekiyor.

```C
bn_digit_t bn_sub_n(bn_digit_t *r, bn_digit_t *op1, bn_digit_t *op2, bn_size_t size)
{
	bn_digit_t carry;
	bn_size_t i;
	for (i = 0, carry = 0; i < size; i++)
	{
		bn_digit_t a = op1[i];
		bn_digit_t b = op2[i];
		b += carry;
		carry = (b < carry);
		carry += (a < b);
		r[i] = a - b;
	}

	return carry;
}
```

Döngüye başladığımızda, eğer bu haneden 1 eksiltmemiz gerekiyorsa, çıkana 1 ekliyoruz.
Çıkana 1 ekleme işlemi taşabileceği için, bunu kontrol etmemiz gerekiyor. Bir üst
haneden değer eksiltmemiz gerektiğini ise eksilen çıkandan küçük olduğunda anlıyoruz.
Son olarak, çıkarma işlemini yapıp, sonucun ilgili hanesine yazıyoruz.

İlerleyen yazılardaki algoritmalarda kullanmak üzere, n-haneli sayı ile 1 haneli sayı
arasında toplama çıkarma yapan, ve m-haneli sayı ile n-haneli (\\(m \geq n\\) olmak üzere)
sayılar arasında toplama çıkarma işlemi yapan fonksiyonlara ihtiyacımız olacak. Bunları egzersiz
olarak yazabilirsiniz, bir sonraki yazının girişinde bu fonksiyonları paylaşacağım. Egzersizleri
yaparken, sayıların başına 0 ekleyerek hane sayılarını eşitlemeden yapmaya çalışın.

Ek Kaynaklar
------------

 - Knuth D. Art of The Computer Programming Vol 2 Section 4.3.1
 - Wikipedia. [Integer overflow](https://en.wikipedia.org/wiki/Integer_overflow)
 - Wikipedia. [Modular Arithmetic](https://en.wikipedia.org/wiki/Modular_arithmetic)
 - x86 Instruction Set Reference [ADC](https://x86.puri.sm/html/file_module_x86_id_4.html)
 - x86 Instruction Set Reference [CLC](https://x86.puri.sm/html/file_module_x86_id_28.html)
 - x86 Instruction Set Reference [STC](https://x86.puri.sm/html/file_module_x86_id_302.html)
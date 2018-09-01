<!--
.. date: 2018/09/01 20:40:00
.. slug: euler-17
.. title: (Euler 17) Sayıların Harf Sayısı
.. description: Sayıları Yazıya dönüştürecek bir program yazımı
.. tags: mathjax
-->

(Problemin orjinali İngilizce kelimeler üzerine kurulu, ben çevirirken Türkçeleştirdim.)

1'den 5'e kadar olan sayılar yazıyla bir, iki, üç, dört ve beş olur ve toplamda 3 + 3 + 2 + 4 + 3 = 15 harften oluşur.

Eğer birden bine kadar (bin dahil) sayılar yazılırsa, kaç harf kullanılır.

(Not: Boşlukları saymayın. Örneğin, yüz yirmi üç 10 harften oluşur) <!-- TEASER_END -->

Problem bize, birden bine kadar olan sayıların, yazıyla kaç karakterden oluştuğunu soruyor. Eline
kağıt kalem alan biri, bu soruya birkaç dakika içerisinde doğru cevabı verebilir. Ama bizler programcı
olduğumuz için, hakimiyetimiz altında bulunan zavallı bilgisayarlara bu görevi devredebiliriz. Arife tarif
gerekmez ama, bilgisayarlara gerekiyor. O yüzden bir algoritmaya ihtiyacımız var.

Bazı sayıların kendine ait bir ismi varken, bazıları ise, diğer sayılarının isimlerinin yanyana gelmesinden
oluşuyor. Örneğin, 10 (on) sayısının kendine ait bir ismi varken, 11 (onbir) sayısı, on ve bir sayılarının
yanyana gelmesiyle adlandırılıyor. Kendine ait ismi olan sayıları bir sözlük veri yapısı içerisinde tutarsak,
diğer sayıları bunların birleşmesi ile elde edebiliriz.

    :::python
    sayi_kelime = {
        0: "sıfır",
        1: "bir",
        2: "iki",
        3: "üç",
        4: "dört",
        5: "beş",
        6: "altı",
        7: "yedi",
        8: "sekiz",
        9: "dokuz",
        10: "on",
        20: "yirmi",
        30: "otuz",
        40: "kırk",
        50: "elli",
        60: "altmış", # http://www.tdk.gov.tr/index.php?option=com_yanlis&view=yanlis&kelimez=59
        70: "yetmiş",
        80: "seksen",
        90: "doksan",
        100: "yüz",
        1000: "bin"
    }
    
Algoritmamız şu şekilde olacak;

 - Sayı binden büyükse, bine bölümünü yazıya dönüştür, "bin" ekle, kalanı yazıya dönüştür.
 - Sayı yüzden büyükse, sayıyı yüze böl, bölümünü sayıya dönüştür, "yüz" ekle, kalanı yazıya dönüştür.
 - Sayı ondan büyükse, sayıyı ona böl, bölümü onla çarp yazıya dönüştür, kalanı yazıya dönüştür
 - Sayı ondan küçükse, yazıya dönüştür
 
Uzatmadan kodlara geçelim;

    :::python
    def yazi(n):

        q,r = divmod(n, 1000)    
        if q > 1:
            return yazi(q) + sayi_yazi[1000] + yazi(r)
        if q == 1:
            return sayi_yazi[1000] + yazi(r)

        q,r = divmod(n, 100)
        if q > 1:
            return sayi_yazi[q] + sayi_yazi[100] + yazi(r)
        if q == 1:
            return sayi_yazi[100] + yazi(r)
            
        q, r = divmod(n, 10)
        if q > 0:
            return sayi_yazi[10 * q] + sayi_yazi[r]
    
    return sayi_yazi[n]
    
Fonksiyonu test edebiliriz;

    :::python
    print(len("".join(map(yazi, range(1,1001)))))
    
Buradan 15603 sonucunu alacağız. 

## Gelecek Problem

Aşağıdaki üçgenin üstünden başlayarak, aşağı satırdaki bitişik sayılar üzerinden ilerleyerek, tepeden aşağı en büyük toplam 23'dür.

<p style="text-align:center;font-family:'courier new';font-size:12pt;"><span style="color:#ff0000;"><b>3</b></span><br><span style="color:#ff0000;"><b>7</b></span> 4<br>
2 <span style="color:#ff0000;"><b>4</b></span> 6<br>
8 5 <span style="color:#ff0000;"><b>9</b></span> 3</p>

Yani, 3 + 7 + 4 + 9 = 23.

Aşağıdaki üçgende, tepeden aşağı en büyük toplamı bulunuz

<p style="text-align:center;font-family:'courier new';">75<br>
95 64<br>
17 47 82<br>
18 35 87 10<br>
20 04 82 47 65<br>
19 01 23 75 03 34<br>
88 02 77 73 07 63 67<br>
99 65 04 28 06 16 70 92<br>
41 41 26 56 83 40 80 70 33<br>
41 48 72 33 47 32 37 16 94 29<br>
53 71 44 65 25 43 91 52 97 51 14<br>
70 11 33 28 77 73 17 78 39 68 17 57<br>
91 71 52 38 17 14 91 43 58 50 27 29 48<br>
63 66 04 68 89 53 67 30 73 16 69 87 40 31<br>
04 62 98 27 23 09 70 98 73 93 38 53 60 04 23</p>


NOT: Sadece 16384 yol olduğundan, bu problemi tüm yolları deneyerek çözmek mümkün. Ancak, 67. problem, aynı sorunun 100 satırlısı; kaba kuvvetle çözülemez, ve zekice bir yöntem gerektiriyor
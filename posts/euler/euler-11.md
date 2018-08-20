<!--
.. date: 2018/08/20 21:59:00
.. slug: euler-11
.. title: (Euler 11) 11. Euler Problemi Çözümü
.. description: 20x20 dizilmiş sayıların içinde, yatay, dikey veya çapraz olarak ardışık 4 sayının çarpımı en fazla kaç olabilir?
.. tags: mathjax
-->

Aşağıdaki 20x20 şeklinde dizilmiş sayılardan, köşegen üzerinde bulunan 4 tanesi kırmızıyla işaretlenmiştir.

<p style="font-family:'courier new';text-align:center;font-size:10pt;">
08 02 22 97 38 15 00 40 00 75 04 05 07 78 52 12 50 77 91 08<br>
49 49 99 40 17 81 18 57 60 87 17 40 98 43 69 48 04 56 62 00<br>
81 49 31 73 55 79 14 29 93 71 40 67 53 88 30 03 49 13 36 65<br>
52 70 95 23 04 60 11 42 69 24 68 56 01 32 56 71 37 02 36 91<br>
22 31 16 71 51 67 63 89 41 92 36 54 22 40 40 28 66 33 13 80<br>
24 47 32 60 99 03 45 02 44 75 33 53 78 36 84 20 35 17 12 50<br>
32 98 81 28 64 23 67 10 <span style="color:#ff0000;"><b>26</b></span> 38 40 67 59 54 70 66 18 38 64 70<br>
67 26 20 68 02 62 12 20 95 <span style="color:#ff0000;"><b>63</b></span> 94 39 63 08 40 91 66 49 94 21<br>
24 55 58 05 66 73 99 26 97 17 <span style="color:#ff0000;"><b>78</b></span> 78 96 83 14 88 34 89 63 72<br>
21 36 23 09 75 00 76 44 20 45 35 <span style="color:#ff0000;"><b>14</b></span> 00 61 33 97 34 31 33 95<br>
78 17 53 28 22 75 31 67 15 94 03 80 04 62 16 14 09 53 56 92<br>
16 39 05 42 96 35 31 47 55 58 88 24 00 17 54 24 36 29 85 57<br>
86 56 00 48 35 71 89 07 05 44 44 37 44 60 21 58 51 54 17 58<br>
19 80 81 68 05 94 47 69 28 73 92 13 86 52 17 77 04 89 55 40<br>
04 52 08 83 97 35 99 16 07 97 57 32 16 26 26 79 33 27 98 66<br>
88 36 68 87 57 62 20 72 03 46 33 67 46 55 12 32 63 93 53 69<br>
04 42 16 73 38 25 39 11 24 94 72 18 08 46 29 32 40 62 76 36<br>
20 69 36 41 72 30 23 88 34 62 99 69 82 67 59 85 74 04 36 16<br>
20 73 35 29 78 31 90 01 74 31 49 71 48 86 81 16 23 57 05 54<br>
01 70 54 71 83 51 54 69 16 92 33 48 61 43 52 01 89 19 67 48<br></p>

Bu sayıların çarpımı 26 × 63 × 78 × 14 = 1788696 yapar.

Bu sayıların içerisinde, yatay, dikey veya çapraz olarak ardışık
4 sayının çarpımı en fazla kaçtır? <!-- TEASER_END -->

Bu problemin çözümü için, bütün olasıkları değerlendirip, içlerinden en büyüğünü seçmek dışında bir çözüm yolumuz yok. Sol üstten
başlayarak, herbir sayı için, 4 farklı yönde gruplar oluşturup, bunların çarpımını alacağız. Örneğin, en üst sırada, soldan dördüncü
sütundaki 97 sayısı için, bu grupları aşağıdaki gibi olacak.

<p style="font-family:'courier new';text-align:center;font-size:10pt;">
08 02 22 <span style="border: 1px solid black"><b>97</b></span> <span style="background-color: #0f0f0f; color: #ffffff"><b>38</b></span> <span style="background-color: #0f0f0f; color: #ffffff"><b>15</b></span> <span style="background-color: #0f0f0f; color: #ffffff"><b>00</b></span> 40 00 75 04 05 07 78 52 12 50 77 91 08<br>
49 49 <span style="background-color: #ff0000"><b>99</b></span> <span style="background-color: #00ff00"><b>40</b></span> <span style="background-color: #0000ff; color: #ffffff"><b>17</b></span> 81 18 57 60 87 17 40 98 43 69 48 04 56 62 00<br>
81 <span style="background-color: #ff0000"><b>49</b></span> 31 <span style="background-color: #00ff00"><b>73</b></span> 55 <span style="background-color: #0000ff; color: #ffffff"><b>79</b></span> 14 29 93 71 40 67 53 88 30 03 49 13 36 65<br>
<span style="background-color: #ff0000"><b>52</b></span> 70 95 <span style="background-color: #00ff00"><b>23</b></span> 04 60 <span style="background-color: #0000ff; color: #ffffff"><b>11</b></span> 42 69 24 68 56 01 32 56 71 37 02 36 91<br>
22 31 16 71 51 67 63 89 41 92 36 54 22 40 40 28 66 33 13 80<br>
24 47 32 60 99 03 45 02 44 75 33 53 78 36 84 20 35 17 12 50<br>
32 98 81 28 64 23 67 10 26 38 40 67 59 54 70 66 18 38 64 70<br>
67 26 20 68 02 62 12 20 95 63 94 39 63 08 40 91 66 49 94 21<br>
24 55 58 05 66 73 99 26 97 17 78 78 96 83 14 88 34 89 63 72<br>
21 36 23 09 75 00 76 44 20 45 35 14 00 61 33 97 34 31 33 95<br>
78 17 53 28 22 75 31 67 15 94 03 80 04 62 16 14 09 53 56 92<br>
16 39 05 42 96 35 31 47 55 58 88 24 00 17 54 24 36 29 85 57<br>
86 56 00 48 35 71 89 07 05 44 44 37 44 60 21 58 51 54 17 58<br>
19 80 81 68 05 94 47 69 28 73 92 13 86 52 17 77 04 89 55 40<br>
04 52 08 83 97 35 99 16 07 97 57 32 16 26 26 79 33 27 98 66<br>
88 36 68 87 57 62 20 72 03 46 33 67 46 55 12 32 63 93 53 69<br>
04 42 16 73 38 25 39 11 24 94 72 18 08 46 29 32 40 62 76 36<br>
20 69 36 41 72 30 23 88 34 62 99 69 82 67 59 85 74 04 36 16<br>
20 73 35 29 78 31 90 01 74 31 49 71 48 86 81 16 23 57 05 54<br>
01 70 54 71 83 51 54 69 16 92 33 48 61 43 52 01 89 19 67 48<br></p>

Sınıra yakın sayılar için, bu dörtlü grupların herbirini oluşturmak mümkün olmayacak. Örneğin, sol üst köşede bulunan 08 sayısı için, sol çapraz
grubunu oluşturmak mümkün değil. Tüm bu taramları ayrı ayrı kodlamak yerine, genel bir fonksiyon yazıp, tarama yolunu argüman olarak vererek
çalıştırabiliriz. Yaptığımız taramanın sınır dışına çıkıp çıkmadığını, döngünün içinde kontrol etmek yerine, döngüye başlamadan kontrol etmek
daha pratik bir yöntem olacaktır. 

    :::python
    from math import sqrt
    from operator import mul

    mul_list = lambda x: reduce(mul, x)

    def tara(matris, vektor):
        """
        Matris Koordinat Sistemi sol üstten başlayıp, sağ altta biter, 0 tabanlıdır
        
        (0,0)  (0,1) (0,2) ... (0, 19)
        (1,0)  (1,1) (1,2) ... (1, 19)
        .
        .
        .
        (19,0) (19,1) (19,2) ... (19, 19)
        
        Matrisi Python içersinde liste listesi olarak tanımlıyacağız.
        
        matris = [
            [8, 2, 22, 97, 38, 15, 0, 40, 0, 75, 4, 5, 7, 78, 52, 12, 50, 77, 91, 8],
            [...],
            [1, 70, 54, 71, 83, 51, 54, 69, 16, 92, 33, 48, 61, 43, 52, 1, 89, 19, 67, 48]
        ]
        
        Vektor (0,0) dan başlayan dörtlünün bitiş koordinatıdır. Blog yazısındaki örneğe göre
        yazılması gerekn vektörler
        
        (3, -3) (Kırmızı dörtlü)
        (3,  0) (Yeşil dörtlü)
        (3,  3) (Mavi dörtlü)
        (0,  3) (Siyah dörtlü)
        
        
        """
        
        "Matris satır ve sütun sayıları"
        n_rows = len(matris)
        n_cols = len(matris[0])
        
        "Tarayacağımız alan sınırları"
        p_row_begin = max(0, -1 * vektor[0])
        p_col_begin   = max(0, -1 * vektor[1])
        p_row_end = min(n_rows, n_rows - 1 * vektor[0])
        p_col_end = min(n_cols, n_cols - 1 * vektor[1])
        
        "Gruplamaya başladıktan sonra, elemanları bulmak için"
        "atacağımız adımların satır ve sütün olarak değerleri"
        v_len = int(sqrt(vektor[0]**2 + vektor[1] ** 2))+1
        row_step = vektor[0] / v_len
        col_step = vektor[1] / v_len
        
        "Bulduğumuz en büyük çarpım ve grup"
        max_product = 0
        max_list = []
        
        "İlk 2 döngü gruplamaya başlayacağımız sayının koordinatları için"
        for p_row in range(p_row_begin, p_row_end):
            for p_col in range(p_col_begin, p_col_end):
            
                "Gruplamayı burada yapıyoruz."
                group = []
                i, k = (0,0)
                for _ in range(v_len):
                    group.append(matris[p_row+i][p_col+k])
                    i += row_step
                    k += col_step
                    
                "Gruplama bitti, çarpım eğer daha önce bulduklarımızdan fazla ise"
                "yeni maksimum olarak bu grubu alalım"
                m = mul_list(group)
                if m > max_product:
                    max_product = m
                    max_list = group
                    
        return (max_product, max_list)

İstediğimiz yönde tarama yapan fonksiyonumuzu yazdığımıza göre, 4 farklı yönde taramalarımızı yapıp, elde ettiğimiz sonuçlar içerisinde en iyisini
bulabiliriz.

    :::python
    reduce(lambda x,y: x if y[0] < x[0] else y,
              map(lambda d: tara(matris, d), (
                  (3, -3), (3, 0), (3, 3), (0, 3)
              ))
          )
          
Bu şekilde genel bir çözüm bulduğumuzda, problemin diğer varyasyonlarını da kolaylıkla çözebiliriz. Örneğin, çarpımı en büyük olan beşli
grubu şu şekilde bulabiliriz.

    :::python
    reduce(lambda x,y: x if y[0] < x[0] else y,
              map(lambda d: tara(matris, d), (
                  (4, -4), (4, 0), (4, 4), (0, 4)
              ))
          )

Ya da, eğer sadece yatay ve dikey dörtlüleri istiyorsak, şöyle birşey yapabiliriz.

    :::python
    reduce(lambda x,y: x if y[0] < x[0] else y,
              map(lambda d: tara(matris, d), (
                (3, 0), (0, 3)
              ))
          )
          
### Bonus (multiprocessing)

Burada çok lüzumlu olmasa da, buna benzer problemlerde problemin çözümü için gerekli işi işlemciler veya server'lar arasında dağıtmak isteyebilirsiniz.
Yukarıda çözdüğümüz Euler Problemi, Map-Reduce mantığıyla çözmek için uygun bir problem. Map-Reduce yönteminde, önce problem belirli alt problemlere
ayrılıp, çözülmesi için ilgili işlemci/server tarafına gönderiliyor (Map kısmı burası), daha sonra elde edilen kısmi çözümler tek bir çözüme
indirgeniyor (Reduce kısmı burası). Ben yukarıdaki çözümü özellikle buna uygun olması için yazdım. Her bir tarama yönünü ayrı bir işlemde
tarayıp, sonuçları ana işlem içererisinde birleştireceğiz.

    :::python
    # -*- coding: utf8 -*-
    from math import sqrt
    from operator import mul

    mul_list = lambda x: reduce(mul, x)

    matris_str = """08 02 22 97 38 15 00 40 00 75 04 05 07 78 52 12 50 77 91 08
    49 49 99 40 17 81 18 57 60 87 17 40 98 43 69 48 04 56 62 00
    81 49 31 73 55 79 14 29 93 71 40 67 53 88 30 03 49 13 36 65
    52 70 95 23 04 60 11 42 69 24 68 56 01 32 56 71 37 02 36 91
    22 31 16 71 51 67 63 89 41 92 36 54 22 40 40 28 66 33 13 80
    24 47 32 60 99 03 45 02 44 75 33 53 78 36 84 20 35 17 12 50
    32 98 81 28 64 23 67 10 26 38 40 67 59 54 70 66 18 38 64 70
    67 26 20 68 02 62 12 20 95 63 94 39 63 08 40 91 66 49 94 21
    24 55 58 05 66 73 99 26 97 17 78 78 96 83 14 88 34 89 63 72
    21 36 23 09 75 00 76 44 20 45 35 14 00 61 33 97 34 31 33 95
    78 17 53 28 22 75 31 67 15 94 03 80 04 62 16 14 09 53 56 92
    16 39 05 42 96 35 31 47 55 58 88 24 00 17 54 24 36 29 85 57
    86 56 00 48 35 71 89 07 05 44 44 37 44 60 21 58 51 54 17 58
    19 80 81 68 05 94 47 69 28 73 92 13 86 52 17 77 04 89 55 40
    04 52 08 83 97 35 99 16 07 97 57 32 16 26 26 79 33 27 98 66
    88 36 68 87 57 62 20 72 03 46 33 67 46 55 12 32 63 93 53 69
    04 42 16 73 38 25 39 11 24 94 72 18 08 46 29 32 40 62 76 36
    20 69 36 41 72 30 23 88 34 62 99 69 82 67 59 85 74 04 36 16
    20 73 35 29 78 31 90 01 74 31 49 71 48 86 81 16 23 57 05 54
    01 70 54 71 83 51 54 69 16 92 33 48 61 43 52 01 89 19 67 48"""

    matris = [
        [int(n) for n in row.split(" ")] for row in matris_str.split("\n")
    ]

    def tara(matris, vektor):
        """
        Matris Koordinat Sistemi sol üstten başlayıp, sağ altta biter, 0 tabanlıdır
        
        (0,0)  (0,1) (0,2) ... (0, 19)
        (1,0)  (1,1) (1,2) ... (1, 19)
        .
        .
        .
        (19,0) (19,1) (19,2) ... (19, 19)
        
        Matrisi Python içersinde liste listesi olarak tanımlıyacağız.

        
        matris = [
            [8, 2, 22, 97, 38, 15, 0, 40, 0, 75, 4, 5, 7, 78, 52, 12, 50, 77, 91, 8],
            [...],
            [1, 70, 54, 71, 83, 51, 54, 69, 16, 92, 33, 48, 61, 43, 52, 1, 89, 19, 67, 48]
        ]
        
        Vektor (0,0) dan başlayan dörtlünün bitiş koordinatıdır. Blog yazısındaki örneğe göre
        yazılması gerekn vektörler
        
        (3, -3) (Kırmızı dörtlü)
        (3,  0) (Yeşil dörtlü)
        (3,  3) (Mavi dörtlü)
        (0,  3) (Siyah dörtlü)
        
        
        """
        x,y = vektor[0], vektor[1]
        
        "Matris satır ve sütun sayıları"
        n_rows = len(matris)
        n_cols = len(matris[0])
        
        "Tarayacağımız alan sınırları"
        p_row_begin = max(0, -1 * x)
        p_col_begin   = max(0, -1 * y)
        p_row_end = min(n_rows, n_rows - 1 * x)
        p_col_end = min(n_cols, n_cols - 1 * y)
        
        "Gruplamaya başladıktan sonra, elemanları bulmak için"
        "atacağımız adımların sayısı ve yönü"
        v_len = max(abs(x), abs(y))
        row_step = max(-1, min(1, x))
        col_step = max(-1, min(1, y))
        
        "Bulduğumuz en büyük çarpım ve grup"
        max_product = 0
        max_list = []
        
        "İlk 2 döngü gruplamaya başlayacağımız sayının koordinatları için"
        for p_row in range(p_row_begin, p_row_end):
            for p_col in range(p_col_begin, p_col_end):
                
                "Gruplamayı burada yapıyoruz."
                group = []
                i, k = (0,0)
                for _ in range(v_len+1):
                    group.append(matris[p_row+i][p_col+k])
                    i += row_step
                    k += col_step
                    
                "Gruplama bitti, çarpım eğer daha önce bulduklarımızdan fazla ise"
                "yeni maksimum olarak bu grubu alalım"
                m = mul_list(group)
                if m > max_product:
                    max_product = m
                    max_list = group
                    
        return (max_product, max_list)
        
    if __name__ == "__main__":
        
        from multiprocessing import Pool
        from functools import partial
        
        "4 işlemden oluşan bir işlem havuzu"
        p = Pool(4)
        
        "Map için kullanılacak fonksiyon tek bir argüman almak zorunda"
        "bu nedenle, matris argümanını önceden sabitliyoruz"
        matris_tara = partial(tara, matris)
        
        "Matris tarama işlerini alt işlemlere dağıtıyoruz"
        alt_cozumler = p.map(matris_tara, [(3, -3), (3, 0), (3, 3), (0, 3)])
        
        "Alt çözümleri, tek bir çözüme dönüştirelim"
        cozum = reduce(lambda x,y: y if y[0] > x[0] else x, alt_cozumler)
        
        "Çözümü yazdıralım"
        print(cozum)

Bu kadar küçük bir problem için, multiprocessing modülünü kullanmanın astarı yüzüden pahalıya gelecektir. Ancak, benzer nitelikte çok daha büyük
problemlerde kullanılabilecek böyle de birşey var.

## Gelecek Problem

Üçgen sayılar sayı dizisi, doğal sayılar eklenerek oluşturulur. Örneğin, 7. üçgen sayı 1 + 2 + 3 + 4 + 5 + 6 + 7 = 28 olur.
İlk 10 terim şu şekildedir.

1, 3, 6, 10, 15, 21, 28, 36, 45, 55, ...

İlk 7 üçgen sayının bölenlerine bakalım;

<pre>
 1: 1
 3: 1,3
 6: 1,2,3,6
10: 1,2,5,10
15: 1,3,5,15
21: 1,3,7,21
28: 1,2,4,7,14,28
</pre>

5'den fazla böleni olan ilk üçgen sayının 28 olduğunu görüyoruz.

500'den fazla böleni olan ilk üçgen sayı kaçtır?
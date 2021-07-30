<!--
.. title: (Euler 16) Büyük Üslü Sayının Haneleri Toplamı
.. slug: euler-16
.. date: 2018/08/26 19:47:00
.. tags: 
.. description: 2'nin 
.. has_math: yes
-->

\\(2^{15} = 32768\\) ve rakamları toplamı \\(3 + 2 + 7 + 6 + 8 = 26\\).

\\(2^{1000}\\) sayısının rakamları toplamı kaçtır? <!--TEASER_END-->


[13. Euler Problemi Çözümünde](/euler/euler-13.html) olduğu gibi, bu sorunun da Python veya BigInteger kütüphanesi
kullanan herhangi bir dilde çözmenin enteresan bir tarafı yok. `sum(int(x) for x in str(2**1000))` yazmanın bir esprisi yok.
16. Euler Problemi çözümünü tekrar C dilinde yapacağım. Kendi mini `bigint_t` türümü tanımlayarak başlıyorum.

    :::c
    #define LIMB_MOD 1000000000
    #define LIMB_COUNT 250

    /* secilen veri tipi 2xLIMB_MOD sayisini 
     * alabilecek kadar buyuk olmali
     */
    typedef uint32_t limb_t; 
    typedef limb_t bigint_t[LIMB_COUNT];
    
Standart bir BigInteger veri türü için dinamik array kullanılsa da, ben kodlaması daha basit
olacağından sabit uzunluklu bir array kullandım. `uint32_t` türündeki her bir
elemanı onluk tabanda 9 haneli bir sayı olarak düşüneceğim.
Her bir eleman onluk sistemde 9 hane tutacağı için, 9x250 = 2250 haneli sayılara kadar işlem
yapabileceğiz. \\(2^n\\) sayısının onluk tabanda hane sayısını tahmin etmek için, \\( n * 0.3 \\) formülünü
kullanabiliriz. Dolayısıyla, tahmini olarak \\(2^{1000}\\) sayısı 300 haneli bir rakam olacak.
2250 hane fazlasıyla yeterli olacaktır.

Devam etmeden önce, LIMB nedir, ondan bahsedeyim. [GMP](https://gmplib.org/) kütüphanesinde, büyük
sayıların her bir parçası için LIMB (tr. uzuv) ismini kullanmışlar. Terminolojiyi oradan aldım.
Eğer her bir `limb` için 64 bit kullanmayı tercih ederseniz, `limb_t`'yi `uint64_t` ve `LIMB_MOD`
sabitini `1000000000000000000` olarak tanımlayabilirsiniz. Bu durumda, her bir limb onluk tabanda 18 hane
yerine geçebilir.


    :::c
    void bigint_set_uc(bigint_t n, limb_t n2)
    {
        memset(n, 0, sizeof(bigint_t));
        div_t d = div(n2, LIMB_MOD);
        n[0] = d.rem;
        n[1] = d.quot;
    }
    
Bunu `bigint_t` değerine ilk atamayı yapmak için kullanıyorum. Burada çok ilginç birşey yok.

    :::c
    void bigint_twice(bigint_t n)
    {
        int i;
        limb_t carry = 0;

        div_t d;

        for(i = 0; i < LIMB_COUNT; i++)
        {
            limb_t tmp = n[i];
            tmp = (2*tmp) + carry;
            div_t d = div(tmp, LIMB_MOD);
            n[i] = d.rem;
            carry = d.quot;
        }

        if(carry > 0)
        {
            // toplam bigint_t'yi aştı
            fprintf(stderr, "!!!!!!OVERFLOW!!!!!!!");
            exit(-1);
        }
    }

Üs alma işlemini tekrar eden çarpma işlemi olarak düşünürsek, büyük sayılarda çarpma işlemi yapmak
için bir fonksiyona ihtiyacımız var. Genel bir fonksiyon yazmak yerine, verilen büyük sayıyı
ikiye katlayan bir fonksiyon yazdım. \\(2^{1000}\\) sayısını hesaplamak için, bu yeterli olacaktır. Sayıyı
ikiyle çarpmak için, kendisiyle toplama işlemi yapıyorum. Basamak taşıma mantığı, [13. Euler Çözümünde](/euler/euler-13.html)
yaptığımla aynı. 

    :::c
    void bigint_print(bigint_t n)
    {
        int i = LIMB_COUNT;
        
        // skip leading zeros
        while(i--)
        {
            if(n[i] != 0)
            {
                printf("%u", n[i]);
                break;
            }
               
        }

        while(i--)
        {
            printf("%09u", n[i]);
        }

        printf("\n");
    }
    
Sayıyı Little-Endian (küçük haneler array'in başında) olarak düşündüğüm için,
yazdırma işlemini sondan başa doğru yapmak gerekiyor. Sayının başındaki sıfırları
yazdırmamak için, iki ayrı döngü kullanmam gerekti.

    :::c
    main(int argc, char const *argv[])
    {
        int i;
        bigint_t n;
        bigint_set_uc(n, 1);

        for(i = 0; i < 1000; i++)
        {
            bigint_twice(n);
            
        }
        bigint_print(n);
        return 0;
    }

Programı denemeye hazırız. Büyük sayıya 1 değerini atayıp, 1000 defa ikiyle çarparsak, istediğimiz sayıyı elde etmiş oluyoruz.

    10715086071862673209484250490600018105614048117055
    33607443750388370351051124936122493198378815695858
    12759467291755314682518714528569231404359845775746
    98574803934567774824230985421074605062371141877954
    18215304647498358194126739876755916554394607706291
    45711964776865421676604298316526243868372056680693
    76
    
Tabi ki, soru bize \\(2^{1000}\\) sayısını değil, hanelerinin toplamını soruyor. Onun için de, ayrı bir fonksiyon yazabiliriz.

    :::c
    unsigned int bigint_sumdigits(bigint_t n)
    {
        int sum = 0;
        int i;

        for(i = 0; i < LIMB_COUNT; i++)
        {
            limb_t tmp = n[i];
            while(tmp)
            {
                sum = sum + (tmp % 10);
                tmp = tmp / 10;
            }

        }

        return sum;
    }
    
Kodların tümü şu şekilde;

    :::c
    #include <stdlib.h>
    #include <stdio.h>
    #include <string.h> /* memset */
    #include <stdint.h> /* uint32_t */

    #define LIMB_MOD 1000000000
    #define LIMB_COUNT 250

    /* secilen veri tipi 2xLIMB_MOD sayisini 
     * alabilecek kadar buyuk olmali
     */
    typedef uint32_t limb_t; 
    typedef limb_t bigint_t[LIMB_COUNT];

    void bigint_set_uc(bigint_t n, limb_t n2)
    {
        memset(n, 0, sizeof(bigint_t));
        div_t d = div(n2, LIMB_MOD);
        n[0] = d.rem;
        n[1] = d.quot;
    }

    void bigint_twice(bigint_t n)
    {
        int i;
        limb_t carry = 0;

        div_t d;

        for(i = 0; i < LIMB_COUNT; i++)
        {
            limb_t tmp = n[i];
            tmp = (2*tmp) + carry;
            div_t d = div(tmp, LIMB_MOD);
            n[i] = d.rem;
            carry = d.quot;
        }

        if(carry > 0)
        {
            // toplam bigint_t'yi aştı
            fprintf(stderr, "!!!!!!OVERFLOW!!!!!!!");
            exit(-1);
        }
    }

    unsigned int bigint_sumdigits(bigint_t n)
    {
        int sum = 0;
        int i;

        for(i = 0; i < LIMB_COUNT; i++)
        {
            limb_t tmp = n[i];
            while(tmp)
            {
                sum = sum + (tmp % 10);
                tmp = tmp / 10;
            }

        }

        return sum;
    }

    // bigint_t is little-endian
    void bigint_print(bigint_t n)
    {
        int i = LIMB_COUNT;
        
        // skip leading zeros
        while(i--)
        {
            if(n[i] != 0)
            {
                printf("%u", n[i]);
                break;
            }
               
        }

        while(i--)
        {
            printf("%09u", n[i]);
        }

        printf("\n");
    }

    main(int argc, char const *argv[])
    {
        int i;
        bigint_t n;
        bigint_set_uc(n, 1);

        for(i = 0; i < 1000; i++)
        {
            bigint_twice(n);
            
        }
        bigint_print(n);
        printf("Haneleri Toplami: %u\n", bigint_sumdigits(n));
        return 0;
    }

Eğer onluk haneleri hiç işin içine katmazsak, \\(2^{1000}\\) sayısını hesaplamak çok daha kolay olur. İkilik tabanda
sayıyı ikiye katlamak için, bitleri sola kaydırmak yeterli. Dolayısıyla, 1001. biti 1 olarak değiştirirsek, \\(2^{1000}\\)
sayısını hesaplamış olacağız.
Ancak, sayıyı onluk hanelere çevirmek için, parça parça bölüm ve kalan hesabı yapmamız imkansız
hale gelecek. Bu nedenle, `bigint_t` üzerinde, bölme ve kalan alma işlemi tanımlamamız gerekiyor. Bölme işlemini, tekrar
eden çıkarma işlemi gibi tanımlayabilecek olsak da, bu şekilde \\(2^{1000}\\) sayısını bir kere bile 10'a bölemeyiz.
(Bing-Bang ile bölmeye başlamış olsak, hala program çalışıyor olurdu).
O yüzden, daha akıllı bir bölme işlemine ihtiyacımız olacak. Boş vakitlerimde, üzerinde 4 işlem yapılabilecek bir
BigInteger kütüphanesi yazmayı düşünüyorum. Eğer tamamlayabilirsem, onu da ayrı bir yazıya konu edeceğim.

## Gelecek Problem

(Problemin orjinali İngilizce kelimeler üzerine kurulu, ben çevirirken Türkçeleştirdim.)

1'den 5'e kadar olan sayılar yazıyla bir, iki, üç, dört ve beş olur ve toplamda 3 + 3 + 2 + 4 + 3 = 15 harften oluşur.

Eğer birden bine kadar (bin dahil) sayılar yazılırsa, kaç harf kullanılır.

(Not: Boşlukları saymayın. Örneğin, yüz yirmi üç 10 harften oluşur)

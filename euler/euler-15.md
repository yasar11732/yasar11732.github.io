<!--
.. date: 2018/08/24 17:55:00
.. slug: euler-15
.. title: (Euler 15) Izgara Üzerindeki Yollar
.. description: 20x20 ızgarada, köşeden köşeye kaç farklı yoldan gidilebilir?
.. tags: mathjax
-->

2x2 ızgaranın sol üst köşesinden başlayarak, ve sadece sağa veya aşağıya hareket ederek, sağ alt köşeye tam olarak 6 yol vardır.

<div style="text-align: center">
<img src="data:image/gif;base64,R0lGODlh0ACXAMQAAAAAALXf/7fg/7zi/8Tl/8jn/8fo/8zp/9Ts/9nv/93x/+Pz/+v2/+34//P6/////wAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAP///yH5BAEAAB8AIf4cVWxlYWQgR0lGIFNtYXJ0U2F2ZXIgVmVyIDIuMAAsAAAAANAAlwAABf/gJ45kaZ5oqq7sB7xwLM9ya98ore8v3vLAoHDmyw2DxSTriFSemNAowEmSWoHU6nVL03K/sawLPHWWxeSzUp0mo91msSidZaPrsLs5H5eri2FUdnV4PYR7hmtyLoJ8fXN6iH9JkziBin6NiZiQh5KRlI6Ui5U3l5yMnmuiqICsPqWAmrE2g4KFtLWzt5mfvJ2/q5utsK+WpLvBuT+4oK7DsMi+j6nBodCy06O9wssrttTX3t/JxOamxscj4yrsRtjR2tnOxfCmVfT17jnl2/no9nSt+wdw35N+81Q9M1gC3LmCBH+kExhxyUSK1cItrPjt4hJp3VQxbNhMoT5rGi3/efw40ORJlxBT+hMnkmPHgBg3ykyok9pIfAhn9hS6UyJOlsCKGv3ZMqTSe/ISMk1KE2atle1AVvVpsx1WclHVdX031SHRlyhVgtE6dObUjFufel3LLa5bumH1tYlCCg7XN3jlptg79gmdpmljJr56ePHSmoVNnHoI1alji0fBUqWM+a3noDzRonoLVzRnZnnF2pVat+3ZeJYFk4Vs9XHtnKZfMy4L9LYXJqpPr+NbeTXs0roNAy8ufPhy3Gp5I5Y95sjx5nOeQ1c8unXnJsyTKxdyPfdx0vuslw99E3z46LQvj+fBfn17+vZ3x6eeHUv94EvtIF57+2H3mw4DIhUd/4L/2faXb/MRkaBmC0rYYGcFTiiZgBoO1o2F+TnYXWTOgRjidt9NBiB8yni3Ww0G8iMOjB1uOExmiKEnyVcyyjeYiScS+BtGOn6IY4/8HXjkQfIAKVlvPv7II5IxNqRikHP9wSCSRX4IIYULSRdbdV0wuVmNNpL4pCZqlmglflB2KUybUF5DJ5lv+peUnKG4iKVXfr5oxZ57beFHoYMChigUizTq6KOQRnrfFZJWaumlmKYoRaacduopptp9KuqopIbJYamopqqqjaeu6uqro8IJ66y0glpmrbjmCqmTuvbqq2u/BiusRcMWa+yxyCar7LLMNuvss9BGK+201FZr7f+12Gar7bbcduvtt+CGK+645JZr7rnopqvuuuy2y+qijOICr3qzzKvelSv+mWWUWZVUJZP4vqevlEx95i+aAE9pZpKs8uvhwRcKFDCKArP4L0kQD/zwxKg5PBvDGINWsTocK3jxkCDXadzIUJUMJsJ5erzwmBrL6HK/Mjec8nQrU9yywmvmHPPOZ5rHssRAh0w0nkt7ljTP29z8sNAonwy10T4jveTMMFfd9dUWf92S1FSKzbTVRYcdMWpkc722kGgjh3XHvLQddNNPp300hkunYrfScf8N9t5wm+133npnzXfgilINlOCDK1742zinRncfkCd+ec+bU06w42MjLnf/vmrXfDfNpJMsusEiS1456oSDlfnosX/edON9lzE765abbHbmRe5+Z38FD3+24brbG2+9X4B+vOcbKx/qjM3jHRjm0i9PffZb9q7ppmRy756pXDgvfIbQD+048LjfHrnr493JfsamK83n3PDrHPjqoNxfevpeA6D6GPe+znHHavNrXf4W5j+y0MuA+rGemB7kMOIsMID1w2AGcxSoCOnpgm6S4Jcq10CCjc93/6vdx9ynOQg6UFYgJJ75+Ie+mg1BgDIUoflUhiby4PB5G8whC2mnQuJ1r4gaROIAf8dDAH4wdYv7HQ1b1CYYKlGIUtza6dzSwSzR6IcJ9N7LWFPFvyNCsXBLcpoWATcG1ZRQU+sTxc3UOEEskrCLXlxjAW1nxGXQ0SS8ihMevTjC+JVoYn9EiRkFKb/zxcaKLZxcaCCZkTcapZGbOGEiNaLJJgZRdEREow8juS9FjrKSgwQUJikVyu+JzxBseCUl9SJLUNZyluW63vZuqUdtVU9evOylL1nZqGAKM1w3DFYy3WXCRebqlMz04Oxihcto9hGUpGqVNZtJmlLdapuTWlYgwblEZE1zXceEVTrJyc52MisEADs=" alt="" />
</div>

20x20 ızgarada bu şekilde kaç adet yol vardır? <!-- TEASER_END -->


    :::python
    from math import factorial as f
    print(f(40)/f(20)**2)


Problemin çözümü bu kadar basit olsa da, çözüme ulaşmak o kadar da kolay olmadı. Her ne kadar sırasıyla tüm yolları
tarayıp saymak en kolay yöntem gibi görünse de, 20X20 bir ızgarada bu yöntem çok uzun sürecektir. Rivayet odur ki,
ikinci dünya savaşı yıllarında başlatılan bir program, bugün hala 20X20 ızgarada gidilebilecek yolları hesaplıyormuş.
(Öyle bir rivayet yok, ben uydurdum.) Ancak, probleme doğru açıdan bakınca, çok daha kolay bir yöntem kendini belli
ediyor. Bu soruyu, doğru cevabı etkilemeyecek bir şekilde, permüstasyon sorusuna dönüştürebiliriz.

Bu problemi permüstasyon problemine dönüştürebilmek için şuna dikkat etmek gerekiyor; 2X2 bir ızgarada sol üst köşeden
sağ alt köşeye gidebilmek için, tam iki kere sağa ve tam iki kere aşağıya doğru hareket etmeniz gerekiyor. Seçilebilecek
yollar arasındaki tek fark, aşağı ve sağa doğru hareketlerin hangi sırayla yapıldığı. Sağa atılacak adımları S,
aşağıya atılacak adımları ise A ile ifade edersek, 2X2 ızgarada seçilebilecek 6 farklı yol şunlardır; "SSAA", "SASA", "SAAS",
"ASSA", "ASAS", "AASS". Dolayısıyla, `{A, A, S, S}` kaç farklı şekilde dizilebilir sorusunua cevap
verdiğimizde, 2X2 ızgarada sol üst köşeden sağ alt köşeye kaç farklı yoldan gidilebilir sorusuna da cevap vermiş oluyoruz.
[Tekrarlı permüstasyon](https://www.google.com.tr/search?q=tekrarlı+permütasyon) formülü ile \\(\frac{4!}{2! \cdot 2!} = 6\\)
olarak sonucu teyit edebiliriz. Aynı yöntemle, \\(m \times n\\) bir ızgarada, bir köşeden karşı köşeye gitmek için seçilebilecek
yol sayısını aşağıdaki Python fonksiyonu ile hesaplayabiliriz.

    :::python
    from math import factorial as f
    def lattice(m, n):
        return f(m+n) / (f(m) * f(n))
        

Bu problemi çözmek için [Pascal Üçgeni](https://www.google.com.tr/search?q=pascal+üçgeni) de kullanabiliriz. Bu yöntemi
[internette rastladığım bir blog yazısında](http://blog.functionalfun.net/2008/07/project-euler-problem-15-city-grids-and.html)
gördüm. Ana fikri anlamak için,  3X3 ızgarada herhangi bir köşeden, sağ alt köşeye gitmek için kaç farklı yoldan geçebileceğimize bir
bakalım.

<style>
img[alt=g5028]
{
    width: 250px;
    heigth: 250px;
    diplay: inline-block;
    margin: 5px;
}
</style>

![g5028](/images/g5028.png)

Eğer ızgaranın en sağ hizasındaysanız, tek seçeneğiniz aşağıya doğru devam etmek. Aynı şekilde, eğer ızgaranın el altındaysanız, tek
seçeneğiniz sağa doğru devam etmek. Bu nedenle, ızgaranın sağ ve alt hizasındaki köşelerde 1 yazılı. Eğer üzerinde 2 yazılı köşedeyseniz,
sona ulaşmak için 2 farklı yol tercih edebilirsiniz. Ya aşağıdan sağa doğru, ya da sağdan aşağı doğru gidebilirsiniz. Eğer alttan ikinci
sırada, üzerinde 3 yazan köşeye bakarsanız, işler ilginçleşmeye başlıyor. Izgaranın bu köşesinden sağa doğru gidilirse, sona ulaşmak
için iki farklı yol seçilebilir. Eğer aşağı doğru gidilirse, sonuca tek bir yoldan ulaşılabilir. Yani, sağa gittikten sonraki 2 seçenek
ve aşağı gittikten sonraki tek seçenekle birlikte, toplam 3 seçeneğimiz olacak. Aynı şekilde, alttan ikinci sıradaki, üzerinde 4
yazılı köşede, ya aşağıya gitmeyi ya da sağdaki 3 seçenekten birini tercih edebiliriz. Bu durumda toplam 4 seçeneğimiz olacak. Yani,
herhangi bir köşedeki toplam seçenek sayımız, sağdaki ve alttaki köşelerin seçenek sayısının toplamı olacak. Eğer yukarıdaki resmi, sağ alt
köşe üste gelecek şekilde döndürürseniz, bir Pascal Üçgeni elde ettiğimizi göreceksiniz.

Orjinal problemi Pascal üçgeni kullanarak çözmek için, istediğimiz sonucu üçgenin neresinde bulacağımızı tespit etmemiz gerekiyor. Adet olduğu
üzere saymaya sıfırdan başlarsak, 1X1 ızgara için çözüm Pascal Üçgenin ikinci satır, birinci sütununda (2,1), 2X2 için çözümü (4,2) koordinatında bulabilirz.
Dolayısıyla, Pascal Üçgeni'nde (40,20) deki değeri bulduğumuzda, soruyu da çözmüş olacağız. Pascal üçgenindeki herhangi bir noktayı bulmak
için bir formül olsa da, önce döngü ile yapalım.

    :::python
    def pascal(r,c, cache={(0,0): 1}):

        if (r,c) in cache:
            return cache[(r,c)]

        if c < 0:
            return 0
        if c > r:
            return 0
        
        cache[(r,c)] = pascal(r-1, c-1) + pascal(r-1,c)
        return cache[(r,c)]


    print(pascal(2,1))
    print(pascal(4,2))
    print(pascal(6,3))
    print(pascal(40, 20))
    
Yukarıdaki gibi bir çözüm de bir hayli hızlı sonuç veriyor. `cache` isimli sözlüğe neden ihtiyacımız olduğunu anlamadıysanız, [(Euler 2) Çift Fibonacci Sayıları](/euler/euler-2.html)
yazısındaki, "Bonus: Özyinelemeli versiyon, sorunları ve çözümleri" başlığı altındaki bölümü okumanızı tavsiye ederim.

Pascal üçgeni üzerinde aradığımız değerin bulunduğu satıra \\(r\\), sütuna da \\(c\\) dersek, istediğimiz değeri \\(\frac{r!}{c!(r-c)!}\\) formülü
ile bulabiliriz. Formül bir yerden tanıdık geliyor. Tekrarlı permüstasyon formülü bu. Bu soruyu çözmeden önce, Pascal Üçgeni ile belki 20 yıldır
muhatap olmamıştım. Binom açılımı için kullanıldığını biliyordum ama, kombinasyon ile ilişkisini yeni öğrendim. Biraz dikkat edince, binom
açılımdaki katsayıların kombinasyon hesabıyla tespit edilmesi çok doğal geliyor. Şimdiye kadar farkedemediğime hayret ettim doğrusu.

Her ne kadar yazının başında tüm yolları taramanın çok uzun süreceğini iddia etmiş olsam da, [taramayı yapmanın yanlış yolları](https://stackoverflow.com/q/2200236/886669)
olduğu gibi, [doğru yolları da](https://www.mathblog.dk/project-euler-15/) var. Örneğin, yukarıdaki resimdeki gibi bir ızgarayı sondan başa
doğru çok hızlı bir şekilde tarayabiliriz. Bu tarz şeyleri C ile yazmak daha keyifli geliyor, o yüzden öyle yaptım.

    :::c
    #include <stdint.h>
    #include <stdio.h>
    #include <limits.h>

    #ifndef GRIDSIZE
    #define GRIDSIZE 20 
    #endif

    #define WILL_OVERFLOW(x,y) (x > ULLONG_MAX - y)

    unsigned long long grid[GRIDSIZE+1][GRIDSIZE+1];

    unsigned long long solve()
    {
        int i, k;
        unsigned long long t1, t2;

        // Kenarlari 1 ile doldur
        for(i = 0; i < GRIDSIZE+1; i++)
        {
            grid[0][i] = 1;
            grid[i][0] = 1;
        }

        for(i = 1; i < GRIDSIZE+1; i++)
        {
            for(k = 1; k < GRIDSIZE+1; k++)
            {
                t1 = grid[i-1][k];
                t2 = grid[i][k-1];

                if(WILL_OVERFLOW(t1, t2))
                {
                    printf("Sayilar cok buyuk, hesaplanamadi\n");
                    return -1;
                }

                grid[i][k] = t1 + t2;
            }  
        }

        return grid[GRIDSIZE][GRIDSIZE];
    }

    main(int argc, char const *argv[])
    {
        printf("%dX%d izgarada %llu yol var.\n", GRIDSIZE, GRIDSIZE, solve());
        return 0;
    }

20X20'lik ve 30x30'luk ızgaraları yukarıdaki programla hesaplayabiliyorum. 35x35 olarak denediğimde, 64-bit integer'a sonuç sığmadı.

Son olarak, [doğru cevabın sayısal değeri](http://www.wolframalpha.com/input/?i=40!%2F(20!*20!)) de çok enteresan. Yaklaşık olarak 138 milyar.
Dünya nüfusunun 7-8 milyar civarı olduğunu düşünürsek, dünyadaki herkesi 20X20 ızgarada farklı yollardan karşı köşeye geçerse, geriye 130
milyar ihtimal daha kalıyor. Bu kadar büyük olacağını beklemezdim.

## Gelecek Problem

\\(2^{15} = 32768\\) ve rakamları toplamı \\(3 + 2 + 7 + 6 + 8 = 26\\).

\\(2^{1000}\\) sayısının rakamları toplamı kaçtır.
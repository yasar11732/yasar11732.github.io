<!--
.. title: (Euler 14) En Uzun Collatz Dizisi
.. slug: euler-14
.. date: 2018/08/24 02:21:00
.. tags: 
.. description: Başlangıcı bir milyondan daha küçük olan en uzun Collatz dizisini bulacağız.
.. has_math: yes
-->

Aşağıdaki yinelemeli dizi pozitif tamsayılar kümesi için tanımlanmıştır:

<p style="margin-left:50px;"><var>n</var> → <var>n</var>/2 (<var>n</var> çift ise)<br><var>n</var> → 3<var>n</var> + 1 (<var>n</var> tek ise)</p>

Yukarıdaki kurala göre, 13 sayısından başlayarak aşağıdaki diziyi elde ederiz:

<div style="text-align:center;">13 → 40 → 20 → 10 → 5 → 16 → 8 → 4 → 2 → 1</div>

13 ile başlayıp 1 ile biten bu dizinin 10 elemanlı olduğu görünüyor. Henüz kanıtlanamamış olsa da, tüm başlangıç sayılarının 1 sayısına ulaştığı düşünülüyor.

Bir milyonun altındaki hangi başlangıç sayısı ile en uzun dizi elde edilir? <!--TEASER_END-->

Not: Dizi başladıktan sonra bir milyon üzerine çıkabilir.

Birden başlayıp bir milyona kadar olan sayılar için Collatz dizisi uzunluğunu karşılaştırmamız gerekiyor. Sık sık aynı hesapları yapmamak için
daha önce bulduğumuz sonuçları hafızada tutacağız.

![Collatz Serisi](/images/collatz.png)

Taramayı küçük sayılardan büyük sayılara doğru yapacağız. Collatz dizisini oluştururken, başladığımız sayıdan daha küçük bir sayıya
rastlarsak, dizinin kalan kısmını daha önceki taramalarda bulmuş olacağımız için, bu kısmın uzunluğunu hafızadan okuyacağız.
Örneğin, 13 → 40 → 20 → 10 → 5 → 16 → 8 → 4 → 2 → 1 serisinde, 10 sayısının
Collatz uzunluğunu hafızadan bulup, üzerine 3 ekleyeğiz, 13'ün Collatz uzunluğunu hafızaya kaydedeceğiz. Ancak, 40 ve 20'nin Collatz
uzunluğunu hafızaya kaydetmeyeceğiz. Böylece, neyin hafıza olduğunu, hafızayı okumadan biliriz. Ayrıca, hafızanın aşırı büyümesinin
önüne geçmiş oluruz. Algoritmanın Python ve C dillerinde uygulaması aşağıdaki şekilde;

    :::python
    #!/usr/bin/python

    cache = [0] * 1000000

    cache[1] = 1
    cache[2] = 2
    cache[4] = 3


    if __name__ == "__main__":
        m, m_i = 0,0

        for a in range(2, 1000000):
            b = a
            c = 0

            while b>=a:
                c+=1
                "Python 3 ile yazilacaksa, en sondaki +2 yerine +1 yazilacak"
                b = b/2 + (b%2) * (b/2 + 2*b + 2)
            
            c = c+cache[b]
            cache[a]=c

            if c > m:
                m = c
                m_i = a

        print("En uzun dizi %s ile basliyor ve %s elemanli" % (m_i, m))
<br />

    :::c
    #include <stdlib.h>
    #include <stdio.h>
    #include <stdint.h>

    // int 4 byte iken yaklaşık 4MB
    #define CACHE_SIZE 1000000

    int cache[CACHE_SIZE];

    int main(int argc, char const *argv[])
    {
        // İlk birkaç seriyi hafızaya alabiliriz
        cache[1] = 1;
        cache[2] = 2;
        cache[4] = 3;

        uint32_t max = 0;
        uint32_t max_i = 0;

        uint32_t a,b,c;
        
        for(a = 2; a<1000000;a++)
        {
            b = a;
            c = 0;
            while(b >= a)
            {
                c++;
                b = b/2 + (b%2) * ( (b/2) + 2*b + 2);
            }

            c = c+cache[b];
            cache[a] = c;

            if(c > max)
            {
                max = c;
                max_i = a;
            }
        }

        printf("En uzun dizi %d ile basliyor ve %d elemanli.\n", max_i, max);
        return 0;
    }

Python versiyonu 1.7 saniye gibi bir sürede tamamlanırken, C versiyonu 15 milisaniyede tamamlanıyor. Eğer hafızadan değer kullanmayı iptal edersek, Python
versiyonunun çalışma süresi 35 saniyeye, C versiyonunun çalışma süresi ise 324 milisaniyeye çıkıyor.

## Gelecek Problem

2x2 ızgaranın sol üst köşesinden başlayarak, ve sadece sağa veya aşağıya hareket ederek, sağ alt köşeye tam olarak 6 yol vardır.

<div style="text-align: center">
<img src="data:image/gif;base64,R0lGODlh0ACXAMQAAAAAALXf/7fg/7zi/8Tl/8jn/8fo/8zp/9Ts/9nv/93x/+Pz/+v2/+34//P6/////wAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAP///yH5BAEAAB8AIf4cVWxlYWQgR0lGIFNtYXJ0U2F2ZXIgVmVyIDIuMAAsAAAAANAAlwAABf/gJ45kaZ5oqq7sB7xwLM9ya98ore8v3vLAoHDmyw2DxSTriFSemNAowEmSWoHU6nVL03K/sawLPHWWxeSzUp0mo91msSidZaPrsLs5H5eri2FUdnV4PYR7hmtyLoJ8fXN6iH9JkziBin6NiZiQh5KRlI6Ui5U3l5yMnmuiqICsPqWAmrE2g4KFtLWzt5mfvJ2/q5utsK+WpLvBuT+4oK7DsMi+j6nBodCy06O9wssrttTX3t/JxOamxscj4yrsRtjR2tnOxfCmVfT17jnl2/no9nSt+wdw35N+81Q9M1gC3LmCBH+kExhxyUSK1cItrPjt4hJp3VQxbNhMoT5rGi3/efw40ORJlxBT+hMnkmPHgBg3ykyok9pIfAhn9hS6UyJOlsCKGv3ZMqTSe/ISMk1KE2atle1AVvVpsx1WclHVdX031SHRlyhVgtE6dObUjFufel3LLa5bumH1tYlCCg7XN3jlptg79gmdpmljJr56ePHSmoVNnHoI1alji0fBUqWM+a3noDzRonoLVzRnZnnF2pVat+3ZeJYFk4Vs9XHtnKZfMy4L9LYXJqpPr+NbeTXs0roNAy8ufPhy3Gp5I5Y95sjx5nOeQ1c8unXnJsyTKxdyPfdx0vuslw99E3z46LQvj+fBfn17+vZ3x6eeHUv94EvtIF57+2H3mw4DIhUd/4L/2faXb/MRkaBmC0rYYGcFTiiZgBoO1o2F+TnYXWTOgRjidt9NBiB8yni3Ww0G8iMOjB1uOExmiKEnyVcyyjeYiScS+BtGOn6IY4/8HXjkQfIAKVlvPv7II5IxNqRikHP9wSCSRX4IIYULSRdbdV0wuVmNNpL4pCZqlmglflB2KUybUF5DJ5lv+peUnKG4iKVXfr5oxZ57beFHoYMChigUizTq6KOQRnrfFZJWaumlmKYoRaacduopptp9KuqopIbJYamopqqqjaeu6uqro8IJ66y0glpmrbjmCqmTuvbqq2u/BiusRcMWa+yxyCar7LLMNuvss9BGK+201FZr7f+12Gar7bbcduvtt+CGK+645JZr7rnopqvuuuy2y+qijOICr3qzzKvelSv+mWWUWZVUJZP4vqevlEx95i+aAE9pZpKs8uvhwRcKFDCKArP4L0kQD/zwxKg5PBvDGINWsTocK3jxkCDXadzIUJUMJsJ5erzwmBrL6HK/Mjec8nQrU9yywmvmHPPOZ5rHssRAh0w0nkt7ljTP29z8sNAonwy10T4jveTMMFfd9dUWf92S1FSKzbTVRYcdMWpkc722kGgjh3XHvLQddNNPp300hkunYrfScf8N9t5wm+133npnzXfgilINlOCDK1742zinRncfkCd+ec+bU06w42MjLnf/vmrXfDfNpJMsusEiS1456oSDlfnosX/edON9lzE765abbHbmRe5+Z38FD3+24brbG2+9X4B+vOcbKx/qjM3jHRjm0i9PffZb9q7ppmRy756pXDgvfIbQD+048LjfHrnr493JfsamK83n3PDrHPjqoNxfevpeA6D6GPe+znHHavNrXf4W5j+y0MuA+rGemB7kMOIsMID1w2AGcxSoCOnpgm6S4Jcq10CCjc93/6vdx9ynOQg6UFYgJJ75+Ie+mg1BgDIUoflUhiby4PB5G8whC2mnQuJ1r4gaROIAf8dDAH4wdYv7HQ1b1CYYKlGIUtza6dzSwSzR6IcJ9N7LWFPFvyNCsXBLcpoWATcG1ZRQU+sTxc3UOEEskrCLXlxjAW1nxGXQ0SS8ihMevTjC+JVoYn9EiRkFKb/zxcaKLZxcaCCZkTcapZGbOGEiNaLJJgZRdEREow8juS9FjrKSgwQUJikVyu+JzxBseCUl9SJLUNZyluW63vZuqUdtVU9evOylL1nZqGAKM1w3DFYy3WXCRebqlMz04Oxihcto9hGUpGqVNZtJmlLdapuTWlYgwblEZE1zXceEVTrJyc52MisEADs=" alt="" />
</div>

20x20 ızgarada bu şekilde kaç adet yol vardır?


<!--
.. date: 2018/08/23 16:36:00
.. slug: euler-13
.. title: (Euler 13) C programlama dilinde büyük sayıları toplama
.. description: 100 adet 50 basamaklı sayının toplamının ilk 10 hanesini bulacağız
.. tags: mathjax
-->

Aşağıdaki 100 adet 50 haneli sayının toplamının ilk 10 hanesini bulunuz.

<div style="font-family:'courier new';font-size:10pt;text-align:center;">
37107287533902102798797998220837590246510135740250<br>
46376937677490009712648124896970078050417018260538<br>
74324986199524741059474233309513058123726617309629<br>
91942213363574161572522430563301811072406154908250<br>
23067588207539346171171980310421047513778063246676<br>
89261670696623633820136378418383684178734361726757<br>
28112879812849979408065481931592621691275889832738<br></div><!--TEASER_END--><div style="font-family:'courier new';font-size:10pt;text-align:center;">
44274228917432520321923589422876796487670272189318<br>
47451445736001306439091167216856844588711603153276<br>
70386486105843025439939619828917593665686757934951<br>
62176457141856560629502157223196586755079324193331<br>
64906352462741904929101432445813822663347944758178<br>
92575867718337217661963751590579239728245598838407<br>
58203565325359399008402633568948830189458628227828<br>
80181199384826282014278194139940567587151170094390<br>
35398664372827112653829987240784473053190104293586<br>
86515506006295864861532075273371959191420517255829<br>
71693888707715466499115593487603532921714970056938<br>
54370070576826684624621495650076471787294438377604<br>
53282654108756828443191190634694037855217779295145<br>
36123272525000296071075082563815656710885258350721<br>
45876576172410976447339110607218265236877223636045<br>
17423706905851860660448207621209813287860733969412<br>
81142660418086830619328460811191061556940512689692<br>
51934325451728388641918047049293215058642563049483<br>
62467221648435076201727918039944693004732956340691<br>
15732444386908125794514089057706229429197107928209<br>
55037687525678773091862540744969844508330393682126<br>
18336384825330154686196124348767681297534375946515<br>
80386287592878490201521685554828717201219257766954<br>
78182833757993103614740356856449095527097864797581<br>
16726320100436897842553539920931837441497806860984<br>
48403098129077791799088218795327364475675590848030<br>
87086987551392711854517078544161852424320693150332<br>
59959406895756536782107074926966537676326235447210<br>
69793950679652694742597709739166693763042633987085<br>
41052684708299085211399427365734116182760315001271<br>
65378607361501080857009149939512557028198746004375<br>
35829035317434717326932123578154982629742552737307<br>
94953759765105305946966067683156574377167401875275<br>
88902802571733229619176668713819931811048770190271<br>
25267680276078003013678680992525463401061632866526<br>
36270218540497705585629946580636237993140746255962<br>
24074486908231174977792365466257246923322810917141<br>
91430288197103288597806669760892938638285025333403<br>
34413065578016127815921815005561868836468420090470<br>
23053081172816430487623791969842487255036638784583<br>
11487696932154902810424020138335124462181441773470<br>
63783299490636259666498587618221225225512486764533<br>
67720186971698544312419572409913959008952310058822<br>
95548255300263520781532296796249481641953868218774<br>
76085327132285723110424803456124867697064507995236<br>
37774242535411291684276865538926205024910326572967<br>
23701913275725675285653248258265463092207058596522<br>
29798860272258331913126375147341994889534765745501<br>
18495701454879288984856827726077713721403798879715<br>
38298203783031473527721580348144513491373226651381<br>
34829543829199918180278916522431027392251122869539<br>
40957953066405232632538044100059654939159879593635<br>
29746152185502371307642255121183693803580388584903<br>
41698116222072977186158236678424689157993532961922<br>
62467957194401269043877107275048102390895523597457<br>
23189706772547915061505504953922979530901129967519<br>
86188088225875314529584099251203829009407770775672<br>
11306739708304724483816533873502340845647058077308<br>
82959174767140363198008187129011875491310547126581<br>
97623331044818386269515456334926366572897563400500<br>
42846280183517070527831839425882145521227251250327<br>
55121603546981200581762165212827652751691296897789<br>
32238195734329339946437501907836945765883352399886<br>
75506164965184775180738168837861091527357929701337<br>
62177842752192623401942399639168044983993173312731<br>
32924185707147349566916674687634660915035914677504<br>
99518671430235219628894890102423325116913619626622<br>
73267460800591547471830798392868535206946944540724<br>
76841822524674417161514036427982273348055556214818<br>
97142617910342598647204516893989422179826088076852<br>
87783646182799346313767754307809363333018982642090<br>
10848802521674670883215120185883543223812876952786<br>
71329612474782464538636993009049310363619763878039<br>
62184073572399794223406235393808339651327408011116<br>
66627891981488087797941876876144230030984490851411<br>
60661826293682836764744779239180335110989069790714<br>
85786944089552990653640447425576083659976645795096<br>
66024396409905389607120198219976047599490197230297<br>
64913982680032973156037120041377903785566085089252<br>
16730939319872750275468906903707539413042652315011<br>
94809377245048795150954100921645863754710598436791<br>
78639167021187492431995700641917969777599028300699<br>
15368713711936614952811305876380278410754449733078<br>
40789923115535562561142322423255033685442488917353<br>
44889911501440648020369068063960672322193204149535<br>
41503128880339536053299340368006977710650566631954<br>
81234880673210146739058568557934581403627822703280<br>
82616570773948327592232845941706525094512325230608<br>
22918802058777319719839450180888072429661980811197<br>
77158542502016545090413245809786882778948721859617<br>
72107838435069186155435662884062257473692284509516<br>
20849603980134001723930671666823555245252804609722<br>
53503534226472524250874054075591789781264330331690<br></div>

Daha önceki Euler problemlerini Python kullanarak çözmüştüm. Python'da sayıların
alabileceği değerlerin bir üst sınırı olmadığından, bu soruyu Python ile çözmenin
ilginç bir yanı yok. Bu nedenle, bu problemi C programlama dilinde çözmeye karar verdim.

Sayıları txt dosyasından okuma için, aşağıdaki kodları kullanıyorum. `sayilar.txt` dosyasinda, satir sonu düzeni linux'e göre olmalı ('\n')
ve dosyasının sonunda en az 1 tane boş bir satır bırakılmalı.

    :::c
    #include <stdio.h>

    #define N_OF_NUMBERS 100
    #define S_OF_NUMBERS 50

    /* +1 NULL için*/
    char numbers[N_OF_NUMBERS][S_OF_NUMBERS+1];

    int read_numbers()
    {
        
        FILE *f = fopen("sayilar.txt", "r");
        if(f == NULL)
        {
            perror("sayilar.txt okunamadi");
            return -1;
        }

        /*+1 \n için, daha sonra NULL'a çevrilecek*/
        size_t n_elems = fread(&(numbers[0]), S_OF_NUMBERS+1, N_OF_NUMBERS, f);
        fclose(f);

        if(n_elems < N_OF_NUMBERS)
        {
            printf("sayilar.txt icerisinde %zd adet sayi bulundu. %d bekleniyordu.", n_elems, N_OF_NUMBERS);
            return -1;
        }

        // Sayıları NULL ile sonlandırmak için
        while (n_elems--)
        {
            numbers[n_elems][S_OF_NUMBERS] = '\0';
        }

        return 0;
    }

50-basamaklı sayılar C'deki standard veri yapılarına sığamayacak kadar büyük olduğundan, karakter dizisi içine okudum. Bunlar üzerinde
işlem yapabilmek için, ASCII kodlarından sayısal değerlere dönüştürme yapmak gerekiyor.

    :::c
    void convert()
    {
        size_t i,k;

        for(i = 0; i < N_OF_NUMBERS; i++)
        {
            for(k = 0; k < S_OF_NUMBERS; k++)
            {
                numbers[i][k] = numbers[i][k] - '0';
            }

        }
    }
    
Toplama işlemine geçmeden önce, toplama işleminin sonucunu barındırabilecek büyüklükte bir karakter-dizisine ihtiyacımız olacak.
Topladığımız sayılar 50 haneli olduğundan, herbirinin alabileceği en büyük değer \\(10^{51} - 1\\) olur. 100 adet sayı topladığımız
için, toplamın alabileceği en büyük değer \\((10^{51} - 1) \cdot 10^2 = 10^{53} - 100\\) olur. Dolayısıyla, 53 elemanlı bir karakter
dizisi işimizi görecektir.

    :::c
    char toplam[53];
    
Toplamın ilk 10 hanesini hesaplamak istediğimiz için, soldan sağa haneleri toplayarak ilerliyeceğiz. Önce 50. haneleri toplama ekleyeceğiz,
sonra 49. haneleri toplama ekleyeceğiz vs. Bunun için toplamın belirli bir hanesine bir rakam eklemek için yardımcı bir fonksiyon yazalım.

    :::c
    void add_to_sum(int basamak, int deger)
    {
        // basamağın toplam dizisindeki indeksi
        size_t i = S_OF_SUM - basamak;

        // toplami barindiracak degisken
        int sum;

        sum = toplam[i] + deger;

        // toplamdan 9 dan büyükse, basamak taşımak gerekiyor
        div_t bolum = div(sum, 10);

        toplam[i] = bolum.rem;

        if(bolum.quot > 0)
        {
            add_to_sum(basamak+1, bolum.quot);
        }
    }
    
Fonksiyonun ilk argümanıyla, hangi basamağa rakam eklemek istediğimizi belirtiyoruz. Birler basamağı için 1, onlar basamağı için 2 gibi.
Basamaklar sağdan sola, dizi indeksleri ise soldan sağa sayıldığı için, indeksin yerini hesaplamamız gerekti. Toplam dizisindeki
her bir eleman bir rakamı ifade ettiğinden, 9'dan büyük olmamasına dikkat etmek gerekiyor. Problem ilk 10 haneyi istese de, şu an tüm 
sayıları toplamamızın önünde bir engel yok.

    :::c
    void sayilari_topla()
    {
        size_t i; /* Topladığımız Sayı */
        size_t k; /* Topladığımız hane */

        for(k = S_OF_NUMBERS; k > 0; k--)
        {
            for(i=0; i< N_OF_NUMBERS;i++)
            {
                add_to_sum(k, numbers[i][S_OF_NUMBERS - k]);
            }
        }
    }
    
Elde ettiğimiz toplamı karakter karakter ekrana yazabiliriz.

    :::c
    // baştaki sıfırları atla
    i = 0;
    while(toplam[i] == 0)
        i++;
    
    for(; i < S_OF_SUM; i++)
    {
        printf("%d", toplam[i]);
    }

    printf("\n");

Elde ettiğimiz sonuç <span style="font-family:'courier new';font-size:10pt">5537376230390876637302048746832985971773659831892672</span>.
Böylece, ilk 10 haneyi de hesaplamış olduk.

## Bonus

Varsayalım ki, tüm sayıları toplamadık ve toplamın ilk 10 hanesini hesaplayıp bırakmak istiyoruz. Tüm sayıların ilk 10 hanelerini
toplayarak başlayalım.

    :::c
    void sayilari_topla()
    {
        size_t i; /* Topladığımız Sayı */
        size_t k; /* Topladığımız hane */

        for(k = S_OF_NUMBERS; k > 39; k--)
        {
            for(i=0; i< N_OF_NUMBERS;i++)
            {
                add_to_sum(k, numbers[i][S_OF_NUMBERS - k]);
            }
        }
    }

Bu şekilde çalıştırdığımızda <span style="font-family:'courier new';font-size:10pt">5537376230342000000000000000000000000000000000000000</span> sonucunu
elde edeceğiz. Soldan 13 hane elde ettik. İhtiyacımız olandan 3 hane fazla.

Toplamaya devam ettiğimizde ilk 10 hanenin değişmeyeceğinden emin miyiz? Diyelim ki, kalan 40 hanede sadece 9 rakamı bulunuyor.
O halde kalan rakamların toplamı en fazla \\( (10^{40} - 1)*10^2 = 10^{42} - 100\\) olabilir, ki bu 42 haneli bir sayıdır. Bu durumda, ilk 10 hanenin
sonundaki 0 rakamı 1 olarak değişebilir. Bu da demek oluyor ki, toplama işlemine devam etmemiz gerekiyor.

    :::c
    void sayilari_topla()
    {
        size_t i; /* Topladığımız Sayı */
        size_t k; /* Topladığımız hane */

        for(k = S_OF_NUMBERS; k > 38; k--)
        {
            for(i=0; i< N_OF_NUMBERS;i++)
            {
                add_to_sum(k, numbers[i][S_OF_NUMBERS - k]);
            }
        }
    }

Soldan 11. haneleri de topladığımızda <span style="font-family:'courier new';font-size:10pt">5537376230386000000000000000000000000000000000000000</span> sayısını elde ettik.
Yukarıdaki hesabı tekrar edersek, kalan hanelerin toplamı en fazla 41 haneli bir rakam olabilir. Bu durumda, 11. hane en fazla 4 olabilir. Böylece,
ilk 10 hanenin daha fazla değişemeyeceğini de görmüş olduk. Problemin cevabı <span style="font-family:'courier new';font-size:10pt">5537376230</span> oldu.

## Bonus 2

Eksik kalmaması açısından, Python çözümünü de ekliyorum.

    :::python
    with open("sayilar.txt") as f:
        sayilar = [int(l.strip())  for l in f]
        print("%s" % str(sum(sayilar))[:10])
    
## Gelecek Problem

Aşağıdaki yinelemeli dizi pozitif tamsayılar kümesi için tanımlanmıştır:

<p style="margin-left:50px;"><var>n</var> → <var>n</var>/2 (<var>n</var> çift ise)<br><var>n</var> → 3<var>n</var> + 1 (<var>n</var> tek ise)</p>

Yukarıdaki kurala göre, 13 sayısından başlayarak aşağıdaki diziyi elde ederiz:

<div style="text-align:center;">13 → 40 → 20 → 10 → 5 → 16 → 8 → 4 → 2 → 1</div>

13 ile başlayıp 1 ile biten bu dizinin 10 elemanlı olduğu görünüyor. Henüz kanıtlanamamış olsa da, tüm başlangıç sayılarının 1 sayısına ulaştığı düşünülüyor.

Bir milyonun altındaki hangi başlangıç sayısı ile en uzun dizi elde edilir?

Not: Dizi başladıktan sonra bir milyon üzerine çıkabilir.

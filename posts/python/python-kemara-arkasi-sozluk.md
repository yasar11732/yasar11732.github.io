<!--
.. date: 2018/09/4 20:12:00
.. slug: sozluk-algoritmasi
.. title: Python Sözlüklerindeki Hash Tablosu Yapısı
.. description: Python sözleri için kullanılan Hash tablolarının yapısıyla ilgili bir inceleme.
-->

Programlama öğrenmek için kullanılabilecek birçok yöntem var. Referans belge okumak, küçük projeler yapmak, soru sormak, soru cevaplamak, blog yazmak ve
belge çevirmek, programlama öğrenirken kullanılabilecek yöntemlerden bazıları. Bunlara ek olarak, profesyonel kişi veya gruplarca yazılmış programların
kaynak kodlarını okumanın çok faydalı olduğunu düşünüyorum. Temel bilgiler öğrenmenin ve başlangıç-orta seviyede programlar yazmanın eğitsel katkısı
giderek azaldığında, kod incelemesi yapmak, öğrenme konusunda yeni bir ivme kazandırabilir. Kişinin yeni fikirlerle veya eski fikirlerin daha rafine
halleriyle karşılaşmasına olanak sağlar. Bu gözle incelenebilecek kodlara örnek olarak, [Python sözlük objesini](https://github.com/python/cpython/blob/2.7/Objects/dictobject.c) verebiliriz.
Dinamik array ve Hash Table (Tr. Komut Çizelgesi)
özelliklerine sahip bu ilginç veri yapısı, _keyword_ argümanları, sınıfların metodları, global ve gömülü değişkenler gibi, bir anahtarla veriyi
eşlemek gereken her yerde kullanılıyor. Bu yüzden Python için önemli bir yeri var. 

Büyük bir projenin kaynak kodlarını okumak, çoğu zaman korkutucudur. Neyse ki, `dictobject.c` içindeki yorumlar öyle açık ki, tahmine gerek bırakmıyor.
Bu yazının büyük bir kısmı, `dictobject.c` içindeki yorumların kendi kelimelerimle ifadesinden ibaret olacak. Burada bahsedilen konuları anlamak için, giriş seviyesinde Python bilgisi,
orta derecede C bilgisi, temel veri yapıları konusunda bilgi sahibi olmanız faydalı olacaktır.

**Not**: Buradaki inceleme Python 2.7'deki `dictobject.c` dosyası üzerinden yapıldı, [bu dosyanın 3.7 deki halinde](https://raw.githubusercontent.com/python/cpython/3.7/Objects/dictobject.c)
ciddi farklılıklar var.

Python sözlükleri C dilinde hash tablosu olarak tasarlanmış. Tablonun her bir girdisi, aşağıdaki yapıda;

    :::c
    typedef struct {
        /* Cached hash code of me_key.  Note that hash codes are C longs.
         * We have to use Py_ssize_t instead because dict_popitem() abuses
         * me_hash to hold a search finger.
         */
        Py_ssize_t me_hash;
        PyObject *me_key;
        PyObject *me_value;
    } PyDictEntry;
    
`struct` yapısı çok basit. Sözlük anahtarı olarak kullanılan objenin `hash` değeri, anahtar ve değer olarak kullanılan objeleri
işaret eden pointerlar var. Tablo içindeki bu girdilerin her birine slot deniyor. Bir slotun, 3 farklı tipi olabiliyor. Kullanılmamış
slotlarda, `me_key` ve `me_value` değerleri `NULL` oluyor. Aktif slotlarda, `me_key != NULL && me_key != dummy` ve `me_value != NULL`
oluyor. Dummy diye adlandırdıkları slotlar ise, eskiden geçerli bir (anahtar, değer) barındıran ama şu an boş olan slotlar. Bunlarda
ise, `me_key == dummy` ve `me_value == NULL` oluyor. `dummy` ilk kez sözlük objesi oluşturulduğunda bir defaya mahsus olmak üzere
oluşturulan ve tek amacı bir hash tablosu slotunun boş olduğunu belirtmek olan bir Python objesi. Bunun neden gerekli olduğu, ekleme
ve arama bölümlerinde açıklanacak.

    :::c
    typedef struct _dictobject PyDictObject;
    struct _dictobject {
        PyObject_HEAD
        Py_ssize_t ma_fill;  /* # Active + # Dummy */
        Py_ssize_t ma_used;  /* # Active */

        /* The table contains ma_mask + 1 slots, and that's a power of 2.
         * We store the mask instead of the size because the mask is more
         * frequently needed.
         */
        Py_ssize_t ma_mask;

        /* ma_table points to ma_smalltable for small tables, else to
         * additional malloc'ed memory.  ma_table is never NULL!  This rule
         * saves repeated runtime null-tests in the workhorse getitem and
         * setitem calls.
         */
        PyDictEntry *ma_table;
        PyDictEntry *(*ma_lookup)(PyDictObject *mp, PyObject *key, long hash);
        PyDictEntry ma_smalltable[PyDict_MINSIZE];
    };
    
`ma_fill` değişkeni
toplam aktif ve dummy slotlarının sayısını tutarken, `ma_used` değişkeni ise, aktif kayıtların sayısını tutuyor. `ma_mask` değişkeni
hash tablosunun kapasitesinin bir eksiğini tutuyor. Bunun neden gerekli olduğunu da ekleme ve arama bölümlerinde açıklanacak, şimdilik
bu haliyle kabul edin. `ma_table` değişkeni ise, tablo için ayrılmış alana işaret eden bir pointer. Sözlük objesi ilk oluşturulduğunda,
`ma_table = &(ma_smalltable[0])` oluyor. Böylece, küçük tablolar için (5 elemana kadar) ayrıca bir `malloc` çağrısı yapmaya gerek kalmıyor.
`PyObject_HEAD` makrosu ve `ma_lookup` fonksiyonu birebir konumuzla alakalı değil. 

## Arama ve Ekleme

Tüm hash tabloları gibi, Python'daki sözlükler de, Python objelerinin hash değerini hesaplayıp, bu değeri aranılan
nesneyi tablo için bulmak için kullanıyor. Ancak, Python sözlüklerinde kullanılan hash tablolarında bazı nüanslar var.
Öncelikle, yaygın kullanılan hash fonksiyonları, hash değerlerini rastgele-gibi dağıtır. Python hash fonksiyonları
bunun aksine gayet düzenlidir. Örneğin;

    >>> map(hash, range(10))
    [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    >>> map(hash, ("aaa","aab","aac","aad"))
    [-1599925404, -1599925401, -1599925402, -1599925407]

Buradan anlaşılacağı üzere, her bir tam sayının hash değeri kendisine eşittir. Sıralı giden `string` objelerinin hash
değerleri ise, birbirine yaklaşık olur. Hash fonksiyonlarının bu özelliğini, şu şekilde gerekçelendirmişler;

 > This isn't necessarily bad!  To the contrary, in a table of size 2**i, taking
 > the low-order i bits as the initial table index is extremely fast, and there
 > are no collisions at all for dicts indexed by a contiguous range of ints.
 > The same is approximately true when keys are "consecutive" strings.  So this
 > gives better-than-random behavior in common cases, and that's very desirable.
 
Açıklamayı kısaca özetlemek gerekirse; ardışık sayı veya metinlerin sözlük
indeksi olarak kullanılması yaygın olduğundan, ardışık hash değerlerinde
herhangi bir çakışma olması söz konusu değildir. Neticede, yaygın kullanımlar
için, rastgeleden-iyi performans sergileriz.

Hash değerlerini tablo indekslerine çevirme konusu ise, bit maskeleme
yöntemi ile yapılıyor. Bunun için, tablo kapasitesi her zaman 2'nin
kuvveti şeklinde tutuluyor. Maske olarak kullanılan değer ise, tablo
kapasitesinin bir eksiği oluyor. Örneğin, tablo kapasitesi 8 olduğunda,
maske değeri 7 ( binary olarak 00000111 ) oluyor. İndeks ise, `hash&mask`
şeklinde hesaplanıyor. Diğer bir deyişle, `2**i` büyüklüğünde bir tablo için,
hash değerinin alttan `i` biti tablo indeksi oluyor.

Genel olarak hash tablolarında, çakışma çözümlemek için iki yöntem vardır. Bunlardan biri,
hash tablosunun her bir slotunda, linked list (tr. bağlı liste) veri yapısı
bulundurmakır (en. seperate chaining). Bu yöntemde, aynı hash değerini
taşıyan elemanlar, bir liste içinde tutulur. Diğer bir yöntem ise, eğer
birden fazla eleman aynı hash değerine sahipse, eleman hash
tablosunda farklı boş bir yerde tutulur (en. open addressing). Python sözlükleri,
bu ikinci bahsettiğim metodu tercih ediyor. Bunun gerekçesi ise, liste
yöntemini performans açısından maliyetli bulmaları.

Hash tablosunda boş yer bulmak için de kullanılabilecek çeşitli yöntemler var.
Örneğin, İlk bulunan indeksten itibaren sırayla tablo taranabilir, veya ikinci bir
hash fonksiyonu kullanılabilir. Python sözlükleri biraz daha kendine özgü
bir yöntem kullanıyor. Bu yöntemin çekirdeğini oluşturan formül şu şekilde;

    j = ((5*j) + 1) mod 2**i
    
Örneğin, kapasitesi 8 olan bir tabloda, çakışan indeks 5 olsun. Bu durumda,
boş yer arama sırası aşağıdaki gibi oluyor;

    5 -> 2 -> 3 -> 0 -> 1 -> 6 -> 7 -> 4 -> 5 (burada tekrar başa sarıyor)
    
Bu formülün özelliği, kendini tekrar etmeden önce tablodaki bütün slotları geziyor olması.
Bununla ilgili detaylı bilgi için, [Linear Congruential Method](https://www.google.com.tr/search?q=Linear+Congruential+Method)
Google aramasına bakabilirsiniz. [Doğrusal Sondalama](https://www.google.com.tr/search?q=doğrusal+sondalama)
yerine bu yöntemin seçilmesinin önemli nedenlerinden biri, Python hash değerlerinin
ardışık olmaya meyilli olması. Rastgele misali bir sırada ilerlenmesi halinde, hızlı
bir şekilde boş yer bulunması ihtimali yükseliyor. Python, tabloda boş yer ararken
bu yöntemin yanında başka şeyler de kullanıyor. Tam algoritma şu şekilde;

 1. `perturb` değişkenini `hash` olarak ata. (Buradaki `hash` maskelenmeden önceki hali)
 2. `j = ((5*j) + perturb + 1) mod 2**i` olsun.
 3. `perturb` değikenini PERTURB_SHIFT sabiti kadar (optimum değeri 5 olarak belirlenmiş) sağa kaydır. (`perturb >>= PERTURB_SHIFT`)
 
Buradaki `perturb` değişkeninin amacı, orjinal hash değerinin üst bitlerini de hesaba katmak.
Böylece, orjinal `j = ((5*j) + 1) mod 2**i` dizisinin doğrusal sondalama (en. linear probing)
yöntemine dönüşmesinin önüne geçiliyor. Örneğin, kapasitesi 8 olan bir tabloya, sırasıyla
hash değerleri 16, 32 ve 64 olan elemanlar ekleneceğini düşünelim. Bu durumda, hepsinin
alt 3 biti 0 olacağından, `j = ((5*j) + 1) mod 2**i` formülüne göre aynı sırada
boş yer aranacak. Ancak, üst bitler de hesaba dahil edilirse, daha erken boş yer bulma
ihtimalimiz oluşuyor. Eğer döngü yeterince uzun çalışırsa, `perturb` değeri sıfırda sabitleneceği için,
döngü tekrar `j = ((5*j) + 1) mod 2**i` haline dönüşüyor. Böylece, tablodaki tüm slotların taranacağı
garanti altına alınmış oluyor.

Peki, ya boş yer kalmamışsa? Boş yer arama sırasında, böyle bir endişe gereksiz, çünkü, tablo
kapasitesi 2/3'e ulaştığında, Python tablonun kapasitesini yükseltiyor. Böylece, tabloda boş
yer olmaması ihtimali ortadan kalkıyor. Tablonun kapasitesini yükseltmek için, geçerli kapasitenin
dört katı (tablo büyükse iki katı) büyüklüğünde hafıza ayrılıp, eski tablodaki bütün girdiler yeni tabloya taşınıyor. Bunun
sıradan bir `realloc` veya `memcpy` işlemi olmadığına dikkat edin. Tüm elemanların yeni tablodaki
yerleri `hash&mask` yöntemiyle hesaplanıp, hash çakışmaları yukarıdaki bahsi geçen yöntemle gideriliyor.

Tabloya yeni anahtar eklemek ve eklenmiş değerleri bulmak için yukarıda bahsedilen yöntem kullanıyor, ancak,
aramanın sona erdirilmesi kriteri farklı. Tabloya yeni anahtar eklenmek isteniyor ise, yazının başında
bahsedilen, kullanılmamış veya dummy slot bulununcaya kadar arama devam ediyor. Bulunan slot, aktif slot
haline getiriliyor ve eğer gerekli görülürse tablo kapasitesi artırılıyor. Eğer, verilen bir anahtarın
tabloda karşılığı aranıyorsa, önce anahtarın hash değeri bulunuyor. Sonra, yukarıdaki arama yöntemiyle,
hash değeri eşleşen bir slot veya kullanılmamış bir slot bulunana kadar arama sürdürülüyor. Eğer arama
sırasında bir dummy slot bulunursa, bu slot dikkate alınmadan arama sürdürülüyor. dummy slotun amacı,
silinen slotların aramayı erken sonlandırılmasını önlemek. Tablodan
herhangi bir slot silineceği zaman ise, `ma_key = dummy`, `ma_value = NULL` olarak atanıyor.

Peki ya tabloya milyonlarca değer ekleyip, sonra geri silerseniz ne olur? Python tablo boyutu ayarlamasını
sadece yeni anahtar eklendikten sonra yaptığı için, sözlüğünüzün hafızada tuttuğu yer azalmaz. Ancak, anahtarları
sildikten sonra, yeni bir anahtar eklemeye kalktığınızda, Python sözlük kapasitesini düşürmeye karar verecektir.

Daha detaylı bilgi almak için, orjinal [dictobject.c](https://github.com/python/cpython/blob/2.7/Objects/dictobject.c)
ve [dictobject.h](https://github.com/python/cpython/blob/2.7/Include/dictobject.h) dosyaları incelenebilir. Python'un
iç işleyişine dair kodlar göz korkutucu olsa da, yorumlardaki açıklamalar oldukça faydalı. Ayrıca, 2015 yılında
Python sözlüklerinden esinlenerek, anahtar ve değerleri string olabilen bir benzer bir veri yapısı yazmıştım. Temel
fikirleri anlatmak açısından faydalı olabileceği düşüncesi ile, [kodları GitHub'a yükledim.](https://github.com/yasar11732/ylib/blob/master/src/dict.c)

Konuyu toplamak gerekirse, sözlük objeleri, Python'un en sık kullanılan veri yapılarından biri olduğu için, üzerine
ciddi kafa yorulmuş. Böyle ustaca tasarlanmış ve optimize edilmiş programları okumak, programlama öğrencileri için
faydalı olacaktır. Python kodlarının geri kalanı, her ne kadar sözlükler kadar iyi belgelendirilmemiş olsa da, github
deposundan ulaşılabiliyor. Biraz göz atılmasını tavsiye ederim.


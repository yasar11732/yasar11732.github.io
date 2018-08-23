<!--
.. date: 2018/08/23 01:01:00
.. slug: sage-math
.. title: SageMath
.. description: Python temelli, açık kaynak matematik yazılımı SageMath tanıtımı
.. tags: mathjax
-->

Eğer bloğumu takip ediyorsanız, son birkaç haftadır Euler problemi çözümlerimi paylaştığımı biliyorsunuz. Euler Problemleri,
programcılık problemleri olduğu kadar, matematik problemleri de sayılabilir. Bu yazıda, bu problemlerin çözümünde sıklıkla faydalandığım
SageMath programından bahsedeceğim. <!--TEASER_END-->

## SageMath nedir?

[SageMath](http://www.sagemath.org/) websitesinde, tanımı şu şekilde yapılıyor.

> SageMath is a free open-source mathematics software system licensed under the GPL.
> It builds on top of many existing open-source packages: NumPy, SciPy, matplotlib,
> Sympy, Maxima, GAP, FLINT, R and many more. Access their combined power through a
> common, Python-based language or directly via interfaces or wrappers.

Şu şekilde çevirebiliriz.

> SageMath GPL lisanslı ücretsiz ve açık-kaynak bir matematik yazılımıdır. Birçok mevcut
> açık-kaynak paketin üzerine inşa edilmiştir: NumPy, SciPy, matplotlib,Sympy, Maxima,
> GAP, FLINT, R ve çok daha fazlası. Python-temelli bir dil aracılığıyla veya
> arayüzler ile doğrudan onların birleşmiş gücüne erişim sağlayın.

Görev tanımları şu şekilde; Magma, Mapple, Mathematica ve Matlab gibi yazılımlara
güvenilir ücretsiz açık-kaynak bir alternatif oluşturmak.

Her ne kadar projenin geçmişi 2005 yılı kadar eski olsa da, bir ay kadar önce varlığından
haberdar olup kullanmaya başladım. Öyle görünüyor ki, popülerlik olarak rakiplerinin
gerisinde kalmış.

<script type="text/javascript" src="https://ssl.gstatic.com/trends_nrtr/1513_RC03/embed_loader.js"></script> <script type="text/javascript"> trends.embed.renderExploreWidget("TIMESERIES", {"comparisonItem":[{"keyword":"SageMath","geo":"","time":"today 5-y"},{"keyword":"Mathlab","geo":"","time":"today 5-y"},{"keyword":"Mapple","geo":"","time":"today 5-y"},{"keyword":"Mathematica","geo":"","time":"today 5-y"}],"category":0,"property":""}, {"exploreQuery":"date=today%205-y&q=SageMath,Mathlab,Mapple,Mathematica","guestPath":"https://trends.google.com.tr:443/trends/embed/"}); </script>

Tabi ki, rakipleri kadar popüler olmaması, SageMath'in diğerlerinden daha geride olduğu anlamına gelmez. Rakipleri ticari programlar olduğundan,
çok daha iyi pazarlanıyor olmaları beklenir. Ayrıca, diğer yazılımların mazisi çok daha eskiye dayandığından, SageMath yarışa biraz daha geriden
başlamış. Örneğin, [Mathematica Revision History'e](https://www.wolfram.com/mathematica/quick-revision-history.html) göre, Mathematica 1988
yılında piyasaya çıkmış, yani 30 yıllık bir geçmişi var.

Ancak, SageMath öldü mü diye düşünmeyin, [SageMath Github Deposu](https://github.com/sagemath/sage) düzenli olarak commit görüyor.

## SageMath ile Neler Yapılabilir?

Aşağıda yazılan özelliklerin çok az bir kısmını kendim kullandım, ancak, [Hamdi Murat Yıldırım'ın 2009 Akademik Bilişim Konferansı Sunumuna](http://ab.org.tr/ab09/sunum/39.pdf)
göre aşağıdaki konu başlıkları altında hesaplamalar yapabiliyor.
 
 - Aritmetik
 - Değişmeli Cebir
 - Lineer Cebir
 - Kriptosistemler
 - Tam sayıyı çarpanlara ayırma
 - Grup Teorisi
 - Kombinasyon Hesabı
 - Grafik Teorisi
 - Sayılar Teorisi
 - Kalkülüs
 - Sembolik Hesaplama
 - 2 ve 3 Boyutlu Grafik Çizimleri
 
## SageMath arayüzü

SageMath'in komut satırı ve ipython-notebook arayüzü var. Ben notebook arayüzüne aşina olduğum için, komut satırı arayüzünü hiç denemedim.
Notebook arayüzünü kullandım ve kullanışlı buldum. Eğer SageMath'i kendi bilgisayarınıza kurmayı tercih ederseniz (Cloud seçeneği de mevcut), masaüstünüzde
SageMath Notebook kısayolu oluşuyor. Bu kısayolu tıkladığınızda, önce SageMath Server başlatılıyor, daha sonra internet tarayıcınızda
<span style="font-family:'courier new';font-size:10pt">http://localhost:8889/</span> adresi açılıyor. Açılan sayfanın [Ipython-Notebook'dan](https://ipython.org/notebook.html)
görünür bir farkı yok. Sadece, yeni notebook oluşturma seçenekleri altına SageMath seçeneği eklenmiş.Buradan SageMath notebook'u oluşturursanız,
SageMath'e özgü fonksiyonlar otomatik olarak yüklenmiş oluyor. Python 2 seçeneği ile klasik ipython-notebook elde ediyorsunuz.

## SageMath örnekleri

Aşağıdaki örnekler, SageMath'in benim kullandığım özelliklerine dair. Bundan çok daha fazlasını yapabildiğini, internetteki çeşitli kaynaklar gösteriyor.

### Çarpanlara Ayırma

<iframe src="/factor.html" style="width: 100%; height:250px; border:1px solid #ccc; border-radius: 1px;padding:0; margin-left:2em; margin-right:2em;"></iframe>

Çarpanlara ayırma işlemi `factor` fonksiyonu ile yapılıyor. Çarpanlara ayırma işlemi sonucunda, `IntegerFactorization` objesi dönüyor. Bunu
örnekteki şekilde listeye çevirebiliyorsunuz.

### Bölenleri Bulma

<iframe src="/divisors.html" style="width: 100%; height:670px; border:1px solid #ccc; border-radius: 1px;padding:0; margin-left:2em; margin-right:2em;"></iframe>

Bölenleri bulmak için `divisors` fonksiyonu kullanılıyor. Bölenlerin sayısını bulmak için `number_of_divisors` fonksiyonu kullanılabilir.

### Asal Sayılar

<iframe src="/primes.html" style="width: 100%; height:600px; border:1px solid #ccc; border-radius: 1px;padding:0; margin-left:2em; margin-right:2em;"></iframe>

`Primes` çağrısı ile asal sayılar kümesisini temsil eden bir nesne elde ediyoruz. Bu nesne üzerinden, asal sayı oluşturma ve asal sayı kontrolü
işlemleri gerçekleştirebiliyoruz.

### Denklem Çözme ve Denklem Sadeleştirme

<iframe src="/equations.html" style="width: 100%; height:870px; border:1px solid #ccc; border-radius: 1px;padding:0; margin-left:2em; margin-right:2em;"></iframe>

SageMath sembolik matematik konusunda hayatımı çok kolaylaştırdı. `var` komutu ile sembolik matematik fonksiyonlarında kullanacağınız
değişkenleri tanımladıktan sonra, yukarıdaki örnekte görüldüğü şekilde denklem tanımlıyorsunuz. Bu denklemleri kullanarak, çözüm kümesi
bulma, denklemi belli bir değişken cinsinden yeniden düzenleme, sadeleştirme vb. işlemler yapabiliyorsunuz. Ayrıca, örnekte 
<span style="font-family:'courier new';font-size:10pt">In [6]</span> satırında görüldüğü gibi, çok bilinmeyenli denklemleri de
çözebiliyorsunuz. SageMath basit denklemleri kendiliğinden sadeleştirirken, logaritmik, üslü ve köklü ifadeler içeren denklemleri
sadeleştirmek için `canonicalize_radical` metodunu kullanabilirsiniz.

### Türev Alma

<iframe src="/turev.html" style="width: 100%; height:870px; border:1px solid #ccc; border-radius: 1px;padding:0; margin-left:2em; margin-right:2em;"></iframe>

Türev almak için, `diff` fonksiyonunu kullanıyoruz. `f` fonksiyonunun `x`'e göre birinci dereceden türevini almak için `diff(f,x)`, ikinci dereceden
türevini almak için `diff(f, x, x)` vb. şekillerde kullanabilirsiniz.

### Grafik Çizme

<iframe src="/grafik-cizme.html" style="width: 100%; height:600px; border:1px solid #ccc; border-radius: 1px;padding:0; margin-left:2em; margin-right:2em;"></iframe>

Çizgi grafiği çizmek için `plot` fonksiyonu kullanılıyor. Grafiğini çizmek istediğiniz denklemi ve x-ekseni aralığını belirtmeniz yeterli. Birden fazla
grafiği `+` sembolü ile üstüste bindirebiliyoruz.

### Serpilme Diyagramı

<iframe src="/serpilme.html" style="width: 100%; height:600px; border:1px solid #ccc; border-radius: 1px;padding:0; margin-left:2em; margin-right:2em;"></iframe>

Serpilme diyagramı çizmek için, (x,y) koordinatlarından oluşan bir liste kullanıyoruz.

### Histogram Oluşturma

<iframe src="/histogram.html" style="width: 100%; height:600px; border:1px solid #ccc; border-radius: 1px;padding:0; margin-left:2em; margin-right:2em;"></iframe>

Histogram çizmek için, `histogram` fonksiyonu kullanılıyor. En sık kullanılacak argümanlar şu şekilde;

 - *normed:* Histogramı normalleştirilmiş olarak çiziyor. Olasılık dağılımı elde etmiş oluyorsunuz.
 - *cumulative:* Histogramı grupları toplayarak çiziyor. En son sütun, verinin tümüne karşılık geliyor.
 - *bins:* Sütun sayısını belirtir.
 
### SageMath Dersleri

Malesef SageMath konusunda Türkçe kaynak neredeyse yok. Bulabildiğim tek kaynak, [Sage Turu'nun bir çevirisi](http://doc.sagemath.org/pdf/tr/a_tour_of_sage/a_tour_of_sage.pdf)
İnglizce kaynaklardan öğrenmek isteyenler için, [Sage for Undergraduates](http://www.people.vcu.edu/~clarson/bard-sage-for-undergraduates-2014.pdf)
ve [Computational Mathematics with SageMath](http://dl.lateralis.org/public/sagebook/sagebook-ba6596d.pdf) isimli iki ücretsiz kitap mevcut. Kitapların
ikisine de yeterince detaylı görünüyor.

### Nasıl Destek Alabilirim

[Ask Sage](https://ask.sagemath.org/questions/) isimli bir Soru-Cevap siteleri var. StackOverflow kadar aktif değil, yine de sorularınız cevapsız
kalmıyor.

### Nasıl Destek Olabilirim

SageMath geliştirme çabaları [trac](https://trac.sagemath.org/) ve [mail listesi](https://groups.google.com/forum/#!forum/sage-devel) üzerinden
organize ediliyor. Şu an için en faydalı iş belgeleri Türkçeleştirmek olabilir.


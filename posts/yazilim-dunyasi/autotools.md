<!--
.. date: 2019-06-23 16:16
.. description: Autotools kullanarak ./configure & make & make install ile yüklenebilecek paketler nasıl hazırlanır
.. slug: autotools
.. title: Autotools Gizemini Çözüyoruz
-->

Autotools, GNU build sistemi oluşturmaya yarayan araçlar grubudur. GNU/Linux sistemlerde
antik çağlardan beri yazılım geliştirme ve paylaşma macerasının merkezinde
olmuş `autotools` programlarını anlamak, hem gnu/linux sistemlerine kurulacak yazılımları yapmak
isteyenlerin, hem de linux dağıtımlarına paket oluşturmak isteyenlerin işine
yarayacaktır. Autotools adını ilk kez duyuyor olabilirsiniz ama, Eğer linux üzerinde kaynak
koddan program derleyip kurmuşsanız, aşağıdaki 3 komutu muhakkak biliyorsunuz.

	:::sh
	./configure
	make
	make install
	
`tar.gz` dosyası bir klasöre açılır, o klasörün içine `cd` ile geçilir, esrarengiz komutlar
verilir ve, Hollywood filmlerindeki hacker sahnelerini andıran yazıları izledikten sonra,
programımız derlenir ve kullanmaya başlarız.

Bu yazıda, GNU/Linux işletim sistemlerinde kaynak kod dağıtma, derleme ve yükleme sisteminin bel kemiğini
oluşturan `autotools` araçlarını kullanmaya yetecek kadar teorik bilgi ve örnek verme niyetindeyim. Hedefim autotools'un
girift detaylarına inmekten ziyade, bu ismi ilk kez duyanları, referans belgelere başvurarak ihtiyaçlarını
karşılayabilecek aşamaya getirecek kadar bu programları tanıtmak.

Autotools araçları, yazdığımız programları, `./configure`, `make` ve `make install` ile çeşitli unix nevinden
sistemlerde derlenip kurulabilmesi için, `./configure` programını, `Makefile` dosyalarını ve konfigürasyon 
dosyalarını (genellikle config.h) üretmeye yarar. Bu nedenle, öncelikle bu 3 komutun vazifelerini hatırlamakta
fayda var. 

`configure` programı aslında POSIX standardında yazılmış bir kabuk betiğidir. Bu betik,
programımızın derleneceği platformun niteliklerini anlamak için bir takım testler yaparak,
gerekli araç ve kütüphanelerin varlığını teyit eder. Eğer derlenecek programın derlenebilmesi
için gerekli program, kütüphane ve araçlar sistemde mevcutsa, yaptığı testlerin sonuçlarını ve
komut satırından aldığı argümanların değerlerini kullanarak `Makefile` dosyalarını ve konfigürasyon
dosyalarını (genellikle `config.h`) oluşturur. `configure` programının başarılı sonuçlanması,
programımızın başarıyla derlenip kurulabileceğini gösterir.

`make` programı, `Makefile` dosyasında tanımlanan görevleri yerine getirir. Autotools
tarafından oluşturulan `Makefile` dosyasında birçok görev tanımlanır. `make` komutu
herhangi bir argüman verilmeden çalıştırıldığında, `Makefile` içindeki öntanımlı (eng. default)
hedefi yerine getirir. Autotools tarafından üretilen `Makefile` dosyasındaki öntanımlı görev
programın derlenmesidir.

`make` programı `install` hedefiyle birlikte çalıştığında, derlenmiş program, kütüphane,
belgeler, header dosyaları ve diğer dosyalar ilgili klasörlere yüklenir. Bunların yükleneceği yer, `configure`
aşamasında özellikle değiştirilmezse, `/bin`, `/lib` vs. gibi standart yollardır.

Şimdi, `autotools` kullanarak, bir `Hello World` uygulaması yapalım. Bu uygulama 5 adımdan oluşacak.

Birinci adımda, kaynak kodlarını içerek klasörü oluşturup, bu klasöre geçeceğiz.

	:::sh
	mkdir helloworld
	cd helloword 

İkinci adımda, derlenecek programı yazacağız. `main.c` adında bir dosya oluşturup, aşağıdaki
programı kopyalayın.

	:::c
	#include <stdio.h>
	#include "config.h"

	int main(void) {
		puts("Hello World.");
		puts("Bu program: " PACKAGE_STRING);
	}

Üçüncü adımda, `Makefile.am` dosyası oluşturup, aşağıdaki satırları yazın.

	:::txt
	bin_PROGRAMS = hello
	hello_SOURCES = main.c
	
Dördüncü adımda, `configure.ac` dosyasını aşağıdaki gibi oluşturun.

	:::txt
	AC_INIT([helloworld],[1.0],[bug-reports@helloworld.com])
	AM_INIT_AUTOMAKE([foreign])
	AC_PROG_CC
	AC_CONFIG_HEADERS([config.h])
	AC_CONFIG_FILES([Makefile])
	AC_OUTPUT

Son olarak, `autoreconf --install` komutu ile, build sistemimiz hazır hale geliyor. Bu aşamada, `./configure`
ve `make` komutlarıyla programınızı derleyip, çıktısını inceleyebilirsiniz.

Eğer elinizde imkan varsa, yazının devamını okumadan önce, yukarıdaki örneği denemenizi tavsiye ederim. Yazının
devamında, bir adım geri gidip, bu örnekte neler olup bittiğine biraz daha yakından bakacağız.

Yazının başından beri, `autotools`'un bir araçlar grubu olduğundan bahsettik, ancak, bu araçların hangileri
olduğuna hiç değinmemiştik. Bu araçların başlıca 2 tanesi, `autoconf`, `automake` diyebiliriz.
Bunlardan `autoconf` programı, otomatik olarak `configure` betiği oluşturmaya, `automake` programı otomatik
olarak `Makefile` oluşturmaya yarıyor. Şu aşamada, `autotools` içindeki diğer programları yardımcı araçlar
olarak düşünebiliriz. Autotools içindeki araçları birbirinden bağımsız programlar olarak düşünmemelisiniz.
Bunların birbiriyle çok sıkı ve karmaşık ilişkileri var. Bu ilişkileri yazının devamında biraz daha detaylı inceleyeceğiz.

Öncelikle, `autoconf` programını inceleyelim. Bu program, `configure.ac` dosyasını okuyarak, `configure`
programını oluşturur. `configure` programının amacından yukarıda bahsettiğim için, konuyu doğrudan `configure.ac`
dosyasına getireceğim. Bu dosyayı, M4 makroları içeren bir kabuk (shell) betiği olarak tanımlayabiliriz.
M4 çok eski bir şablon dilidir. `configure.ac` içindeki M4 makroları, `autoconf` tarafından shell
programına dönüştürülür. Bu makrolar, bir veya daha fazla argüman alabilir. Bu argümanların da
bazıları gerekli, bazıları ise seçmeli olabilir. Bunları, makro adından sonra gelen
parantezler içinde virgülle ayrılmış olarak belirtiriz. Ayrıca, her bir argümanı köşeli
parantezler içine alırız. `configure.ac` dosyasında kendi yazdığınız makroları kullanabileceğiniz
gibi, `autotools` tarafından sağlanan makroları da kullanabilirsiniz. `autotools` içinde o kadar çok
hazır makro var ki, ihtiyacınız olan makroyu hazır olanlar içinde bulamamanız mümkün olsa da muhtemel değil.
Bu yazıda, nasıl makro yazabileceğimiz konusuna değinmeyeceğiz.

Örneğimizdeki `configure.ac` dosyası, sadece makrolardan oluşuyor. Sırayla bu makroların gereğine ve 
aldıkları argümanlara göz atalım. `AC_INIT` makrosu, ikisi zorunlu üçü seçmeli olmak üzere 5 argüman
alabiliyor. Bu makronun görevi, `configure` programının aldığı komut satırı argümanlarını işlemek
ve programı kullanılabilir hale getirmek. Eğer ne yaptığınızı çok iyi bilmiyorsanız, `configure.ac`
dosyasına daima `AC_INIT` makrosuyla başlayın. Bu makronun ilk argümanı paketinizin ismini, ikinci
argümanı ise paketinizin versiyonunu içerir. Bu makro hakkında daha detaylı bilgiyi [Autoconf Belgelerinde](https://www.gnu.org/software/autoconf/manual/autoconf-2.67/html_node/Initializing-configure.html) bulabilirsiniz.

Kullandığımız ikinci makro, `AM_INIT_AUTOMAKE`. Bu makro, `automake` programına ayar vermek için kullanılır.
Burada `foreign` seçeneğini kullanmamızın nedeni, yazdığımız
programın GNU standartlarına uymadığını belirtmek. Eğer bu seçeneği belirtmezsek, README, NEW, AUTHORS
gibi tüm standart dosyaları oluşturmak zorunda kalırız. Bu makro hakkında daha fazla detaya şu an için
gerek yok.

`AC_PROG_CC` makrosu, sistemde çalışan bir C derleyicisi bulur.

`AC_CONFIG_HEADERS` makrosu, bir konfigürasyon header dosyası (Örnekte config.h) oluşturur. Bu header içindeki tanımlamalar,
daha önce çalışan makrolardan elde edilir. Örneğin, `AC_INIT` makrosu tarafından ayarlanan paketin adı
ve versiyonu gibi bilgiler, bu header dosyasına yazılır. Böylece, C programımızın içinde bu bilgilere
ulaşabiliriz.

`AC_CONFIG_FILES` makrosu ile, `configure` programının oluşturacağı dosyalar belirtilir. Bu dosyalar
`.in` uzantılı olarak aranır, işlendikten sonra `.in` uzantısı olmadan kaydedilir. Bizim örneğimizde,
`Makefile.in` dosyası, `Makefile` dosyasına dönüşecek. Bu dönüşüm işleminde pek matah birşey yok. `Makefile.in`
dosyasının içinde iki @ işareti arasında belirtilen değişkenler doldurulacak. Bu değişkenlerin değeri de,
çalışan makrolar tarafından belirleniyor. Mesela, `CC` değişkeni, `AC_PROG_CC` makrosu sayesinde tanımlanıyor.

`AC_OUTPUT` makrosu, `config.status` isminde bir shell programı oluşturup, bu programı çalıştırır.
`Makefile` ve `config.h` dosyalarının oluşması gibi görevler `config.status` tarafından gerçekleştiği
için, bu makronun kullanılması zaruridir.

Devam etmeden önce, biraz toparlayalım. `autoconf` programı `configure.ac` dosyasını okuyarak,
`configure` kabuk programını oluşturuyor. `configure` programının amacı ise, platformun
özelliklerini test edip, Makefile ve config.h dosyalarını oluşturmak.

Autotools içinde merkezi yeri olan diğer program da, `automake`'dir. Bu program, `Makefile.am`
dosyalarındaki tanımlamalara göre, `Makefile.in` dosyaları oluşturur. `Makefile.in` dosyalarının
`configure` betiği tarafından işlenip, `Makefile` dosyalarına dönüştüğünü yukarıda belirmiştim.

Örneğimizdeki `Makefile.am` dosyası, sadece iki satırdan oluşuyor. İlk satırda, `bin_PROGRAMS = hello`
tanımlaması, üç şey belirtiyor. Birincisi, o satırda tanımı yapılan hedefin `bindir` klasörüne yükleneceği,
ikincisi bu hedefin bir program olduğu, üçüncüsü ise bunun adının hello olduğu. Burada `bin_` olarak
belirtilen önek, yükleme yerini belirtir. `bin`, `lib`,
`include`, `data` gibi önceden tanımlı değerleri kullanabilirsiniz. Önekten sonra gelen kısım ise,
hedefin türünü belirtiyor. Hedef türü olarak, şunlardan birini seçmelisiniz; ‘PROGRAMS’, ‘LIBRARIES’,
‘LTLIBRARIES’, ‘LISP’, ‘PYTHON’, ‘JAVA’, ‘SCRIPTS’, ‘DATA’, ‘HEADERS’, ‘MANS’, ve ‘TEXINFOS’. Bunların
isimleri yeterince açıklayıcı. Her hedef türü doğru çalışabilmesi için, çeşitli değişkenlere
ihtiyaç duyar. `PROGRAMS` hedef türü için, `_SOURCES` değişkeni ile, programın hangi C dosyaları
kullanılarak derleneceğini belirttik. Eğer `_SOURCES` ile kaynak dosyalarını belirtmezsek,
`automake` bizim için tahminde bulunacaktır, ama, açıkca belirtmek daha güvenli olur. `configure.ac`
örneğine geri dönerseniz, `AC_PROG_CC` programı ile, geçerli bir C derleyecisi bulmuştuk. `PROGRAMS`
haricindeki diğer hedef türleri için, `AC_PROG_CC` benzeri bir kontrolü `configure.ac`'ye eklemek
gerekebilir. Bunun detayları için, [Automake Belgeleri](https://www.gnu.org/software/automake/manual/automake.html)
yeterince detaylı açıklamalar içeriyor.

Sıra `main.c` dosyasını incelemeye geldi. `main.c` programında, `config.h` header dosyasını kullandık.
Bu noktaya kadar dikkatle okuduysanız, `config.h` dosyasının otomatik olarak oluşturulduğunu anlamışsınızdır.
Bu sayede, `configure` aşamasında tanımlanan yapılandırma değerlerini, C kaynak kodlarımız içinde kullanabiliriz.
Örnek programımızda, `PACKAGE_STRING` değişkenini kullandık. Bu değişken, `AC_INIT` makrosu tarafından
tanımlanıyor. Bizim örneğimizde, `helloworld 1.0` değerini alıyor.

`autoconf` ve `automake` programlardan bahsettik ama, dikkat ederseniz örneğimizde bu iki programı
hiç kullanmadık. Eğer `automake` ve `autoconf` programlarını manuel olarak tetiklemek isterseniz,
`autoheader`, `aclocal`, `autoconf` ve `automake` gibi programları doğru sırada çalıştırmanız gerekiyor.
Manuel çalıştırmak hataya çok müsait olduğu için, `autoreconf` programı, `autotools` içindeki diğer
araçları doğru şekilde çalıştırmaya yarıyor. 

Yeni başlayanlar için, `autotools` çok yıpratıcı olabilir. Şu ana kadar, birçok yeni konseptle
karşılaştınız, ve kafanızın karışmış olması gayet normal. Ama başardığımız şeye dikkat edin.
6 satırlık bir `configure.ac` ve 2 satırlık `Makefile.am` ile, elle yazabileceğimizden
çok daha iyi bir `Makefile` elde ettik. `make install` hedefi sayesinde, programınızı
kurabilirsiniz, `configure` aşamasında programın nereye kurulması gerektiğini seçebilirsiniz,
`make dist` ile `tar.gz` paketi oluşturabilirsiniz. Standart bir GNU/Linux paketinde olmasını
bekleyeceğiniz herşeyi, hem kolayca, hem de hataya fazla yer bırakmayacak bir şekilde elde ettik.
Bu da, Linux paket yöneticileri için, büyük kolaylık demek.

Bu noktada, `autotools` temellerini kavradığınızı varsayıyorum. Birkaç yeni örnek ile,
hem öğrendiklerimiz pekiştireceğiz, hem de `autotools`'un diğer kabiliyetleri hakkında
bilgi sahibi olacağız.

Diyelim ki, Linux üstünde çalışacak bir oyun programladınız. Yazdığınız oyunda grafik
ve ses dosyaları kullanmak isteyeceksiniz. Kullandığınız data dosyaları, farklı linux
sürümlerinde, farklı klasörlere yüklenebilir. Bu örnekte, C programımızın, data
klasöründeki dosyaları bulmasını sağlayacağız.

Öncelikle, `Makefile.am` dosyasına bakalım;

	bin_PROGRAMS = oyun
	oyun_SOURCES = oyun.c
	dist_pkgdata_DATA = esound.wav \
				   another.wav \
				   background.png
	AM_CFLAGS = -DDATADIR=\"$(pkgdatadir)\"

İlk iki satırı zaten biliyorsunuz. Üçüncü satırda, `pkgdata` klasörüne yüklenecek olan,
`DATA` dosyalarını tanımladık. Burada ikinci bir önek olarak `dist` öneki kullandık. `DATA`
dosyalarını `tar.gz` dağıtımına dahil etmek için, `dist` öneki kullanmalısınız. Üçüncü satırda,
C derleyicisinin komut satırına gönderilecek bir argüman tanımladık. Burada kullandığımız `pkgdatadir`,
autoconf/automake tarafından ayarlanan bir değişken. Böylece, C dosyalarımızda kullanılabilecek bir makro
tanımı yapmış olduk. Şimdi, `oyun.c` dosyasına bakalım.

	:::c
	int main(void) {
		IMAGE background = load_image(DATADIR "/background.png")
		return 0;
	}
	
Böylece, programımız ilgili data dosyalarını bulabilecek bir şekilde derlenmiş oldu.

İyice pekiştirmek için, bir örnek daha yapalım. Bu örneğimizde, `configure` betiğinin,
programımızın bazı özelliklerini açıp kapatabilmesini sağlayacağız. Öncelikle, `configure.ac`
dosyasına, aşağıdaki iki satırı ekleyeceğiz.

	AC_ARG_ENABLE([debug], AS_HELP_STRING([--enable-debug]),[ENABLE_DEBUG=$enableval],[ENABLE_DEBUG="no"])
	AS_IF([test "x$ENABLE_DEBUG" = "xyes"], AC_DEFINE(ENABLE_DEBUG, 1, [Enable Debugging])
	
Şimdi, `config.h.in` dosyasına, aşağıdaki satırı eklememiz gerekiyor.

	#undef ENABLE_DEBUG
	
Bundan sonra, `autoreconf -i` ile, configure betiğini yeniden oluşturmak gerekiyor. Böylece, `./configure --enable-debug`
komutu ile, `config.h` dosyasında `#define ENABLE_DEBUG` satırı eklenmesini sağlayabiliriz. Bu makro tanımlı olduğunda,
program çıktı verirken bu makronun varlığını kontrol ederek, ekstra bilgi sunabilir.


Toparlamak gerekirse, `autotools` kullanarak bir build sistemi oluşturmak konusuna yüzeysel bir giriş yaptık. Bu araçlar hakkında
söylenebilecekler malesef bir blog yazısına sığamayacak kadar çok. Eğer projenizde `autotools` kullanmaya karar verirseniz,
sıfırdan `configure.ac` ve `Makefile.am` dosyaları yazmak yerine, yapacağınız projeye benzer bir projenin dosyalarını
kullanarak başlamanız işinizi kolaylaştıracaktır. Eğer [Github'da autotools kullanan projeleri](https://github.com/search?q=configure+extension%3Aac&type=Code)
aratırsanız, karşınıza binlerce sonuç çıkacatır. `automake` ve `autoconf` belgeleri içinde,
kullanabileceğiniz tüm makrolar hakkında bilgi alabilirsiniz.
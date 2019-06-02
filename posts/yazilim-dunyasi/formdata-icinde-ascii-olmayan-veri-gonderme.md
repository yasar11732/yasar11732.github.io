<!--
.. date: 2019-06-02 12:20
.. description: HTTP Multipart/Form-Data isteği gönderirken, ascii dışındaki isimlerin gönderimi konusunda sabit bir standart olmadığı anlaşılıyor.
.. slug: content-disposition-satirinda-us-ascii-harici-karakterler
.. title: Content-Disposition Satırında US-ASCII Harici Karakterler Nasıl Kodlanmalı
-->

Aşağıdaki sıradan dosya yükleme formuna bir göz atalım.

    :::html
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8" />
    </head>
    <body>
        <form method="POST" action="upload.php" enctype="multipart/form-data">
            <input type="file" name="dosya" />
            <input type="submit" value="Gönder">
         </form>
    </body>
    </html>
    
Bu formu doldurup, Gönder'e bastığımızda, multipart/form-data formatında oluşturulmuş bir
HTTP isteği sunucuya gönderilir. Aşağıda, bu formu Google Chrome ile gönderdiğimde,
tarayıcı tarafından oluşturulan isteğin, wireshark ile yakalanmış bir örneğini bulabilirsiniz.


    POST /upload.php HTTP/1.1
    Host: develserver.site
    Connection: keep-alive
    Content-Length: 231
    Cache-Control: max-age=0
    Origin: http://develserver.site
    Upgrade-Insecure-Requests: 1
    DNT: 1
    Content-Type: multipart/form-data; boundary=----WebKitFormBoundaryAGtIBnrsMB1w90XW
    User-Agent: Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36
    Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3
    Referer: http://develserver.site/test.html
    Accept-Encoding: gzip, deflate
    Accept-Language: tr,en;q=0.9

    ------WebKitFormBoundaryAGtIBnrsMB1w90XW
    Content-Disposition: form-data; name="dosya"; filename="post-test.txt"
    Content-Type: text/plain


    Bu dosya örnek olarak oluşturulmuştur.
    ------WebKitFormBoundaryAGtIBnrsMB1w90XW--
    
Buraya kadar herşey normal, ama, yüklenen dosyanın adında, us-ascii ile kodlanamayacak
karakterlerin olduğu durumlarda, `filename` parametresinin nasıl kodlanması gerektiği,
ilk bakışta çok aşikar değil. Yakın geçmişte, Multipart/Form-Data türünde bir HTTP
isteğini oluşturan küçük bir C kütüphanesi yazmayı denediğimden, bu konuyu araştırmaya
koyuldum.

Bu konu ile ilgili çeşitli RFC'ler okumama rağmen, en net cevabı [RFC 2231](https://tools.ietf.org/html/rfc2231)
veriyor gibi görünüyor. Bu RFC'ye göre, karakter kodlaması ve içerik dili bilgisi içeren Content-Disposition ve Content-Type
alanları aşağıdaki şekilde kodlanmalı.

    Content-Disposition: form-data; name="dosya"; filename*=utf-8''Ya%C5%9Far%20Arabac%C4%B1

Bu formatı kısaca incelemek gerekirse, `*=` ile tanımlanan parametreler, opsiyonel olarak
karakter kodlama bilgisi, ve metin dili bilgisi içerebiliyor. Bu parametreler, birbirinden
tek tırnak işareti ile ayrılmış 3 kısımdan oluşuyor. Birinci kısımda, karakter kodlaması,
ikinci kısımda metin dili, üçüncü kısımda ise kodlanmış parametre değeri bulunuyor. Yukarıdaki
örnekte, metin dili ile ilgili kısım boş bırakılmış. Herhangi bir kısım boş bırakılsa dahi,
ayraç olarak kullanılan tek tırnak karakterlerini eksik bırakamıyoruz. İkinci tek tırnak
karakterinden sonra, parametre değeri geliyor. Parametre değeri içerisindeki
aşağıdaki karakterler kodlanmak zorunda.

 - 7 bit ascii (us-ascii) dışındaki karakterler
 - Boşluk
 - Kontrol Karakterleri (ASCII tablosundaki boşluk karakterinden önceki tüm karakterler ve DEL karakteri)
 - Asteriks (*)
 - Tek Tırnak (')
 - Yüzde İşareti (%)
 - Şu karaterlerin hepsi: `()<>@,;:\"/[]?=` (Bu karakterler RFC'de tspecials olarak geçiyor)

Bu karakterleri kodlamak için, % (yüzde) karakterinin ardından, kodlanacak byte'ın hex gösterimi
2 karakterden oluşacak şekilde yazılıyor. Bunu yapan bir mini bir C kütüphanesini [başka bir yazıda](rfc2231.html)
paylaşmıştım.

RFC bu konuda oldukça net olmakla birlikte, ne tüm HTTP istemcileri bunu uyguluyor, ne de
tüm HTTP server'lar bu formattaki bir isteği doğru bir biçimde yorumlayabiliyor.

Bunu test etmek için, yukarıdaki örnek form ile `yaşar arabacı.txt' isimli bir
dosyayı, farklı istemcilerden yükledim. Content-Disposition satırları şu şekilde
oluştu:

    Google Chrome: (parametre değeri utf8 olarak kodlanmıştı)
    Content-Disposition: form-data; name="dosya"; filename="ya..ar arabac...txt"

    Firefox: (parametre değeri utf8 olarak kodlanmıştı)
    Content-Disposition: form-data; name="dosya"; filename="ya..ar arabac...txt"

    İnternet Explorer: (parametre değeri utf8 olarak kodlanmıştı)
    Content-Disposition: form-data; name="dosya"; filename="yaşar arabacı.txt"

    .NET HttpClient
    Content-Disposition: form-data; name=dosya; filename="=?utf-8?B?eWHFn2FyIGFyYWJhY8SxLnR4dA==?="; filename*=utf-8''ya%C5%9Far%20arabac%C4%B1.txt

    Windows için curl (parametre değeri latin-5 olarak kodlanmıştı)
    Content-Disposition: form-data; name="dosya"; filename="ya.ar arabac..txt"

Örnek formu içeren html belgesinden
`<meta charset='utf-8'>` etiketini kaldırırsam, oluşan HTTP isteğinin de
değiştiğini gördüm. Örneğin, Google Chrome ve Firefox'da bu etiketi kaldırıp, formu gönderirsem
Content-Disposition satırı şu şekilde oluştu:

    Content-Disposition: form-data; name="dosya"; filename="ya&#351;ar arabac&#305;.txt"
    
Bu iki tarayıcı, filename kısmını kodlarken, html belgesinin kodlamasını kullanıyor. Eğer
HTML belgesinin kodlamasını tespit edemezse, fallback olarak html-entity kodlaması
kullanıyor. Diğer yandan internet explorer, meta etiketini kaldırsam dahi, utf8
kodlaması kullanmaya devam etti.

Denediğim client'lar içinde, bir tek .NET HttpClient RFC2231'de anlatılan şekilde
HTTP isteği gönderdi. Ancak, diğer yandan, Content-Disposition içindeki 
`filename="=?utf-8?B?eWHFn2FyIGFyYWJhY8SxLnR4dA==?="` kısmı problemli. Bu kısım,
[RFC 2047](https://tools.ietf.org/html/rfc2047)'de bahsedilen, encoded-word betimlemesine
göre yazılmış. Ancak, bu kullanım aynı RFC içinde geçen aşağıdaki 2 kuralı birden ihlal ediyor.

 - An 'encoded-word' MUST NOT appear within a 'quoted-string'.
 - An 'encoded-word' MUST NOT be used in parameter of a MIME Content-Type or Content-Disposition field, or in any structured field body except within a 'comment' or 'phrase'.
 
Parametre değerini bu şekilde kullanmak, hem yaygın kullanıma, hem de RFC standardına aykırı
olduğu için, çoğu server bu .NET HttpClient ile gönderilen ve ASCII ile kodlanamayan
dosya isimlerini yanlış değerlendirecektir (malesef bunu çok acı bir şekilde tecrübe ettim).
Örnek vermek gerekirse, sunucu tarafında çalışan en yaygın dillerden biri olan PHP ile
yazılmış basit bir dosya yükleme betiği aşağıdaki şekilde olabilir.

    :::php
    <?php

    $uploaddir = "uploads/";
    $targetfile = $uploaddir . basename($_FILES["dosya"]["name"]);

    move_uploaded_file($_FILES["dosya"]["tmp_name"], $targetfile);
    
Bu kodu .NET HttpClient ile test ettiğimde, `$_FILES["dosya"]["name"]`
değeri `=?utf-8?B?eWHFn2FyIGFyYWJhY8SxLnR4dA==?=` olarak görünüyordu.
Sonuç olarak, test dosyası, adı ve dosya uzantısı kaybolmuş bir şekilde
kaydedilmiş oldu.

Toparlamak gerekirse, RFC2231 Content-Disposition ve Content-Type
HTTP başlıklarında us-ascii ile kodlanamayacak karakterlerin
nasıl kodlanması gerektiği hakkında bir görüş belirtmiş olsa da,
bu uygulamada pek yaygınlaşmış görünmüyor. Bu nedenle, yeni yazılacak
programların, günümüzün HTTP ekosistemiyle uyumlu çalışabilmesi
için, Content-Type ve Content-Disposition satırlarındaki us-ascii
dışındaki karakterlerin, tırnak içinde, HTML formunun karakter
kodlaması ile kodlanması gerektiğini, HTML formunun olmadığı
veya karakter kodlamasının tespit edilemediği durumlarda ise,
içinde NULL byte barındırmadığı ve neredeyse tüm sunucular
tarafından doğru anlaşılacağı için, utf8 ile kodlanması gerektiğini
düşünüyorum.
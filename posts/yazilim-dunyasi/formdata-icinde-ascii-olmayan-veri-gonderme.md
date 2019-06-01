<!--
.. date: 2019-06-03 17:05
.. description: HTTP Multipart/Form-Data isteği gönderirken, ascii dışındaki isimlerin gönderimi konusunda sabit bir standart olmadığı anlaşılıyor.
.. slug: multipart-form-data-icinde-ascii-olmayan-veri-gonderme
.. title: Multipart/Form-Data ile ASCII Dışındaki Karakterleri Nasıl Kodlarız
-->

Aşağıda, bir server'a dosya göndermek için gerekli HTML formunun asgari bir örneği var;

    :::html
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8" />
    </head>
    <body>
        <form method="POST" action="upload.php" enctype="multipart/form-data">
            <input type="file" name="dosya" />
            <input type="submit" value="Submit">
         </form>
    </body>
    </html>
    
Bu formu doldurup, sunucuya gönderdiğinizde, multipart/form-data formatında oluşturulmuş bir
HTTP isteği sunucuya gönderilir. Gönderilen isteğin detayları, isteği oluşturan yazılıma
göre değişebilir. Aşağıda, bu formu Google Chrome ile gönderdiğimde, tarayıcı tarafından
oluşturulan isteğin, wireshark ile yakalanmış bir örneğini bulabilirsiniz.


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
    
Buraya kadar ilginç birşey yok. Ben buraya kopyalaması kolay olması için, sıradan metin
belgesi ile deneme yaptım. Ancak, ofis belgesi, resim dosyası gibi bir dosyayı göndermiş
olsaydık, dosya içeriği herhangi bir değişiklik yapılmadan http isteği içeriğine kopyalanacaktı.

Peki, diyelim ki dosya adı içerisinde 7 bit ascii ile kodlanamayacak karakterler var. Öyle olsaydı,
Content-Disposition satırını nasıl kodlamak gerekecekti? Bu sorunun cevabını önce RFC'ler içinde,
daha sonra farklı yazılımların uygulamalarına göre inceleyeceğiz.

Bu konunun etrafında dolanan farklı RFC'ler okumama rağmen, konuyla en ilgili olan [RFC 2231](https://tools.ietf.org/html/rfc2231)
gibi görünüyor. Bu RFC'ye göre, karakter kodlaması ve içerik dili bilgisi içeren Content-Disposition ve Content-Type
alanları aşağıdaki şekilde kodlanmalı.

    Content-Disposition: form-data; name="dosya"; filename*=utf-8''Ya%C5%9Far%20Arabac%C4%B1

Bu formatı kısaca incelemek gerekirse, karakter kodlaması ve içerik dili bilgisi kullanan
anahtar/değer çiftlerini eşittir karakteri yerine, *= karakterleri ile birleştiriyoruz. Anahtardan
sonra gelen değer 3 parçadan oluşuyor. Birinci kısımda, karakter kodlaması, ikinci kısımda içeriğin
dili, üçüncü kısımda ise kodlanmış değer bulunuyor. Bu üç alan, tek tırnak karakteri ile
birbirinden ayrılıyor. Yukarıdaki örnekte, içerik dili kısmı boş bırakılmış. Karakter seti
ve dil ile ilgili bilgilerin gereksiz olduğu durumlarda, bu kısımlar boş bırakılabiliyor.
Bu durumda, kısımları ayıran tırnak işaretleri yine de bulunmak zorunda. İçerik kısmında,
7 bit ascii dışındaki tüm karakter ile, aşağıda belirtilen karakterler % formatında kodlanması gerekiyor.
Kodlanması gereken karakterler şunlardır:

 - Boşluk
 - Kontrol Karakterleri (ASCII tablosundaki boşluk karakterinden önceki tüm karakterler ve DEL karakteri)
 - Asteriks (*)
 - Tek Tırnak (')
 - Yüzde İşareti (%)
 - Şu karaterlerin hepsi -> ()<>@,;:\"/[]?= (Bu karakterler RFC'de tspecials olarak geçiyor)
 
% formatında kodlamaya yapmak için, kodlanacak her bir byte için önce % işareti, daha sonra
kodlanacak byte'ın hex gösterimini yazıyoruz. Bunu yapan bir mini bir C kütüphanesini [başka bir yazıda](urlencode-utf8-data.html)
paylaşmıştım.

RFC bu konuda oldukça net olmakla birlikte, ne tüm HTTP istemcileri bunu uyguluyor, ne de
tüm HTTP server'lar bu formattaki bir isteği doğru bir biçimde yorumlayabiliyor.




 

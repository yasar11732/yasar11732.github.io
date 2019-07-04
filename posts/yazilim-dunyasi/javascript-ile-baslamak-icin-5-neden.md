<!--
.. date: 2019/07/04 23:05
.. description: 
.. slug: javascript-ile-baslamak-icin-6-neden
.. title: Programlamaya JavaScript ile Başlamak İçin 6 Neden
-->

Hobi olarak programlama öğrenmek isteyenler veya programlamaya bir yerden başlayıp, zaman içinde
meslek haline getirmek isteyenler, zaman zaman e-posta yolu ile bana ulaşıp, hangi programlama diliyle
başlamaları gerektiği konusunda fikir almak istiyorlar. Bugüne kadar, bazen C, bazen de Python lehine
tavsiye veriyordum. Son zamanlarda, JavaScript'in başlangıç dili olmaya çok müsait olduğu konusunda
giderek kuvvetlenen bir kanaat geliştirdim. Neden böyle düşündüğümü, 6 madde halinde sizlerle paylaşmak istedim.


Şimdi Başlayabilirsiniz
=========================

Eğer bu yazıyı şahsi bilgisayarınızdaki bir web tarayıcı üzerinden okuyorsanız, JavaScript
kodlamaya hemen başlayabilirsiniz. JavaScript ile programlamaya başlamak için, diğer dillerde
olduğu gibi, geliştiricilere yönelik araç/gereçlerin kurulumuna ihtiyacınız yok. Bir metin
düzenleyici (notepad, gedit, textedit gibi) ve web tarayıcı işinizi görecektir.

Platform Özgürlüğü
==================

JavaScript kodlarınız tarayıcıda çalışacağı için, derleyici/yorumlayıcı sürümleri,
işletim sistemi veya işlemci mimarisi
gibi platformlar arasındaki farklılıklarla dikkatinizi bölmenize gerek kalmayacak. Tarayıcılar
arasında da birtakım farklılıklar olabilse de, bunlar öğrenme aşamasında engel olacak konular değil.


Otomatik Hafıza Yönetimi
========================

Bu özellik çoğu modern dil için de geçerli, ama, JavaScript özelinde
tekrar etmekte fayda var. Hafızada yer ayırmak, işi bittikten sonra
hafızayı iade etmek gibi işler JavaScript tarafından kontrol ediliyor.
Ayrıca, kullanacağınız değişkenlerin veri tiplerini de açıkla belirtmek zorunda değilsiniz.
Bu sayede, doğrudan
aritmetik işlemler, fonksiyonlar, döngüler, koşullu ifadeler gibi programlama
konularına geçebilir, hızlı deneme/yanılma süreci sayesinde, kendinizi geliştirebilirsiniz.


Arayüz Programlama
==================

Python/C/Java gibi dillerle programlama öğrenmeye başlayan biri, neredeyse her zaman
konsol programları yaparak başlar. Konsol programlarının gerekliliği ve faydası
tartışmaya açık olmamakla birlikte, programlamaya yeni başlayanların, özellikle de
hobi olarak programlama öğrenmek isteyenlerin hayalinde konsol uygulamaları yapmaktan
ziyade, arayüzü olan interaktif programlar yapmak var. İnternetin programlama dili
olan JavaScript, HTML/CSS ile birlikte, arayüzü olan interaktif uygulamalar yapmaya
çok elverişli. O kadar elverişli ki, bazı masaüstü programları bile, programın içine
gömülü web tarayıcı sayesinde HTML/JavaScript ile kodlanıyor.

Güvenli Ortam
=============

Acemi programcının, bilgisayara zarar verme endişesi taşımasına gerek yok. JavaScript
ile aşırı RAM/CPU kullanımı neticesinde tarayıcıyı veya tüm bilgisayarı kilitleme
riski olsa da, istemeden binlerce dosyayı silme, binlerce dosya oluşturma, bilgisayar
ayarlarında zararlı değişiklikler yapma gibi potansiyel riskler sıfıra yakın.


Diğer Dillerle Benzerliği
=========================

JavaScript grameri, koşullu ifadeleri, döngüleri gibi özellikleri C/C++/Java/C#
gibi dillere çok yakın. JavaScript yazarken edindiğiniz alışkanlıkları, bu dillere
geçerken yanınızda götürebilirsiniz.

İkna Oldum, Şimdi Ne Yapmalıyım?
================================

Boş bir metin dosyası oluşturun, aşağıdaki satırları yapıştırın, ve `.html` uzantısı ile
kaydedin.

	<p id="metin"></p>
	<script>
		document.getElementById("metin").innerText = "Merhaba Dünya!"
	</script>

İlk JavaScript programınızı bir tarayıcıda test etmeye hazırsınız. Belki bugün
programlama maceranızın bir başlangıcı olur.
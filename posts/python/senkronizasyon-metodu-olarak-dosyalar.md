<!--
.. date: 2019-06-04 21:03
.. slug: senkronizasyon-araci-olarak-dosyalar
.. title: Senkronizasyon Aracı Olarak Dosyalar
-->

Zaman zaman, yazdığımız programlarda yapılacak işi, multi-threading veya
multi-processing kullanarak paralel olarak gerçekleştirme ihtiyacı hissederiz.
Bu gibi durumlarda, aynı anda çalışmakta olan işlemleri veya iş parçacıklarını (thread)
belirli bir senkronizasyon içinde çalıştırmamız gerekir. Bu senkronizasyonu sağlamak
için, kullandığımız programlama dilinin bize sağladığı araçları kullanırız.

Geçmişte, python ile yazdığım bir program ile, internetteki çeşitli kaynaklardan
binlerce json belgesi indirmem gerekti. Python'daki threading ve multi-processing
modüllerini kullanmak yerine, değişik birşey yapmak istedim. Bu yazıda kısaca,
aynı anda çalışan işlemleri senkronize etmek için kullandığım metotdan bahsedeceğim.

Python'da dosya açarken, standard `open` fonksiyonunun yanında, `os` modülü içindeki
`open` fonksiyonunu da kullanabiliyoruz. `os` modülü içindeki `open` fonksiyonu ile
dosya açarken, daha fazla kontrole sahibiz. Bunun için, `os.open` fonksiyonunun ikinci
argümanına, dosya açmak için gerekli seçenekleri, bitwise or (|) ile birleştirerek belirtiyoruz. Burada
göstereceğim yöntem için gerekli olan argümanlar `os.O_CREAT` ve `os.O_EXCL`. Bu iki
argüman birlikte kullanıldığında, oluşturmaya çalıştığımız dosya zaten varsa, dosya açma
işlemi başarısız oluyor. Bunu nasıl kullanabileceğimizi görmek için, aşağıdaki örnek
kodları inceleyebiliriz.

    :::python
    import os
    import requests

    s = requests.session()
    flags = os.O_CREAT | os.O_EXCL | os.O_WRONLY
    endpoint = "http://www.example.com/api"

    with open("id-listesi.txt") as f:
        
        for line in f:
            error = False
            _id = line.strip()
            hedef = "indirmeler/%s.json" % _id
            
            try:
                file_handle = os.open(hedef, flags)
            except OSError as e:
                if e.errno == errno.EEXIST:
                    """
                    Dosya zaten var hatası aldık, bu beklediğimiz bir durum
                    bu nedenle, hiçbirşey yapmayacağız
                    """
                    pass
                else:
                    """
                    Dosya var hatası dışında bir hata alırsak,
                    bu hatayı görmek istiyoruz.
                    """
                    raise
            else:  # Herhangi bir hata almadık, indirme işlemine geç
                """
                os modülü bize file-descriptor veriyor. Bu descriptor'u
                kullanarak, standard bir python dosya objesi oluşturmak
                için, os.fdopen fonksiyonunu kullanıyoruz
                """
                with os.fdopen(file_handle, 'w') as file_obj:
                    print "%s indiriliyor" % _id
                    
                    r = s.post(endpoint, json={"id": _id})
                    
                    try:
                        json.dump(r.json(), file_obj)
                    except:
                        error = True
                        
            if error:
                os.remove(hedef)
                        
Yukarıdaki kodları incelerseniz, `multiprocessing` ve `threading` modüllerinden
hiç bahsedilmediğini göreceksiniz. İşin güzelliği de burada. Yukarıdaki programı
yanyana birkaç kere çalıştırırsanız, herhangi bir işlemin indirmeye başladığı
dosyayı bir diğeri indirmeyecektir. İşin püf noktası şöyle; tüm işlemler, bir
linki indirmeye başlamadan önce, o linkin daha önce indirilmeye başlayıp
başlamadığını anlamak için, dosyayı (os.O_CREAT | os.O_EXCL) seçenekleriyle
açmaya çalışıyor. Eğer o dosya daha önce oluşturulmuşsa, bir sonraki linkten
denemeye devam ediyor.

Peki, aşağıdaki şekilde yapmış olsak, işimizi görmez miydi?

    :::python
    if not os.path.isfile(hedef):
        with open(hedef,'w') as f:
            # burada indirme işlemini yap
            
Dürüst olmak gerekirse, eğer çok kritik bir iş yapmıyorsanız, bu yöntem
de işinizi görebilir. Ancak, prensip olarak yanlış, çünkü, race-condition
olarak tabir edilen duruma neden oluyor. Yani, yanyana çalışan işlemlerden
birinin dosyanın olmadığını görmesi ile dosyayı oluşturması arasında
geçen süre zarfında, diğer işlemler de aynı dosyanın olmadığını görüp
oluşturmaya çalışacaklardır. Bu kimi zaman aynı dosyanın iki kere indirilmesine
neden olacak, kimi zaman ise, beklenmedik hatalara yol açacaktır. Bu nedenle, (os.O_CREAT | os.O_EXCL) ile dosyanın
olmaması halinde açılması tek adımda gerçekleştiği için, bu ihtimal
ortadan kalkıyor. Bu şekilde dosya açmak, bir nevi mutex vazifesi görüyor.

Özetle, uygulamadaki basitliğinden ve esnekliğinden dolayı, uygun olduğu durumlarda,
multiprocessing veya threading modüllerini kullanmak yerine, bu yöntemle yazdığım programı
yanyana çalıştırıyorum. Şimdiye kadar herhangi bir sorunla karşılaşmadım. Siz de,
basit uygulamalarınızda buradaki gibi bir yöntem kullanabilirsiniz.
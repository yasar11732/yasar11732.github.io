<!--
.. date: 2018/09/18 22:30:56
.. slug: stack-protector
.. title: GCC'nin Stack Koruması
.. description: GCC'nin -fstack-protector özelliği nasıl çalışır?
-->

C dilinde, fonksiyon argümanları, yerel değişkenler (statik olmayan) ve fonksiyon çağrısı bittiğinde
programın çalışmaya devam edeceği dönüş adresi stack'de tutuluyor. Program hafızasının LIFO mantığıyla
çalışan bu bölümü, fonksiyonların birbiriyle iletişimi ve program
akışının sağlanması açısından önemli. Stack'in kötü niyetli kullanım veya programlama hatası nedeniyle bozulması, programın hatalı
sonuç üretmesi, çökmesi veya yetkisiz işleme izin vermesi gibi çeşitli olumsuzluklara neden olabilir.
Modern C derleyicileri, bu tip olumsuzlukları kontrol altında tutmak için bir yöntem kullanıyor.

Öncelikle sorunu görmek açısından, aşağıdaki programı gcc'nin bu özelliğini
kapatarak (-fno-stack-protector seçeneği ile) derleyip, programın assembly koduna bakalım.

    :::c
    #include <stdio.h>

    void return_input()
    {
        char buffer[12];
        gets(buffer);
        printf("%s\n", buffer);
    }

    int main(int argc, char const *argv[])
    {
        return_input();
        return 0;
    }

Yukarıdaki fonksiyonda, `gets` fonksiyonu komut satırından bir metin alıp, `buffer` içine kaydedecek. Eğer,
okunan metin 11 haneden daha fazla ise, buffer için ayrılan hafızanın dışına yazmaya devam edecek. fno-stack-protector ile
derlenmiş programdaki, `return_input` fonksiyonu nasıl derlenmiş bir göz atalım.

    Dump of assembler code for function return_input:
       0x08048404 <+0>:     push   ebp
       0x08048405 <+1>:     mov    ebp,esp
       0x08048407 <+3>:     sub    esp,0x28
       0x0804840a <+6>:     lea    eax,[ebp-0x14]
       0x0804840d <+9>:     mov    DWORD PTR [esp],eax
       0x08048410 <+12>:    call   0x8048310 <gets@plt>
       0x08048415 <+17>:    lea    eax,[ebp-0x14]
       0x08048418 <+20>:    mov    DWORD PTR [esp],eax
       0x0804841b <+23>:    call   0x8048320 <puts@plt>
       0x08048420 <+28>:    leave
       0x08048421 <+29>:    ret
    End of assembler dump.

Burada herşey normal. İlk iki satır C'deki standart fonksiyon çağırma geleneğine göre `ebp` register'ını ayarlıyor
. Daha sonra stack üzerinde 0x28 (40) byte yer ayrılıyor. Devamı ise,
`gets` ve `puts` fonksiyon çağrıları ve geri dönüş. Programı gdb ile çalıştırıp, buffer ve frame pointer
adreslerine bakabiliriz. Bende, `buffer`, `0xffffd704` adresinde, `ebp` ise, `0xffffd718` adresinde çıktı. Bu durumda,
`buffer` üzerine 0x14 (20) byte yazılması haline, `return_input` fonksiyonu için ayrılmış alanın dışına çıkılacak. Eğer
fonksiyonda başka yerel değişkenler olsaydı, bu değişkenlerin üzerine yazılması ihtimali de ortaya çıkacaktı. Peki,
fonksiyon için ayrılmış alanın dışında ne var? Öncelikle, bu fonksiyonu çağıran fonksiyonun (bu örnekte main) frame pointer'ı ve 
`return_input`'un dönüş adresi (main fonksiyonunda, `return_input` çağrısından sonraki adres), daha sonra, çağıran fonksiyonun yerel değişkenleri veya fonksiyon
çağrısından önce kaydettiği register değerleri olabilir. Bunların üzerine yazılması halinde, en iyi ihtimalle programın geçersiz
bir adrese zıplamaya çalışıp çökmesini umabiliriz. Kötü ihtimal ise, programa verilen kötü niyetle tasarlanmış bir metin yüzünden,
programın yetkisiz/zararlı işlemler yapması.

Aynı fonksiyonun *stack protector* aktif olarak derlenmiş hali aşağıdaki gibi;

    Dump of assembler code for function return_input:
       0x08048464 <+0>:     push   ebp
       0x08048465 <+1>:     mov    ebp,esp
       0x08048467 <+3>:     sub    esp,0x28
       0x0804846a <+6>:     mov    eax,gs:0x14
       0x08048470 <+12>:    mov    DWORD PTR [ebp-0xc],eax
       0x08048473 <+15>:    xor    eax,eax
       0x08048475 <+17>:    lea    eax,[ebp-0x18]
       0x08048478 <+20>:    mov    DWORD PTR [esp],eax
       0x0804847b <+23>:    call   0x8048360 <gets@plt>
       0x08048480 <+28>:    lea    eax,[ebp-0x18]
       0x08048483 <+31>:    mov    DWORD PTR [esp],eax
       0x08048486 <+34>:    call   0x8048380 <puts@plt>
       0x0804848b <+39>:    mov    eax,DWORD PTR [ebp-0xc]
       0x0804848e <+42>:    xor    eax,DWORD PTR gs:0x14
       0x08048495 <+49>:    je     0x804849c <return_input+56>
       0x08048497 <+51>:    call   0x8048370 <__stack_chk_fail@plt>
       0x0804849c <+56>:    leave
       0x0804849d <+57>:    ret
    End of assembler dump.

Burada fonksiyon ilkine göre biraz daha uzun görünüyor. Anlaşılmasına yardımcı olması için, bunun bir
benzeri C ile yazabiliriz.

    #include <stdio.h>
    #include <time.h>
    #include <stdlib.h>

    int canary; 

    struct BoundArray {
        char array[12];
        int  boundary;
    };

    void return_input()
    {
        struct BoundArray buffer;
        buffer.boundary = canary;
        gets(buffer.array);
        puts(buffer.array);

        if(buffer.boundary == canary)
            return;
        
        fprintf(stderr, "==== BUFFER OVERFLOW ====");
        exit(-1);
    }

    int main(int argc, char const *argv[])
    {
        srand(time(NULL));
        canary = rand();
        return_input();
        printf("return_input sonrasi main\n");
        return 0;
    }
    
Yukarıdaki program fno-stack-protector ile derlendiğinde (kendi stack protector mantığımızı yazdığımız için)
eğer komut satırından okunan metin 12 haneden daha az ise, `return_input` fonksiyonundan dönülecek. Eğer alınan
metin array sınırları dışına çıkarsa, `return_input` fonksiyonu asla dönmeyecek ve hata mesajı gösterilip program
sonlandırılacak. Bunu sağlamak için array'in hemen arkasına rastgele bir değer atıyoruz. Fonksiyondan dönmeden önce,
bu değerin aynı kaldığını test ediyoruz. Eğer bu değer değiştiyse, programın güvenilmez olduğuna karar verip,
çalışmayı durduruyoruz.

Yukarıdaki C programına bakarak, assembly çıktısını daha rahat inceleyebiliriz. Assembly çıktısındaki `mov eax,gs:0x14`
satırı, glibc'nin program başlangıcında, `main` çağırılmadan önce ayarladığı rastgele sayıyı (canary) alıyor ve `mov DWORD PTR [ebp-0xc],eax`
satırı bunu array'in sınırına kaydediyor. `gets` ve `puts` çağrısından sonra ise, `mov eax,DWORD PTR [ebp-0xc]` satırı, array
sınırındaki değeri okuyor ve `xor eax,DWORD PTR gs:0x14` satırı bu değerin değişmediğini teyit ediyor. Eğer bir değişme varsa,
glibc tarafından sağlanan `__stack_chk_fail` fonksiyonuna atlıyoruz. Bu fonksiyonun amacı, detaylı hata mesajı yazdırıp, programı
sonlandırmak.


Yukarıdaki örneği, bir de Visual Studio ile derleyip (Visual Studio 14, 32bit cl.exe -Z7 ile)
gcc ile karşılaştırabilriz.

    void return_input()
    {
    011C6B30  push        ebp  
    011C6B31  mov         ebp,esp  
    011C6B33  sub         esp,10h  
    011C6B36  mov         eax,dword ptr [__security_cookie (0121E008h)]  
    011C6B3B  xor         eax,ebp  
    011C6B3D  mov         dword ptr [ebp-4],eax  
        char buffer[12];
        gets(buffer);
    011C6B40  lea         eax,[buffer]  
    011C6B43  push        eax  
    011C6B44  call        _gets (011C3508h)  
    011C6B49  add         esp,4  
        printf("%s\n", buffer);
    011C6B4C  lea         ecx,[buffer]  
    011C6B4F  push        ecx  
        printf("%s\n", buffer);
    011C6B50  push        121E000h  
    011C6B55  call        _printf (011C3990h)  
    011C6B5A  add         esp,8  
    }
    011C6B5D  mov         ecx,dword ptr [ebp-4]  
    011C6B60  xor         ecx,ebp  
    011C6B62  call        @__security_check_cookie@4 (011C30FDh)  
    011C6B67  mov         esp,ebp  
    011C6B69  pop         ebp  
    011C6B6A  ret
    
Visual Studio da gcc gibi, stack üzerinde buffer overflow kontrolü yapıyor.

Toparlamak gerekirse, GCC ve Visual Studio (ve muhtemel diğer modern C derleyicileri)
stack üzerindeki buffer overflow'ların yan etkilerini kontrol altında tutmak için
ekstra kod üretiyorlar. Burada akılda kalması gereken husus, bu yöntemlerin
buffer overflow'u önlemek amaçlı değil, buffer overflow sonucunda programın yanlış
noktaya zıplamasını önlemek. Böylece, en klasik exploit yöntemlerinden birinin uygulanması
bir hayli zorlaşmış oluyor. Yine de, özellikle kritik programlarda, derleyiciden medet ummak yerine, programın
overflow'a izin vermeyecek şekilde tasarlanması veya, C#, Java, Python gibi hafıza
yönetimini kendi yapan bir dilde yazılması çok daha akıllıca bir seçim olacaktır diye düşünüyorum.


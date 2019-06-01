<!--
.. date: 2019-05-29 23:12
.. description: C Programlama Dilinde Wide Char türündeki veriyi url kodlanmış utf8'e dönüştürme
.. slug: urlencode-utf8-data
.. title: C Programlama Dilinde UTF8 Veriyi URL Kodlama
-->

Not: Bu yazıda birtakım eksiklikler olduğu için, yeniden yazma ihtiyacı hissetim. Yazının güncel versiyonuna [buradan](rfc2231.html) ulaşabilirsiniz.

Anahtar Kelimeler
=================

 - C ile UTF8 kodlama
 - C ile URL Kodlama
 - Wide Karakter Array'i MultiByte Karakter Array'ine dönüştürme
 
&nbsp;

    :::C
    #define WINDOWS_LEAN_AND_MEAN
    #include <windows.h>
    #include <stdio.h> // fopen, fclose
    #include <wchar.h>
    
    // 0-15 arası değelerin hex karşılığı
    char base16[] = { '0','1','2','3','4','5','6','7','8','9','A','B','C','D','E','F' };
    
    // LPSTR ==> char *
    // LPWSTR ==> wchar_t *
    LPSTR utf8UrlEncode(LPWSTR s, size_t *len)
    {
        // wide char türündeki veriyi, utf8 olarak kodlamak
        // için windowsda WideCharToMultiByte kullanıyoruz
        // linux için wcstombs fonksiyonu kullanılabilir

        // Gerekli buffer büyüklüğünü öğrenmek için
        // dördüncü parametreye -1 veriyoruz.
        int buffersize = WideCharToMultiByte(65001, 0, s, -1, NULL, 0, NULL, NULL);

        // utf8 olarak veriyi tutmak için gerekli
        // buffer'ı oluştur
        char *utf8data = malloc(buffersize);


        WideCharToMultiByte(65001, 0, s, -1, utf8data, buffersize, NULL, NULL);

        // url kodlama için gerekli buffer büyüklüğünü
        // hesaplıyoruz.
        char *p;
        buffersize = 0;

        for (p = utf8data; *p != '\0'; p++)
        {
            // [0-9a-zA-Z] olduğu gibi kalacak,
            // diger karakterleri % kodlayacağız.
            char c = *p;
            if ((c >= '0' && c <= '9')
                || (c >= 'a' && c <= 'z')
                || (c >= 'A' && c <= 'Z')) {
                buffersize++;
            }
            else {
                buffersize += 3;
            }
        }

        // url kodlama için gerekli buffer
        char *encodedutf8data = malloc(buffersize);

        // url kodlama
        char *p2 = encodedutf8data;
        for (p = utf8data; *p != '\0'; p++)
        {
            // [0-9a-zA-Z] olduğu gibi kalacak,
            // diger karakterleri % kodlayacağız.
            char c = *p;
            if ((c >= '0' && c <= '9')
                || (c >= 'a' && c <= 'z')
                || (c >= 'A' && c <= 'Z')) {
                *p2++ = *p;
            }
            else {
                *p2++ = '%';
                *p2++ = base16[(unsigned char)(*p) >> 4];
                *p2++ = base16[(unsigned char)(*p) & 0xF];
            }
        }

        // kodlanmış datanın büyüklüğü
        *len = buffersize;

        free(utf8data);

        return encodedutf8data;
    }

    int WINAPI wWinMain(HINSTANCE hInstance, HINSTANCE hPrevInstance,
        PWSTR pCmdLine, int nCmdShow)
    {
        FILE *f = fopen("utf8encodetest.txt", "w");
        size_t data_len;

        char *data = utf8UrlEncode(L"Yaşar Arabacı", &data_len);

        fwrite(data, 1, data_len, f);

        fclose(f);
        

        return 0;

    }
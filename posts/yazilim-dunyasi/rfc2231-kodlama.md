<!--
.. date: 2019-06-01 21:10
.. description: RFC2231'de Gösterilen Kodlamanın C Dilinde Uygulanması
.. slug: rfc2231
.. title: RFC2231 Kodlaması
-->

Aşağıda [RFC 2231](https://tools.ietf.org/html/rfc2231) içinde
belirtilen kodlamanın C dilinde yazılmış bir örneğini aşağıda
bulabilirsiniz. `wchar_t` türünüdeki bir string'i utf8 kodlamak
için WIN32 API içindeki `WideCharToMultiByte` fonksiyonunu
kullandım. POSIX sistemlerde bunun yerine `iconv` kullanılabilir.


Anahtar Kelimeler
=================
 - WideCharToMultiByte
 - RFC2231
 - UTF-8
 
&nbsp;

    :::C
    char base16[] = { '0','1','2','3','4','5','6','7','8','9','A','B','C','D','E','F' };
    
    char special_chars[] = {
        ' ', '*', '\'', '%', '(',')','<','>','@',',',
        ';',':','\\','"','/','[',']','?','='
    };

    int should_encode(char c)
    {
        // bir utf8 byte'ı % ile kodlanmalı mı?
        // evet  -> 1
        // hayir -> 0

        // 7 bit üzeri ascii
        if (c < 0)
            return 1;

        // kontrol karakterleri
        if (c < ' ' || c == 127)
            return 1;

        int i;
        for (i = 0; i < sizeof(special_chars); i++)
        {
            if (special_chars[i] == c)
                return 1;
        }

        return 0;
    }

    unsigned long encoded_size(char *utf8data)
    {
        unsigned long size = 0;

        for ( ; *utf8data != '\0'; utf8data++)
        {
            if (should_encode(*utf8data))
                size += 3;
            else
                size += 1;
        }
        
        size += 1; // NULL için

        return size;
    }

    char *utf8Encode(LPWSTR s, int *len)
    {
        char *encoded;
        size_t cchInputLength = wcslen(s) + 1; // +1 null için

        *len = WideCharToMultiByte(65001, 0, s, cchInputLength, NULL, 0, NULL, NULL);
        encoded = malloc(*len);
        WideCharToMultiByte(65001, 0, s, cchInputLength, encoded, *len, NULL, NULL);

        return encoded;
    }

    char *rfc2231_utf8_encode(LPWSTR s, int *len)
    {
        static char _hdr[] = "utf-8\'\'";

        char *utf8encoded = utf8Encode(s, len);
        *len = encoded_size(utf8encoded);
        char *param_encoded = malloc(*len + sizeof(_hdr) - 1);
        
        memcpy(param_encoded, _hdr, sizeof(_hdr) - 1);
        
        char *temp = param_encoded + sizeof(_hdr) - 1;

        char *temp2 = utf8encoded;

        for (; *temp2 != '\0'; temp2++)
        {
            if (should_encode(*temp2))
            {
                *temp++ = '%';
                *temp++ = base16[(unsigned char)(*temp2) >> 4];
                *temp++ = base16[(unsigned char)(*temp2) & 0xF];
            } else {
                *temp++ = *temp2;
            }
        }
        
        *temp = '\0';
        
        free(utf8encoded);

        return param_encoded;
    }
    
    int WINAPI wWinMain(HINSTANCE hInstance, HINSTANCE hPrevInstance,
        PWSTR pCmdLine, int nCmdShow)
    {	
        int buffersize;
        char *encoded = rfc2231_utf8_encode(L"Yaşar Arabacı.png", &buffersize);
        FILE *f = fopen("encodelen.txt", "wb");

        fwrite(encoded, 1, buffersize - 1, f); // -1 NULL için

        fclose(f);


        return 0;
    }
    

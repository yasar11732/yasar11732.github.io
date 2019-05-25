<!--
.. date: 2019/05/25 22:48
.. slug: clipboard
.. title: Windows Api İle Clipboard'dan Metin Okuma
.. description: Windows Api İle Clipboard'dan Metin Okuma
-->

Aşağıda Windows API ile Clipboard'dan metin okuyan küçük bir program bulabilirsiniz.

Anahtar Kelimeler
=================

 - Win32 API ile dosyaya yazma
 - Windowsda Clipboard'dan metin okuma
 - WideCharToMultiByte ile utf8 kodlama

&nbsp;

    :::c++
    int WINAPI wWinMain(HINSTANCE hInstance, HINSTANCE hPrevInstance,
        PWSTR pCmdLine, int nCmdShow)
    {

        HANDLE hOutputFile = CreateFile(L"ClipBoard.txt",
            GENERIC_WRITE,
            FILE_SHARE_READ,
            NULL,
            CREATE_NEW,
            FILE_ATTRIBUTE_NORMAL,
            NULL);

        if (hOutputFile != INVALID_HANDLE_VALUE)
        {

            if (OpenClipboard(NULL))
            {
                // clipboard'daki unicode text'e ulaşmak için handle oluşturuyoruz.	
                HANDLE hData = GetClipboardData(CF_UNICODETEXT);

                if (hData != nullptr)
                {
                    /*
                    Clipboard'daki verileri okumak için, GlobalLock ile kilitlememiz
                    gerekiyor. Böylece, verileri okuabileceğimiz bir pointer elde
                    ediyoruz.
                    */
                    WCHAR *s = static_cast<WCHAR *>(GlobalLock(hData));
                    
                    // veriyi wchar olarak tutacak buffer
                    WCHAR wbuffer[1024];
                    
                    // veriyi utf-8 olarak tutacak buffer
                    char  utf8[4096];

                    // veriyi sonuna kadar okuyup okumadığımz
                    BOOL done = false;

                    // kaçıncı karakteri okuduğumuz
                    int k = 0;

                    while (!done)
                    {
                        int i;

                        // buffer doluncaya veya okunacak veri bitinceye kadar buffer'ı dolduruyoruz.
                        for (i = 0; i < 1024; i++)
                        {
                            WCHAR c = s[k++];
                            if (c == '\0')
                            {
                                done = true;
                                break;
                            }

                            wbuffer[i] = c;
                        }

                        // wchar turundeki karakterleri, utf8 olarak kodlamak için
                        DWORD cbUtf8 = WideCharToMultiByte(CP_UTF8, 0, wbuffer, i, utf8, 4096, NULL, NULL);
                        
                        // utf8 olarak kodlanan veriyi dosyaya yazmak için
                        DWORD cbWritten;
                        WriteFile(hOutputFile, utf8, cbUtf8, &cbWritten, 0);
                    }

                    // kilitlediğimiz handle'ı işimiz bitince bırakıyoruz.
                    GlobalUnlock(hData);
                }

                // Açtığımız clipboard'u kapatıyoruz.
                CloseClipboard();
            }

            // açtığımız dosyayı kapatıyoruz.
            CloseHandle(hOutputFile);
        }
    }
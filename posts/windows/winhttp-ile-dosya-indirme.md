<!--
.. date: 2019/05/26 22:45
.. slug: winhttp-ile-dosya-indirme
.. title: WinHTTP İle İnternetten Dosya İndirme
-->

Merhabalar,

Son günlerde olduğu gibi, windows platformuna özgü küçük programlar paylaşmaya devam ediyorum. Aşağıdaki örnekte, winhttp ile kullanarak
internetten dosya indirme örneği bulabilirsiniz. Bir sonraki yazıda, multipart-formdata türünde bir istek göndermeyi deneyeceğim.

Örneğe geçmeden önce, neden winhttp kullanmaya yöneldiğimden de bahsetmek istiyorum. Windows'da çalışacak minimalist bir
arkaplan uygulaması yapacağım. Bunun için, C#/.NET kullanmak yerine, windows 7/8/10 da halihazırda mevcut olan apilerini
kullamak istiyorum. Böylece, hem windows'un apisini daha yakından tanıma fırsatım olacak, hem de belirli bir .NET runtime'a
bağlı kalmadan, programı çeşitli windows sürümlerine taşıyabileceğimi umut ediyorum.

Anahtar Kelimeler
=================

 - WinHttpOpen
 - WinHttpConnect
 - WinHttpOpenRequest
 - WinHttpSendRequest
 - WinHttpRecieveResponse
 - WinHttpReadData
 - WinHttpCrackUrl nasıl çalışır

&nbsp;

    :::c
    #define WINDOWS_LEAN_AND_MEAN
    #include <windows.h>
    #include <stdio.h> // fopen, fclose
    #include <winhttp.h>
    #include <wchar.h> // _wcsicmp

    #pragma comment(lib,"winhttp")


    void *winhttp_download(HINTERNET hSession, LPCWSTR url, LPDWORD cbDownloaded)
    {
        if (hSession == NULL || url == NULL)
            return NULL;

        /*
        Öncelikle, url'i parçalara ayırarak, scheme
        ve hostname ve path değerlerini elde etmemiz gerekiyor
        bunun için WinHttpCrackUrl fonksiyonunu kullanacağız
        */
        URL_COMPONENTS urlComp;
        WCHAR scheme[10];
        WCHAR host[256];

        // kullanmadan önce, urlComp'u sıfırlamamız gerekiyor
        memset(&urlComp, 0, sizeof(urlComp));

        // bunu yapmak mecburi
        urlComp.dwStructSize = sizeof(urlComp);
        
        // protokol bilgisini tutacak buffer'ın
        // adresini ve büyüklüğünü belirtiyoruz.
        urlComp.lpszScheme = &scheme;
        urlComp.dwSchemeLength = 10;

        // hostname bilgisini tutacak buffer'ın
        // adresini ve büyüklüğünü belirtiyoruz.
        urlComp.lpszHostName = &host;
        urlComp.dwHostNameLength = 256;

        // path bilgisi için ekstra bir buffer
        // kullanmayacağız. WinHttp crack url
        // bize bir pointer sağlaması için,
        // dwUrlPathLength elemanına 0'dan farklı
        // bir değer vermek gerekiyor
        urlComp.dwUrlPathLength = (DWORD)-1;

        if (!WinHttpCrackUrl(url, wcslen(url), 0, &urlComp))
            return NULL;

        INTERNET_PORT port = -1;
        DWORD flags = 0;

        if (_wcsicmp(L"HTTPS",scheme) == 0)
        {
            port = INTERNET_DEFAULT_HTTPS_PORT;
            flags = WINHTTP_FLAG_SECURE;
        }

        if (_wcsicmp(L"HTTP", scheme) == 0)
        {
            port = INTERNET_DEFAULT_HTTP_PORT;
        }

        if (port == -1)
            return NULL;

        HANDLE hConnect = WinHttpConnect(hSession, host, port, 0);
        if (hConnect)
        {
            WCHAR *accept_types[] = { "*/*", NULL };

            HANDLE hRequest = WinHttpOpenRequest(
                hConnect, L"GET", urlComp.lpszUrlPath, NULL,
                WINHTTP_NO_REFERER, accept_types, flags);

            if (hRequest) {
                BOOL bResult = WinHttpSendRequest(hRequest,
                    WINHTTP_NO_ADDITIONAL_HEADERS, 0,
                    WINHTTP_NO_REQUEST_DATA, 0, 0, 0);

                if (bResult) {
                    bResult = WinHttpReceiveResponse(hRequest, 0);
                    if (bResult) {
                        DWORD cap = 4096;
                        char *downloaded_data = malloc(cap);
                        DWORD pos = 0;

                        DWORD dbDownloaded;
                        while (WinHttpReadData(hRequest,
                            downloaded_data + pos, 4096, &dbDownloaded))
                        {
                            if (dbDownloaded == 0)
                                break;

                            pos += dbDownloaded;

                            if (pos + 4097 > cap)
                            {
                                cap = cap * 2;
                                downloaded_data = realloc(downloaded_data, cap);
                            }

                        }
                        *cbDownloaded = pos;
                        return downloaded_data;
                    }
                }

                WinHttpCloseHandle(hRequest);
            }

            WinHttpCloseHandle(hConnect);
        }

        return NULL;

    }
    int WINAPI wWinMain(HINSTANCE hInstance, HINSTANCE hPrevInstance,
        PWSTR pCmdLine, int nCmdShow)
    {
        HINTERNET hSession = NULL,
            hConnect = NULL,
            hRequest = NULL;

        hSession = WinHttpOpen(L"Agent Smith",
            WINHTTP_ACCESS_TYPE_AUTOMATIC_PROXY,
            WINHTTP_NO_PROXY_NAME,
            WINHTTP_NO_PROXY_BYPASS,
            0);
               
        WCHAR *url =
            L"https://ysar.net/windows/windows-api-ile-ekran-goruntusu.html";

        if (hSession)
        {
            FILE *fpOutput = fopen("test.html", "w");
            if (fpOutput)
            {
                DWORD downloaded;
                void *data = winhttp_download(hSession,
                    url, &downloaded);
                fwrite(data, 1, downloaded, fpOutput);
                free(data);
                fclose(fpOutput);
            }

            WinHttpCloseHandle(hSession);
        }
        

        return 0;

    }
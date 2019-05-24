<!--
.. date: 2019/05/24 22:16
.. slug: windows-api-ile-acik-pencereleri-listele
.. title: Windows Api İle Açık Pencereleri Listele
.. description: Açık Pencelerin Listesini Kaydeden Küçük Bir C++/Win32 uygulaması
-->

Merhabalar,

Win32 API'sini öğrenmeye devam ediyorum. Bugün, açık pencelerin başlıklarını bir txt dosyasına kaydeden bir program yazdım. [Bir önceki yazıda](windows-api-ile-ekran-goruntusu.html) da belirttiğim gibi, artık eskisi gibi uzun açıklamalar içeren yazılar yazmaya fırsatım olmuyor. Bu nedenle, referans olarak kullanmak isteyenler için, kodları olduğu
gibi yapıştırıyorum.

Anahtar Kelimeler
=================

 - Win32 API ile dosyaya yazma
 - Windowsda pencerelerin listesini alma
 - Windowsda pencerenin görünür olup olmadığını kontrol etme

&nbsp;

    :::c++
    #define WINDOWS_LEAN_AND_MEAN
    #include <windows.h>
    #include <strsafe.h>

    BOOL CALLBACK EnumWindowsProc(HWND hwnd, LPARAM lParam)
    {
        if (IsWindowVisible(hwnd))
        {
            HANDLE h = reinterpret_cast<HANDLE>(lParam);
            WCHAR buffer[512];
            int size = GetWindowTextW(hwnd, buffer, 512);
            if (size > 3)
            {
                DWORD written;
                StringCchCat(buffer, 512 * sizeof(WCHAR), L"\r\n");
                WriteFile(h, buffer, (size + 2) * sizeof(WCHAR), &written, 0);
            }
        }


        return true;
    }



    int WINAPI wWinMain(HINSTANCE hInstance, HINSTANCE hPrevInstance,
        PWSTR pCmdLine, int nCmdShow)
    {

        HANDLE hOutputFile = CreateFile(L"pencereler.txt",
            GENERIC_WRITE,
            FILE_SHARE_READ,
            NULL,
            CREATE_NEW,
            FILE_ATTRIBUTE_NORMAL,
            NULL);

        if (hOutputFile != INVALID_HANDLE_VALUE)
        {
            EnumWindows(EnumWindowsProc, reinterpret_cast<LPARAM>(hOutputFile));

            CloseHandle(hOutputFile);
        }

        return 0;
    }
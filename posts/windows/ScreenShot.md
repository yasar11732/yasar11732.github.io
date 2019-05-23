<!--
.. date: 2019/05/23 22:16
.. slug: windows-api-ile-ekran-goruntusu
.. title: Windows Api İle Ekran Görüntüsü Yakalamak
.. description: Win32/C++ uygulaması ile, ekran görüntüsü kaydediyoruz.
-->

Merhabalar,

Bu mecrada uzun süredir genel olarak yazılımla ilgili yazılar paylaşıyorum. Uzun süredir bu blogu takip edenlerinizin
tasdik edeceği üzere, blog yazılarım genellikle seçtiğim bir konu hakkındaki detaylı anlatımlardan oluşuyor. Aynı zamanda,
son birkaç yılda, blogumda yayınladığım yazıların sayısının da bir hayli azaldığını da farketmişsinizdir. Bunun nedeni,
artık yazılımla uğraşmıyor olmam değil, detaylı ve açıklayıcı yazılar yazmaya vakit ayıramıyor olmam. Blog konusunda
alıştığım tarzda devam etmeye çalışmanın artık beyhude bir heves olduğuna kanaat getirdim. Bu nedenle, artık blog
yazılarımı makale formatında değil, son zamanlarda uğraştığım konularda kısa günlük yazıları şeklinde yazmayı düşünüyorum.
Bu yazı, bahsettiğim türden yazıların ilki olacak.

Son birkaç gündür, Win32 API'siyle ilgili kendimi geliştirmeye çalışıyorum. C++ ile Win32 API fonksiyonlarını kullanarak,
ekran görüntüsü kaydeden küçük bir program yazdım.

Anahtar Kelimeler
=================

 - C++ ile ekran görüntüsü kaydetme
 - WIC (Windows Imaging Component) ile JPEG dosyası kaydetme
 - Akıllı Pointer Örneği
 - COM objesi oluşturma ve kullanma örneği
 - Windows'da C++ ile ekran boyutu tespit etme

&nbsp;

    :::c++
    #define WIN32_LEAN_AND_MEAN
    #include <windows.h>
    #include <winuser.h>
    #include <objbase.h>
    #include <combaseapi.h>
    #include <wincodec.h>
    #include <wincodecsdk.h>
    #include <atlbase.h>

    HRESULT SaveHBITMAP(HBITMAP bitmap, LPCWSTR filename)
    {

        HRESULT hr = S_OK;
        BITMAP _b;

        GetObject(bitmap, sizeof(BITMAP), &_b);

        CComPtr<IWICImagingFactory> pFactory;
        CComPtr<IWICBitmap> wicbitmap;
        CComPtr<IWICStream> stream;
        CComPtr<IWICBitmapEncoder> encoder;
        CComPtr<IWICBitmapFrameEncode> frame;

        if (SUCCEEDED(hr))
        {
            hr = CoCreateInstance(CLSID_WICImagingFactory, NULL, CLSCTX_INPROC_SERVER, IID_PPV_ARGS(&pFactory));
        }

        if (SUCCEEDED(hr))
        {
            hr = pFactory->CreateBitmapFromHBITMAP(bitmap, NULL, WICBitmapIgnoreAlpha, &wicbitmap);
        }



        if (SUCCEEDED(hr))
        {
            hr = pFactory->CreateStream(&stream);
        }

        if (SUCCEEDED(hr))
        {
            hr = stream->InitializeFromFilename(filename, GENERIC_WRITE);
        }

        if (SUCCEEDED(hr))
        {
            hr = pFactory->CreateEncoder(GUID_ContainerFormatJpeg, NULL, &encoder);
        }

        if (SUCCEEDED(hr))
        {
            hr = encoder->Initialize(stream, WICBitmapEncoderNoCache);
        }

        if (SUCCEEDED(hr))
        {
            hr = encoder->CreateNewFrame(&frame, NULL);
        }

        if (SUCCEEDED(hr))
        {
            hr = frame->Initialize(NULL);
        }

        if (SUCCEEDED(hr))
        {
            hr = frame->SetSize(_b.bmWidth, _b.bmHeight);
        }

        if (SUCCEEDED(hr))
        {
            GUID pixel_format = GUID_WICPixelFormat24bppRGB;
            hr = frame->SetPixelFormat(&pixel_format);
        }

        if (SUCCEEDED(hr))
        {
            hr = frame->WriteSource(wicbitmap, NULL);
        }

        if (SUCCEEDED(hr))
        {
            hr = frame->Commit();
        }

        if (SUCCEEDED(hr))
        {
            hr = encoder->Commit();
        }

        return hr;
    }

    int WINAPI wWinMain(HINSTANCE hInstance, HINSTANCE hPrevInstance, PWSTR pCmdLine, int nCmdShow)
    {
        HRESULT hr = S_OK;
        hr = CoInitializeEx(NULL, COINIT_APARTMENTTHREADED | COINIT_DISABLE_OLE1DDE);
        if (FAILED(hr))
            return 0;

        DEVMODE d;

        if (EnumDisplaySettings(NULL, ENUM_CURRENT_SETTINGS, &d))
        {



            HWND desktop = GetDesktopWindow();
            HDC desktopDC = GetDC(desktop);
            HDC captureDC = CreateCompatibleDC(desktopDC);
            HBITMAP hCaptureBitmap = CreateCompatibleBitmap(desktopDC, d.dmPelsWidth, d.dmPelsHeight);

            SelectObject(captureDC, hCaptureBitmap);

            BitBlt(captureDC, 0, 0, d.dmPelsWidth, d.dmPelsHeight, desktopDC, 0, 0, SRCCOPY | CAPTUREBLT);

            SaveHBITMAP(hCaptureBitmap, L"My New ScreenShot.jpg");

            ReleaseDC(desktop, desktopDC);
            DeleteDC(captureDC);
            DeleteObject(hCaptureBitmap);

            
        }

        CoUninitialize();
        return 0;
    }
    

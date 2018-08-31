<!-- 
.. description: C Programlama Dilinde Basit Bir Şablon Programı
.. date: 2018/08/31 00:15
.. title: C ile Komut Okuyan ve Şablon Dolduran Program
.. slug: sablon-doldurucu
-->

Malum, bir aydan daha fazla süredir boş vakitlerimde Euler Problemlerinin çözümüyle uğraşıyordum. [13.](/euler/euler-13.html) ve [16.](/euler/euler-16)
Euler problemlerinin çözümünü, problemin varoluş gayesine uygun olsun diye C Programla Dili ile yaptım. Bu esnada, C ile program yazma konusunda nostaljik bir keyif
aldım. Birkaç gündür C ile değişik küçük programlar deniyorum. Yaptığım programlardan birini, blog yazımda paylaşayım diye düşündüm. Aşağıdaki program `{*` ve `*}`
tagları arasındaki komutları çalıştırıp, metin belgesinde yerine koyan basit bir şablon doldurma programı. Girdisini standart girdiden alıyor, çıktısını standart çıktıya veriyor.

    :::c
    #include <stdio.h>
    #include <stdlib.h>
    #include <sys/types.h>
    #include <sys/wait.h>
    #include <unistd.h>

    /* longest possible command */
    #define BUFFERSIZE 4096

    typedef struct _parser {
        char data[BUFFERSIZE];
        int num_data;

        char *args[32];
        int num_args;

        int argc;
        const char const **argv;

        void (*state)(struct _parser *);

    } Parser;

    void parser_double_quotes(Parser *);
    void parser_single_quotes(Parser *);
    void parser_normal_state(Parser *);
    void parser_seen_asteriks(Parser *);
    void parser_end_of_token(Parser *);

    void parser_variable_state(Parser *p)
    {
        int position = 0;
        int c;

        for(c = getc(stdin); c >= '0' && c <='9'; c=getc(stdin))
        {
            position = 10*position + (c - '0');
        }

        ungetc(c, stdin);

        p->args[p->num_args] = p->args[p->num_args-1];
        p->args[p->num_args-1] = p->argv[position];
        p->num_args++;

        p->state = parser_normal_state;
    }

    void parser_finalize(Parser *p)
    {

        if(p->data[p->num_data]  != '\0')
        {
            p->data[p->num_data] = '\0';
        } else {
            p->num_args--;
        }

        p->args[p->num_args] = NULL;
        p->state = 0;

    }

    void parser_seen_asteriks(Parser *p)
    {
        int c = getc(stdin);
        switch(c)
        {
            case '}':
                parser_finalize(p);
                return;
            default:
                p->data[p->num_data++] = '*';
                ungetc(c, stdin);
                p->state = parser_normal_state;
                return;
        }
    }

    void parser_single_quotes(Parser *p)
    {
        int c = getc(stdin);
        switch(c)
        {
            case EOF:
                fprintf(stderr, "Invalid Input");
                exit(-1);
            case '\'':
                p->state = parser_end_of_token;
                return;
            default:
                p->data[p->num_data++] = c;
        }
    }

    void parser_double_quotes(Parser *p)
    {
        int c = getc(stdin);
        switch(c)
        {
            case EOF:
                fprintf(stderr, "Invalid Input");
                exit(-1);
            case '"':
                p->state = parser_end_of_token;
                return;
            default:
                p->data[p->num_data++] = c;
        }
    }

    void parser_end_of_token(Parser *p)
    {

        if(p->num_data == 0 || p->data[p->num_data-1] == '\0')
        {
            // empty token, return to normal state;
            p->state = parser_normal_state;
            return;
        }

        p->data[p->num_data++] = '\0';

        p->args[p->num_args++] = &(p->data[p->num_data]);
    }

    void parser_normal_state(Parser *p)
    {
        int c = getc(stdin);
        switch(c)
        {
            case '\\':
                p->data[p->num_data++] = getc(stdin);
                return;
            case ' ':
                p->state = parser_end_of_token;
                return;
            case '*':
                p->state = parser_seen_asteriks;
                return;
            case '"':
                p->state = parser_double_quotes;
                return;
            case '\'':
                p->state = parser_single_quotes;
                return;
            case '$':
                p->state = parser_variable_state;
                return;
            case EOF:
                fprintf(stderr, "Invalid Input");
                exit(-1);
            default:
                p->data[p->num_data++] = c;
        }
    }

    void expand_command(Parser *p)
    {
        pid_t processId;
        int status;
        
        // initialize parser state
        p->num_data = 0;
        p->num_args = 0;

        p->args[p->num_args++] = &(p->data[0]);
        p->state = parser_normal_state;
        
        while(p->state)
        {
            p->state(p);
        }

        processId = fork();

        if(processId < 0)
        {
            exit(-1);
        } else if(processId == 0)
        {
            execvp(p->args[0], p->args);
        } else {
            wait(&status);
            if(status != 0)
            {
                fprintf(stderr, "Subprocess failed.");
                exit(-1);
            }
        }

    }

    int main(int argc, char const *argv[])
    {
        int c;
        Parser p;
        p.argc = argc;
        p.argv = argv;

        while((c = getc(stdin)) != EOF)
        {
            if(c == '{')
            {
                int n = getc(stdin);
                if(n == '*')
                {
                    fflush(stdout);
                    expand_command(&p);
                } else if(n == EOF){
                    putchar(c);
                    break;
                } else {
                    putchar(c);
                    putchar(n);
                }
            } else {
                putchar(c);
            }   
        }

        return 0;
    }
    
Programın iki ayrı modu var. Normal modunda standart girdiden okuduğu karakterleri, standart çıktıya kopyalıyor. Eğer `{*` tagı görürse,
bir Sonlu Durum Makinesi (En. State Machine) olarak çalışıp, komutu argümanlarına ayırıyor. Eğer `$2` gibi bir işaret görürse, komut
satırından aldığı değişkeni komuta argüman olarak veriyor. Tek ve Çift tırnak içerisinde ise, boşluklara ve diğer özel karakterlere
dikkat etmeden ayrıştırma yapıyor. Örneğin, bu programa aşağıdaki metin belgesini girdi olarak verirsek;

    Merhaba, ben {* whoami *}.
    Şu an tarih: {* date +"%d-%m-%y" *}

    Alın size bir inek

    {* cowsay "Blog yazisinda bir inek mi?" *}

    Bu da bir alıntı.
    {* fortune *}

    Komut satırından aldığım argümanları, çağırdım programlarda kullanabiliyorum.

    {* echo "yasar arabaci"  $1 $0 *}

şu hale dönüştürebiliyor;

    Merhaba, ben vagrant
    .
    Şu an tarih: 30-08-18


    Alın size bir inek

     _____________________________
    < Blog yazisinda bir inek mi? >
     -----------------------------
            \   ^__^
             \  (oo)\_______
                (__)\       )\/\
                    ||----w |
                    ||     ||


    Bu da bir alıntı.
    Alimony and bribes will engage a large share of your wealth.


    Komut satırından aldığım argümanları, çağırdım programlarda kullanabiliyorum.

    yasar arabaci test1 ./command_expand
    

Bu programı kendi statik site oluşturucu programımı yapma gayesi ile yazmıştım. O projede ne kadar ileri giderim şimdilik bilemiyorum.
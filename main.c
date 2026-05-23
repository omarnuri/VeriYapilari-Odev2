/*
 * BLM2512 Veri Yapilari ve Algoritmalar - Odev 2
 * Konu: Stack ve Queue
 *
 * Cagri merkezi simulasyonu: T adet musteri temsilcisi olan bir
 * cagri merkezinde musteri aramalari, aktarmalar ve temsilci bitis
 * olaylari islenir. Bekleme sirasi Queue (FIFO), aktarma alani
 * Stack (LIFO) veri yapisi ile gerceklestirilmistir.
 *
 * Kullanim: ./program <girdi_dosyasi>
 */

#include <stdio.h>
#include <stdlib.h>

/* Olay yapisi: her satir icin zaman, tip ve arguman bilgisini tutar */
struct Event {
    int zaman; /* Olayin gerceklestigi zaman adimi */
    int tip;   /* Olay tipi: 1=musteri aramasi, 2=temsilci bitis, 3=aktarma */
    int arg;   /* Tip 1/3: musteriId, Tip 2: sicilNo */
};

/* Bagli liste dugumu: kuyruk ve yigin icin ortak dugum yapisi */
struct Node {
    int musteriId;      /* Dugumde saklanan musteri kimligi */
    struct Node* next;  /* Sonraki dugume gosterici */
};

/* Kuyruk yapisi: FIFO duzeni ile normal bekleme sirasini temsil eder */
struct Queue {
    struct Node* front; /* Kuyrugun on elemani */
    struct Node* rear;  /* Kuyrugun arka elemani */
};

/* Yigin yapisi: LIFO duzeni ile aktarma bekleme alanini temsil eder */
struct Stack {
    struct Node* top; /* Yiginin ust elemani */
};

/* Musteri temsilcisi yapisi: mesgulluk durumu ve mevcut musteri bilgisi */
struct Representative {
    int isBusy;          /* 0: bos, 1: mesgul */
    int currentMusteriId; /* Hizmet verilen musteri kimligi (-1 ise bos) */
};

/*
 * @brief Kuyruga yeni bir musteri ekler. Musteri kuyrugun arkasina
 * eklenerek FIFO duzeni saglanir.
 *
 * @param q  islem yapilacak kuyruk gostericisi
 * @param id kuyruya eklenecek musteri kimligi
 *
 * @return
 */
void enqueue(struct Queue* q, int id) {
    struct Node* newNode = (struct Node*)malloc(sizeof(struct Node));
    newNode->musteriId = id;
    newNode->next = NULL;

    if (q->rear == NULL) { /* Kuyruk bos ise hem on hem arka yeni dugumu gosterir */
        q->front = newNode;
        q->rear = newNode;
    } else { /* Kuyruk dolu ise yeni dugum arkaya eklenir */
        q->rear->next = newNode;
        q->rear = newNode;
    }
}

/*
 * @brief Kuyruktan on taraftaki musterilyi cikarir ve kimligini dondurur.
 * FIFO duzeni korunarak on eleman alinir.
 *
 * @param q islem yapilacak kuyruk gostericisi
 *
 * @return cikartilan musteri kimligi; kuyruk bos ise -1
 */
int dequeue(struct Queue* q) {
    int id = -1; /* Bos kuyruk durumu icin varsayilan deger */
    struct Node* temp;

    if (q->front != NULL) { /* Kuyruk bos degilse on eleman cikarilir */
        temp = q->front;
        id = temp->musteriId;
        q->front = q->front->next;

        if (q->front == NULL) { /* Kuyruk bosaldiysa arka gostericiyi de sifirla */
            q->rear = NULL;
        }
        free(temp);
    }
    return id;
}

/*
 * @brief Kuyrugun bos olup olmadigini kontrol eder.
 *
 * @param q kontrol edilecek kuyruk gostericisi
 *
 * @return kuyruk bos ise 1, degilse 0
 */
int isQueueEmpty(struct Queue* q) {
    int empty = 0;
    if (q->front == NULL) { /* On gosterici NULL ise kuyruk bos demektir */
        empty = 1;
    }
    return empty;
}

/*
 * @brief Yigina yeni bir musteri ekler. Musteri yiginin ustune
 * eklenerek LIFO duzeni saglanir.
 *
 * @param s  islem yapilacak yigin gostericisi
 * @param id yigina eklenecek musteri kimligi
 *
 * @return
 */
void push(struct Stack* s, int id) {
    struct Node* newNode = (struct Node*)malloc(sizeof(struct Node));
    newNode->musteriId = id;
    newNode->next = s->top; /* Yeni dugum mevcut ust elemani gosterir */
    s->top = newNode;
}

/*
 * @brief Yigin ustundeki musterilyi cikarir ve kimligini dondurur.
 * LIFO duzeni korunarak ust eleman alinir.
 *
 * @param s islem yapilacak yigin gostericisi
 *
 * @return cikartilan musteri kimligi; yigin bos ise -1
 */
int pop(struct Stack* s) {
    int id = -1; /* Bos yigin durumu icin varsayilan deger */
    struct Node* temp;

    if (s->top != NULL) { /* Yigin bos degilse ust eleman cikarilir */
        temp = s->top;
        id = temp->musteriId;
        s->top = s->top->next;
        free(temp);
    }
    return id;
}

/*
 * @brief Yiginin bos olup olmadigini kontrol eder.
 *
 * @param s kontrol edilecek yigin gostericisi
 *
 * @return yigin bos ise 1, degilse 0
 */
int isStackEmpty(struct Stack* s) {
    int empty = 0;
    if (s->top == NULL) { /* Ust gosterici NULL ise yigin bos demektir */
        empty = 1;
    }
    return empty;
}

/*
 * @brief Programin giris noktasi. Komut satiri argumani olarak verilen
 * dosyayi okur, olaylari zamansal siraya gore isleyerek her basarili
 * musteri-temsilci baglanmasini ekrana yazdirir.
 *
 * @param argc komut satiri arguman sayisi
 * @param argv komut satiri argumanlari; argv[1] girdi dosyasinin yoludur
 *
 * @return 0 basarili cikis, 1 hata durumu
 */
int main(int argc, char* argv[]) {
    int T = 0, O = 0; /* T: temsilci sayisi, O: olay sayisi */
    int i, j;         /* dongu indisleri */
    struct Event* events;        /* dinamik olay dizisi */
    struct Representative* reps; /* dinamik temsilci dizisi */
    struct Queue q;   /* normal bekleme sirasi (FIFO) */
    struct Stack s;   /* aktarma bekleme alani (LIFO) */
    int eventType;    /* islenen olayin tipi (1, 2 veya 3) */
    int eventTime;    /* islenen olayin zamani */
    int eventArg;     /* islenen olayin argumani (musteriId veya sicilNo) */
    int freeRepIndex; /* bos bulunan temsilcinin indisi */
    int nextMusteriId; /* siradaki musterinin kimligi */
    int foundRep;     /* aktarilan musteriye hizmet veren temsilcinin indisi */
    FILE* fp;         /* girdi dosyasi gostericisi */

    /* Komut satiri argumani kontrolu */
    if (argc < 2) {
        printf("Kullanim: %s <girdi_dosyasi>\n", argv[0]);
        return 1;
    }

    /* Girdi dosyasini goreli yol ile ac */
    fp = fopen(argv[1], "r");
    if (fp == NULL) { /* Dosya acilaamazsa hata mesaji yazdirilir */
        printf("Dosya acilamadi: %s\n", argv[1]);
        return 1;
    }

    /* Kuyruk ve yigin baslangic degerlerini sifirla */
    q.front = NULL;
    q.rear = NULL;
    s.top = NULL;

    /* Temsilci sayisi ve olay sayisini dosyadan oku */
    fscanf(fp, "%d", &T);
    fscanf(fp, "%d", &O);

    /* Olay ve temsilci dizileri icin dinamik bellek ayir */
    events = (struct Event*)malloc(O * sizeof(struct Event));
    reps = (struct Representative*)malloc(T * sizeof(struct Representative));

    /* Tum temsilcileri baslangicta bos olarak ayarla */
    for (i = 0; i < T; i++) {
        reps[i].isBusy = 0;
        reps[i].currentMusteriId = -1;
    }

    /* Tum olaylari dosyadan oku ve diziye yaz */
    for (i = 0; i < O; i++) {
        fscanf(fp, "%d %d %d", &events[i].zaman, &events[i].tip, &events[i].arg);
    }

    /* Dosyayi kapat */
    fclose(fp);

    /* Olaylari zamansal siraya gore isle */
    for (i = 0; i < O; i++) {
        eventType = events[i].tip;
        eventTime = events[i].zaman;
        eventArg  = events[i].arg;

        if (eventType == 1) {
            /* Tip 1: Musteri arama olayi
               Bos temsilci varsa en kucuk sicil numaraliyla baglanir,
               yoksa musteri normal bekleme sirasina (queue) alinir. */
            freeRepIndex = -1;
            for (j = 0; j < T; j++) {
                if (reps[j].isBusy == 0 && freeRepIndex == -1) { /* ilk bos temsilci secilir */
                    freeRepIndex = j;
                }
            }

            if (freeRepIndex != -1) { /* Bos temsilci bulundu: musteri baglanir */
                reps[freeRepIndex].isBusy = 1;
                reps[freeRepIndex].currentMusteriId = eventArg;
                printf("%d %d %d\n", eventTime, eventArg, freeRepIndex);
            } else { /* Tum temsilciler mesgul: musteri siraya alinir */
                enqueue(&q, eventArg);
            }

        } else if (eventType == 2) {
            /* Tip 2: Temsilci bitis olayi
               Temsilci serbest kalir; once aktarma alani (stack), sonra
               normal kuyruk kontrol edilerek yeni musteri atanir. */
            reps[eventArg].isBusy = 0;
            reps[eventArg].currentMusteriId = -1;

            if (!isStackEmpty(&s)) { /* Aktarma alaninda bekleyen varsa oncelik ona verilir (LIFO) */
                nextMusteriId = pop(&s);
                reps[eventArg].isBusy = 1;
                reps[eventArg].currentMusteriId = nextMusteriId;
                printf("%d %d %d\n", eventTime, nextMusteriId, eventArg);
            } else if (!isQueueEmpty(&q)) { /* Normal bekleme sirasinda bekleyen varsa (FIFO) */
                nextMusteriId = dequeue(&q);
                reps[eventArg].isBusy = 1;
                reps[eventArg].currentMusteriId = nextMusteriId;
                printf("%d %d %d\n", eventTime, nextMusteriId, eventArg);
            }

        } else if (eventType == 3) {
            /* Tip 3: Musteri aktarma talebi olayi
               Musteri aktarma bekleme alanina (stack) alinir ve hizmet
               veren temsilci serbest birakilir. Serbest kalan temsilci
               once aktarma alanindan, yoksa kuyruktan yeni musteri alir. */
            foundRep = -1;
            for (j = 0; j < T; j++) {
                if (reps[j].isBusy == 1 && reps[j].currentMusteriId == eventArg) { /* musteriyi hizmet veren temsilci aranir */
                    foundRep = j;
                }
            }

            if (foundRep != -1) { /* Musteri bulunan temsilci yigina eklenir ve serbest birakilir */
                push(&s, eventArg);
                reps[foundRep].isBusy = 0;
                reps[foundRep].currentMusteriId = -1;

                if (!isStackEmpty(&s)) { /* Aktarma alaninda bekleyen varsa oncelik ona verilir (LIFO) */
                    nextMusteriId = pop(&s);
                    reps[foundRep].isBusy = 1;
                    reps[foundRep].currentMusteriId = nextMusteriId;
                    printf("%d %d %d\n", eventTime, nextMusteriId, foundRep);
                } else if (!isQueueEmpty(&q)) { /* Normal bekleme sirasinda bekleyen varsa (FIFO) */
                    nextMusteriId = dequeue(&q);
                    reps[foundRep].isBusy = 1;
                    reps[foundRep].currentMusteriId = nextMusteriId;
                    printf("%d %d %d\n", eventTime, nextMusteriId, foundRep);
                }
            }
        }
    }

    /* Kalan kuyruk dugumlerini bellekten temizle */
    while (!isQueueEmpty(&q)) {
        dequeue(&q);
    }
    /* Kalan yigin dugumlerini bellekten temizle */
    while (!isStackEmpty(&s)) {
        pop(&s);
    }

    /* Dinamik olarak ayrilmis bellegi serbest birak */
    free(events);
    free(reps);

    return 0;
}

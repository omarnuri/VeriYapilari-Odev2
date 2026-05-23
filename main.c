/*
 * BLM2512 Veri Yapilari ve Algoritmalar - Odev 2
 * Konu: Stack ve Queue
 *
 * Problem: Cagri merkezi simulasyonu.
 * T adet musteri temsilcisi olan bir cagri merkezinde
 * musteri aramalari, aktarmalar ve temsilci bitis olaylari
 * islenir. Bekleme sirasi Queue (FIFO), aktarma alani
 * Stack (LIFO) veri yapisi ile gercekllestirilmistir.
 *
 * Kullanim: ./program <girdi_dosyasi>
 */

#include <stdio.h>
#include <stdlib.h>

/* Olay yapisi: her satir icin zaman, tip ve arguman bilgisini tutar */
struct Event {
    int zaman; /* Olayin gerceklestigi zaman */
    int tip;   /* Olay tipi: 1=arama, 2=bitis, 3=aktarma */
    int arg;   /* Tip 1/3 icin musteriID, tip 2 icin sicilNo */
};

/* Bagli liste dugumu: kuyruk ve yigin icin ortak dugum yapisi */
struct Node {
    int musteriID;      /* Dugugde saklanan musteri kimligi */
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
    int isBusy;           /* 0: bos, 1: mesgul */
    int currentMusteriID; /* Hizmet verilen musteri kimligi (-1 ise bos) */
};

/*
 * enqueue: Kuyruga yeni bir musteri ekler (FIFO - arka uca ekleme).
 * q  : islem yapilacak kuyruk gostericisi
 * id : kuyruya eklenecek musteri kimligi
 */
void enqueue(struct Queue* q, int id) {
    struct Node* newNode = (struct Node*)malloc(sizeof(struct Node));
    newNode->musteriID = id;
    newNode->next = NULL;

    if (q->rear == NULL) {
        /* Kuyruk bos ise hem on hem arka yeni dugumu gosterir */
        q->front = newNode;
        q->rear = newNode;
    } else {
        q->rear->next = newNode;
        q->rear = newNode;
    }
}

/*
 * dequeue: Kuyruktan on taraftaki musterilyi cikarir ve kimligini dondurur.
 * q      : islem yapilacak kuyruk gostericisi
 * Donus  : cikartilan musteri kimligi; kuyruk bos ise -1
 */
int dequeue(struct Queue* q) {
    int id = -1;
    struct Node* temp;

    if (q->front != NULL) {
        temp = q->front;
        id = temp->musteriID;
        q->front = q->front->next;

        if (q->front == NULL) {
            /* Kuyruk bosaldiysa arka gostericiyi de sifirla */
            q->rear = NULL;
        }
        free(temp);
    }
    return id;
}

/*
 * isQueueEmpty: Kuyrugun bos olup olmadigini kontrol eder.
 * q     : kontrol edilecek kuyruk gostericisi
 * Donus : kuyruk bos ise 1, degilse 0
 */
int isQueueEmpty(struct Queue* q) {
    int empty = 0;
    if (q->front == NULL) {
        empty = 1;
    }
    return empty;
}

/*
 * push: Yigina yeni bir musteri ekler (LIFO - ust uca ekleme).
 * s  : islem yapilacak yigin gostericisi
 * id : yigina eklenecek musteri kimligi
 */
void push(struct Stack* s, int id) {
    struct Node* newNode = (struct Node*)malloc(sizeof(struct Node));
    newNode->musteriID = id;
    newNode->next = s->top;
    s->top = newNode;
}

/*
 * pop: Yigin ustundeki musterilyi cikarir ve kimligini dondurur.
 * s      : islem yapilacak yigin gostericisi
 * Donus  : cikartilan musteri kimligi; yigin bos ise -1
 */
int pop(struct Stack* s) {
    int id = -1;
    struct Node* temp;

    if (s->top != NULL) {
        temp = s->top;
        id = temp->musteriID;
        s->top = s->top->next;
        free(temp);
    }
    return id;
}

/*
 * isStackEmpty: Yiginin bos olup olmadigini kontrol eder.
 * s     : kontrol edilecek yigin gostericisi
 * Donus : yigin bos ise 1, degilse 0
 */
int isStackEmpty(struct Stack* s) {
    int empty = 0;
    if (s->top == NULL) {
        empty = 1;
    }
    return empty;
}

/*
 * main: Programin giris noktasi.
 * Komut satiri argumani olarak verilen dosyayi okur,
 * olaylari isleyerek her basarili baglanmayi ekrana yazdirir.
 * argc : komut satiri arguman sayisi
 * argv : komut satiri argumanlari (argv[1] = girdi dosya yolu)
 */
int main(int argc, char* argv[]) {
    int T = 0, O = 0;
    int i, j;
    struct Event* events;
    struct Representative* reps;
    struct Queue q;
    struct Stack s;
    int eventType, eventTime, eventArg;
    int freeRepIndex;
    int nextMusteriID;
    int foundRep;
    FILE* fp;

    /* Komut satiri argumani kontrolu */
    if (argc < 2) {
        printf("Kullanim: %s <girdi_dosyasi>\n", argv[0]);
        return 1;
    }

    /* Girdi dosyasini ac */
    fp = fopen(argv[1], "r");
    if (fp == NULL) {
        printf("Dosya acilamadi: %s\n", argv[1]);
        return 1;
    }

    /* Kuyruk ve yigin baslangic degerlerini sifirla */
    q.front = NULL;
    q.rear = NULL;
    s.top = NULL;

    /* Temsilci sayisi ve olay sayisini oku */
    fscanf(fp, "%d", &T);
    fscanf(fp, "%d", &O);

    /* Dinamik bellek ayir */
    events = (struct Event*)malloc(O * sizeof(struct Event));
    reps = (struct Representative*)malloc(T * sizeof(struct Representative));

    /* Tum temsilcileri bos olarak baslat */
    for (i = 0; i < T; i++) {
        reps[i].isBusy = 0;
        reps[i].currentMusteriID = -1;
    }

    /* Tum olaylari dosyadan oku */
    for (i = 0; i < O; i++) {
        fscanf(fp, "%d %d %d", &events[i].zaman, &events[i].tip, &events[i].arg);
    }

    /* Dosyayi kapat */
    fclose(fp);

    /* Olaylari sirali sekilde isle */
    for (i = 0; i < O; i++) {
        eventType = events[i].tip;
        eventTime = events[i].zaman;
        eventArg  = events[i].arg;

        if (eventType == 1) {
            /* Tip 1: Musteri arama - bos temsilci varsa bagla, yoksa siraya al */
            freeRepIndex = -1;
            for (j = 0; j < T; j++) {
                if (reps[j].isBusy == 0 && freeRepIndex == -1) {
                    freeRepIndex = j; /* En kucuk sicil numarali bos temsilci */
                }
            }

            if (freeRepIndex != -1) {
                /* Bos temsilci bulundu: musterilyi bagla */
                reps[freeRepIndex].isBusy = 1;
                reps[freeRepIndex].currentMusteriID = eventArg;
                printf("%d %d %d\n", eventTime, eventArg, freeRepIndex);
            } else {
                /* Tum temsilciler mesgul: musterilyi bekleme sirasina ekle */
                enqueue(&q, eventArg);
            }

        } else if (eventType == 2) {
            /* Tip 2: Temsilci gorusmesini bitirdi - once aktarma alani, sonra kuyruk */
            reps[eventArg].isBusy = 0;
            reps[eventArg].currentMusteriID = -1;

            if (!isStackEmpty(&s)) {
                /* Aktarma alaninda bekleyen var: yigin oncelikli (LIFO) */
                nextMusteriID = pop(&s);
                reps[eventArg].isBusy = 1;
                reps[eventArg].currentMusteriID = nextMusteriID;
                printf("%d %d %d\n", eventTime, nextMusteriID, eventArg);
            } else if (!isQueueEmpty(&q)) {
                /* Normal bekleme sirasinda bekleyen var (FIFO) */
                nextMusteriID = dequeue(&q);
                reps[eventArg].isBusy = 1;
                reps[eventArg].currentMusteriID = nextMusteriID;
                printf("%d %d %d\n", eventTime, nextMusteriID, eventArg);
            }

        } else if (eventType == 3) {
            /* Tip 3: Musteri aktarma talebi - yigina alinir, temsilci bosalir */
            foundRep = -1;
            for (j = 0; j < T; j++) {
                if (reps[j].isBusy == 1 && reps[j].currentMusteriID == eventArg) {
                    foundRep = j; /* Musterilyi hizmet veren temsilciyi bul */
                }
            }

            if (foundRep != -1) {
                /* Musterilyi aktarma alanina (yigina) ekle */
                push(&s, eventArg);
                /* Temsilciyi serbest birak */
                reps[foundRep].isBusy = 0;
                reps[foundRep].currentMusteriID = -1;

                /* Bosalan temsilciyi once aktarma alani, sonra kuyrukla doldur */
                if (!isStackEmpty(&s)) {
                    nextMusteriID = pop(&s);
                    reps[foundRep].isBusy = 1;
                    reps[foundRep].currentMusteriID = nextMusteriID;
                    printf("%d %d %d\n", eventTime, nextMusteriID, foundRep);
                } else if (!isQueueEmpty(&q)) {
                    nextMusteriID = dequeue(&q);
                    reps[foundRep].isBusy = 1;
                    reps[foundRep].currentMusteriID = nextMusteriID;
                    printf("%d %d %d\n", eventTime, nextMusteriID, foundRep);
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

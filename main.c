#include <stdio.h>
#include <stdlib.h>

struct Event {
    int zaman;
    int tip;
    int arg;
};

struct Node {
    int musteriID;
    struct Node* next;
};

struct Queue {
    struct Node* front;
    struct Node* rear;
};

struct Stack {
    struct Node* top;
};

struct Representative {
    int isBusy;
    int currentMusteriID;
};

void enqueue(struct Queue* q, int id) {
    struct Node* newNode = (struct Node*)malloc(sizeof(struct Node));
    newNode->musteriID = id;
    newNode->next = NULL;

    if (q->rear == NULL) {
        q->front = newNode;
        q->rear = newNode;
    } else {
        q->rear->next = newNode;
        q->rear = newNode;
    }
}

int dequeue(struct Queue* q) {
    int id = -1;
    struct Node* temp;

    if (q->front != NULL) {
        temp = q->front;
        id = temp->musteriID;
        q->front = q->front->next;

        if (q->front == NULL) {
            q->rear = NULL;
        }
        free(temp);
    }
    return id;
}

int isQueueEmpty(struct Queue* q) {
    int empty = 0;
    if (q->front == NULL) {
        empty = 1;
    }
    return empty;
}

void push(struct Stack* s, int id) {
    struct Node* newNode = (struct Node*)malloc(sizeof(struct Node));
    newNode->musteriID = id;
    newNode->next = s->top;
    s->top = newNode;
}

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

int isStackEmpty(struct Stack* s) {
    int empty = 0;
    if (s->top == NULL) {
        empty = 1;
    }
    return empty;
}

int main() {
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

    q.front = NULL;
    q.rear = NULL;
    s.top = NULL;

    scanf("%d", &T);
    scanf("%d", &O);

    events = (struct Event*)malloc(O * sizeof(struct Event));
    reps = (struct Representative*)malloc(T * sizeof(struct Representative));

    for (i = 0; i < T; i++) {
        reps[i].isBusy = 0;
        reps[i].currentMusteriID = -1;
    }

    for (i = 0; i < O; i++) {
        scanf("%d %d %d", &events[i].zaman, &events[i].tip, &events[i].arg);
    }

    for (i = 0; i < O; i++) {
        eventType = events[i].tip;
        eventTime = events[i].zaman;
        eventArg = events[i].arg;

        if (eventType == 1) {
            freeRepIndex = -1;
            for (j = 0; j < T; j++) {
                if (reps[j].isBusy == 0 && freeRepIndex == -1) {
                    freeRepIndex = j;
                }
            }
            
            if (freeRepIndex != -1) {
                reps[freeRepIndex].isBusy = 1;
                reps[freeRepIndex].currentMusteriID = eventArg;
                printf("%d %d %d\n", eventTime, eventArg, freeRepIndex);
            } else {
                enqueue(&q, eventArg);
            }
        } else if (eventType == 2) {
            reps[eventArg].isBusy = 0;
            reps[eventArg].currentMusteriID = -1;
            
            if (!isStackEmpty(&s)) {
                nextMusteriID = pop(&s);
                reps[eventArg].isBusy = 1;
                reps[eventArg].currentMusteriID = nextMusteriID;
                printf("%d %d %d\n", eventTime, nextMusteriID, eventArg);
            } else if (!isQueueEmpty(&q)) {
                nextMusteriID = dequeue(&q);
                reps[eventArg].isBusy = 1;
                reps[eventArg].currentMusteriID = nextMusteriID;
                printf("%d %d %d\n", eventTime, nextMusteriID, eventArg);
            }
        } else if (eventType == 3) {
            foundRep = -1;
            for (j = 0; j < T; j++) {
                if (reps[j].isBusy == 1 && reps[j].currentMusteriID == eventArg) {
                    foundRep = j;
                }
            }
            
            if (foundRep != -1) {
                push(&s, eventArg);
                reps[foundRep].isBusy = 0;
                reps[foundRep].currentMusteriID = -1;
                
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

    while (!isQueueEmpty(&q)) {
        dequeue(&q);
    }
    while (!isStackEmpty(&s)) {
        pop(&s);
    }

    free(events);
    free(reps);
    return 0;
}

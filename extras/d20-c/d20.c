#include <time.h>
#include <stdio.h>
#include <unistd.h>
#include <stdint.h>
#include <stdlib.h>

typedef struct node_t Node;

struct node_t {
    Node* next;
    Node* prev;
    int64_t data;
};

void slide(Node* node, int len);

int64_t grove_coords(Node* node);

int main() {
    FILE* input = fopen("d20.in", "r");

    struct timespec begin, end;
    clock_gettime(CLOCK_MONOTONIC, &begin);

    Node nodes[5000];
    Node big_nodes[5000];
    int size = 0;
    int zero = 0;
    int64_t curr = 0;

    while (fscanf(input, "%ld", &curr) > 0) {
        Node n = {.next = NULL, .prev = NULL, .data = curr};
        Node big = {.next = NULL, .prev = NULL, .data = curr * 811589153L};
        if (curr == 0) {
            zero = size;
        }
        big_nodes[size] = big;
        nodes[size++] = n;
    }

    fclose(input);

    for (int i = 0; i < size; ++i) {
        int next_idx = i + 1 < size ? i + 1 : 0;
        int prev_idx = i - 1 > 0 ? i - 1 : size - 1;
        nodes[i].next = &nodes[next_idx];
        nodes[i].prev = &nodes[prev_idx];

        big_nodes[i].next = &big_nodes[next_idx];
        big_nodes[i].prev = &big_nodes[prev_idx];
    }

    for (int i = 0; i < size; ++i) {
        slide(&nodes[i], size);
        slide(&big_nodes[i], size);
    }

    for (int i = 0; i < 9; ++i) {
        for (int i = 0; i < size; ++i) {
            slide(&big_nodes[i], size);
        }
    }

    int64_t p1 = grove_coords(&nodes[zero]);
    int64_t p2 = grove_coords(&big_nodes[zero]);

    clock_gettime(CLOCK_MONOTONIC, &end);
    printf("Part 1: %ld\nPart 2: %ld\n", p1, p2);
    float ns = 1e9 * (end.tv_sec - begin.tv_sec) + (end.tv_nsec - begin.tv_nsec);
    printf("%.3f ms\n", ns / 1e6);
}

int64_t grove_coords(Node* curr) {
    int64_t s = 0;
    for (int l = 0; l < 3; ++l) {
        for (int i = 0; i < 1000; ++i) {
            curr = curr->next;
        }
        s += curr->data;
    }
    return s;
}

void slide(Node* node, int len) {
    if (!node->data) {
        return;
    }

    Node* curr = node;
    int move_amt = node->data % (~-len);
    if (node->data > 0) {
        for (int i = 0; i < move_amt; ++i) {
            curr = curr->next;
        }

        node->next->prev = node->prev;
        node->prev->next = node->next;

        node->prev = curr;
        node->next = curr->next;
    } else {
        for (int i = move_amt; i < 0; ++i) {
            curr = curr->prev;
        }

        node->next->prev = node->prev;
        node->prev->next = node->next;

        node->prev = curr->prev;
        node->next = curr;
    }
    node->next->prev = node;
    node->prev->next = node;
}


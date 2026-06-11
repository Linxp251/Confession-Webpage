/**
 * 实验三：可变分区内存分配 —— 首次适应算法模拟
 * 使用双向链表管理内存分区，支持分配、回收与合并
 */
#include <iostream>
#include <fstream>
#include <sstream>
#include <cstdlib>
#include <cstring>
#include <iomanip>

using namespace std;

#define FREE  0   // 空闲状态
#define BUSY  1   // 已分配状态
#define OK    1
#define ERROR 0

// 分区信息
struct Partition {
    long address;   // 起始地址 (KB)
    long size;      // 分区大小 (KB)
    int  state;     // FREE 或 BUSY
    int  job_id;    // 占用该分区的作业号，空闲时为 -1
};

// 双向链表结点
struct DuLNode {
    Partition data;
    DuLNode *prior;
    DuLNode *next;
};

DuLNode *head_node = nullptr;  // 头结点
DuLNode *end_node = nullptr;   // 尾结点
long total_memory = 640;       // 总内存大小 (KB)

// 函数声明
int  init_memory(long size);
int  first_fit(int job_id, long need);
int  free_memory(int job_id);
void show_partitions();
void show_free_chain();
int  alloc_interactive();
int  free_interactive();
void run_batch(const char *input_file);
void cleanup();

// 初始化内存空间：整个空间作为一个空闲分区
int init_memory(long size) {
    total_memory = size;
    head_node = (DuLNode *)malloc(sizeof(DuLNode));
    end_node  = (DuLNode *)malloc(sizeof(DuLNode));
    if (!head_node || !end_node) return ERROR;

    head_node->prior = nullptr;
    head_node->next  = end_node;
    end_node->prior  = head_node;
    end_node->next   = nullptr;
    end_node->data.address = 0;
    end_node->data.size    = size;
    end_node->data.state   = FREE;
    end_node->data.job_id  = -1;
    return OK;
}

// 首次适应算法：从低地址向高地址查找第一个满足要求的空闲分区
int first_fit(int job_id, long need) {
    if (need <= 0) {
        cout << "  [错误] 申请大小必须大于 0！" << endl;
        return ERROR;
    }

    DuLNode *p = head_node->next;
    while (p) {
        if (p->data.state == FREE && p->data.size >= need) {
            if (p->data.size == need) {
                // 整块分配
                p->data.state  = BUSY;
                p->data.job_id = job_id;
            } else {
                // 分割分区：从低地址分配
                DuLNode *temp = (DuLNode *)malloc(sizeof(DuLNode));
                if (!temp) return ERROR;
                temp->data.address = p->data.address;
                temp->data.size    = need;
                temp->data.state   = BUSY;
                temp->data.job_id  = job_id;
                temp->prior = p->prior;
                temp->next  = p;
                p->prior->next = temp;
                p->prior = temp;
                p->data.address += need;
                p->data.size    -= need;
            }
            cout << "  [分配成功] 作业" << job_id << " 获得 " << need << "KB 内存" << endl;
            return OK;
        }
        p = p->next;
    }
    cout << "  [分配失败] 内存不足，无法满足作业" << job_id << " 的 " << need << "KB 请求" << endl;
    return ERROR;
}

// 回收内存：根据作业号释放，并合并相邻空闲分区
int free_memory(int job_id) {
    DuLNode *p = head_node->next;
    while (p) {
        if (p->data.state == BUSY && p->data.job_id == job_id) {
            long freed_size = p->data.size;
            p->data.state  = FREE;
            p->data.job_id = -1;

            // 与前驱空闲分区合并
            if (p->prior != head_node && p->prior->data.state == FREE) {
                p->prior->data.size += p->data.size;
                p->prior->next = p->next;
                if (p->next) p->next->prior = p->prior;
                DuLNode *old = p;
                p = p->prior;
                free(old);
            }

            // 与后继空闲分区合并
            if (p->next && p->next->data.state == FREE) {
                p->data.size += p->next->data.size;
                DuLNode *old = p->next;
                p->next = old->next;
                if (old->next) old->next->prior = p;
                free(old);
            }

            cout << "  [回收成功] 作业" << job_id << " 释放 " << freed_size << "KB 内存" << endl;
            return OK;
        }
        p = p->next;
    }
    cout << "  [回收失败] 未找到作业" << job_id << " 的内存分区" << endl;
    return ERROR;
}

// 显示所有分区（含已分配和空闲）
void show_partitions() {
    cout << "\n  ========== 当前内存分区表 ==========" << endl;
    cout << "  分区号  起始地址(KB)  大小(KB)  状态      作业号" << endl;
    cout << "  ----------------------------------------------" << endl;
    int idx = 0;
    DuLNode *p = head_node->next;
    while (p) {
        cout << "  " << setw(4) << idx++
             << setw(12) << p->data.address
             << setw(10) << p->data.size
             << setw(10) << (p->data.state == FREE ? "空闲" : "已分配")
             << setw(10) << (p->data.job_id == -1 ? "-" : to_string(p->data.job_id))
             << endl;
        p = p->next;
    }
    cout << "  ==============================================" << endl;
}

// 显示空闲分区链
void show_free_chain() {
    int free_count = 0;
    cout << "\n  ---------- 空闲内存分区链 ----------" << endl;
    cout << "  序号  起始地址(KB)  大小(KB)" << endl;
    DuLNode *p = head_node->next;
    int seq = 1;
    while (p) {
        if (p->data.state == FREE) {
            cout << "  " << setw(4) << seq++
                 << setw(14) << p->data.address
                 << setw(10) << p->data.size << endl;
            free_count++;
        }
        p = p->next;
    }
    cout << "  空闲分区总数: " << free_count << endl;
    cout << "  ------------------------------------" << endl;
}

// 交互式分配
int alloc_interactive() {
    int job_id;
    long need;
    cout << "\n  请输入作业号: ";
    cin >> job_id;
    cout << "  请输入申请内存大小(KB): ";
    cin >> need;
    return first_fit(job_id, need);
}

// 交互式回收
int free_interactive() {
    int job_id;
    cout << "\n  请输入要释放的作业号: ";
    cin >> job_id;
    return free_memory(job_id);
}

// 批处理模式：从文件读取请求序列并执行
void run_batch(const char *input_file) {
    ifstream inf(input_file);
    if (!inf.is_open()) {
        cerr << "无法打开输入文件: " << input_file << endl;
        return;
    }

    cout << "\n============================================================" << endl;
    cout << "  可变分区内存分配 —— 首次适应算法 批处理测试" << endl;
    cout << "  初始内存: " << total_memory << "KB" << endl;
    cout << "============================================================" << endl;

    int seq = 0;
    int num;
    char state;
    long len;
    while (inf >> num >> state >> len) {
        seq++;
        cout << "\n>>> 序列" << seq << ": 作业" << num;
        if (state == 'a' || state == 'A')
            cout << " 申请 " << len << "KB" << endl;
        else
            cout << " 释放 " << len << "KB" << endl;

        if (state == 'a' || state == 'A')
            first_fit(num, len);
        else
            free_memory(num);

        show_partitions();
        show_free_chain();
        cout << endl;
    }
    inf.close();
}

void cleanup() {
    if (!head_node) return;
    DuLNode *p = head_node->next;
    while (p && p != end_node) {
        DuLNode *next = p->next;
        free(p);
        p = next;
    }
    free(head_node);
    free(end_node);
    head_node = end_node = nullptr;
}

void print_menu() {
    cout << "\n+--------------------------------------------------+" << endl;
    cout << "|  可变分区内存分配 —— 首次适应算法模拟            |" << endl;
    cout << "+--------------------------------------------------+" << endl;
    cout << "|  1. 分配内存 (首次适应)                          |" << endl;
    cout << "|  2. 回收内存                                     |" << endl;
    cout << "|  3. 显示内存分区表                               |" << endl;
    cout << "|  4. 显示空闲分区链                               |" << endl;
    cout << "|  5. 运行批处理测试 (640KB标准序列)               |" << endl;
    cout << "|  0. 退出                                         |" << endl;
    cout << "+--------------------------------------------------+" << endl;
    cout << "  请选择操作: ";
}

int main(int argc, char *argv[]) {
    // 支持命令行批处理: ./first_fit batch in.txt
    if (argc >= 3 && strcmp(argv[1], "batch") == 0) {
        long mem_size = 640;
        if (argc >= 4) mem_size = atol(argv[3]);
        init_memory(mem_size);
        run_batch(argv[2]);
        cleanup();
        return 0;
    }

    cout << "\n  请输入初始内存大小(KB) [默认640]: ";
    string line;
    getline(cin, line);
    long mem_size = 640;
    if (!line.empty()) mem_size = atol(line.c_str());

    init_memory(mem_size);
    cout << "  内存初始化完成，总大小: " << mem_size << "KB" << endl;

    while (true) {
        print_menu();
        int choice;
        cin >> choice;

        switch (choice) {
            case 1:
                alloc_interactive();
                show_partitions();
                break;
            case 2:
                free_interactive();
                show_partitions();
                break;
            case 3:
                show_partitions();
                break;
            case 4:
                show_free_chain();
                break;
            case 5:
                run_batch("in.txt");
                break;
            case 0:
                cout << "\n  程序退出。" << endl;
                cleanup();
                return 0;
            default:
                cout << "  输入有误，请重新选择！" << endl;
        }
    }
}

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <termios.h>
#include <unistd.h>
#include <curl/curl.h>

typedef struct {
    char ip[16];
    char psk[32];
} TVConfig;

// This function swallows the response data so it doesn't print to your terminal
size_t silence_output(void *ptr, size_t size, size_t nmemb, void *data) {
    return size * nmemb;
}

void send_ircc(TVConfig *config, const char *code) {
    CURL *curl;
    curl = curl_easy_init();
    if(curl) {
        char url[100];
        snprintf(url, sizeof(url), "http://%s/sony/ircc", config->ip);

        struct curl_slist *headers = NULL;
        char auth_header[64];
        snprintf(auth_header, sizeof(auth_header), "X-Auth-PSK: %s", config->psk);
        
        headers = curl_slist_append(headers, auth_header);
        headers = curl_slist_append(headers, "Content-Type: text/xml; charset=UTF-8");
        headers = curl_slist_append(headers, "SOAPACTION: \"urn:schemas-sony-com:service:IRCC:1#X_SendIRCC\"");

        char data[512];
        snprintf(data, sizeof(data), 
            "<?xml version=\"1.0\"?><s:Envelope xmlns:s=\"http://schemas.xmlsoap.org/soap/envelope/\" "
            "s:encodingStyle=\"http://schemas.xmlsoap.org/soap/encoding/\"><s:Body>"
            "<u:X_SendIRCC xmlns:u=\"urn:schemas-sony-com:service:IRCC:1\"><IRCCCode>%s</IRCCCode>"
            "</u:X_SendIRCC></s:Body></s:Envelope>", code);

        curl_easy_setopt(curl, CURLOPT_URL, url);
        curl_easy_setopt(curl, CURLOPT_HTTPHEADER, headers);
        curl_easy_setopt(curl, CURLOPT_POSTFIELDS, data);
        curl_easy_setopt(curl, CURLOPT_TIMEOUT_MS, 500L);
        
        // --- THE SILENCING TRICK ---
        // Redirect the write function to our empty callback
        curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, silence_output);

        curl_easy_perform(curl);
        
        curl_slist_free_all(headers);
        curl_easy_cleanup(curl);
    }
}

int main() {
    TVConfig config;
    printf("Enter TV IP: ");
    scanf("%15s", config.ip);
    printf("Enter PSK: ");
    scanf("%31s", config.psk);

    // Clear screen for a cleaner feel
    printf("\e[1;1H\e[2J");
    printf("--- Sony Bravia C Remote (Silent Mode) ---\n");
    printf("W/A/S/D: Nav | F: OK | B: Back | H: Home\n");
    printf("v/V: Vol | p: Power | q: Quit\n");
    printf("------------------------------------------\n");

    struct termios oldt, newt;
    tcgetattr(STDIN_FILENO, &oldt);
    newt = oldt;
    newt.c_lflag &= ~(ICANON | ECHO);
    tcsetattr(STDIN_FILENO, TCSANOW, &newt);

    char c;
    while (read(STDIN_FILENO, &c, 1) == 1 && c != 'q') {
        switch(c) {
            case 'w': send_ircc(&config, "AAAAAQAAAAEAAAB0Aw=="); break;
            case 's': send_ircc(&config, "AAAAAQAAAAEAAAB1Aw=="); break;
            case 'a': send_ircc(&config, "AAAAAQAAAAEAAAA0Aw=="); break;
            case 'd': send_ircc(&config, "AAAAAQAAAAEAAAAzAw=="); break;
            case 'f': send_ircc(&config, "AAAAAQAAAAEAAABlAw=="); break;
            case 'b': send_ircc(&config, "AAAAAgAAAJcAAAAjAw=="); break;
            case 'h': send_ircc(&config, "AAAAAQAAAAEAAABgAw=="); break;
            case 'v': send_ircc(&config, "AAAAAQAAAAEAAAATAw=="); break;
            case 'V': send_ircc(&config, "AAAAAQAAAAEAAAASAw=="); break;
            case 'p': send_ircc(&config, "AAAAAQAAAAEAAAAVAw=="); break;
        }
    }

    tcsetattr(STDIN_FILENO, TCSANOW, &oldt);
    printf("\nDone.\n");
    return 0;
}

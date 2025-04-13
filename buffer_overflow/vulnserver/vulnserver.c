/**
 * Purposefully designed vulnerable server intended for buffer overflow studies.
 */

#define _WIN32_WINNT 0x0601
#define WINVER 0x0601
#define NTDDI_VERSION 0x06010000

#include <winsock2.h>
#include <ws2tcpip.h>
#include <stdio.h>
#include <string.h>
#include <windows.h>

#define DEFAULT_PORT "9999"

HINSTANCE hDll = NULL;

void received_name(const char *name)
{
    printf("[*] Name received: %s\n", name);
}

void handle_client(SOCKET client_sock)
{
    char buffer[500];

    const char *msg = "Enter your name: ";
    send(client_sock, msg, strlen(msg), 0);

    int received = recv(client_sock, buffer, 1000, 0);
    if (received <= 0)
    {
        printf("[-] Connection closed by client\n");
        closesocket(client_sock);
        return;
    }

    buffer[received] = '\0';

    int i;
    for (i = 0; i < received; i++)
    {
        if (buffer[i] == '\r' || buffer[i] == '\n')
        {
            buffer[i] = '\0';
            break;
        }
    }

    received_name(buffer);

    char welcome_msg[600];
    sprintf(welcome_msg, "Welcome, %s!\n", buffer);
    send(client_sock, welcome_msg, strlen(welcome_msg), 0);

    closesocket(client_sock);
}

int main()
{
    hDll = LoadLibrary("serverdll.dll");
    if (!hDll)
    {
        printf("[!] Error loading DLL: %lu\n", GetLastError());
        return 1;
    }

    WSADATA wsaData;
    SOCKET ListenSocket = INVALID_SOCKET;
    SOCKET ClientSocket = INVALID_SOCKET;
    struct addrinfo *result = NULL,
                    hints;
    int iResult;

    iResult = WSAStartup(MAKEWORD(2, 2), &wsaData);
    if (iResult != 0)
    {
        printf("[!] WSAStartup failed with error: %d\n", iResult);
        return 1;
    }

    ZeroMemory(&hints, sizeof(hints));
    hints.ai_family = AF_UNSPEC;
    hints.ai_socktype = SOCK_STREAM;
    hints.ai_protocol = IPPROTO_TCP;
    hints.ai_flags = AI_PASSIVE;

    iResult = getaddrinfo(NULL, DEFAULT_PORT, &hints, &result);
    if (iResult != 0)
    {
        printf("[!] getaddrinfo failed with error: %d\n", iResult);
        WSACleanup();
        return 1;
    }

    ListenSocket = socket(result->ai_family, result->ai_socktype, result->ai_protocol);
    if (ListenSocket == INVALID_SOCKET)
    {
        printf("[!] socket creation failed: %d\n", WSAGetLastError());
        freeaddrinfo(result);
        WSACleanup();
        return 1;
    }

    if (result->ai_family == AF_INET6)
    {
        int ipv6only = 0;
        if (setsockopt(ListenSocket, IPPROTO_IPV6, 27,
                       (char *)&ipv6only, sizeof(ipv6only)) == SOCKET_ERROR)
        {
            printf("[!] Warning: Failed to set IPV6_V6ONLY: %d\n", WSAGetLastError());
        }

        char ipstr[INET6_ADDRSTRLEN];
        DWORD ipstrlen = INET6_ADDRSTRLEN;
        WSAAddressToStringA(result->ai_addr, (DWORD)result->ai_addrlen, NULL, ipstr, &ipstrlen);
    }

    iResult = bind(ListenSocket, result->ai_addr, (int)result->ai_addrlen);
    if (iResult == SOCKET_ERROR)
    {
        printf("[!] bind failed: %d\n", WSAGetLastError());
        freeaddrinfo(result);
        closesocket(ListenSocket);
        WSACleanup();
        return 1;
    }

    freeaddrinfo(result);

    iResult = listen(ListenSocket, SOMAXCONN);
    if (iResult == SOCKET_ERROR)
    {
        printf("[!] listen failed: %d\n", WSAGetLastError());
        closesocket(ListenSocket);
        WSACleanup();
        return 1;
    }

    printf("[+] Server listening on port %s...\n", DEFAULT_PORT);
    printf("[*] Ready to accept connections\n");

    while (1)
    {
        ClientSocket = accept(ListenSocket, NULL, NULL);
        if (ClientSocket == INVALID_SOCKET)
        {
            printf("[!] accept failed: %d\n", WSAGetLastError());
            closesocket(ListenSocket);
            WSACleanup();
            return 1;
        }

        printf("[+] New connection accepted\n");
        handle_client(ClientSocket);
    }

    closesocket(ListenSocket);
    WSACleanup();
    printf("[*] Server shutdown complete\n");

    return 0;
}
#include <stdio.h>
#include <string.h>

// a must not share a common factor with B64_TABLE_SIZE i.e they are coprimes
#define a 13
#define b 5
#define B64_TABLE_SIZE 256

const char base64Table[] = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/";

int getB64Value(char c) {
    if (c >= 'A' && c <= 'Z') return c - 'A';
    if (c >= 'a' && c <= 'z') return c - 'a' + 26;
    if (c >= '0' && c <= '9') return c - '0' + 52;
    if (c == '+') return 62;
    if (c == '/') return 63;
    return 0; // For '='
}

void encrypt(char text[], char *outputBuffer, int textSize) {
    char encryptedBytes[textSize];
    
    for(int c=0; c<textSize; c++){
        unsigned char character = (unsigned char)text[c];
        int code = (b + a*character) % B64_TABLE_SIZE;
        encryptedBytes[c] = (char)code;
    }

    int b64Size = 4 * ((textSize + 2) / 3);
    char base64Result[b64Size + 1]; // +1 for the \0
    
    /**
     * TO BASE64 CONVERTION
     * Since a byte (1 char) is 8bits and in base 64 we work with 
     * 6bits group, we must use 3 bytes and divide it into 4 groups 
     */
    int d = 0;
    for(int c=0; c < textSize; c+=3){
        unsigned char b1 = encryptedBytes[c];
        unsigned char b2 = (c+1 < textSize) ? encryptedBytes[c+1] : 0;
        unsigned char b3 = (c+2 < textSize) ? encryptedBytes[c+2] : 0;

        int first = b1 >> 2;
        int second = ((b1 & 0x03) << 4) | (b2 >> 4);
        int third = ((b2 & 0x0F) << 2) | (b3 >> 6);
        int fourth = (b3 & 0x3F);

        base64Result[d++] = base64Table[first];
        base64Result[d++] = base64Table[second];
        base64Result[d++] = base64Table[third];
        base64Result[d++] = base64Table[fourth];
    }
    base64Result[d] = '\0'; 

    if(textSize % 3 == 1){
        base64Result[d-1] = '=';
        base64Result[d-2] = '=';
    } 
    else if(textSize % 3 == 2){
        base64Result[d-1] = '=';
    }

    strcpy(outputBuffer, base64Result);
}

void decrypt(char encryptedText[], char *outputBuffer, int textSize) {

    int plainTextSize = 3*textSize/4;
    char encryptedBytes[plainTextSize + 1];
    int i =0;
    for(int d=0; d < textSize; d+=4){
        int b1 = getB64Value(encryptedText[d]);
        int b2 = getB64Value(encryptedText[d + 1]);
        int b3 = getB64Value(encryptedText[d + 2]);
        int b4 = getB64Value(encryptedText[d + 3]);
        
        encryptedBytes[i++] = (b1 << 2) | (b2 >> 4);

        if(encryptedText[d+2] != '='){
            encryptedBytes[i++] = ((b2 & 0x0F) << 4) | (b3 >> 2);
        }

        if(encryptedText[d+3] != '='){
            encryptedBytes[i++] = ((b3 & 0x03) << 6) | b4;
        }
    }
    encryptedBytes[i] = '\0';
    int actualEncryptedSize = i;

    int modularMultiplicativeInverse;
    for(int c=1; c< B64_TABLE_SIZE; c++){
        if(a*c % B64_TABLE_SIZE == 1){
            modularMultiplicativeInverse = c;
            break;
        }
    }
    
    for(int c=0; c< actualEncryptedSize; c++){
        unsigned char character = (unsigned char)encryptedBytes[c];
        int code = modularMultiplicativeInverse*(character - b + B64_TABLE_SIZE) % B64_TABLE_SIZE;
        outputBuffer[c] = (char)code;
    }
    outputBuffer[actualEncryptedSize] = '\0';
}

int main(int argc, char *argv[]){
    if(argc == 1){
        printf("This is a Linear Cypher Algorithm!\nTo use it just do:\n");
        printf("./LinearCypher encrypt your_text\n./LinearCypher decrypt your_encrypted_text\n");
        return 0;
    }
    if (argc != 3){
        printf("Invalid number of Arguments!");
        return 1;
    }
    
    int textLength = strlen(argv[2]);
    char output[2*textLength];
    if((strcmp(argv[1], "encrypt") == 0)){
        encrypt(argv[2], output, textLength);
        printf("%s", output);
    } else if(strcmp(argv[1], "decrypt") == 0){
        decrypt(argv[2], output, textLength);
        printf("%s", output);
    } else {
        printf("Invalid Arguments");
        return 1;
    }
    
    return 0;
}

// TODO - Read from a file and generate a encrypted text
// Multiple encryption iterations